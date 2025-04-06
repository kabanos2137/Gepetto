let createAssistantOwnImage = false;

class appSettingsBar {
    static logoffEventListener(event) {
        localStorage.removeItem("username");
        localStorage.removeItem("password");

        swup.navigate("/");
    }

    static expandEventListener(event) {
        document.getElementById("app-content").classList.toggle("blurred");
        document.getElementById("app-settings-bar").classList.toggle("expanded");
    }

    static addEventListeners() {
        document.getElementById("app-settings-bar-home").addEventListener("click", (event) => {
            swup.navigate("/app");
        });

        document.getElementById("app-settings-bar-logoff").addEventListener("click", (event) => {
            this.logoffEventListener(event);
        });

        document.getElementById("app-settings-bar-expand").addEventListener("click", (event) => {
            this.expandEventListener(event);
        })

        document.getElementById("app-settings-bar-logoff-p").addEventListener("click", (event) => {
            this.logoffEventListener(event);
        });
    }
}

class appPage {
    static contentCreateAssistantEventListener(event) {
        swup.navigate("/create-assistant");
    }

    static addEventListeners() {
        document.getElementById("app-content-create-assistant").addEventListener("click", (event) => {
            this.contentCreateAssistantEventListener(event);
        })
    }
}

class createAssistantPage {
    static nameEventListener(event) {
        if(!createAssistantOwnImage){
            const canvas = document.getElementById("create-assistant-form-profile-picture-generator");
            const ctx = canvas.getContext("2d");
            const diameter = 150;
            const letter = event.target.value ? event.target.value[0].toUpperCase() : "";

            ctx.beginPath();
            ctx.arc(diameter / 2, diameter / 2, diameter / 2, 0, Math.PI * 2);
            ctx.fillStyle = "#707070";
            ctx.fill();
            ctx.closePath();

            ctx.font = "70px Jura";
            ctx.fillStyle = "#D9D9D9";
            ctx.textAlign = "center";
            ctx.textBaseline = "middle";
            ctx.fillText(letter, diameter / 2, diameter / 2);

            document.getElementById("create-assistant-form-profile-picture").src = canvas.toDataURL("image/png");
        }
    }

    static errorDisplay(errorMSG) {
        let error = document.getElementById("create-assistant-error");

        error.innerHTML = errorMSG;
        error.className = "";
    }

    static createEventListener(event) {
        let form = new FormData(document.forms['create-assistant-form']);
        let canvas = document.getElementById("create-assistant-form-profile-picture-generator")

        let name = form.get("name");
        let description = form.get("description");
        let responseStyle = form.get("response-style");
        let tone = form.get("tone");
        let profilePicture = canvas.toDataURL("image/png");

        if(name === "" || description === "" || responseStyle === "" || tone === "") {
            this.errorDisplay("Please fill in all fields");
            return;
        }

        fetch("/api/assistant", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({
                assistant_name: name,
                description: description,
                response_style: responseStyle,
                tone: tone,
                profile_picture: profilePicture,
                username: localStorage.getItem("username"),
                password: localStorage.getItem("password"),
            })
        })
            .then(res => res.json())
            .then(res => {
            })
            .catch(err => {
                console.error(err);
            })
    }

    static addEventListeners() {
        createAssistantOwnImage = false;

        document.getElementById("create-assistant-form-name").addEventListener("input", (event) => {
            this.nameEventListener(event);
        });

        document.addEventListener('keypress', function(event) {
            if (event.key === 'Enter') {
                event.preventDefault();
                createAssistantPage.createEventListener(event);
            }
        });

        document.getElementById("create-assistant-submit").addEventListener("click", (event) => {
            this.createEventListener(event);
        })
    }
}