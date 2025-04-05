class appPage {
    static logoffEventListener(event) {
        localStorage.removeItem("username");
        localStorage.removeItem("password");

        swup.navigate("/");
    }

    static addEventListeners() {
        document.getElementById("app-settings-bar-logoff").addEventListener("click", (event) => {
            console.log("aa")
            this.logoffEventListener(event);
        });
    }
}