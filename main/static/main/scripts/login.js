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

    static logInButtonEventListener (event) {
        event.preventDefault();

        fetch("/api/public_key")
            .then(res => res.json())
            .then(data => {
                let publicKey = data.public_key

                const encryptor = new JSEncrypt();
                encryptor.setPublicKey(publicKey);

                let form = new FormData(document.forms["log-in-form"]);
                let password = form.get("password");

                let encryptedPassword = encryptor.encrypt(password.toString());
                let username = form.get("username");

                fetch("/api/login", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        'X-CSRFToken': csrftoken
                    },
                    body: JSON.stringify({
                        username: username,
                        password: encryptedPassword
                    })
                })
                    .then(res => res.json())
                    .then(res => {
                        if(res.found){
                            localStorage.setItem("token", res.token);
                            localStorage.setItem("username", username.toString());
                            localStorage.setItem("password", password.toString());
                            if(isMobile(window)){
                                swup.navigate("/m-app")
                            }else{
                                swup.navigate("/app")
                            }
                        }else{
                            this.errorDisplay();
                        }
                    })
                    .catch(err => console.log(err));
            })
            .catch(err => console.log(err));
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