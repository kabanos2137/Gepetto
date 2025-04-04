class logInForm {
    static logInButtonEventListener(event) {
        event.preventDefault();

        let form = new FormData(document.forms["log-in-form"]);

        let username = form.get("username");
        let password = form.get("password");

        fetch("/api/login?username=" + username + "&password=" + password)
            .then(res => res.json())
            .then(res => {
                if(res.found){
                    swup.navigate("/app")
                }else{
                    //TODO: show error message
                }
            })
            .catch(err => console.error(err));
    }

    static addEventListeners() {
        document.getElementById("log-in-form-button-log-in").addEventListener("click", (event) => {
            logInForm.logInButtonEventListener(event);
        });
    }
}