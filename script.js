console.log("[STEP 1] script.js file has successfully loaded into the browser.");

let currentQuery = '';
let products = [];

async function searchProducts() {
    console.log("[STEP 4] searchProducts() function was triggered.");
    
    const searchInput = document.getElementById('search');
    if (!searchInput) {
        console.error("[FATAL ERROR] Could not find the input box with id='search'");
        return;
    }

    currentQuery = searchInput.value.trim();
    console.log(`[STEP 5] Read query value: '${currentQuery}'`);
    
    if (!currentQuery) {
        console.warn("[WARNING] Search query is empty, aborting fetch.");
        return;
    }

    const resultsContainer = document.getElementById('results');
    if (resultsContainer) {
        resultsContainer.innerHTML = '<p style="color: #94a3b8; grid-column: 1/-1;">Scraping results, please wait...</p>';
        console.log("[STEP 6] Updated UI to show loading state.");
    }

    await applyFilters();
}

async function applyFilters() {
    console.log("[STEP 7] applyFilters() started. Building URL...");
    const checkedBoxes = document.querySelectorAll('#platform-checkboxes input[type="checkbox"]:checked');
    const selectedOptions = Array.from(checkedBoxes).map(box => box.value);

    const params = new URLSearchParams();
    params.append('query', currentQuery);

    if (selectedOptions.length === 0 || selectedOptions.includes('all')) {
        params.append('platforms', 'all');
    } else {
        selectedOptions.forEach(p => params.append('platforms', p));
    }

    const url = `http://127.0.0.1:8000/search?${params.toString()}`;
    console.log(`[STEP 8] Preparing to fetch from URL: ${url}`);

    try {
        console.log("[STEP 9] Executing fetch request to backend...");
        const response = await fetch(url);
        
        console.log(`[STEP 10] Received backend response. Status Code: ${response.status}`);
        
        if (!response.ok) {
            throw new Error(`HTTP error: ${response.status}`);
        }
        
        products = await response.json();
        console.log(`[STEP 11] Successfully parsed JSON. Item count: ${products.length}`);
        
        sortProducts();
        console.log("[STEP 12] Flow complete and UI rendered.");
        
    } catch (error) {
        console.error('[CRITICAL FAILURE] Fetch request died:', error);
        const resultsContainer = document.getElementById('results');
        if (resultsContainer) {
            resultsContainer.innerHTML = '<p style="color: #ef4444; grid-column: 1/-1;">Failed to fetch results. Ensure backend is running.</p>';
        }
    }
}

function sortProducts() {
    if (!products || !products.length) {
        displayProducts([]);
        return;
    }

    const sortElement = document.getElementById('sort-select');
    const sortOrder = sortElement ? sortElement.value : 'low-to-high';

    if (sortOrder === 'high-to-low') {
        products.sort((a, b) => (b.price || 0) - (a.price || 0));
    } else {
        products.sort((a, b) => {
            const priceA = (a.price && a.price > 0) ? a.price : Infinity;
            const priceB = (b.price && b.price > 0) ? b.price : Infinity;
            return priceA - priceB;
        });
    }

    displayProducts(products);
}

function displayProducts(items) {
    const resultsContainer = document.getElementById('results');
    if (!resultsContainer) return;

    if (!items || !items.length) {
        resultsContainer.innerHTML = '<p style="color: #94a3b8; grid-column: 1/-1;">No products found</p>';
        return;
    }

    const html = items.map(p => {
        if (!p) return '';

        const formattedPrice = (typeof p.price === 'number' && p.price > 0) 
            ? `₹${p.price.toLocaleString('en-IN')}` 
            : 'Price unavailable';
        const platformName = p.platform || 'Store';
        let brandName = p.brand || 'Generic';
        const cleanBrand = brandName.toLowerCase();

        if (cleanBrand === 'galaxy') {
            brandName = 'Samsung';
        } else if (['mi', 'redmi', 'xiaomi'].includes(cleanBrand)) {
            brandName = 'Mi';
        }
        
        const imageSrc = p.image || 'https://via.placeholder.com/200';
        const specsText = (p.specs && p.specs.length > 0) ? p.specs.slice(0, 2).join(' • ') : 'No specs available';

        return `
            <div class="product-card">
                <img src="${imageSrc}" alt="${p.title || 'Product'}" class="product-image" onerror="this.src='https://via.placeholder.com/200'">
                <div class="product-info">
                    <div class="product-badges">
                        <span class="product-platform">${platformName}</span>
                        <span class="product-brand">${brandName}</span>
                    </div>
                    <p class="product-title">${p.title || 'Untitled Product'}</p>
                    <p class="product-price">${formattedPrice}</p>
                    <p class="product-specs">${specsText}</p>
                    <a href="${p.url || '#'}" target="_blank" class="product-link">View on ${platformName}</a>
                </div>
            </div>
        `;
    }).join('');

    resultsContainer.innerHTML = html;
}

document.addEventListener('DOMContentLoaded', () => {
    console.log("[STEP 2] HTML DOM fully loaded. Binding event listeners...");
    
    const searchInput = document.getElementById('search');
    const searchBtn = document.getElementById('search-btn') || document.querySelector('button');
    const sortSelect = document.getElementById('sort-select');
    const platformCheckboxes = document.querySelectorAll('#platform-checkboxes input[type="checkbox"]');

    if (searchBtn) {
        console.log("[STEP 3A] Search button found. Attaching click listener.");
        searchBtn.addEventListener('click', (e) => {
            console.log("[USER ACTION] Button clicked!");
            e.preventDefault();
            searchProducts();
        });
    }

    if (searchInput) {
        console.log("[STEP 3B] Search input found. Attaching Enter key listener.");
        searchInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                console.log("[USER ACTION] Enter key pressed!");
                e.preventDefault();
                searchProducts();
            }
        });
    }

    if (sortSelect) {
        sortSelect.addEventListener('change', sortProducts);
    }

    platformCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', () => {
            if (currentQuery) {
                console.log("[USER ACTION] Filter changed!");
                applyFilters();
            }
        });
    });
});