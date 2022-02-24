import { findAll } from "highlight-words-core";

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
    if (string !== undefined && string !== null) {
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
    if (string !== undefined && string !== null) {
        return string.charAt(0).toUpperCase() + string.slice(1);
    } else {
        return string
    }

}

export function generateHighlightedHtml(textToHighlight, query, sanitizeFunction) {

    var searchWords

    if (query == "") {
        searchWords = []
    } else {
        searchWords = generateSearchWords(query)
    }
    const chunks = findAll({
        sanitize: sanitizeFunction,
        searchWords: searchWords,
        textToHighlight: textToHighlight

    });

    const highlightedText = chunks
        .map(chunk => {
            const { end, highlight, start } = chunk;
            const text = textToHighlight.substr(start, end - start);
            if (highlight) {
                return `<mark>${text}</mark>`;
            } else {
                return text;
            }
        })
        .join("");
    return highlightedText
}
