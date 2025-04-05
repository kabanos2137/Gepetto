const swup = new Swup();

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
    let username = localStorage.getItem("username");
    let password = localStorage.getItem("password");

    if(url === "/create-acc"){
        if(username === null || password === null){
            document.getElementById("create-acc-form").reset();
            createAccountForm.addEventListeners();
        }else {
            if(isMobile(window)) {
                swup.navigate("/m-app")
            }else{
                swup.navigate("/app")
            }
        }
    }else if(url === "/"){
        if(username === null || password === null){
            document.getElementById("log-in-form").reset();
            logInForm.addEventListeners();
        }else {
            if(isMobile(window)) {
                swup.navigate("/m-app")
            }else{
                swup.navigate("/app")
            }
        }
    }else if(url === "/app") {
        if (username === null || password === null) {
            swup.navigate("/")
        } else {
            if(isMobile(window)) {
                swup.navigate("/m-app")
            }else{
                appPage.addEventListeners();
            }
        }
    }else if(url === "/m-app") {
        if (username === null || password === null) {
            swup.navigate("/")
        } else {
            if(isMobile(window)) {

            }else{
                swup.navigate("/app")
            }
        }
    }
}