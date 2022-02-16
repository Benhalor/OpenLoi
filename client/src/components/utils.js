export function convertDate(str) {

    var date = new Date(str)
    let monthNames = ["jan.", "fev.", "mars", "avril",
        "mai", "juin", "juill.", "août",
        "sept.", "oct.", "nov.", "dec."];

    let day = date.getDate();

    let monthIndex = date.getMonth();
    let monthName = monthNames[monthIndex];

    let year = date.getFullYear();

    return `${day} ${monthName} ${year} `;
}

export function sanitizeWords(string) {
    if (string !== undefined) {
        return string.normalize("NFD").replace(/\p{Diacritic}/gu, "")
    } else {
        return string
    }
}

export function generateSearchWords(spacedSeparatedWords) {
    var listOfWords = spacedSeparatedWords.split(" ")
    for (var i = 0; i < listOfWords.length; i++) {
        listOfWords[i] = "\\b(?=\\w*" + listOfWords[i] + ")\\w+\\b"
    }
    return listOfWords
}

export function firstLetterUppercase(string) {
    if (string !== undefined) {
        return string.charAt(0).toUpperCase() + string.slice(1);
    } else {
        return string
    }

}
