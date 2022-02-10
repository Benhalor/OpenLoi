function convertDate(str) {
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


export default convertDate
