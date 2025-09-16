document.addEventListener('DOMContentLoaded', function() {
    // Mobile menu functionality
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const navLinks = document.querySelector('.nav-links');
    
    if (mobileMenuBtn) {
        mobileMenuBtn.addEventListener('click', function() {
            navLinks.classList.toggle('active');
        });
    }

    // Apply custom scrollbar styles
    const style = document.createElement('style');
    style.textContent = `
      /* Webkit browsers (Chrome, Safari, newer versions of Opera) */
      ::-webkit-scrollbar {
        width: 5px;
        background-color: transparent;
      }
      
      ::-webkit-scrollbar-track {
        background-color: transparent;
        border-radius: 5px;
      }
      
      ::-webkit-scrollbar-thumb {
        background-color: rgba(255, 255, 255, 0);
        border-radius: 5px;
        border: 2px solid transparent;
        background-clip: content-box;
        transition: background-color 0.3s;
      }
      
      ::-webkit-scrollbar-thumb:hover {
        background-color: rgba(255, 255, 255, 0);
      }
      
      /* For Firefox */
      * {
        scrollbar-width: thin;
        scrollbar-color: rgba(255, 255, 255, 0.2) transparent;
      }
      
      /* Hide scrollbar when not scrolling (optional) */
      body:not(:hover)::-webkit-scrollbar-thumb {
        background-color: rgba(255, 255, 255, 0);
      }
    `;
    document.head.appendChild(style);
  
    let currentScroll = window.pageYOffset;
    let targetScroll = currentScroll;
    let ticking = false;
    
    function smoothPageScroll() {
        const diff = targetScroll - currentScroll;
        if (Math.abs(diff) < 0.5) {
            currentScroll = targetScroll;
            window.scrollTo(0, currentScroll);
            ticking = false;
            return;
        }
        currentScroll += diff * 0.1;
        window.scrollTo(0, currentScroll);
        if (currentScroll !== targetScroll) {
            requestAnimationFrame(smoothPageScroll);
        } else {
            ticking = false;
        }
    }
    
    function handleWheel(e) {
        e.preventDefault();
        targetScroll = Math.max(0, Math.min(document.body.scrollHeight - window.innerHeight, targetScroll + e.deltaY));
        if (!ticking) {
            ticking = true;
            requestAnimationFrame(smoothPageScroll);
        }
    }
    
    window.addEventListener('wheel', handleWheel, { passive: false });
    
    window.addEventListener('keydown', function(e) {
        let scrollAmount = 0;
        switch(e.key) {
            case 'ArrowDown': scrollAmount = 40; break;
            case 'ArrowUp': scrollAmount = -40; break;
            case 'PageDown': scrollAmount = window.innerHeight * 0.9; break;
            case 'PageUp': scrollAmount = -window.innerHeight * 0.9; break;
            case 'Home': targetScroll = 0; break;
            case 'End': targetScroll = document.body.scrollHeight - window.innerHeight; break;
            default: return;
        }
        if (scrollAmount !== 0) {
            e.preventDefault();
            targetScroll = Math.max(0, Math.min(document.body.scrollHeight - window.innerHeight, targetScroll + scrollAmount));
        }
        if (!ticking) {
            ticking = true;
            requestAnimationFrame(smoothPageScroll);
        }
    });

    // Get DOM elements for filters and project grid
    const yearFilter = document.getElementById('year-filter');
    const categoryFilter = document.getElementById('category-filter');
    const projectsGrid = document.querySelector('.projects-grid');
    
    // Project data - in a real application, this would come from a database
    const projects = [
        {
            id: 1,
            title: "Modern Residential Home",
            description: "Contemporary design with sustainable materials and energy-efficient features for a family of four.",
            thumbnail: "css/images/image1.jpg",
            image: "css/images/image1.jpg",
            year: "2023",
            category: "residential",
            featured: true
        },
        {
            id: 2,
            title: "Corporate Office Building",
            description: "Open-concept workspace design with collaborative areas and natural lighting throughout.",
            thumbnail: "css/images/image2.jpeg",
            image: "css/images/image2.jpeg",
            year: "2022",
            category: "commercial",
            featured: true
        },
        {
            id: 3,
            title: "Public Library Renovation",
            description: "Modernization of a historic library building while preserving its architectural heritage.",
            thumbnail: "css/images/image3.jpg",
            image: "css/images/image3.jpg",
            year: "2021",
            category: "public",
            featured: true
        },
        {
            id: 4,
            title: "Luxury Apartment Complex",
            description: "High-end residential complex with premium amenities and stunning city views.",
            thumbnail: "css/images/image4.jpg",
            image: "css/images/image4.jpg",
            year: "2023",
            category: "residential",
            featured: false
        },
        {
            id: 5,
            title: "Beachfront Restaurant",
            description: "Coastal dining experience with panoramic ocean views and sustainable design.",
            thumbnail: "css/images/image5.jpg",
            image: "css/images/image5.jpg",
            year: "2022",
            category: "commercial",
            featured: false
        },
        {
            id: 6,
            title: "Urban Park Design",
            description: "Community green space with recreational areas, walking paths, and native landscaping.",
            thumbnail: "css/images/image6.jpg",
            image: "css/images/image6.jpg",
            year: "2021",
            category: "public",
            featured: false
        },
        {
            id: 7,
            title: "Minimalist Villa",
            description: "Sleek, modern villa with clean lines and seamless indoor-outdoor living spaces.",
            thumbnail: "css/images/image7.jpg",
            image: "css/images/image7.jpg",
            year: "2024",
            category: "residential",
            featured: false
        },
        {
            id: 8,
            title: "Healthcare Center",
            description: "Patient-centered medical facility designed for comfort, efficiency, and healing.",
            thumbnail: "css/images/image8.jpg",
            image: "css/images/image8.jpg",
            year: "2020",
            category: "public",
            featured: false
        },
        {
            id: 9,
            title: "Boutique Hotel",
            description: "Intimate luxury hotel with unique character and personalized guest experiences.",
            thumbnail: "css/images/image9.jpg",
            image: "css/images/image9.jpg",
            year: "2023",
            category: "commercial",
            featured: false
        }
    ];

    // Function to render projects based on filters
    function renderProjects(year = 'all', category = 'all') {
        // Clear current projects
        projectsGrid.innerHTML = '';
        
        // Filter projects
        let filteredProjects = projects;
        
        if (year !== 'all') {
            filteredProjects = filteredProjects.filter(project => project.year === year);
        }
        
        if (category !== 'all') {
            if (category === 'featured') {
                filteredProjects = filteredProjects.filter(project => project.featured);
            } else {
                filteredProjects = filteredProjects.filter(project => project.category === category);
            }
        }
        
        // If no projects match filters
        if (filteredProjects.length === 0) {
            projectsGrid.innerHTML = '<div class="no-projects">No projects match your filter criteria.</div>';
            return;
        }
        
        // Render filtered projects - this is where duplication was happening previously
        filteredProjects.forEach(project => {
            const projectCard = document.createElement('div');
            projectCard.className = 'project-card';
            
            projectCard.innerHTML = `
                <div class="project-image">
                    <img src="${project.thumbnail}" alt="${project.title}" onerror="this.src='css/images/kristelle.jpg';">
                    <div class="layer"></div>
                </div>
                <div class="project-info">
                    <h3>${project.title}</h3>
                    <p>${project.description}</p>
                    <div class="project-metadata">
                        <span class="project-year">${project.year}</span>
                        <span class="project-category">${formatCategory(project.category)}</span>
                    </div>
                    <a href="project-detail.html?id=${project.id}" class="project-link">View Details</a>
                </div>
            `;
            
            projectsGrid.appendChild(projectCard);
        });
    }

    function populateFilters() {
        // Check if filter elements exist on the page
        if (!yearFilter || !categoryFilter) {
            console.error('Filter elements not found');
            return;
        }
        
        // Get unique years
        const years = [...new Set(projects.map(project => project.year))];
        years.sort((a, b) => b - a); // Sort descending (newest first)
        
        // Clear and rebuild year filter
        yearFilter.innerHTML = '<option value="all">All</option>';
        years.forEach(year => {
            const option = document.createElement('option');
            option.value = year;
            option.textContent = year;
            yearFilter.appendChild(option);
        });
        
        // Get unique categories
        const categories = [...new Set(projects.map(project => project.category))];
        
        // Clear and rebuild category filter
        categoryFilter.innerHTML = '<option value="all">All</option>';
        
        // Add featured option if applicable
        if (projects.some(project => project.featured)) {
            const featuredOption = document.createElement('option');
            featuredOption.value = 'featured';
            featuredOption.textContent = 'Featured';
            categoryFilter.appendChild(featuredOption);
        }
        
        // Add all other categories
        categories.forEach(category => {
            const option = document.createElement('option');
            option.value = category;
            option.textContent = formatCategory(category);
            categoryFilter.appendChild(option);
        });
    }

    // Format category text for display
    function formatCategory(category) {
        switch(category) {
            case 'residential':
                return 'Residential';
            case 'commercial':
                return 'Commercial';
            case 'public':
                return 'Public';
            default:
                return category.charAt(0).toUpperCase() + category.slice(1);
        }
    }
    
    
    // Initialize filters if they exist on the page
    if (yearFilter && categoryFilter) {
        populateFilters();
        
        // Filter change event listeners
        yearFilter.addEventListener('change', function() {
            renderProjects(this.value, categoryFilter.value);
        });
        
        categoryFilter.addEventListener('change', function() {
            renderProjects(yearFilter.value, this.value);
        });
    }
    
    // Initialize featured projects interactivity
    const featuredProjects = document.querySelectorAll('.featured-project');
    const viewProjectBtn = document.querySelector('.view-project-btn');
    
    // Set up featured project click handling
    if (featuredProjects.length > 0 && viewProjectBtn) {
        // First, associate project IDs with featured projects
        featuredProjects.forEach((project, index) => {
            if (projects[index]) {
                project.setAttribute('data-project-id', projects[index].id);
            }
        });
        
        // Set default selected project (first project is already active in HTML)
        const activeProject = document.querySelector('.featured-project.active');
        if (activeProject) {
            const projectId = activeProject.getAttribute('data-project-id');
            if (projectId) {
                viewProjectBtn.setAttribute('data-project-id', projectId);
            } else if (projects && projects.length > 0) {
                viewProjectBtn.setAttribute('data-project-id', projects[0].id);
            }
        }
        
        // Add click event listeners to featured projects
        featuredProjects.forEach(project => {
            project.addEventListener('click', function() {
                // Remove active class from all projects
                featuredProjects.forEach(p => p.classList.remove('active'));
                
                // Add active class to clicked project
                this.classList.add('active');
                
                // Update view project button with project ID
                const projectId = this.getAttribute('data-project-id');
                if (projectId) {
                    viewProjectBtn.setAttribute('data-project-id', projectId);
                    
                    // Add pulse animation to button
                    viewProjectBtn.classList.add('pulse');
                    setTimeout(() => {
                        viewProjectBtn.classList.remove('pulse');
                    }, 1000);
                }
            });
        });
        
        // Add mousemove event listener to track cursor position
        viewProjectBtn.addEventListener('mousemove', (e) => {
            // Get position relative to the button
            const rect = viewProjectBtn.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            // Update CSS variables for glow effect position
            viewProjectBtn.style.setProperty('--x', `${x}px`);
            viewProjectBtn.style.setProperty('--y', `${y}px`);
        });
        
        // Add click event to view project button
        viewProjectBtn.addEventListener('click', function(e) {
            e.preventDefault();
            
            const projectId = this.getAttribute('data-project-id');
            if (projectId) {
                window.location.href = `project-detail.html?id=${projectId}`;
            } else {
                window.location.href = 'project-detail.html';
            }
        });
    }
    
    // Initialize projects grid if it exists
    if (projectsGrid) {
        renderProjects();
    }
});
