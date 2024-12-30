document.addEventListener('DOMContentLoaded', () => {
    const content = document.getElementById('content');
    const loader = document.getElementById('loader');
    let page = 0;
    const pageSize = 20;
    let articles = [];
    let favorites = new Set();

    // Load articles from JSON file
    fetch('2018-2023.json')
        .then(response => response.json())
        .then(data => {
            articles = data;
            articles = articles.sort(() => Math.random() - 0.5);
            console.log(articles)
            loadMoreArticles();
        });

    // Load more articles on scroll
    window.addEventListener('scroll', () => {
        if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 100) {
            loadMoreArticles();
        }
    });

    function loadMoreArticles() {
        if (page * pageSize >= articles.length) return;
        loader.style.display = 'block';
        setTimeout(() => {
            const start = page * pageSize;
            const end = start + pageSize;
            const newArticles = articles.slice(start, end);
            newArticles.forEach(article => {
                const articleElement = document.createElement('div');
                articleElement.className = 'article';
                articleElement.innerHTML = `
                    <h2>${article.name}</h2>
                    <p>${article.year}</p>
                    <p>${article.description}</p>
                    <button class="like-button" data-name="${article.name}">Like</button>
                    <a href="${article.url}" target="_blank">Article</a>
                `;
                content.appendChild(articleElement);
            });
            page++;
            loader.style.display = 'none';
        }, 1000);
    }

    // Handle like button click
    content.addEventListener('click', (event) => {
        if (event.target.classList.contains('like-button')) {
            const button = event.target;
            const articleName = button.getAttribute('data-name');
            if (favorites.has(articleName)) {
                favorites.delete(articleName);
                button.classList.remove('liked');
                button.textContent = 'Like';
            } else {
                favorites.add(articleName);
                button.classList.add('liked');
                button.textContent = 'Liked';
            }
            saveFavorites();
        }
    });

    function saveFavorites() {
        localStorage.setItem('favorites', JSON.stringify(Array.from(favorites)));
    }

    function loadFavorites() {
        const savedFavorites = JSON.parse(localStorage.getItem('favorites'));
        if (savedFavorites) {
            favorites = new Set(savedFavorites);
        }
    }

    loadFavorites();
});