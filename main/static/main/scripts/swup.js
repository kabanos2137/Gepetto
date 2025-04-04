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

swup.hooks.on("page:view", (visit) => {
    addEventListeners(visit.to.url)
});

window.addEventListener("load", (event) => {
    addEventListeners(window.location.pathname)
})

swup.hooks.on('content:replace', () => {
    document.documentElement.classList.remove('is-leaving');
});

const addEventListeners = (url) => {
    if(url === "/create-acc"){
        document.getElementById("create-acc-form").reset();
        createAccountForm.addEventListeners();
    }else if(url === "/"){
        document.getElementById("log-in-form").reset();
        logInForm.addEventListeners();
    }
}