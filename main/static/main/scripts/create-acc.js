let hasAtLeastEightChars = false; // Initialize variable to check if password has at least 8 characters
let hasLowerUpperCase = false; // Initialize variable to check if password has both lower and upper case letters
let hasSpecialCharsOrNumbers = false; // Initialize variable to check if password has special characters or numbers
let passwordSame = false; // Initialize variable to check if password and retype password are the same

let loginDuplicate = false; // Initialize variable to check if username is already taken
let emailDuplicate = false; // Initialize variable to check if email is already taken

class createAccountForm {
    static interpolateColor(startColor, endColor, progress) { // Interpolate between two colors
        const start = startColor.match(/\w\w/g).map(c => parseInt(c, 16)); // Convert hex to RGB
        const end = endColor.match(/\w\w/g).map(c => parseInt(c, 16)); // Convert hex to RGB
        const result = start.map((s, i) => Math.round(s + (end[i] - s) * progress)); // Interpolate each color channel
        return `rgb(${result[0]}, ${result[1]}, ${result[2]})`; // Convert to RGB
    }

    static animateLine(element, target, duration, startColor, endColor) { // Animate the line from one point to another
        let startTime = null; // Initialize start time
        const initial = { // Get initial coordinates
            x1: parseFloat(element.getAttribute("x1")),
            y1: parseFloat(element.getAttribute("y1")),
            x2: parseFloat(element.getAttribute("x2")),
            y2: parseFloat(element.getAttribute("y2"))
        };

        function step(timestamp) { // Animation step function
            if (!startTime) startTime = timestamp; // Set start time
            let progress = (timestamp - startTime) / duration; // Calculate progress
            if (progress > 1) progress = 1; // Clamp progress to 1

            element.setAttribute("x1", initial.x1 + (target.x1 - initial.x1) * progress); // Interpolate x1
            element.setAttribute("y1", initial.y1 + (target.y1 - initial.y1) * progress); // Interpolate y1
            element.setAttribute("x2", initial.x2 + (target.x2 - initial.x2) * progress); // Interpolate x2
            element.setAttribute("y2", initial.y2 + (target.y2 - initial.y2) * progress); // Interpolate y2
            element.setAttribute("stroke", createAccountForm.interpolateColor(startColor, endColor, progress)); // Interpolate color

            if (progress < 1) { // Continue animation
                requestAnimationFrame(step); // Request next frame
            }
        }

        requestAnimationFrame(step); // Start animation
    }
    static displayCorrectAnimation(svg) { // Display the correct animation
        this.animateLine(svg.children[0], { x1: 1, y1: 8, x2: 8, y2: 15 }, 400, "#b30000", "#00b300"); // Animate the line from one point to another
        this.animateLine(svg.children[1], { x1: 8, y1: 15, x2: 15, y2: 1 }, 400, "#b30000", "#00b300"); // Animate the line from one point to another
    }

    static displayWrongAnimation(svg) { // Display the wrong animation
        this.animateLine(svg.children[0], { x1: 1, y1: 1, x2: 15, y2: 15 }, 400, "#00b300", "#b30000"); // Animate the line from one point to another
        this.animateLine(svg.children[1], { x1: 1, y1: 15, x2: 15, y2: 1 }, 400, "#00b300", "#b30000"); // Animate the line from one point to another
    }

    static passwordEventListener(event) {
        let value = event.target.value; // Get the value of the password input field
        let retypeValue = document.getElementById("create-acc-form-retype-password").value; // Get the value of the retype password input field

        if(value.length > 7 && hasAtLeastEightChars === false) { // Check if the password has at least 8 characters
            hasAtLeastEightChars = true; // Set the flag to true
            let svg = document.getElementById("create-acc-form-password-validation").children[0].children[0]; // Get the SVG element
            this.displayCorrectAnimation(svg); // Display the correct animation
        }else if(value.length < 8 && hasAtLeastEightChars){
            hasAtLeastEightChars = false; // Set the flag to false
            let svg = document.getElementById("create-acc-form-password-validation").children[0].children[0]; // Get the SVG element
            this.displayWrongAnimation(svg); // Display the wrong animation
        }

        if(hasBothCases(value) && hasLowerUpperCase === false){ // Check if the password has both lower and upper case letters
            hasLowerUpperCase = true; // Set the flag to true
            let svg = document.getElementById("create-acc-form-password-validation").children[1].children[0]; // Get the SVG element
            this.displayCorrectAnimation(svg); // Display the correct animation
        }else if(!hasBothCases(value) && hasLowerUpperCase){
            hasLowerUpperCase = false; // Set the flag to false
            let svg = document.getElementById("create-acc-form-password-validation").children[1].children[0]; // Get the SVG element
            this.displayWrongAnimation(svg); // Display the wrong animation
        }

        if(hasSpecialOrNumber(value) && hasSpecialCharsOrNumbers === false) { // Check if the password has special characters or numbers
            hasSpecialCharsOrNumbers = true; // Set the flag to true
            let svg = document.getElementById("create-acc-form-password-validation").children[2].children[0]; // Get the SVG element
            this.displayCorrectAnimation(svg); // Display the correct animation
        }else if(!hasSpecialOrNumber(value) && hasSpecialCharsOrNumbers){
            hasSpecialCharsOrNumbers = false; // Set the flag to false
            let svg = document.getElementById("create-acc-form-password-validation").children[2].children[0]; // Get the SVG element
            this.displayWrongAnimation(svg); // Display the wrong animation
        }

        if(value === retypeValue && passwordSame === false && value !== "") { // Check if the password and retype password are the same
            passwordSame = true; // Set the flag to true
            let svg = document.getElementById("create-acc-form-password-validation").children[3].children[0]; // Get the SVG element
            this.displayCorrectAnimation(svg); // Display the correct animation
        } else if ((value !== retypeValue && passwordSame) || (value === "" && retypeValue === "" && passwordSame)) {
            passwordSame = false; // Set the flag to false
            let svg = document.getElementById("create-acc-form-password-validation").children[3].children[0]; // Get the SVG element
            this.displayWrongAnimation(svg); // Display the wrong animation
        }
    }

    static retypePasswordEventListener(event) {
        let value = event.target.value; // Get the value of the retype password input field
        let passwordValue = document.getElementById("create-acc-form-password").value // Get the value of the password input field

        if(value === passwordValue && passwordSame === false && value !== "") { // Check if the password and retype password are the same
            passwordSame = true; // Set the flag to true
            let svg = document.getElementById("create-acc-form-password-validation").children[3].children[0]; // Get the SVG element
            this.displayCorrectAnimation(svg); // Display the correct animation
        } else if ((value !== passwordValue && passwordSame) || (value === "" && passwordValue === "" && passwordSame)) {
            passwordSame = false; // Set the flag to false
            let svg = document.getElementById("create-acc-form-password-validation").children[3].children[0]; // Get the SVG element
            this.displayWrongAnimation(svg); // Display the wrong animation
        }
    }

    static errorDisplay(errorMSG) {
        let display;
        let error = document.getElementById("create-acc-form-err-message");

        if(errorMSG){
            display = errorMSG;
        }else if(loginDuplicate && emailDuplicate){
            display = "Username and email are already taken"; // Display error message
        }else if(loginDuplicate) {
            display = "Username is already taken"; // Display error message
        }else if(emailDuplicate) {
            display = "Email is already taken"; // Display error message
        }else{
            error.className = "hidden"; // Set class name to hidden
            return;
        }

        error.innerHTML = display;
        error.className = "";
    }

    static loginEventListener(event) { // Add event listener to the login input field
        let value = event.target.value;

        fetch("/api/user?username=" + value)
            .then(res => res.json())
            .then(res => {
                loginDuplicate = res.found; // Check if the username is already taken
                this.errorDisplay() // Display error message if username is already taken
            })
    }

    static emailEventListener(event) { // Add event listener to the login input field
        let value = event.target.value;

        fetch("/api/user?email=" + value)
            .then(res => res.json())
            .then(res => {
                emailDuplicate = res.found; // Check if the username is already taken
                this.errorDisplay() // Display error message if mail is already taken
            })
    }

    static createAccountEventListener(event) { // Add event listener to the create account button
        event.preventDefault(); // Prevent default action)

        let form = new FormData(document.forms["create-acc-form"]); // Get the form data

        let username = form.get("username"); // Get the username
        let password = form.get("password"); // Get the password
        let email = form.get("email"); // Get the email

        if (username === "") { // Check if the data is valid
            this.errorDisplay("Username cannot be empty")
            return;
        }else if(password === ""){
            this.errorDisplay("Password cannot be empty")
            return;
        }else if(email === ""){
            this.errorDisplay("E-mail cannot be empty")
            return;
        }

        if(hasAtLeastEightChars && hasLowerUpperCase && hasSpecialCharsOrNumbers && passwordSame && !loginDuplicate && !emailDuplicate) { // Check if the data is valid
            fetch("/api/user", { // Send the data to the server
                method: "POST",
                headers: {
                    "Content-Type": "application/json" // Set content type to JSON
                },
                body: JSON.stringify({
                    username: username,
                    password: password,
                    email: email
                })
            })
                .then(res => res.json())
                .then(() => {
                    swup.navigate('/create-acc-success'); // Navigate to the success page
                });
        }
    }

    static addEventListeners() {
        document.getElementById("create-acc-form-username").addEventListener("input", (event) => { // Add event listener to the username input field)
            this.loginEventListener(event); // Add event listener to the username input field
        });

        document.getElementById("create-acc-form-email").addEventListener("input", (event) => { // Add event listener to the username input field)
            this.emailEventListener(event); // Add event listener to the email input field
        });

        document.getElementById("create-acc-form-password").addEventListener("input", (event) => { // Add event listener to the password input field
            this.passwordEventListener(event); // Add event listener to the password input field
        });

        document.getElementById("create-acc-form-retype-password").addEventListener("input", (event) => { // Add event listener to the retype password input field
            this.retypePasswordEventListener(event); // Add event listener to the retype password input field
        });

        document.getElementById("create-acc-form-button-create-account").addEventListener("click", (event) => {
           this.createAccountEventListener(event); // Add event listener to the create account button
        });
    }
}
