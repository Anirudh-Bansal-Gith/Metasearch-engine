console.log("[INIT] App started");

const isLocal = 
    window.location.hostname === "localhost" || 
    window.location.hostname === "127.0.0.1" || 
    window.location.protocol === "file:" ||
    window.location.hostname === "";

const API_BASE_URL = isLocal
    ? "http://127.0.0.1:8000/search"
    : "https://metasearch-engine.onrender.com/search";

const state = {
    currentQuery: '',
    rawProducts: [],
    selectedPlatforms: new Set(['flipkart', 'amazon', 'croma', 'jiomart']),
    selectedBrands: new Set(),
    sortOrder: 'low-to-high'
};

async function searchProducts() {
    console.log("[SEARCH] Searching for:", document.getElementById('search').value);
    
    const query = document.getElementById('search').value.trim();
    if (!query) return;

    state.currentQuery = query;
    state.selectedBrands.clear();
    
    document.querySelectorAll('#brand-checkboxes input').forEach(cb => cb.checked = false);
    
    await fetchData();
}

async function fetchData() {
    console.log("[FETCH] Calling API");
    
    document.getElementById('results').innerHTML = '<p class="no-results">Loading...</p>';

    try {
        const response = await fetch(`${API_BASE_URL}?query=${encodeURIComponent(state.currentQuery)}`);
        if (!response.ok) throw new Error('API Error');

        const data = await response.json();
        console.log("[FETCH] Got", data.length, "products");

        state.rawProducts = data.map(normalizeProduct).filter(Boolean);
        buildBrandCheckboxes();
        applyFilters();
    } catch (err) {
        console.error("[ERROR]", err);
        document.getElementById('results').innerHTML = '<p class="no-results">Error loading results</p>';
    }
}

function normalizeProduct(p) {
    let brand = p.brand || p.title?.split(' ')[0] || 'Other';
    
    const clean = String(brand).toLowerCase();
    if (clean === 'galaxy') brand = 'Samsung';
    else if (['mi', 'redmi'].includes(clean)) brand = 'Xiaomi';
    else brand = String(brand).charAt(0).toUpperCase() + String(brand).slice(1);

    return {
        platform: p.platform || 'Store',
        title: p.title || 'Product',
        brand: brand,
        price: p.price || 0,
        url: p.url || '#',
        image: p.image || 'https://via.placeholder.com/200',
        specs: p.specs || []
    };
}

function buildBrandCheckboxes() {
    console.log("[BRANDS] Building checkboxes");
    
    const brandMap = new Map();
    state.rawProducts.forEach(p => {
        brandMap.set(p.brand, (brandMap.get(p.brand) || 0) + 1);
    });

    const sorted = Array.from(brandMap.keys()).sort();
    const container = document.getElementById('brand-checkboxes');
    
    container.innerHTML = sorted.map(brand => `
        <label>
            <input type="checkbox" value="${brand}" onchange="applyFilters()">
            ${brand} (${brandMap.get(brand)})
        </label>
    `).join('');
}

function applyFilters() {
    console.log("[FILTER] Applying filters");
    
    state.selectedPlatforms.clear();
    document.querySelectorAll('#platform-checkboxes input:checked').forEach(cb => {
        state.selectedPlatforms.add(cb.value.toLowerCase());
    });

    state.selectedBrands.clear();
    document.querySelectorAll('#brand-checkboxes input:checked').forEach(cb => {
        state.selectedBrands.add(cb.value);
    });

    state.sortOrder = document.getElementById('sort-select').value;

    let filtered = state.rawProducts.filter(p => 
        state.selectedPlatforms.has(p.platform.toLowerCase())
    );

    if (state.selectedBrands.size > 0) {
        filtered = filtered.filter(p => state.selectedBrands.has(p.brand));
    }

    filtered.sort((a, b) => {
        const priceA = a.price || Infinity;
        const priceB = b.price || Infinity;
        return state.sortOrder === 'high-to-low' ? priceB - priceA : priceA - priceB;
    });

    console.log("[FILTER] Filtered to", filtered.length, "products");
    renderCards(filtered);
}

function renderCards(items) {
    console.log("[RENDER] Rendering", items.length, "cards");
    
    const container = document.getElementById('results');
    
    if (!items.length) {
        container.innerHTML = '<p class="no-results">No products found</p>';
        return;
    }

    container.innerHTML = items.map(p => `
        <div class="product-card">
            <img src="${p.image}" alt="" class="product-image" onerror="this.src='https://via.placeholder.com/200'">
            <div class="product-info">
                <div class="product-platform">${p.platform}</div>
                <div class="product-brand">${p.brand}</div>
                <div class="product-title">${p.title}</div>
                <div class="product-price">₹${p.price.toLocaleString('en-IN')}</div>
                <div class="product-specs">${p.specs.slice(0, 2).join(' • ') || 'No specs'}</div>
                <a href="${p.url}" target="_blank" class="product-link">View</a>
            </div>
        </div>
    `).join('');
}

document.addEventListener('DOMContentLoaded', () => {
    console.log("[INIT] DOM Ready");
    const searchInput = document.getElementById('search');
    searchInput.focus();

    searchInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            searchProducts();
        }
    });
});
