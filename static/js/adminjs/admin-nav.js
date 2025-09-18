// Admin Dropdown Navigation JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Get all dropdown toggles
    const dropdownToggles = document.querySelectorAll('.dropdown-toggle');
    
    // Add click event to each dropdown toggle
    dropdownToggles.forEach(toggle => {
        toggle.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Toggle active class on parent dropdown
            const dropdown = this.parentElement;
            
            // Close all other dropdowns first
            document.querySelectorAll('.dropdown').forEach(item => {
                if (item !== dropdown && item.classList.contains('active')) {
                    item.classList.remove('active');
                }
            });
            
            // Toggle current dropdown
            dropdown.classList.toggle('active');
        });
    });
    
    // Close dropdowns when clicking outside
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.dropdown')) {
            document.querySelectorAll('.dropdown').forEach(dropdown => {
                dropdown.classList.remove('active');
            });
        }
    });
    
    // Mark active menu items based on current page
    const currentPage = window.location.pathname.split('/').pop();
    
    if (currentPage) {
        const menuLinks = document.querySelectorAll('.nav-links a');
        
        menuLinks.forEach(link => {
            const linkHref = link.getAttribute('href');
            
            if (linkHref && linkHref.includes(currentPage)) {
                link.classList.add('active');
                
                // If the link is in a dropdown, also activate the dropdown
                const parentDropdown = link.closest('.dropdown');
                if (parentDropdown) {
                    parentDropdown.querySelector('.dropdown-toggle').classList.add('active');
                }
            }
        });
    } else {
        // If no current page is detected, set the home link as active
        const homeLink = document.querySelector('.nav-links a[href*="home.html"]');
        if (homeLink) {
            homeLink.classList.add('active');
        }
    }
    
    // Mobile menu toggle
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const navLinks = document.querySelector('.nav-links');
    
    if (mobileMenuBtn) {
        mobileMenuBtn.addEventListener('click', function() {
            navLinks.classList.toggle('active');
            this.classList.toggle('active');
        });
    }
}); 