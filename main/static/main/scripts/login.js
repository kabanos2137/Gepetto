class logInForm {
    static errorDisplay(remove = false) {
        let error = document.getElementById("log-in-form-err-message");

        if(remove){
            error.className = "hidden";
        }else{
            error.innerHTML = "Login was unsuccessful. Please try again.";
            error.className = "";
        }

    }

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
                    this.errorDisplay();
                }
            })
            .catch(err => console.error(err));
    }

    static formFieldEventListener(event) {
        this.errorDisplay(true);
    }

    static addEventListeners() {
        document.getElementById("log-in-form-button-log-in").addEventListener("click", (event) => {
            logInForm.logInButtonEventListener(event);
        });

        document.getElementById("log-in-form-username").addEventListener("input", (event) => {
            logInForm.formFieldEventListener(event);
        });

        document.getElementById("log-in-form-password").addEventListener("input", (event) => {
            logInForm.formFieldEventListener(event);
        });
    }
}