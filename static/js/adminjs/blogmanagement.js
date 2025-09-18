document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const tableViewBtn = document.getElementById('tableViewBtn');
    const gridViewBtn = document.getElementById('gridViewBtn');
    const tableView = document.getElementById('tableView');
    const gridView = document.getElementById('gridView');
    const expandAllBtn = document.getElementById('expandAllBtn');
    const collapseAllBtn = document.getElementById('collapseAllBtn');
    const filterToggle = document.getElementById('filterToggle');
    const filterOptions = document.getElementById('filterOptions');
    const searchInput = document.querySelector('.search-input');
    const resetFiltersBtn = document.getElementById('resetFilters');
    const applyFiltersBtn = document.getElementById('applyFilters');
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const navLinks = document.getElementById('navLinks');
    
    // Modal Elements
    const blogPreviewModal = document.getElementById('blogPreviewModal');
    const closeBlogPreviewModal = document.getElementById('closeBlogPreviewModal');
    const blogPreviewActions = document.getElementById('blogPreviewActions');
    const rejectionModal = document.getElementById('rejectionModal');
    const closeRejectionModal = document.getElementById('closeRejectionModal');
    const cancelRejection = document.getElementById('cancelRejection');
    const confirmRejection = document.getElementById('confirmRejection');
    const rejectionReason = document.getElementById('rejectionReason');
    const rejectBlogId = document.getElementById('rejectBlogId');
    const notificationModal = document.getElementById('notificationModal');
    const notificationTitle = document.getElementById('notificationTitle');
    const notificationMessage = document.getElementById('notificationMessage');
    const closeNotificationModal = document.getElementById('closeNotificationModal');
    const confirmNotification = document.getElementById('confirmNotification');

    // Initialize view
    let currentView = 'table'; // Default view
    
    // Initialize the page
    init();

    function init() {
        // Set up event listeners
        setupEventListeners();
        
        // Initialize view toggle
        toggleView(currentView);
        
        // Initialize filter toggle
        filterOptions.style.display = 'none';
        
        // Update summary counts
        updateSummaryCounts();
    }

    function setupEventListeners() {
        // View toggle buttons
        if (tableViewBtn && gridViewBtn) {
            tableViewBtn.addEventListener('click', () => toggleView('table'));
            gridViewBtn.addEventListener('click', () => toggleView('grid'));
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
        
        // Modal close buttons
        if (closeBlogPreviewModal) {
            closeBlogPreviewModal.addEventListener('click', closeBlogPreview);
        }
        
        if (closeRejectionModal) {
            closeRejectionModal.addEventListener('click', () => rejectionModal.style.display = 'none');
        }
        
        if (cancelRejection) {
            cancelRejection.addEventListener('click', () => rejectionModal.style.display = 'none');
        }
        
        if (confirmRejection) {
            confirmRejection.addEventListener('click', handleRejection);
        }
        
        if (closeNotificationModal) {
            closeNotificationModal.addEventListener('click', () => notificationModal.style.display = 'none');
        }
        
        if (confirmNotification) {
            confirmNotification.addEventListener('click', () => notificationModal.style.display = 'none');
        }
    }

    function toggleView(view) {
        currentView = view;
        
        if (view === 'table') {
            tableView.style.display = 'block';
            gridView.style.display = 'none';
            tableViewBtn.classList.add('active');
            gridViewBtn.classList.remove('active');
        } else {
            tableView.style.display = 'none';
            gridView.style.display = 'grid';
            gridViewBtn.classList.add('active');
            tableViewBtn.classList.remove('active');
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
        // For future implementation if needed
        console.log('Expand all functionality');
    }

    function collapseAll() {
        // For future implementation if needed
        console.log('Collapse all functionality');
    }

    function handleSearch() {
        const searchTerm = searchInput.value.toLowerCase();
        
        // Search in table view
        document.querySelectorAll('tbody tr').forEach(row => {
            const blogTitle = row.querySelector('.blog-title').textContent.toLowerCase();
            const category = row.cells[2].textContent.toLowerCase();
            const author = row.cells[3].textContent.toLowerCase();
            const tags = Array.from(row.querySelectorAll('.blog-tag'))
                .map(tag => tag.textContent.toLowerCase())
                .join(' ');
                
            const text = `${blogTitle} ${category} ${author} ${tags}`;
            row.style.display = text.includes(searchTerm) ? '' : 'none';
        });
        
        // Search in grid view
        document.querySelectorAll('.blog-card').forEach(card => {
            const blogTitle = card.querySelector('.blog-card-title').textContent.toLowerCase();
            const category = card.querySelector('.blog-card-info span:nth-child(1)').textContent.toLowerCase();
            const author = card.querySelector('.blog-card-info span:nth-child(2)').textContent.toLowerCase();
            const tags = Array.from(card.querySelectorAll('.blog-tag'))
                .map(tag => tag.textContent.toLowerCase())
                .join(' ');
                
            const text = `${blogTitle} ${category} ${author} ${tags}`;
            card.style.display = text.includes(searchTerm) ? '' : 'none';
        });
    }

    function resetFilters() {
        // Reset all filter inputs
        document.querySelectorAll('#filterOptions select, #filterOptions input').forEach(el => {
            el.value = '';
        });
        
        // Reset search
        if (searchInput) searchInput.value = '';
        
        // Show all blogs
        document.querySelectorAll('tbody tr').forEach(row => {
            row.style.display = '';
        });
        
        document.querySelectorAll('.blog-card').forEach(card => {
            card.style.display = '';
        });
    }

    function applyFilters() {
        const statusFilter = document.getElementById('filter-status').value.toLowerCase();
        const categoryFilter = document.getElementById('filter-category').value.toLowerCase();
        const authorFilter = document.getElementById('filter-author').value.toLowerCase();
        const dateFrom = document.getElementById('filter-date-from').value;
        const dateTo = document.getElementById('filter-date-to').value;
        
        // Filter table rows
        document.querySelectorAll('tbody tr').forEach(row => {
            const status = row.querySelector('.status-badge').textContent.toLowerCase();
            const category = row.cells[2].textContent.toLowerCase();
            const author = row.cells[3].textContent.toLowerCase();
            const date = row.cells[4].textContent;
            
            let show = true;
            
            if (statusFilter && !status.includes(statusFilter)) show = false;
            if (categoryFilter && !category.includes(categoryFilter)) show = false;
            if (authorFilter && !author.includes(authorFilter)) show = false;
            
            // Simple date range filtering
            if (dateFrom && date < dateFrom) show = false;
            if (dateTo && date > dateTo) show = false;
            
            row.style.display = show ? '' : 'none';
        });
        
        // Filter grid cards
        document.querySelectorAll('.blog-card').forEach(card => {
            const status = card.querySelector('.blog-card-status').textContent.toLowerCase();
            const category = card.querySelector('.blog-card-info span:nth-child(1)').textContent.toLowerCase();
            const author = card.querySelector('.blog-card-info span:nth-child(2)').textContent.toLowerCase();
            const date = card.querySelector('.blog-card-info span:nth-child(3)').textContent.replace('Date: ', '');
            
            let show = true;
            
            if (statusFilter && !status.includes(statusFilter)) show = false;
            if (categoryFilter && !category.includes(categoryFilter)) show = false;
            if (authorFilter && !author.includes(authorFilter)) show = false;
            
            // Simple date range filtering
            if (dateFrom && date < dateFrom) show = false;
            if (dateTo && date > dateTo) show = false;
            
            card.style.display = show ? '' : 'none';
        });
    }
    
    // Blog preview functionality
    window.viewBlog = function(blogId) {
        // Hide all blog previews
        document.querySelectorAll('.blog-preview').forEach(preview => {
            preview.style.display = 'none';
        });
        
        // Show the selected blog preview
        const selectedBlog = document.getElementById(`blogPreview${blogId}`);
        if (selectedBlog) {
            selectedBlog.style.display = 'block';
        }
        
        // Set action buttons based on current blog status
        const blogRow = document.querySelector(`tr[data-id="${blogId}"]`);
        const statusBadge = blogRow ? blogRow.querySelector('.status-badge') : null;
        const status = statusBadge ? statusBadge.textContent.trim() : '';
        
        // Clear previous action buttons
        blogPreviewActions.innerHTML = '';
        
        if (status === 'Pending') {
            // Add approve and reject buttons for pending blogs
            const approveButton = document.createElement('button');
            approveButton.className = 'btn btn-success';
            approveButton.innerHTML = '<i class="fas fa-check"></i> Approve';
            approveButton.addEventListener('click', () => approveBlog(blogId));
            
            const rejectButton = document.createElement('button');
            rejectButton.className = 'btn btn-danger';
            rejectButton.innerHTML = '<i class="fas fa-times"></i> Reject';
            rejectButton.addEventListener('click', () => rejectBlog(blogId));
            
            blogPreviewActions.appendChild(approveButton);
            blogPreviewActions.appendChild(rejectButton);
        } else if (status === 'Rejected') {
            // Add approve button for rejected blogs
            const approveButton = document.createElement('button');
            approveButton.className = 'btn btn-success';
            approveButton.innerHTML = '<i class="fas fa-check"></i> Approve';
            approveButton.addEventListener('click', () => approveBlog(blogId));
            
            blogPreviewActions.appendChild(approveButton);
        }
        
        // Add a close button to the actions for all modals
        const closeButton = document.createElement('button');
        closeButton.className = 'btn btn-secondary';
        closeButton.innerHTML = '<i class="fas fa-times"></i> Close';
        closeButton.addEventListener('click', closeBlogPreview);
        blogPreviewActions.appendChild(closeButton);
        
        // Show the modal
        blogPreviewModal.style.display = 'flex';
        
        // Reset modal scroll position
        blogPreviewModal.querySelector('.modal-body').scrollTop = 0;
    };
    
    function closeBlogPreview() {
        blogPreviewModal.style.display = 'none';
    }
    
    // Approve blog functionality
    window.approveBlog = function(blogId) {
        // Update status badge in table view
        const tableRow = document.querySelector(`tr[data-id="${blogId}"]`);
        if (tableRow) {
            const statusBadge = tableRow.querySelector('.status-badge');
            statusBadge.textContent = 'Approved';
            statusBadge.className = 'status-badge status-approved';
            
            // Update actions column
            const actionsCell = tableRow.querySelector('.actions');
            actionsCell.innerHTML = `
                <button class="action-btn view" title="View" onclick="viewBlog(${blogId})"><i class="fas fa-eye"></i></button>
                <button class="action-btn edit" title="Edit"><i class="fas fa-edit"></i></button>
                <button class="action-btn delete" title="Delete"><i class="fas fa-trash"></i></button>
            `;
        }
        
        // Update status badge in grid view
        const gridCard = document.querySelector(`.blog-card[data-id="${blogId}"]`);
        if (gridCard) {
            const statusBadge = gridCard.querySelector('.blog-card-status');
            statusBadge.textContent = 'Approved';
            statusBadge.className = 'blog-card-status status-approved';
            
            // Update action buttons
            const cardActions = gridCard.querySelector('.blog-card-actions');
            cardActions.innerHTML = `
                <button class="btn btn-primary" onclick="viewBlog(${blogId})"><i class="fas fa-eye"></i> View</button>
                <button class="btn btn-secondary"><i class="fas fa-edit"></i> Edit</button>
                <button class="btn btn-danger"><i class="fas fa-trash"></i> Delete</button>
            `;
        }
        
        // Show notification
        showNotification('Blog Approved', 'The blog has been approved and is now published.');
        
        // Close the blog preview modal
        closeBlogPreview();
        
        // Update summary counts
        updateSummaryCounts();
    };
    
    // Reject blog functionality
    window.rejectBlog = function(blogId) {
        // Show rejection modal
        rejectionModal.style.display = 'flex';
        rejectBlogId.value = blogId;
        rejectionReason.value = ''; // Clear any previous reason
    };
    
    function handleRejection() {
        const blogId = rejectBlogId.value;
        const reason = rejectionReason.value.trim();
        
        if (!reason) {
            alert('Please provide a reason for rejection.');
            return;
        }
        
        // Update status badge in table view
        const tableRow = document.querySelector(`tr[data-id="${blogId}"]`);
        if (tableRow) {
            const statusBadge = tableRow.querySelector('.status-badge');
            statusBadge.textContent = 'Rejected';
            statusBadge.className = 'status-badge status-rejected';
            
            // Update actions column
            const actionsCell = tableRow.querySelector('.actions');
            actionsCell.innerHTML = `
                <button class="action-btn view" title="View" onclick="viewBlog(${blogId})"><i class="fas fa-eye"></i></button>
                <button class="action-btn approve" title="Approve" onclick="approveBlog(${blogId})"><i class="fas fa-check"></i></button>
                <button class="action-btn edit" title="Edit"><i class="fas fa-edit"></i></button>
            `;
        }
        
        // Update status badge in grid view
        const gridCard = document.querySelector(`.blog-card[data-id="${blogId}"]`);
        if (gridCard) {
            const statusBadge = gridCard.querySelector('.blog-card-status');
            statusBadge.textContent = 'Rejected';
            statusBadge.className = 'blog-card-status status-rejected';
            
            // Update action buttons
            const cardActions = gridCard.querySelector('.blog-card-actions');
            cardActions.innerHTML = `
                <button class="btn btn-primary" onclick="viewBlog(${blogId})"><i class="fas fa-eye"></i> View</button>
                <button class="btn btn-success" onclick="approveBlog(${blogId})"><i class="fas fa-check"></i> Approve</button>
                <button class="btn btn-secondary"><i class="fas fa-edit"></i> Edit</button>
            `;
        }
        
        // Hide the rejection modal
        rejectionModal.style.display = 'none';
        
        // Show notification
        showNotification('Blog Rejected', `The blog has been rejected. Reason: ${reason}`);
        
        // Close the blog preview modal
        closeBlogPreview();
        
        // Update summary counts
        updateSummaryCounts();
    }
    
    // Show notification
    function showNotification(title, message) {
        notificationTitle.textContent = title;
        notificationMessage.textContent = message;
        notificationModal.style.display = 'flex';
    }
    
    // Update summary counts
    function updateSummaryCounts() {
        const totalBlogsEl = document.getElementById('totalBlogs');
        const pendingBlogsEl = document.getElementById('pendingBlogs');
        const approvedBlogsEl = document.getElementById('approvedBlogs');
        const rejectedBlogsEl = document.getElementById('rejectedBlogs');
        
        // Count blogs by status
        const totalBlogs = document.querySelectorAll('.blog-item').length;
        const pendingBlogs = document.querySelectorAll('.status-badge.status-pending').length;
        const approvedBlogs = document.querySelectorAll('.status-badge.status-approved').length;
        const rejectedBlogs = document.querySelectorAll('.status-badge.status-rejected').length;
        
        // Update the display
        if (totalBlogsEl) totalBlogsEl.textContent = totalBlogs;
        if (pendingBlogsEl) pendingBlogsEl.textContent = pendingBlogs;
        if (approvedBlogsEl) approvedBlogsEl.textContent = approvedBlogs;
        if (rejectedBlogsEl) rejectedBlogsEl.textContent = rejectedBlogs;
    }
});
