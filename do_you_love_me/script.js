document.addEventListener('DOMContentLoaded', () => {
    const yesBtn = document.getElementById('yesBtn');
    const noBtn = document.getElementById('noBtn');
    const mainContainer = document.getElementById('mainContainer');
    const bgMusic = document.getElementById('bgMusic');

    let isMusicPlaying = false;

    function startMusic() {
        if (isMusicPlaying || !bgMusic) return;

        bgMusic.volume = 0.3;
        bgMusic.play().then(() => {
            isMusicPlaying = true;
            // 5 saniye içinde (5000ms) sesi 0.3'ten 1.0'a çıkar
            const duration = 5000;
            const interval = 50; 
            const steps = duration / interval;
            const increment = (1.0 - 0.3) / steps;

            const volumeInterval = setInterval(() => {
                if (bgMusic.volume < 0.99) {
                    bgMusic.volume = Math.min(bgMusic.volume + increment, 1);
                } else {
                    bgMusic.volume = 1;
                    clearInterval(volumeInterval);
                }
            }, interval);
        }).catch(err => {
            console.log("Otomatik oynatma engellendi, etkileşim bekleniyor...");
        });
    }

    // Kullanıcı herhangi bir yere tıkladığında sesi başlat (Eğer otomatik başlamadıysa)
    document.body.addEventListener('click', () => {
        startMusic();
    }, { once: true }); // Sadece bir kez tetiklenmesi yeterli

    // Sayfa yüklendiğinde denemeye çalış (Bazı tarayıcılar izin verebilir)
    startMusic();

    let yesFontSize = 1.2;
    let yesPaddingV = 15;
    let yesPaddingH = 40;

    let clickCount = 0;
    const maxClicks = 5;

    noBtn.addEventListener('click', () => {
        clickCount++;

        if (clickCount === 1) {
            const btnGroup = document.getElementById('btnGroup');
            btnGroup.style.position = 'absolute';
            btnGroup.style.width = '100%';
            btnGroup.style.height = '100vh';
            btnGroup.style.top = '0';
            btnGroup.style.left = '0';
            btnGroup.style.transform = 'none';

            yesBtn.style.position = 'absolute';
            yesBtn.style.left = '50%';
            yesBtn.style.transform = 'translate(-50%, -50%)';
            yesBtn.style.transition = 'all 0.4s ease';

            noBtn.style.position = 'absolute';
            noBtn.style.left = 'calc(50% + 80px)';
            noBtn.style.transform = 'translate(0, -50%)';
            noBtn.style.transition = 'all 0.4s ease';
        }

        const progress = Math.min(clickCount / maxClicks, 1);
        const targetWidthVW = 95;
        const targetHeightVH = 95;
        const targetFontSizeRem = 10;

        const currentWidthVW = progress * targetWidthVW;
        const currentHeightVH = progress * targetHeightVH;
        const currentFontSizeRem = 1.2 + (progress * (targetFontSizeRem - 1.2));

        const topProgress = 65 - (progress * 15);
        yesBtn.style.top = `${topProgress}%`;
        noBtn.style.top = `${topProgress}%`;

        yesBtn.style.padding = '0';
        yesBtn.style.width = currentWidthVW > 0 ? `calc(${currentWidthVW}vw + 120px)` : '120px';
        yesBtn.style.height = currentHeightVH > 0 ? `calc(${currentHeightVH}vh + 50px)` : '50px';
        yesBtn.style.fontSize = `${currentFontSizeRem}rem`;

        const moveY = (Math.random() - 0.5) * 40;
        noBtn.style.left = `calc(50% + ${currentWidthVW / 2}vw + 80px)`;
        noBtn.style.transform = `translate(0, calc(-50% + ${moveY}px)) rotate(${Math.random() * 20 - 10}deg)`;

        const texts = ["Emin misin?", "Lütfen!", "LÜTFEEEEN!!", "😭😭😭", "🤨🤨🤨"];
        noBtn.innerText = texts[Math.floor(Math.random() * texts.length)];

        if (clickCount >= maxClicks) {
        }
    });

    yesBtn.addEventListener('click', () => {
        playLoadingAnimation();
    });

    function playLoadingAnimation() {
        mainContainer.innerHTML = '';
        const loaderContainer = document.createElement('div');
        loaderContainer.className = 'loader-container';
        loaderContainer.innerHTML = `
            <div class="loader-dot dot-1"></div>
            <div class="loader-dot dot-2"></div>
            <div class="loader-dot dot-3"></div>
            <svg class="loader-heart" viewBox="0 0 32 29.6">
                <path d="M23.6,0c-3.4,0-6.3,2.7-7.6,5.6C14.7,2.7,11.8,0,8.4,0C3.8,0,0,3.8,0,8.4c0,9.4,9.5,11.9,16,21.2
                c6.1-9.3,16-12.1,16-21.2C32,3.8,28.2,0,23.6,0z" fill="currentColor"/>
            </svg>
        `;
        mainContainer.appendChild(loaderContainer);

        setTimeout(() => {
            triggerSuccess();
        }, 3100);
    }

    function triggerSuccess() {
        mainContainer.innerHTML = '';
        mainContainer.style.background = 'transparent';
        mainContainer.style.boxShadow = 'none';

        const successDiv = document.createElement('div');
        successDiv.className = 'success-message';
        successDiv.style.display = 'flex';
        successDiv.style.flexDirection = 'column';
        successDiv.style.alignItems = 'center';
        successDiv.style.justifyContent = 'center';
        successDiv.style.width = '100vw';
        successDiv.style.height = '100vh';
        successDiv.innerHTML = `
            <img src="assets/yipiiiieee.jpg" alt="Arkadaşlar" style="max-width: 400px; border-radius: 10px; margin-bottom: 20px;">
            <div style="text-align: center; color: var(--dark);">
                Yippieee! ❤️<br>
                <span style="font-size: 1.5rem; display: block; margin-top: 20px;">BENDE SENİ SEVİYORUM</span>
            </div>
        `;
        document.body.appendChild(successDiv);

        document.body.style.background = '#fff0f3';

        createHearts();
    }

    function createHearts() {
        setInterval(() => {
            const heart = document.createElement('div');
            heart.innerHTML = '❤️';
            heart.style.position = 'absolute';
            heart.style.left = Math.random() * 100 + 'vw';
            heart.style.top = '-50px';
            heart.style.fontSize = (Math.random() * 20 + 10) + 'px';
            const duration = (Math.random() * 3 + 2) * 3.5;
            heart.style.animation = `fall ${duration}s linear forwards`;
            heart.style.color = '#ff4d6d';
            heart.style.opacity = Math.random() * 0.5 + 0.5;
            document.body.appendChild(heart);

            setTimeout(() => {
                heart.remove();
            }, duration * 1000);
        }, 100);
    }
});
