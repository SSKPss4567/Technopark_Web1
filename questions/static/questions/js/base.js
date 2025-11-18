document.addEventListener('DOMContentLoaded', function() {
    const searchBtn = document.querySelector('.mobile-search-button');
    const searchContainer = document.querySelector('.mobile-search-container');
    const searchBox = searchContainer.querySelector('.search-box');
    const searchExpandBtn = searchContainer.querySelector('.mobile-search-expand-button');
    
    const elementsToHide = [
        document.querySelector('.logo'),
        document.querySelector('.avatar'),
        document.querySelector('.enter-button'),
        document.querySelector('.auth-details'),
        document.querySelector('.ask-question-icon')
    ];
    
    searchContainer.style.display = 'none';
    
    searchBtn.addEventListener('click', function() {
        searchContainer.style.display = 'block';
        
        searchBtn.style.display = 'none';
        
        elementsToHide.forEach(element => {
            if (element) element.style.display = 'none';
        });
        
        setTimeout(() => searchBox.focus(), 50);
    });
    
 
    function closeSearch() {
        searchContainer.style.display = 'none';
        
        searchBtn.style.display = 'block';
        
        elementsToHide.forEach(element => {
            if (element) element.style.display = '';
        });
        
        searchBox.value = '';
    }

    
    searchExpandBtn.addEventListener('click', function() {
        if (!searchBox.value.trim()) {
            closeSearch();
        } else {
            performSearch(searchBox.value.trim());
        }
    });
    
    searchBox.addEventListener('keydown', function(e) {
        if (e.key === 'Enter') {
            if (searchBox.value.trim()) {
                performSearch(searchBox.value.trim());
            } else {
                closeSearch();
            }
        }
        if (e.key === 'Escape') {
            closeSearch();
        }
    });
    
    function performSearch(query) {
        console.log('Search:', query);
        closeSearch(); 
    }
    
});



