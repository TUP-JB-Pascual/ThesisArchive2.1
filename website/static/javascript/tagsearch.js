// Function to filter links based on the search input
function filterLinks() {
    let searchTerm = document.getElementById('searchInput').value.toLowerCase(); // Get the search term
    let links = document.getElementsByClassName('tag_item'); // Get all <a> tags with class 'link'

    // Loop through the links and hide or show based on search term
    for (let i = 0; i < links.length; i++) {
        let linkText = links[i].textContent.toLowerCase(); // Get text content of each link
        
        if (linkText.indexOf(searchTerm) > -1) {
            links[i].style.display = "initial"; // Show the link if it matches
            links[i].style = "margin: 0px 0px 3px 0px;"; // Show the link if it matches
        } else {
            links[i].style.display = "none"; // Hide the link if it doesn't match
        }
    }
}