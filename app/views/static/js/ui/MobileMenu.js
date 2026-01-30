export function initMobileMenu() {
    const toggle = document.getElementById('mobileMenuToggle');
    const nav = document.querySelector('.nav-tabs');

    if (!toggle || !nav) return;

    toggle.addEventListener('click', e => {
        e.stopPropagation();
        nav.classList.toggle('show');
    });

    document.addEventListener('click', e => {
        if (!e.target.closest('.navbar')) {
            nav.classList.remove('show');
        }
    });
}
