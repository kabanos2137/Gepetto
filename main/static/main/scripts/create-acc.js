let hasAtLeastEightChars = false; // Initialize variable to check if password has at least 8 characters
let hasLowerUpperCase = false; // Initialize variable to check if password has both lower and upper case letters
let hasSpecialCharsOrNumbers = false; // Initialize variable to check if password has special characters or numbers
let passwordSame = false; // Initialize variable to check if password and retype password are the same

//#region Functions

function interpolateColor(startColor, endColor, progress) { // Interpolate between two colors
    const start = startColor.match(/\w\w/g).map(c => parseInt(c, 16)); // Convert hex to RGB
    const end = endColor.match(/\w\w/g).map(c => parseInt(c, 16)); // Convert hex to RGB
    const result = start.map((s, i) => Math.round(s + (end[i] - s) * progress)); // Interpolate each color channel
    return `rgb(${result[0]}, ${result[1]}, ${result[2]})`; // Convert to RGB
}

function animateLine(element, target, duration, startColor, endColor) { // Animate the line from one point to another
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
        element.setAttribute("stroke", interpolateColor(startColor, endColor, progress)); // Interpolate color

        if (progress < 1) { // Continue animation
            requestAnimationFrame(step); // Request next frame
        }
    }

    requestAnimationFrame(step); // Start animation
}

function hasBothCases(str) { // Check if the string has both lower and upper case letters
    return /[a-z]/.test(str) && /[A-Z]/.test(str); // Check if the string has both lower and upper case letters
}

function hasSpecialOrNumber(str) { // Check if the string has special characters or numbers
    return /[\d\W]/.test(str); // Check if the string has special characters or numbers
}

const displayCorrectAnimation = (svg) => { // Display the correct animation
    animateLine(svg.children[0], { x1: 1, y1: 8, x2: 8, y2: 15 }, 400, "#b30000", "#00b300"); // Animate the line from one point to another
    animateLine(svg.children[1], { x1: 8, y1: 15, x2: 15, y2: 1 }, 400, "#b30000", "#00b300"); // Animate the line from one point to another
}

const displayWrongAnimation = (svg) => { // Display the wrong animation
    animateLine(svg.children[0], { x1: 1, y1: 1, x2: 15, y2: 15 }, 400, "#00b300", "#b30000"); // Animate the line from one point to another
    animateLine(svg.children[1], { x1: 1, y1: 15, x2: 15, y2: 1 }, 400, "#00b300", "#b30000"); // Animate the line from one point to another
}

//#endregion

document.getElementById("create-acc-form-password").addEventListener("input", (event) => { // Add event listener to the password input field
    let value = event.target.value; // Get the value of the password input field
    let retypeValue = document.getElementById("create-acc-form-retype-password").value; // Get the value of the retype password input field

    if(value.length > 7 && hasAtLeastEightChars === false) { // Check if the password has at least 8 characters
        hasAtLeastEightChars = true; // Set the flag to true
        let svg = document.getElementById("create-acc-form-password-validation").children[0].children[0]; // Get the SVG element
        displayCorrectAnimation(svg); // Display the correct animation
    }else if(value.length < 8 && hasAtLeastEightChars){
        hasAtLeastEightChars = false; // Set the flag to false
        let svg = document.getElementById("create-acc-form-password-validation").children[0].children[0]; // Get the SVG element
        displayWrongAnimation(svg); // Display the wrong animation
    }

    if(hasBothCases(value) && hasLowerUpperCase === false){ // Check if the password has both lower and upper case letters
        hasLowerUpperCase = true; // Set the flag to true
        let svg = document.getElementById("create-acc-form-password-validation").children[1].children[0]; // Get the SVG element
        displayCorrectAnimation(svg); // Display the correct animation
    }else if(!hasBothCases(value) && hasLowerUpperCase){
        hasLowerUpperCase = false; // Set the flag to false
        let svg = document.getElementById("create-acc-form-password-validation").children[1].children[0]; // Get the SVG element
        displayWrongAnimation(svg); // Display the wrong animation
    }

    if(hasSpecialOrNumber(value) && hasSpecialCharsOrNumbers === false) { // Check if the password has special characters or numbers
        hasSpecialCharsOrNumbers = true; // Set the flag to true
        let svg = document.getElementById("create-acc-form-password-validation").children[2].children[0]; // Get the SVG element
        displayCorrectAnimation(svg); // Display the correct animation
    }else if(!hasSpecialOrNumber(value) && hasSpecialCharsOrNumbers){
        hasSpecialCharsOrNumbers = false; // Set the flag to false
        let svg = document.getElementById("create-acc-form-password-validation").children[2].children[0]; // Get the SVG element
        displayWrongAnimation(svg); // Display the wrong animation
    }

    if(value === retypeValue && passwordSame === false && value !== "") { // Check if the password and retype password are the same
        passwordSame = true; // Set the flag to true
        let svg = document.getElementById("create-acc-form-password-validation").children[3].children[0]; // Get the SVG element
        displayCorrectAnimation(svg); // Display the correct animation
    } else if ((value !== retypeValue && passwordSame) || (value === "" && retypeValue === "" && passwordSame)) {
        passwordSame = false; // Set the flag to false
        let svg = document.getElementById("create-acc-form-password-validation").children[3].children[0]; // Get the SVG element
        displayWrongAnimation(svg); // Display the wrong animation
    }
});

document.getElementById("create-acc-form-retype-password").addEventListener("input", (event) => { // Add event listener to the retype password input field
    let value = event.target.value; // Get the value of the retype password input field
    let passwordValue = document.getElementById("create-acc-form-password").value // Get the value of the password input field

    if(value === passwordValue && passwordSame === false && value !== "") { // Check if the password and retype password are the same
        passwordSame = true; // Set the flag to true
        let svg = document.getElementById("create-acc-form-password-validation").children[3].children[0]; // Get the SVG element
        displayCorrectAnimation(svg); // Display the correct animation
    } else if ((value !== passwordValue && passwordSame) || (value === "" && passwordValue === "" && passwordSame)) {
        passwordSame = false; // Set the flag to false
        let svg = document.getElementById("create-acc-form-password-validation").children[3].children[0]; // Get the SVG element
        displayWrongAnimation(svg); // Display the wrong animation
    }
});