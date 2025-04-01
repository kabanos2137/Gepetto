const swup = new Swup({
    animationSelector: '.transition-fade'
});

swup.hooks.on('animation:out:start', (visit) => {
    document.documentElement.classList.add('is-leaving');
    return new Promise((resolve) => {
        setTimeout(() => {
            resolve(); // Kontynuuje po 500ms
        }, 500);
    });
});

swup.hooks.on('content:replace', () => {
    document.documentElement.classList.remove('is-leaving');
});