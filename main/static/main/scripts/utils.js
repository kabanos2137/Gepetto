function hasBothCases(str) { // Check if the string has both lower and upper case letters
    return /[a-z]/.test(str) && /[A-Z]/.test(str); // Check if the string has both lower and upper case letters
}

function hasSpecialOrNumber(str) { // Check if the string has special characters or numbers
    return /[\d\W]/.test(str); // Check if the string has special characters or numbers
}