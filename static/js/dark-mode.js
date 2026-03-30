document.addEventListener('DOMContentLoaded', () => {
    const darkModeToggle = document.getElementById('darkmodeID');
    const body = document.body;

    if (localStorage.getItem('dark-mode') === 'enabled') {
        body.classList.add('dark-mode');
        if (darkModeToggle) darkModeToggle.textContent = 'Modo Claro';
    } else {
        if (darkModeToggle) darkModeToggle.textContent = 'Modo Escuro';
    }

    if (darkModeToggle) {
        darkModeToggle.addEventListener('click', () => {
            body.classList.toggle('dark-mode');
            if (body.classList.contains('dark-mode')) {
                localStorage.setItem('dark-mode', 'enabled');
                darkModeToggle.textContent = 'Modo Claro';
            } else {
                localStorage.setItem('dark-mode', 'disabled');
                darkModeToggle.textContent = 'Modo Escuro';
            }
        });
    }
});
