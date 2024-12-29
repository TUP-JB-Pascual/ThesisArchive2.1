let currentSortColumn = -1;  // Keeps track of the current sorted column
let currentSortDirection = 'asc';  // Keeps track of the current sort direction

// Function to search the table
function searchTable() {
    let input = document.getElementById("searchInput");
    let filter = input.value.toUpperCase();
    let table = document.getElementById("dataTable");
    let tr = table.getElementsByTagName("tr");
    
    for (let i = 1; i < tr.length; i++) {
        let td = tr[i].getElementsByTagName("td");
        let match = false;
        
        for (let j = 0; j < td.length; j++) {
            if (td[j]) {
                let txtValue = td[j].textContent || td[j].innerText;
                if (txtValue.toUpperCase().indexOf(filter) > -1) {
                    match = true;
                }
            }
        }
        
        if (match) {
            tr[i].style.display = "";
        } else {
            tr[i].style.display = "none";
        }
    }
}

// Function to sort the table based on a column
function sortTable(n) {
    let table = document.getElementById("dataTable");
    let rows = table.rows;
    let switching = true;
    let switchcount = 0;

    // Check if the clicked column is already sorted
    if (currentSortColumn === n) {
        currentSortDirection = currentSortDirection === 'asc' ? 'desc' : 'asc';
    } else {
        currentSortColumn = n;
        currentSortDirection = 'asc';
    }

    while (switching) {
        switching = false;
        let rowsArray = Array.from(rows);
        
        for (let i = 1; i < rowsArray.length - 1; i++) {
            let x = rowsArray[i].getElementsByTagName("TD")[n];
            let y = rowsArray[i + 1].getElementsByTagName("TD")[n];
            
            if (currentSortDirection === "asc" && x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
                rowsArray[i].parentNode.insertBefore(rowsArray[i + 1], rowsArray[i]);
                switching = true;
                switchcount++;
                break;
            } else if (currentSortDirection === "desc" && x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
                rowsArray[i].parentNode.insertBefore(rowsArray[i + 1], rowsArray[i]);
                switching = true;
                switchcount++;
                break;
            }
        }

        if (switchcount === 0) {
            switching = false;
        }
    }

    // Update the sorting arrow indicators
    updateSortIndicators(n);
}

// Function to update the sorting arrows based on the column and direction
function updateSortIndicators(n) {
    let arrows = document.querySelectorAll('.sort-arrow');
    arrows.forEach((arrow) => {
        arrow.innerHTML = '';  // Reset all arrows
    });

    // Update the sort arrow for the column that was clicked
    let currentArrow = document.getElementById(n === 0 ? 'titleArrow' : n === 1 ? 'posterArrow' : n === 6 ? 'requestTitleArrow' :  n === 7 ? 'petitionerArrow' :  n === 8 ? 'emailArrow' : 'requestDateArrow');
    if (currentSortDirection === 'asc') {
        currentArrow.innerHTML = '<i class="fa-solid fa-caret-up"></i>';  // Up arrow for ascending
    } else {
        currentArrow.innerHTML = '<i class="fa-solid fa-caret-down"></i>';  // Down arrow for descending
    }
}
