// Global variables
let papersData = [];
let analyzedData = {};
let currentPage = 1;
const papersPerPage = 10;

// DOM Elements
const tabButtons = document.querySelectorAll('.nav-tabs button');
const tabContents = document.querySelectorAll('.tab-content');
const refreshBtn = document.getElementById('refresh-btn');
const lastUpdatedEl = document.getElementById('last-updated');
const totalPapersEl = document.getElementById('total-papers');
const averageScoreEl = document.getElementById('average-score');
const topCategoryEl = document.getElementById('top-category');
const latestUpdateEl = document.getElementById('latest-update');
const topPapersListEl = document.getElementById('top-papers-list');
const literatureListEl = document.getElementById('literature-list');
const paginationEl = document.getElementById('pagination');
const categoriesListEl = document.getElementById('categories-list');
const timelineContentEl = document.getElementById('timeline-content');
const searchInput = document.getElementById('search-input');
const searchBtn = document.getElementById('search-btn');
const categoryFilter = document.getElementById('category-filter');
const timeFilter = document.getElementById('time-filter');
const sourceFilter = document.getElementById('source-filter');
const timelineCategoryFilter = document.getElementById('timeline-category-filter');
const timelineDateFilter = document.getElementById('timeline-date-filter');
const paperModal = document.getElementById('paper-modal');
const paperDetailEl = document.getElementById('paper-detail');
const closeModal = document.getElementsByClassName('close')[0];

// Initialize the application
function initApp() {
    // Setup event listeners
    setupEventListeners();
    
    // Load data
    loadData();
}

// Setup event listeners
function setupEventListeners() {
    // Tab switching
    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const tabId = button.dataset.tab;
            switchTab(tabId);
        });
    });

    // Refresh data
    refreshBtn.addEventListener('click', refreshData);

    // Search functionality
    searchBtn.addEventListener('click', performSearch);
    searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            performSearch();
        }
    });

    // Filter changes
    categoryFilter.addEventListener('change', filterLiterature);
    timeFilter.addEventListener('change', filterLiterature);
    sourceFilter.addEventListener('change', filterLiterature);
    timelineCategoryFilter.addEventListener('change', updateTimeline);
    timelineDateFilter.addEventListener('change', updateTimeline);

    // Modal functionality
    closeModal.addEventListener('click', () => {
        paperModal.style.display = 'none';
    });

    window.addEventListener('click', (e) => {
        if (e.target == paperModal) {
            paperModal.style.display = 'none';
        }
    });
}

// Switch tabs
function switchTab(tabId) {
    // Update tab buttons
    tabButtons.forEach(button => {
        button.classList.remove('active');
        if (button.dataset.tab === tabId) {
            button.classList.add('active');
        }
    });

    // Update tab contents
    tabContents.forEach(content => {
        content.classList.remove('active');
        if (content.id === `${tabId}-tab`) {
            content.classList.add('active');
        }
    });

    // Initialize tab-specific content
    if (tabId === 'literature') {
        renderLiteratureList();
    } else if (tabId === 'categories') {
        renderCategories();
    } else if (tabId === 'timeline') {
        updateTimeline();
    }
}

// Load data from local JSON files
async function loadData() {
    try {
        // Show loading state
        document.querySelectorAll('.tab-content').forEach(content => {
            if (content.classList.contains('active')) {
                content.innerHTML = '<div class="loading-container"><div class="loading-spinner"></div><p>Loading data...</p></div>';
            }
        });

        // Load papers data
        const papersResponse = await fetch('data/papers.json');
        papersData = await papersResponse.json();

        // Load analyzed data
        const analyzedResponse = await fetch('data/analyzed.json');
        analyzedData = await analyzedResponse.json();

        // Update UI
        updateDashboard();
        updateLastUpdated();
        populateFilters();

    } catch (error) {
        console.error('Error loading data:', error);
        showErrorMessage('Failed to load data. Please try again.');
    }
}

// Refresh data
async function refreshData() {
    try {
        refreshBtn.disabled = true;
        refreshBtn.innerHTML = '<span class="loading"></span> Refreshing...';

        // Re-load data
        await loadData();

        showSuccessMessage('Data refreshed successfully!');

    } catch (error) {
        console.error('Error refreshing data:', error);
        showErrorMessage('Failed to refresh data. Please try again.');
    } finally {
        refreshBtn.disabled = false;
        refreshBtn.innerHTML = 'Refresh Data';
    }
}

// Update dashboard
function updateDashboard() {
    if (!analyzedData || !papersData.length) return;

    // Update stats
    totalPapersEl.textContent = papersData.length;
    averageScoreEl.textContent = `${analyzedData.average_importance_score.toFixed(2)}/10`;

    // Find top category
    const categories = analyzedData.category_counts;
    const topCategory = Object.entries(categories)
        .sort(([,a], [,b]) => b - a)[0];
    if (topCategory) {
        topCategoryEl.textContent = `${topCategory[0]} (${topCategory[1]} papers)`;
    }

    // Update latest update time
    latestUpdateEl.textContent = new Date().toLocaleString();

    // Render top papers
    renderTopPapers();

    // Render charts
    renderCharts();
}

// Update last updated time
function updateLastUpdated() {
    lastUpdatedEl.textContent = new Date().toLocaleString();
}

// Render top papers
function renderTopPapers() {
    if (!analyzedData || !analyzedData.papers) return;

    const topPapers = [...analyzedData.papers]
        .sort((a, b) => b.importance_score - a.importance_score)
        .slice(0, 5);

    topPapersListEl.innerHTML = '';

    topPapers.forEach(paper => {
        const paperItem = document.createElement('div');
        paperItem.className = 'paper-item';
        paperItem.onclick = () => showPaperDetail(paper);

        paperItem.innerHTML = `
            <h4>${paper.title}</h4>
            <p>${paper.abstract ? paper.abstract.substring(0, 150) + '...' : 'No abstract available'}</p>
            <div class="paper-meta">
                <span>Score: ${paper.importance_score}/10</span>
                <span>Category: ${paper.classifications[0]}</span>
                <span>Date: ${paper.publication_date}</span>
            </div>
        `;

        topPapersListEl.appendChild(paperItem);
    });
}

// Render charts
function renderCharts() {
    if (!analyzedData) return;

    // Check if Chart is available
    if (typeof Chart !== 'undefined') {
        // Category distribution chart
        renderCategoryChart();

        // Timeline chart
        renderTimelineChart();
    } else {
        console.warn('Chart.js not available, skipping chart rendering');
    }
}

// Render category distribution chart
function renderCategoryChart() {
    const ctx = document.getElementById('category-chart').getContext('2d');
    const categories = analyzedData.category_counts;

    const categoryNames = Object.keys(categories);
    const categoryCounts = Object.values(categories);

    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: categoryNames,
            datasets: [{
                data: categoryCounts,
                backgroundColor: [
                    '#667eea', '#764ba2', '#f093fb', '#f5576c',
                    '#4facfe', '#00f2fe', '#43e97b', '#38f9d7',
                    '#ffecd2', '#fcb69f', '#a8edea', '#fed6e3',
                    '#ff9a9e', '#fecfef', '#fad0c4', '#ffdac1'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'right',
                }
            }
        }
    });
}

// Render timeline chart
function renderTimelineChart() {
    const ctx = document.getElementById('timeline-chart').getContext('2d');

    // Group papers by month
    const papersByMonth = {};
    papersData.forEach(paper => {
        if (paper.publication_date) {
            const month = paper.publication_date.substring(0, 7); // YYYY-MM
            papersByMonth[month] = (papersByMonth[month] || 0) + 1;
        }
    });

    // Sort months
    const sortedMonths = Object.keys(papersByMonth).sort();
    const sortedCounts = sortedMonths.map(month => papersByMonth[month]);

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: sortedMonths,
            datasets: [{
                label: 'Number of Papers',
                data: sortedCounts,
                backgroundColor: '#667eea',
                borderColor: '#667eea',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        precision: 0
                    }
                }
            }
        }
    });
}

// Populate filter options
function populateFilters() {
    if (!analyzedData) return;

    const categories = Object.keys(analyzedData.category_counts);

    // Populate category filter
    categoryFilter.innerHTML = '<option value="all">All Categories</option>';
    categories.forEach(category => {
        const option = document.createElement('option');
        option.value = category;
        option.textContent = `${category} (${analyzedData.category_counts[category]})`;
        categoryFilter.appendChild(option);
    });

    // Populate timeline category filter
    timelineCategoryFilter.innerHTML = '<option value="all">All Categories</option>';
    categories.forEach(category => {
        const option = document.createElement('option');
        option.value = category;
        option.textContent = `${category} (${analyzedData.category_counts[category]})`;
        timelineCategoryFilter.appendChild(option);
    });

    // Calculate source counts
    const sourceCounts = {};
    papersData.forEach(paper => {
        const source = paper.source;
        sourceCounts[source] = (sourceCounts[source] || 0) + 1;
    });

    // Populate source filter
    sourceFilter.innerHTML = '<option value="all">All Sources</option>';
    Object.keys(sourceCounts).forEach(source => {
        const option = document.createElement('option');
        option.value = source;
        option.textContent = `${source} (${sourceCounts[source]})`;
        sourceFilter.appendChild(option);
    });

    // Set current date for timeline filter
    const today = new Date();
    const currentMonth = today.toISOString().substring(0, 7);
    timelineDateFilter.value = currentMonth;
}

// Render literature list
function renderLiteratureList() {
    const filteredPapers = getFilteredPapers();
    const totalPages = Math.ceil(filteredPapers.length / papersPerPage);
    const startIndex = (currentPage - 1) * papersPerPage;
    const endIndex = startIndex + papersPerPage;
    const paginatedPapers = filteredPapers.slice(startIndex, endIndex);

    // Render papers
    literatureListEl.innerHTML = '';

    if (paginatedPapers.length === 0) {
        literatureListEl.innerHTML = '<p>No papers found. Please adjust your filters.</p>';
    } else {
        paginatedPapers.forEach(paper => {
            const paperItem = document.createElement('div');
            paperItem.className = 'paper-item';
            paperItem.onclick = () => showPaperDetail(paper);

            paperItem.innerHTML = `
                <h4>${paper.title}</h4>
                <p>${paper.abstract ? paper.abstract.substring(0, 150) + '...' : 'No abstract available'}</p>
                <div class="paper-meta">
                    <span>Authors: ${paper.authors ? paper.authors.slice(0, 3).join(', ') + (paper.authors.length > 3 ? ' et al.' : '') : 'Unknown'}</span>
                    <span>Source: ${paper.source}</span>
                    <span>Date: ${paper.publication_date}</span>
                </div>
            `;

            literatureListEl.appendChild(paperItem);
        });
    }

    // Render pagination
    renderPagination(totalPages);
}

// Get filtered papers
function getFilteredPapers() {
    let filteredPapers = [...papersData];

    // Apply category filter
    const selectedCategory = categoryFilter.value;
    if (selectedCategory !== 'all') {
        filteredPapers = filteredPapers.filter(paper => {
            const analyzedPaper = analyzedData.papers.find(p => p.title === paper.title);
            return analyzedPaper && analyzedPaper.classifications.includes(selectedCategory);
        });
    }

    // Apply time filter
    const selectedTime = timeFilter.value;
    if (selectedTime !== 'all') {
        const now = new Date();
        let cutoffDate;

        switch (selectedTime) {
            case 'last-month':
                cutoffDate = new Date(now.setMonth(now.getMonth() - 1));
                break;
            case 'last-3months':
                cutoffDate = new Date(now.setMonth(now.getMonth() - 3));
                break;
            case 'last-6months':
                cutoffDate = new Date(now.setMonth(now.getMonth() - 6));
                break;
            case 'last-year':
                cutoffDate = new Date(now.setFullYear(now.getFullYear() - 1));
                break;
        }

        filteredPapers = filteredPapers.filter(paper => {
            if (!paper.publication_date) return false;
            const paperDate = new Date(paper.publication_date);
            return paperDate >= cutoffDate;
        });
    }

    // Apply source filter
    const selectedSource = sourceFilter.value;
    if (selectedSource !== 'all') {
        filteredPapers = filteredPapers.filter(paper => paper.source === selectedSource);
    }

    return filteredPapers;
}

// Render pagination
function renderPagination(totalPages) {
    paginationEl.innerHTML = '';

    for (let i = 1; i <= totalPages; i++) {
        const button = document.createElement('button');
        button.className = `pagination-btn ${i === currentPage ? 'active' : ''}`;
        button.textContent = i;
        button.onclick = () => {
            currentPage = i;
            renderLiteratureList();
        };
        paginationEl.appendChild(button);
    }
}

// Filter literature list
function filterLiterature() {
    currentPage = 1;
    renderLiteratureList();
}

// Perform search
function performSearch() {
    const searchTerm = searchInput.value.toLowerCase();
    if (!searchTerm) return;

    const searchResults = papersData.filter(paper => {
        return (
            paper.title.toLowerCase().includes(searchTerm) ||
            (paper.abstract && paper.abstract.toLowerCase().includes(searchTerm)) ||
            (paper.authors && paper.authors.some(author => author.toLowerCase().includes(searchTerm)))
        );
    });

    // Switch to literature tab and display results
    switchTab('literature');
    
    // Render search results
    literatureListEl.innerHTML = '';
    paginationEl.innerHTML = '';

    if (searchResults.length === 0) {
        literatureListEl.innerHTML = `<p>No results found for "${searchTerm}".</p>`;
    } else {
        searchResults.forEach(paper => {
            const paperItem = document.createElement('div');
            paperItem.className = 'paper-item';
            paperItem.onclick = () => showPaperDetail(paper);

            paperItem.innerHTML = `
                <h4>${paper.title}</h4>
                <p>${paper.abstract ? paper.abstract.substring(0, 150) + '...' : 'No abstract available'}</p>
                <div class="paper-meta">
                    <span>Authors: ${paper.authors ? paper.authors.slice(0, 3).join(', ') + (paper.authors.length > 3 ? ' et al.' : '') : 'Unknown'}</span>
                    <span>Source: ${paper.source}</span>
                    <span>Date: ${paper.publication_date}</span>
                </div>
            `;

            literatureListEl.appendChild(paperItem);
        });
    }
}

// Render categories
function renderCategories() {
    if (!analyzedData) return;

    const categories = analyzedData.category_counts;
    const sortedCategories = Object.entries(categories)
        .sort(([,a], [,b]) => b - a);

    categoriesListEl.innerHTML = '';

    sortedCategories.forEach(([category, count]) => {
        const categoryItem = document.createElement('div');
        categoryItem.className = 'category-item';

        categoryItem.innerHTML = `
            <h3>
                ${category}
                <span class="category-count">${count}</span>
            </h3>
            <p>Papers in this category: ${count}</p>
            <button onclick="filterByCategory('${category}')">View Papers</button>
        `;

        categoriesListEl.appendChild(categoryItem);
    });
}

// Filter by category
function filterByCategory(category) {
    categoryFilter.value = category;
    switchTab('literature');
    filterLiterature();
}

// Update timeline
function updateTimeline() {
    const selectedCategory = timelineCategoryFilter.value;
    const selectedDate = timelineDateFilter.value;

    let filteredPapers = [...papersData];

    // Apply category filter
    if (selectedCategory !== 'all') {
        filteredPapers = filteredPapers.filter(paper => {
            const analyzedPaper = analyzedData.papers.find(p => p.title === paper.title);
            return analyzedPaper && analyzedPaper.classifications.includes(selectedCategory);
        });
    }

    // Apply date filter
    if (selectedDate) {
        filteredPapers = filteredPapers.filter(paper => {
            if (!paper.publication_date) return false;
            return paper.publication_date.startsWith(selectedDate);
        });
    }

    // Sort by date
    filteredPapers.sort((a, b) => {
        return new Date(b.publication_date) - new Date(a.publication_date);
    });

    // Render timeline
    timelineContentEl.innerHTML = '';

    if (filteredPapers.length === 0) {
        timelineContentEl.innerHTML = '<p>No papers found for the selected filters.</p>';
    } else {
        filteredPapers.forEach(paper => {
            const timelineItem = document.createElement('div');
            timelineItem.className = 'timeline-item';

            timelineItem.innerHTML = `
                <div class="timeline-date">${paper.publication_date}</div>
                <h4>${paper.title}</h4>
                <p>${paper.abstract ? paper.abstract.substring(0, 100) + '...' : 'No abstract available'}</p>
                <div class="paper-meta">
                    <span>Source: ${paper.source}</span>
                    <span>Authors: ${paper.authors ? paper.authors.slice(0, 2).join(', ') + (paper.authors.length > 2 ? ' et al.' : '') : 'Unknown'}</span>
                </div>
                <button onclick="showPaperDetail(paper)">View Details</button>
            `;

            timelineContentEl.appendChild(timelineItem);
        });
    }
}

// Show paper detail modal
function showPaperDetail(paper) {
    paperDetailEl.innerHTML = `
        <h2>${paper.title}</h2>
        <p><strong>Authors:</strong> ${paper.authors ? paper.authors.join(', ') : 'Unknown'}</p>
        <p><strong>Journal:</strong> ${paper.journal || 'Unknown'}</p>
        <p><strong>Publication Date:</strong> ${paper.publication_date || 'Unknown'}</p>
        <p><strong>Source:</strong> ${paper.source}</p>
        <p><strong>DOI:</strong> <a href="${paper.url}" target="_blank">${paper.doi || 'Unknown'}</a></p>
        <p><strong>Abstract:</strong> ${paper.abstract || 'No abstract available'}</p>
    `;

    paperModal.style.display = 'block';
}

// Show success message
function showSuccessMessage(message) {
    const messageEl = document.createElement('div');
    messageEl.className = 'success-message';
    messageEl.textContent = message;

    document.querySelector('main .container').prepend(messageEl);

    setTimeout(() => {
        messageEl.remove();
    }, 3000);
}

// Show error message
function showErrorMessage(message) {
    const messageEl = document.createElement('div');
    messageEl.className = 'error-message';
    messageEl.textContent = message;

    document.querySelector('main .container').prepend(messageEl);

    setTimeout(() => {
        messageEl.remove();
    }, 3000);
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', initApp);