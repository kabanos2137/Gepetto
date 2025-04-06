const swup = new Swup();

swup.hooks.on('animation:out:start', (visit) => {
    if (
        (visit.from.url === '/app' && visit.to.url === '/create-assistant') ||
        (visit.from.url === '/create-assistant' && visit.to.url === '/app')
    ) {
        document.body.classList.add('partial-transition');
    }

    document.documentElement.classList.add('is-leaving');
    return new Promise((resolve) => {
        setTimeout(() => {
            resolve();
        }, 500);
    });
});

swup.hooks.on('content:replace', () => {
    document.documentElement.classList.remove('is-leaving');
    document.body.classList.remove('partial-transition');
});

swup.hooks.on("page:view", (visit) => {
    addEventListeners(visit.to.url);
});

window.addEventListener("load", () => {
    addEventListeners(window.location.pathname);
});

const addEventListeners = (url) => {
    let username = localStorage.getItem("username");
    let password = localStorage.getItem("password");

    if(url === "/create-acc"){
        if(username === null || password === null){
            document.getElementById("create-acc-form").reset();
            createAccountForm.addEventListeners();
        } else {
            swup.navigate(isMobile(window) ? "/m-app" : "/app");
        }
    } else if(url === "/"){
        if(username === null || password === null){
            document.getElementById("log-in-form").reset();
            logInForm.addEventListeners();
        } else {
            swup.navigate(isMobile(window) ? "/m-app" : "/app");
        }
    } else if(url === "/app" || url === "/create-assistant") {
        if(username === null || password === null) {
            swup.navigate("/");
        } else {
            if(url === "/app") {
                appSettingsBar.addEventListeners();
                appPage.addEventListeners();
            }else if(url === "/create-assistant"){
                appSettingsBar.addEventListeners();
            }
        }
    } else if(url === "/m-app") {
        if(username === null || password === null) {
            swup.navigate("/");
        } else {
            swup.navigate(isMobile(window) ? null : "/app");
        }
    }
}
