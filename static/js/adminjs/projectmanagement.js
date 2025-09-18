document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const timelineViewBtn = document.getElementById('timelineViewBtn');
    const tableViewBtn = document.getElementById('tableViewBtn');
    const timelineView = document.getElementById('timelineView');
    const tableView = document.getElementById('tableView');
    const expandAllBtn = document.getElementById('expandAllBtn');
    const collapseAllBtn = document.getElementById('collapseAllBtn');
    const filterToggle = document.getElementById('filterToggle');
    const filterOptions = document.getElementById('filterOptions');
    const searchInput = document.querySelector('.search-input');
    const resetFiltersBtn = document.getElementById('resetFilters');
    const applyFiltersBtn = document.getElementById('applyFilters');
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const navLinks = document.getElementById('navLinks');

    // Initialize view
    let currentView = 'timeline'; // Default view
    let expandedState = {}; // Track expanded state of items

    // Initialize the page
    init();

    function init() {
        // Set up event listeners
        setupEventListeners();
        
        // Initialize view toggle
        toggleView(currentView);
        
        // Initialize filter toggle
        filterOptions.style.display = 'none';
    }

    function setupEventListeners() {
        // View toggle buttons
        if (timelineViewBtn && tableViewBtn) {
            timelineViewBtn.addEventListener('click', () => toggleView('timeline'));
            tableViewBtn.addEventListener('click', () => toggleView('table'));
        }

        // Expand/Collapse buttons
        if (expandAllBtn && collapseAllBtn) {
            expandAllBtn.addEventListener('click', expandAll);
            collapseAllBtn.addEventListener('click', collapseAll);
        }

        // Filter toggle
        if (filterToggle) {
            filterToggle.addEventListener('click', toggleFilters);
        }

        // Mobile menu
        if (mobileMenuBtn && navLinks) {
            mobileMenuBtn.addEventListener('click', toggleMobileMenu);
        }

        // Search functionality
        if (searchInput) {
            searchInput.addEventListener('input', handleSearch);
        }

        // Filter buttons
        if (resetFiltersBtn && applyFiltersBtn) {
            resetFiltersBtn.addEventListener('click', resetFilters);
            applyFiltersBtn.addEventListener('click', applyFilters);
        }

        // Click handlers for timeline items
        document.addEventListener('click', function(e) {
            // Handle timeline item expansion
            if (e.target.closest('.timeline-header')) {
                const header = e.target.closest('.timeline-header');
                const contentId = header.getAttribute('data-id');
                toggleTimelineItem(contentId);
            }

            // Handle action buttons
            if (e.target.closest('.action-btn')) {
                const btn = e.target.closest('.action-btn');
                const action = btn.classList.contains('edit') ? 'edit' :
                              btn.classList.contains('delete') ? 'delete' :
                              btn.classList.contains('download') ? 'download' : null;
                
                if (action) handleAction(action, btn);
            }
        });
    }

    function toggleView(view) {
        currentView = view;
        
        if (view === 'timeline') {
            timelineView.style.display = 'block';
            tableView.style.display = 'none';
            timelineViewBtn.classList.add('active');
            tableViewBtn.classList.remove('active');
        } else {
            timelineView.style.display = 'none';
            tableView.style.display = 'block';
            tableViewBtn.classList.add('active');
            timelineViewBtn.classList.remove('active');
        }
    }

    function toggleFilters() {
        const isVisible = filterOptions.style.display === 'block';
        filterOptions.style.display = isVisible ? 'none' : 'block';
        
        const icon = filterToggle.querySelector('i');
        const text = filterToggle.querySelector('span');
        
        if (isVisible) {
            icon.classList.remove('fa-chevron-up');
            icon.classList.add('fa-chevron-down');
            text.textContent = 'Show Filters';
        } else {
            icon.classList.remove('fa-chevron-down');
            icon.classList.add('fa-chevron-up');
            text.textContent = 'Hide Filters';
        }
    }

    function toggleMobileMenu() {
        navLinks.classList.toggle('active');
        const icon = mobileMenuBtn.querySelector('i');
        icon.classList.toggle('fa-bars');
        icon.classList.toggle('fa-times');
    }

    function expandAll() {
        document.querySelectorAll('.timeline-content').forEach(content => {
            const contentId = content.id.replace('content', '');
            expandedState[contentId] = true;
            content.style.maxHeight = content.scrollHeight + 'px';
            content.classList.add('active');
            
            // Update chevron icon
            const header = document.querySelector(`.timeline-header[data-id="${contentId}"]`);
            if (header) {
                const icon = header.querySelector('.action-btn.expand i');
                if (icon) {
                    icon.classList.remove('fa-chevron-down');
                    icon.classList.add('fa-chevron-up');
                }
            }
        });
    }

    function collapseAll() {
        document.querySelectorAll('.timeline-content').forEach(content => {
            const contentId = content.id.replace('content', '');
            expandedState[contentId] = false;
            content.style.maxHeight = '0';
            content.classList.remove('active');
            
            // Update chevron icon
            const header = document.querySelector(`.timeline-header[data-id="${contentId}"]`);
            if (header) {
                const icon = header.querySelector('.action-btn.expand i');
                if (icon) {
                    icon.classList.remove('fa-chevron-up');
                    icon.classList.add('fa-chevron-down');
                }
            }
        });
    }

    function toggleTimelineItem(contentId) {
        const content = document.getElementById(`content${contentId}`);
        const isExpanded = content.classList.contains('active');
        
        if (isExpanded) {
            content.style.maxHeight = '0';
            content.classList.remove('active');
            expandedState[contentId] = false;
        } else {
            content.style.maxHeight = content.scrollHeight + 'px';
            content.classList.add('active');
            expandedState[contentId] = true;
        }
        
        // Update chevron icon
        const header = document.querySelector(`.timeline-header[data-id="${contentId}"]`);
        if (header) {
            const icon = header.querySelector('.action-btn.expand i');
            if (icon) {
                icon.classList.toggle('fa-chevron-down');
                icon.classList.toggle('fa-chevron-up');
            }
        }
    }

    function handleSearch() {
        const searchTerm = searchInput.value.toLowerCase();
        
        // Search in timeline view
        document.querySelectorAll('.timeline-item').forEach(item => {
            const text = item.textContent.toLowerCase();
            item.style.display = text.includes(searchTerm) ? 'block' : 'none';
        });
        
        // Search in table view
        document.querySelectorAll('tbody tr').forEach(row => {
            const text = row.textContent.toLowerCase();
            row.style.display = text.includes(searchTerm) ? '' : 'none';
        });
    }

    function resetFilters() {
        // Reset all filter inputs
        document.querySelectorAll('#filterOptions select, #filterOptions input').forEach(el => {
            el.value = '';
        });
        
        // Reset search
        if (searchInput) searchInput.value = '';
        
        // Show all items
        document.querySelectorAll('.timeline-item').forEach(item => {
            item.style.display = 'block';
        });
        
        document.querySelectorAll('tbody tr').forEach(row => {
            row.style.display = '';
        });
    }

    function applyFilters() {
        const projectFilter = document.getElementById('filter-project').value.toLowerCase();
        const dateFrom = document.getElementById('filter-date-from').value;
        const dateTo = document.getElementById('filter-date-to').value;
        const weatherFilter = document.getElementById('filter-weather').value.toLowerCase();
        const personnelFilter = document.getElementById('filter-personnel').value.toLowerCase();
        
        // Filter timeline items
        document.querySelectorAll('.timeline-item').forEach(item => {
            const itemProject = item.querySelector('h3').textContent.toLowerCase();
            const itemDate = item.querySelector('.timeline-date span').textContent;
            const itemWeather = item.querySelector('.weather-detail:nth-child(2) span').textContent.toLowerCase();
            const itemPersonnel = item.querySelector('.info-value:nth-child(2)').textContent.toLowerCase();
            
            let show = true;
            
            if (projectFilter && !itemProject.includes(projectFilter)) show = false;
            if (weatherFilter && !itemWeather.includes(weatherFilter)) show = false;
            if (personnelFilter && !itemPersonnel.includes(personnelFilter)) show = false;
            
            // Date filtering would need proper date comparison in a real app
            item.style.display = show ? 'block' : 'none';
        });
        
        // Filter table rows
        document.querySelectorAll('tbody tr').forEach(row => {
            const rowProject = row.querySelector('.table-project-name').textContent.toLowerCase();
            const rowWeather = row.querySelector('.table-weather span').textContent.toLowerCase();
            const rowPersonnel = row.querySelector('td:nth-child(5)').textContent.toLowerCase();
            
            let show = true;
            
            if (projectFilter && !rowProject.includes(projectFilter)) show = false;
            if (weatherFilter && !rowWeather.includes(weatherFilter)) show = false;
            if (personnelFilter && !rowPersonnel.includes(personnelFilter)) show = false;
            
            row.style.display = show ? '' : 'none';
        });
    }

    function handleAction(action, btn) {
        const row = btn.closest('tr') || btn.closest('.timeline-item');
        const projectName = row.querySelector('.table-project-name') ? 
                           row.querySelector('.table-project-name').textContent :
                           row.querySelector('h3').textContent;
        
        switch(action) {
            case 'edit':
                alert(`Editing entry for ${projectName}`);
                break;
            case 'delete':
                if (confirm(`Are you sure you want to delete ${projectName}?`)) {
                    row.style.opacity = '0.5';
                    setTimeout(() => {
                        row.remove();
                    }, 500);
                }
                break;
            case 'download':
                alert(`Downloading PDF for ${projectName}`);
                break;
        }
    }
});