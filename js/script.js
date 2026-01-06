/**
 * Interactive Service Selector
 * Provides functionality for selecting, filtering, and managing services
 */

// Service data structure
const services = [
    {
        id: 1,
        name: 'Web Development',
        category: 'Development',
        description: 'Full-stack web development services',
        icon: 'code',
        price: 'Starting at $5000'
    },
    {
        id: 2,
        name: 'Mobile App Development',
        category: 'Development',
        description: 'iOS and Android app development',
        icon: 'mobile',
        price: 'Starting at $8000'
    },
    {
        id: 3,
        name: 'UI/UX Design',
        category: 'Design',
        description: 'User interface and experience design',
        icon: 'palette',
        price: 'Starting at $3000'
    },
    {
        id: 4,
        name: 'Graphic Design',
        category: 'Design',
        description: 'Professional graphic design services',
        icon: 'image',
        price: 'Starting at $2000'
    },
    {
        id: 5,
        name: 'Digital Marketing',
        category: 'Marketing',
        description: 'SEO, SEM, and social media marketing',
        icon: 'trending-up',
        price: 'Starting at $1500'
    },
    {
        id: 6,
        name: 'Content Writing',
        category: 'Marketing',
        description: 'Professional content creation and copywriting',
        icon: 'pen-tool',
        price: 'Starting at $500'
    },
    {
        id: 7,
        name: 'Branding',
        category: 'Branding',
        description: 'Complete branding and identity design',
        icon: 'star',
        price: 'Starting at $2500'
    },
    {
        id: 8,
        name: 'Consulting',
        category: 'Consulting',
        description: 'Business strategy and tech consulting',
        icon: 'briefcase',
        price: 'Custom pricing'
    }
];

// State management
const state = {
    selectedServices: [],
    activeFilter: 'All',
    searchQuery: ''
};

// DOM elements cache
const domElements = {
    serviceContainer: null,
    filterButtons: null,
    searchInput: null,
    selectedList: null,
    clearButton: null,
    submitButton: null
};

/**
 * Initialize the application
 */
function init() {
    cacheDOM();
    render();
    attachEventListeners();
}

/**
 * Cache DOM elements for performance
 */
function cacheDOM() {
    domElements.serviceContainer = document.getElementById('service-container');
    domElements.filterButtons = document.querySelectorAll('[data-filter]');
    domElements.searchInput = document.getElementById('search-input');
    domElements.selectedList = document.getElementById('selected-services');
    domElements.clearButton = document.getElementById('clear-btn');
    domElements.submitButton = document.getElementById('submit-btn');
}

/**
 * Attach event listeners to DOM elements
 */
function attachEventListeners() {
    // Filter button events
    if (domElements.filterButtons) {
        domElements.filterButtons.forEach(button => {
            button.addEventListener('click', handleFilterClick);
        });
    }

    // Search input event
    if (domElements.searchInput) {
        domElements.searchInput.addEventListener('input', handleSearch);
    }

    // Clear button event
    if (domElements.clearButton) {
        domElements.clearButton.addEventListener('click', handleClear);
    }

    // Submit button event
    if (domElements.submitButton) {
        domElements.submitButton.addEventListener('click', handleSubmit);
    }
}

/**
 * Handle filter button clicks
 */
function handleFilterClick(event) {
    const filterValue = event.target.dataset.filter;
    state.activeFilter = filterValue;
    updateFilterButtons();
    render();
}

/**
 * Update filter button active states
 */
function updateFilterButtons() {
    domElements.filterButtons.forEach(button => {
        if (button.dataset.filter === state.activeFilter) {
            button.classList.add('active');
        } else {
            button.classList.remove('active');
        }
    });
}

/**
 * Handle search input
 */
function handleSearch(event) {
    state.searchQuery = event.target.value.toLowerCase();
    render();
}

/**
 * Handle clear selection
 */
function handleClear() {
    state.selectedServices = [];
    state.activeFilter = 'All';
    state.searchQuery = '';
    
    if (domElements.searchInput) {
        domElements.searchInput.value = '';
    }
    
    updateFilterButtons();
    render();
}

/**
 * Handle form submission
 */
function handleSubmit() {
    if (state.selectedServices.length === 0) {
        showAlert('Please select at least one service', 'warning');
        return;
    }

    const selectedServiceNames = state.selectedServices
        .map(id => services.find(s => s.id === id).name)
        .join(', ');

    showAlert(`Selected services: ${selectedServiceNames}`, 'success');
    
    // You can add additional submission logic here
    console.log('Submitted services:', state.selectedServices);
}

/**
 * Filter services based on active filter and search query
 */
function getFilteredServices() {
    return services.filter(service => {
        const matchesFilter = state.activeFilter === 'All' || service.category === state.activeFilter;
        const matchesSearch = service.name.toLowerCase().includes(state.searchQuery) ||
                            service.description.toLowerCase().includes(state.searchQuery) ||
                            service.category.toLowerCase().includes(state.searchQuery);
        
        return matchesFilter && matchesSearch;
    });
}

/**
 * Get unique categories from services
 */
function getCategories() {
    return ['All', ...new Set(services.map(s => s.category))];
}

/**
 * Toggle service selection
 */
function toggleServiceSelection(serviceId) {
    const index = state.selectedServices.indexOf(serviceId);
    
    if (index > -1) {
        state.selectedServices.splice(index, 1);
    } else {
        state.selectedServices.push(serviceId);
    }
    
    render();
}

/**
 * Check if service is selected
 */
function isServiceSelected(serviceId) {
    return state.selectedServices.includes(serviceId);
}

/**
 * Render the entire application
 */
function render() {
    renderServices();
    renderSelectedServices();
    updateStats();
}

/**
 * Render service cards
 */
function renderServices() {
    const filteredServices = getFilteredServices();
    
    if (!domElements.serviceContainer) return;
    
    if (filteredServices.length === 0) {
        domElements.serviceContainer.innerHTML = `
            <div class="no-results">
                <p>No services found matching your criteria.</p>
                <p>Try adjusting your filters or search terms.</p>
            </div>
        `;
        return;
    }
    
    domElements.serviceContainer.innerHTML = filteredServices
        .map(service => createServiceCard(service))
        .join('');
    
    // Attach click handlers to service cards
    document.querySelectorAll('.service-card').forEach(card => {
        card.addEventListener('click', () => {
            toggleServiceSelection(parseInt(card.dataset.serviceId));
        });
    });
}

/**
 * Create a service card HTML element
 */
function createServiceCard(service) {
    const isSelected = isServiceSelected(service.id);
    const selectedClass = isSelected ? 'selected' : '';
    
    return `
        <div class="service-card ${selectedClass}" data-service-id="${service.id}">
            <div class="service-header">
                <div class="service-icon">
                    <i class="icon-${service.icon}"></i>
                </div>
                <div class="service-checkbox">
                    <input type="checkbox" id="service-${service.id}" ${isSelected ? 'checked' : ''}>
                </div>
            </div>
            <div class="service-body">
                <h3 class="service-name">${escapeHTML(service.name)}</h3>
                <p class="service-category">${escapeHTML(service.category)}</p>
                <p class="service-description">${escapeHTML(service.description)}</p>
                <p class="service-price">${escapeHTML(service.price)}</p>
            </div>
        </div>
    `;
}

/**
 * Render selected services list
 */
function renderSelectedServices() {
    if (!domElements.selectedList) return;
    
    if (state.selectedServices.length === 0) {
        domElements.selectedList.innerHTML = '<p class="empty-message">No services selected</p>';
        return;
    }
    
    const selectedServiceElements = state.selectedServices
        .map(id => services.find(s => s.id === id))
        .filter(service => service) // Safety check
        .map(service => `
            <div class="selected-item">
                <span class="selected-name">${escapeHTML(service.name)}</span>
                <span class="selected-category">${escapeHTML(service.category)}</span>
                <button class="remove-btn" data-service-id="${service.id}" title="Remove">×</button>
            </div>
        `)
        .join('');
    
    domElements.selectedList.innerHTML = selectedServiceElements;
    
    // Attach click handlers to remove buttons
    document.querySelectorAll('.remove-btn').forEach(button => {
        button.addEventListener('click', (e) => {
            e.stopPropagation();
            toggleServiceSelection(parseInt(button.dataset.serviceId));
        });
    });
}

/**
 * Update statistics display
 */
function updateStats() {
    const statsElement = document.getElementById('selection-stats');
    if (!statsElement) return;
    
    const filteredCount = getFilteredServices().length;
    const selectedCount = state.selectedServices.length;
    
    statsElement.textContent = `Selected: ${selectedCount} | Showing: ${filteredCount}`;
}

/**
 * Show alert message
 */
function showAlert(message, type = 'info') {
    const alertElement = document.createElement('div');
    alertElement.className = `alert alert-${type}`;
    alertElement.textContent = message;
    
    document.body.appendChild(alertElement);
    
    // Auto-remove after 3 seconds
    setTimeout(() => {
        alertElement.remove();
    }, 3000);
}

/**
 * Escape HTML to prevent XSS
 */
function escapeHTML(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Export selected services data
 */
function exportSelectedServices() {
    const selectedData = state.selectedServices
        .map(id => services.find(s => s.id === id))
        .filter(service => service);
    
    return {
        count: selectedData.length,
        services: selectedData,
        timestamp: new Date().toISOString()
    };
}

/**
 * Get service by ID
 */
function getServiceById(serviceId) {
    return services.find(s => s.id === serviceId);
}

/**
 * Get all services in a category
 */
function getServicesByCategory(category) {
    if (category === 'All') return services;
    return services.filter(s => s.category === category);
}

/**
 * Reset to initial state
 */
function reset() {
    state.selectedServices = [];
    state.activeFilter = 'All';
    state.searchQuery = '';
    
    if (domElements.searchInput) {
        domElements.searchInput.value = '';
    }
    
    updateFilterButtons();
    render();
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}

// Export functions for external use
window.serviceSelector = {
    getSelectedServices: () => state.selectedServices,
    getFilteredServices,
    getCategories,
    exportSelectedServices,
    getServiceById,
    getServicesByCategory,
    reset,
    toggleServiceSelection
};
