class appPage {
    menuExpanded = false;

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
        document.getElementById("app-settings-bar-logoff").addEventListener("click", (event) => {
            this.logoffEventListener(event);
        });

        document.getElementById("app-settings-bar-expand").addEventListener("click", (event) => {
            this.expandEventListener(event);
        })

        document.getElementById("app-settings-bar-logoff-p").addEventListener("click", (event) => {
            this.logoffEventListener(event);
        });

        document.getElementById("app-settings-bar-expand-p").addEventListener("click", (event) => {
            this.expandEventListener(event);
        })
    }
}