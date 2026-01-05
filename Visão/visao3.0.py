#%%
import cv2  # Biblioteca OpenCV para captura e manipulação de vídeo/imagens
import mediapipe as mp  # Biblioteca MediaPipe para processamento de visão computacional
import pyautogui as pg
import http.client
import time

# Inicializa o MediaPipe Pose para detectar e processar os pontos de referência do corpo humano.
mp_pose = mp.solutions.pose  # Acessa a solução de pose do MediaPipe
pose = mp_pose.Pose()  # Cria um objeto Pose para detectar landmarks no corpo humano

# Inicializa o utilitário de desenho do MediaPipe, utilizado para desenhar os pontos de referência e as conexões no corpo.
mp_drawing = mp.solutions.drawing_utils  # Utilitário de desenho para desenhar landmarks e conexões
# Inicia a captura de vídeo usando a câmera de índice 1.
cap = cv2.VideoCapture(0)  # Abertura da câmera. 0 é o índice da câmera, caso haja múltiplas conectadas.

# Obtém as dimensões da tela
screen_width, screen_height = pg.size()

# Função que desenha os landmarks (pontos de referência) e calcula o centro entre os ombros.
def draw_landmarks_and_center(image, landmarks):
    # Obtém as dimensões da imagem (altura e largura) para calcular as coordenadas em pixels.
    height, width, _ = image.shape  # Obtém as dimensões da imagem para referência posterior.

    # Acessa os landmarks dos ombros esquerdo e direito, que têm os índices 11 e 12 no modelo Pose.
    shoulder_left = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]  # Landmark do ombro esquerdo
    shoulder_right = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]  # Landmark do ombro direito

    # Converte as coordenadas normalizadas dos ombros para valores em pixels no espaço da imagem.
    shoulder_left_x = int(shoulder_left.x * width)  # Converte a coordenada X do ombro esquerdo para pixels
    shoulder_left_y = int(shoulder_left.y * height)  # Converte a coordenada Y do ombro esquerdo para pixels
    shoulder_right_x = int(shoulder_right.x * width)  # Converte a coordenada X do ombro direito para pixels
    shoulder_right_y = int(shoulder_right.y * height)  # Converte a coordenada Y do ombro direito para pixels

    # Calcula a média das coordenadas X e Y dos dois ombros para encontrar o centro entre os ombros.
    center_x = int((shoulder_left_x + shoulder_right_x) / 2)  # Média das coordenadas X dos ombros
    center_y = int((shoulder_left_y + shoulder_right_y) / 2)  # Média das coordenadas Y dos ombros

    # Desenha um círculo verde no centro calculado entre os ombros, com raio 10 pixels.
    cv2.circle(image, (center_x, center_y), 10, (0, 255, 0), -1)  # Desenha o ponto central entre os ombros

    # Movendo o mouse para a posição calculada
    pg.FAILSAFE = False
    pg.moveTo(center_x, center_y)  # Mover o mouse para o centro calculado

    # Retorna a imagem com o círculo desenhado no centro.
    return image

# Inicia um loop para capturar e processar cada frame do vídeo.
while cap.isOpened():
    # Captura um frame da câmera.
    ret, frame = cap.read()  # Captura um frame da câmera, ret é um valor booleano de sucesso/falha

    # Se não foi possível capturar o frame, interrompe o loop.
    if not ret:
        break  # Se o frame não foi capturado corretamente, sai do loop.

    # Corrige a inversão horizontal da imagem
    frame_flipped = cv2.flip(frame, 1)  # 1 para inverter horizontalmente

    # Redimensiona a imagem para o tamanho da tela.
    frame_resized = cv2.resize(frame_flipped, (screen_width, screen_height))  # Redimensiona para o tamanho da tela

    # Converte a imagem BGR (OpenCV) para RGB (formato esperado pelo MediaPipe).
    image_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)  # OpenCV usa BGR, mas o MediaPipe espera RGB.

    # Processa a imagem RGB com o modelo Pose para detectar os landmarks da pose do corpo.
    results = pose.process(image_rgb)  # Passa a imagem para o modelo de Pose do MediaPipe

    # Se a detecção de landmarks for bem-sucedida, os landmarks do corpo serão desenhados na imagem.
    if results.pose_landmarks:  # Verifica se landmarks foram detectados na imagem
        # Desenha todos os landmarks e as conexões do corpo (linhas entre pontos de referência) no frame.
        mp_drawing.draw_landmarks(
            frame_resized,  # A imagem onde os landmarks serão desenhados
            results.pose_landmarks,  # Os landmarks detectados na imagem
            mp_pose.POSE_CONNECTIONS,  # As conexões entre os pontos de referência do corpo
            mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),  # Especificações de desenho para os landmarks (cor verde e raio de círculo de 2 pixels)
            mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=2),  # Especificações de desenho para as conexões (cor vermelha e espessura de 2 pixels)
        )
        # Chama a função `draw_landmarks_and_center` para desenhar o ponto central entre os ombros na imagem.
        frame_resized = draw_landmarks_and_center(frame_resized, results.pose_landmarks.landmark)  # Desenha o centro entre os ombros

    # Exibe a imagem com os landmarks desenhados e o centro calculado na janela "Pose Detection".
    cv2.imshow('Pose Detection', frame_resized)  # Exibe o frame com os landmarks desenhados

    # Se a tecla 'q' for pressionada, o loop é interrompido e o programa será fechado.
    if cv2.waitKey(10) & 0xFF == ord('q'):  # Espera por 10ms para verificar se a tecla 'q' foi pressionada
        break  # Sai do loop caso a tecla 'q' seja pressionada

# Libera a câmera e fecha todas as janelas do OpenCV.
cap.release()  # Libera a captura de vídeo
cv2.destroyAllWindows()  # Fecha todas as janelas do OpenCV

# Substitua pelo IP do seu ESP32
esp32_ip = '192.168.0.12'  # Altere para o IP do seu ESP32
port = 80  # Porta padrão do HTTP

def check_motion():
    conn = http.client.HTTPConnection(esp32_ip, port)
    try:
        conn.request("GET", "/movimento")
        response = conn.getresponse()
        data = response.read().decode()
        print(f"Resposta do ESP32: {data}")
        pg.press('f5')
    except Exception as e:
        print(f"Erro: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    while True:
        check_motion()
        time.sleep(1)  # Espera 1 segundo antes da próxima verificação
