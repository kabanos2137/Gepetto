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