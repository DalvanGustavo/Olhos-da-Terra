import http.client
import time
import pyautogui as pg
# Substitua pelo IP do seu ESP32
esp32_ip = '192.168.0.101'  # Altere para o IP do seu ESP32
port = 80  # Porta padrão do HTTP

def check_motion():
    conn = http.client.HTTPConnection(esp32_ip, port)
    try:
        conn.request("GET", "/movimento")
        response = conn.getresponse()
        data = response.read().decode()
        print(f"Resposta do ESP32: {data}")
        if int(data) == 1:
            pg.press('f5')
    except Exception as e:
        print(f"Erro: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    while True:
        check_motion()
        time.sleep(1)  # Espera 5 segundos antes da próxima verificação

