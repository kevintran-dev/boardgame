
let UPC = ""
let boardgameName = ""
let bggId = ""

async function UPC_lookup() {
    const res = await axios.get(`https://api.gameupc.com/test/upc/${UPC}`, { headers: { 'x-api-key': 'test_test_test_test_test' } });
    console.log(res)
    boardgameName = res.data.name
    if (res.data.bgg_info.length != 0) {
        bggId = res.data.bgg_info[0].id
        let name_line = document.getElementById('game_name');
        name_line.value = boardgameName;
        let id_line = document.getElementById('bgg_id')
        id_line.value = bggId;
        UPC = "";
        boardgameName = "";
        bggId = "";
    }
    else {
        console.log('no bgg_info')
        let name_line = document.getElementById('game_name');
        name_line.value = boardgameName;
        let id_line = document.getElementById('bgg_id');
        bggId = "";
        id_line.value = bggId;
        UPC = "";
        boardgameName = "";
    }
}

function displayStars() {
    let x = document.querySelectorAll("[data-rating]")
    console.log(x)
}


/**
 * Sorts a HTML table.
 *
 * @param {HTMLTableElement} table The table to sort
 * @param {number} column The index of the column to sort
 * @param {boolean} asc Determines if the sorting will be in ascending
 */
function sortTableByColumn(table, column, asc = true) {
    const dirModifier = asc ? 1 : -1;
    const tBody = table.tBodies[0];
    console.log(tBody);
    const rows = Array.from(tBody.querySelectorAll("tr"));
    // Sort each row
    const sortedRows = rows.sort((a, b) => {
        console.log(a);
        console.log(b);
        const aColText = a.querySelector(`td:nth-child(${column + 1})`).textContent.trim();
        const bColText = b.querySelector(`td:nth-child(${column + 1})`).textContent.trim();
        return aColText > bColText ? (1 * dirModifier) : (-1 * dirModifier);
    });

    // Remove all existing TRs from the table
    while (tBody.firstChild) {
        tBody.removeChild(tBody.firstChild);
    }

    // Re-add the newly sorted rows
    tBody.append(...sortedRows);

    // Remember how the column is currently sorted
    table.querySelectorAll("th").forEach(th => th.classList.remove("th-sort-asc", "th-sort-desc"));
    table.querySelector(`th:nth-child(${column + 1})`).classList.toggle("th-sort-asc", asc);
    table.querySelector(`th:nth-child(${column + 1})`).classList.toggle("th-sort-desc", !asc);
}

document.querySelectorAll(".sort").forEach(headerCell => {
    headerCell.addEventListener("click", () => {
        const tableElement = headerCell.parentElement.parentElement.parentElement;
        console.log(tableElement)
        const headerIndex = Array.prototype.indexOf.call(headerCell.parentElement.children, headerCell);
        const currentIsAscending = headerCell.classList.contains("th-sort-asc");

        sortTableByColumn(tableElement, headerIndex, !currentIsAscending);
    });
});

