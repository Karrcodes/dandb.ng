// Gallery functionality
document.addEventListener('DOMContentLoaded', () => {
    // Trusted By auto-scroll gallery
    const trustedByTrack = document.querySelector('.trusted-by-track');

    if (trustedByTrack) {
        // Logo data (from current site)
        const logos = [
            'logo1.png', 'logo2.png', 'logo3.png', 'logo4.png',
            'logo5.png', 'logo6.png', 'logo7.png', 'logo8.png'
        ];

        // Duplicate logos for infinite scroll
        const logosHTML = logos.map(logo =>
            `<img src="../media/trusted-by/${logo}" alt="Trusted client logo" class="trusted-logo">`
        ).join('');

        // Add logos twice for seamless loop
        trustedByTrack.innerHTML = logosHTML + logosHTML;

        // Pause on touch
        let isPaused = false;
        trustedByTrack.addEventListener('touchstart', () => {
            trustedByTrack.style.animationPlayState = 'paused';
            isPaused = true;
        });

        trustedByTrack.addEventListener('touchend', () => {
            setTimeout(() => {
                if (isPaused) {
                    trustedByTrack.style.animationPlayState = 'running';
                    isPaused = false;
                }
            }, 2000);
        });
    }

    // Project galleries with scroll indicators
    const galleries = document.querySelectorAll('.project-gallery');

    galleries.forEach(gallery => {
        // Add scroll indicator
        const indicator = document.createElement('div');
        indicator.className = 'scroll-indicator';
        indicator.textContent = 'Scroll >';
        gallery.parentElement.style.position = 'relative';
        gallery.parentElement.appendChild(indicator);

        // Hide indicator on scroll
        let scrollTimeout;
        gallery.addEventListener('scroll', () => {
            if (gallery.scrollLeft > 10) {
                indicator.classList.add('hidden');
            } else {
                indicator.classList.remove('hidden');
            }

            clearTimeout(scrollTimeout);
            scrollTimeout = setTimeout(() => {
                if (gallery.scrollLeft <= 10) {
                    indicator.classList.remove('hidden');
                }
            }, 1000);
        }, { passive: true });
    });
});
