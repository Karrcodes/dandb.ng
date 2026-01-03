// Populate Trusted By logos
document.addEventListener('DOMContentLoaded', () => {
    const track = document.querySelector('.trusted-by-track');
    if (!track) return;

    const logos = ['NNPC.png', 'central-bank-of-nigeria-cbn-logo-42FD3093EE-seeklogo.com.png', 'cropped-kdsg-logo.png', 'fct-logo_0.png', 'NSITF-logo.png', 'Yobe_State_Logo.png', 'ZMSG.png', 'Taraba-Logo3.png'];

    // Triple logos for infinite scroll
    const allLogos = [...logos, ...logos, ...logos];
    track.innerHTML = allLogos.map(logo => `<img src="media/Logos/${logo}" alt="Client logo" class="trusted-logo" loading="lazy">`).join('');
});
