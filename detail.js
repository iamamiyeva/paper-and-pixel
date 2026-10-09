let data = [];

async function fetchData() {
    const urlParams = new URLSearchParams(window.location.search);
    const bookID = urlParams.get('id');
    if(!bookID) {
        console.error("Couldn't find the ID of the book!");
        return;
    }
    const url = `http://127.0.0.1:5000/api/books/${bookID}`

    try{
        const response = await fetch(url);

        if(!response.ok){
            throw new Error("Couldn't fetch response");
        }
        data = await response.json();

        renderBook(data);
    }
    catch(error){
            console.error(error);   
    }
}

function renderBook() {
    if (document.getElementById("book-title")) {
        document.getElementById("book-title").innerText = data.title;
    }
    if (document.getElementById("book-author")){
        document.getElementById("book-author").innerText = data.author;
    }
    if (document.getElementById("book-category")){
        document.getElementById("book-category").innerText = data.category;
    }
    if (document.getElementById("book-point")){
        document.getElementById("book-point").innerText = data.point;
    }
    if (document.getElementById("book-page")) {
        document.getElementById("book-page").innerText = data.page_num + " pages";
    }
    if (document.getElementById("book-cover") && data.image_url){
        document.getElementById("book-cover").src = data.image_url;
    }
    if (document.getElementById("book-summary")) {
        console.log("image url: ", data.image_url);
        document.getElementById("book-summary").innerText = data.summary;
    }
}

fetchData();

async function fetchBooksByCategory(categoryId) {
    const url = "http://127.0.0.1:5000/api/books";
    
    if (categoryId) {
        url += `?category_id=${categoryId}`
    }

    try{
        const response = await fetch(url);
        const book = await response.json();

        renderBook(book);
    }
    catch(error) {
        console.error("There was an ERROR on fetching!", error);
    }
}


/*    index.html  ucin   */
/* kici ekranda sidebar hide etmek */

const menuIcon = document.querySelector('.material-icons');
const sidebar = document.querySelector('.sidebar');

menuIcon.addEventListener('click', (e) => {
        sidebar.classList.toggle('active');
})


/* search bar */
const bookSearch = document.querySelector('.book-search');

bookSearch.addEventListener("input", e => {
    const value = e.target.value.toLowerCase().trim();

    const bookCard = document.querySelectorAll('.book-card');
    
    bookCard.forEach(card => {
        const title = card.querySelector('.name') ? card.querySelector('.name').innerText.toLowerCase() : '';
        const author = card.querySelector('.author') ? card.querySelector('.author').innerText.toLowerCase() : '';
        
        if (title.includes(value) || author.includes(value)) {
            card.style.display = "block";
        } else {
            card.style.display = "none";
        }
    })
})