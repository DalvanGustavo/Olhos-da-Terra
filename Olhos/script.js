window.onload = function () {
    const olhoGrande = document.querySelector('#olho-grande');
    olhoGrande.classList.add('visible');

    // Após 3 segundos, esconde o olho-grande e mostra os outros olhos
    setTimeout(() => {
        olhoGrande.classList.remove('visible');
        document.querySelectorAll('.eye').forEach(eye => eye.classList.add('visible'));
    }, 13000);

    const iris = document.querySelectorAll('.iris');
    const eyes = document.querySelectorAll('.eye');

    let blinkCount = 0;
    let lastBlinkTime = Date.now(); // Marca o tempo do último piscar

    document.addEventListener('mousemove', (event) => {
        const { clientX, clientY } = event;

        // Movimento do mouse para os olhos
        eyes.forEach((eye, index) => {
            const eyeRect = eye.getBoundingClientRect();
            const eyeX = eyeRect.left + eyeRect.width / 2;
            const eyeY = eyeRect.top + eyeRect.height / 2;
            const deltaX = clientX - eyeX;
            const deltaY = clientY - eyeY;
            const angle = Math.atan2(deltaY, deltaX);
            const irisX = Math.cos(angle) * 30;
            const irisY = Math.sin(angle) * 10;

            iris[index].style.transform = `translate(-50%, -50%) translate(${irisX}px, ${irisY}px)`;
        });

        // Movimento do mouse para o olho grande
        const olhoGrandeRect = olhoGrande.getBoundingClientRect();
        const olhoGrandeX = olhoGrandeRect.left + olhoGrandeRect.width / 2;
        const olhoGrandeY = olhoGrandeRect.top + olhoGrandeRect.height / 2;
        const deltaXGrande = clientX - olhoGrandeX;
        const deltaYGrande = clientY - olhoGrandeY;
        const angleGrande = Math.atan2(deltaYGrande, deltaXGrande);
        const irisXGrande = Math.cos(angleGrande) * 200;
        const irisYGrande = Math.sin(angleGrande) * 70;

        olhoGrande.querySelector('.iris').style.transform = `translate(-50%, -50%) translate(${irisXGrande}px, ${irisYGrande}px)`;
    });

    function blink(eye) {
        eye.classList.add('blink');
        setTimeout(() => {
            eye.classList.remove('blink');
        }, 500);
    }

    // Função de piscar para um olho aleatório
    function blinkRandomEye() {
        const randomIndex = Math.floor(Math.random() * eyes.length);  // Seleciona um índice aleatório
        const randomEye = eyes[randomIndex];
        blink(randomEye);
    }

    // Intervalo para piscar um olho aleatório de cada vez a cada 5 segundos
    setInterval(() => {
        blinkRandomEye();
    }, 3000); // Pisca um olho aleatório a cada 5 segundos

    function positionEyesRandomly() {
        const margin = 20;
        const usedPositions = [];
        
        eyes.forEach((eye) => {
            let isOverlapping;
            let randomX, randomY;

            do {
                randomX = margin + Math.random() * (window.innerWidth - eye.offsetWidth - 2 * margin);
                randomY = margin + Math.random() * (window.innerHeight - eye.offsetHeight - 2 * margin);

                isOverlapping = usedPositions.some((pos) => {
                    const distanceX = Math.abs(pos.x - randomX);
                    const distanceY = Math.abs(pos.y - randomY);
                    return distanceX < eye.offsetWidth + margin && distanceY < eye.offsetHeight + margin;
                });
            } while (isOverlapping);

            usedPositions.push({ x: randomX, y: randomY });

            eye.style.position = 'absolute';
            eye.style.left = `${randomX}px`;
            eye.style.top = `${randomY}px`;
        });
    }

    positionEyesRandomly();
    setTimeout(() => {
        document.querySelectorAll('.eye').forEach(eye => eye.classList.remove('visible'));
    }, 246000);
};
