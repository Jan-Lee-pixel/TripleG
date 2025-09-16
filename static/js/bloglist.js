/**
 * Triple G BuildHub Blog Listing JavaScript
 * Handles blog filtering, search, pagination and animations
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize variables
    const searchInput = document.getElementById('blogSearch');
    const searchButton = document.getElementById('searchButton');
    const blogPostsContainer = document.getElementById('blogPostsContainer');
    const filterTags = document.querySelectorAll('.filter-tag');
    const paginationButtons = document.querySelectorAll('.pagination-btn');

    // Mobile menu toggle
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const navLinks = document.getElementById('navLinks');

    if (mobileMenuBtn && navLinks) {
        mobileMenuBtn.addEventListener('click', function() {
            navLinks.classList.toggle('active');
        });
    }

    // Initialize video background
    initVideoBackground();

    /**
     * Blog Post Data (Mock data - would typically come from a database)
     * In a real application, this would be fetched from an API or backend
     */
    const allPosts = Array.from(document.querySelectorAll('.blog-card'));
    let currentPage = 1;
    const postsPerPage = 6; // Number of posts to show per page
    let filteredPosts = [...allPosts]; // Start with all posts

    // Initialize the page
    initializePage();

    /**
     * Sets up the initial page state and event listeners
     */
    function initializePage() {
        // Initialize filter tags
        if (filterTags.length > 0) {
            filterTags.forEach(tag => {
                tag.addEventListener('click', function() {
                    // Remove active class from all tags
                    filterTags.forEach(t => t.classList.remove('active'));
                    // Add active class to clicked tag
                    this.classList.add('active');
                    
                    // Filter posts based on selected category
                    const category = this.getAttribute('data-category');
                    filterPostsByCategory(category);
                });
            });
        }

        // Initialize search
        if (searchInput && searchButton) {
            searchButton.addEventListener('click', function() {
                searchPosts(searchInput.value);
            });

            searchInput.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    searchPosts(this.value);
                }
            });
        }

        // Initialize pagination
        if (paginationButtons.length > 0) {
            paginationButtons.forEach(button => {
                if (!button.classList.contains('pagination-next') && !button.classList.contains('pagination-prev')) {
                    button.addEventListener('click', function() {
                        const pageNum = parseInt(this.textContent);
                        if (!isNaN(pageNum)) {
                            goToPage(pageNum);
                        }
                    });
                }
            });

            // Next page button
            const nextButton = document.querySelector('.pagination-next');
            if (nextButton) {
                nextButton.addEventListener('click', function() {
                    goToPage(currentPage + 1);
                });
            }
        }

        // Load More button (alternative to pagination)
        const loadMoreBtn = document.getElementById('loadMoreBtn');
        if (loadMoreBtn) {
            loadMoreBtn.addEventListener('click', function() {
                loadMorePosts();
            });
        }

        // Initial display of posts
        updatePostDisplay();

        // Add animation to blog cards on hover
        addCardAnimations();
    }

    /**
     * Filter posts based on category
     * @param {string} category - The category to filter by
     */
    function filterPostsByCategory(category) {
        // Reset to page 1 when filtering
        currentPage = 1;

        if (category === 'all') {
            filteredPosts = [...allPosts];
        } else {
            filteredPosts = allPosts.filter(post => {
                return post.getAttribute('data-category') === category;
            });
        }

        updatePostDisplay();
        updatePaginationState();
    }

    /**
     * Search posts based on keyword
     * @param {string} keyword - The search term
     */
    function searchPosts(keyword) {
        // Reset to page 1 when searching
        currentPage = 1;

        if (!keyword || keyword.trim() === '') {
            filteredPosts = [...allPosts];
        } else {
            keyword = keyword.toLowerCase().trim();
            filteredPosts = allPosts.filter(post => {
                const postTitle = post.querySelector('h3').textContent.toLowerCase();
                const postContent = post.querySelector('p').textContent.toLowerCase();
                return postTitle.includes(keyword) || postContent.includes(keyword);
            });
        }

        updatePostDisplay();
        updatePaginationState();

        // Show search results message
        const resultsCount = filteredPosts.length;
        const searchResultMsg = document.createElement('div');
        searchResultMsg.className = 'search-results-message';
        searchResultMsg.innerHTML = `
            <p>${resultsCount} ${resultsCount === 1 ? 'result' : 'results'} found for "${keyword}"</p>
            ${resultsCount === 0 ? '<p>Try a different search term</p>' : ''}
        `;

        // Insert the message before the blog posts grid
        const blogPostsParent = blogPostsContainer.parentElement;
        const existingMsg = blogPostsParent.querySelector('.search-results-message');
        if (existingMsg) {
            blogPostsParent.removeChild(existingMsg);
        }
        blogPostsParent.insertBefore(searchResultMsg, blogPostsContainer);

        // Scroll to search results
        searchResultMsg.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    /**
     * Navigate to a specific page
     * @param {number} pageNum - The page number to navigate to
     */
    function goToPage(pageNum) {
        // Validate page number
        const maxPages = Math.ceil(filteredPosts.length / postsPerPage);
        if (pageNum < 1 || pageNum > maxPages) {
            return;
        }

        currentPage = pageNum;
        updatePostDisplay();
        updatePaginationState();

        // Scroll to top of posts
        blogPostsContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    /**
     * Load more posts (alternative to pagination)
     */
    function loadMorePosts() {
        currentPage++;
        const maxPages = Math.ceil(filteredPosts.length / postsPerPage);
        
        if (currentPage >= maxPages) {
            const loadMoreBtn = document.getElementById('loadMoreBtn');
            if (loadMoreBtn) {
                loadMoreBtn.style.display = 'none';
            }
        }

        updatePostDisplay(true); // true means append instead of replace
    }

    /**
     * Update which posts are displayed based on current filters, search, and pagination
     * @param {boolean} append - Whether to append to existing posts (for load more) or replace
     */
    function updatePostDisplay(append = false) {
        if (!blogPostsContainer) return;

        // Calculate start and end indices for current page
        const startIndex = (currentPage - 1) * postsPerPage;
        const endIndex = Math.min(startIndex + postsPerPage, filteredPosts.length);
        const postsToShow = filteredPosts.slice(startIndex, endIndex);

        // Hide all posts first if not appending
        if (!append) {
            allPosts.forEach(post => {
                post.style.display = 'none';
            });
        }

        // Show the posts for this page
        postsToShow.forEach((post, index) => {
            post.style.display = 'block';
            
            // Add staggered animation when posts appear
            post.style.opacity = '0';
            post.style.transform = 'translateY(20px)';
            
            setTimeout(() => {
                post.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
                post.style.opacity = '1';
                post.style.transform = 'translateY(0)';
            }, index * 100); // Stagger the animations
        });

        // Show "No results" message if needed
        if (filteredPosts.length === 0) {
            const noResultsMsg = document.createElement('div');
            noResultsMsg.className = 'no-results-message';
            noResultsMsg.innerHTML = '<p>No blog posts found matching your criteria.</p>';
            
            // Clear existing posts and append message
            blogPostsContainer.innerHTML = '';
            blogPostsContainer.appendChild(noResultsMsg);
        } else if (!append) {
            // Remove any existing "No results" message
            const existingMsg = blogPostsContainer.querySelector('.no-results-message');
            if (existingMsg) {
                blogPostsContainer.removeChild(existingMsg);
            }
        }
    }

    /**
     * Update the pagination buttons to reflect current page
     */
    function updatePaginationState() {
        const paginationContainer = document.querySelector('.pagination');
        if (!paginationContainer) return;

        const totalPages = Math.ceil(filteredPosts.length / postsPerPage);
        
        // Update the active state of page buttons
        const pageButtons = paginationContainer.querySelectorAll('.pagination-btn:not(.pagination-next):not(.pagination-prev)');
        pageButtons.forEach(button => {
            const pageNum = parseInt(button.textContent);
            if (pageNum === currentPage) {
                button.classList.add('active');
            } else {
                button.classList.remove('active');
            }
        });

        // Update next button state
        const nextButton = paginationContainer.querySelector('.pagination-next');
        if (nextButton) {
            if (currentPage >= totalPages) {
                nextButton.classList.add('disabled');
                nextButton.setAttribute('disabled', true);
            } else {
                nextButton.classList.remove('disabled');
                nextButton.removeAttribute('disabled');
            }
        }
    }

    /**
     * Add hover animations and effects to blog cards
     */
    function addCardAnimations() {
        // Add hover effect to blog cards
        const blogCards = document.querySelectorAll('.blog-card, .featured-post-card');
        
        blogCards.forEach(card => {
            // Add hover effects
            card.addEventListener('mouseenter', function() {
                const image = this.querySelector('img');
                if (image) {
                    image.style.transform = 'scale(1.05)';
                }
                
                const readMore = this.querySelector('.read-more, .btn');
                if (readMore) {
                    readMore.style.color = getComputedStyle(document.documentElement).getPropertyValue('--highlight-color');
                }
            });
            
            card.addEventListener('mouseleave', function() {
                const image = this.querySelector('img');
                if (image) {
                    image.style.transform = '';
                }
                
                const readMore = this.querySelector('.read-more, .btn');
                if (readMore && !readMore.classList.contains('btn-primary')) {
                    readMore.style.color = getComputedStyle(document.documentElement).getPropertyValue('--accent-color');
                }
            });
        });
    }

    /**
     * Newsletter Signup Form Handler
     */
    const newsletterForm = document.getElementById('newsletterForm');
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const emailInput = this.querySelector('input[type="email"]');
            
            if (emailInput && emailInput.value.trim() !== '') {
                // Show a success message (in a real app, this would send to a server)
                const formParent = this.parentElement;
                this.style.display = 'none';
                
                const successMsg = document.createElement('div');
                successMsg.className = 'newsletter-success';
                successMsg.innerHTML = `
                    <i class="fas fa-check-circle"></i>
                    <p>Thank you for subscribing!</p>
                    <p>We'll keep you updated with the latest construction industry insights.</p>
                `;
                
                formParent.appendChild(successMsg);
            }
        });
    }

    /**
     * Initialize and handle video background
     */
    function initVideoBackground() {
        const video = document.getElementById('header-bg-video');
        const videoBackground = document.querySelector('.video-background');
        
        if (!video || !videoBackground) return;
        
        // Check if browser can play video
        const canPlayVideo = video.canPlayType && (
            video.canPlayType('video/mp4').replace(/no/, '') ||
            video.canPlayType('video/webm').replace(/no/, '')
        );
        
        // Handle video events
        video.addEventListener('loadeddata', function() {
            // Video has loaded, ensure it's visible
            video.style.opacity = '1';
        });
        
        video.addEventListener('error', function() {
            // Error loading video, show fallback
            showFallbackBackground();
        });
        
        // If browser can't play video, show fallback immediately
        if (!canPlayVideo) {
            showFallbackBackground();
        }
        
        /**
         * Show fallback background when video can't be played
         */
        function showFallbackBackground() {
            // Hide video element
            if (video) video.style.display = 'none';
            
            // Add fallback background image
            if (videoBackground) {
                videoBackground.style.backgroundImage = 'url("../css/images/blog-header-bg.jpg")';
                videoBackground.style.backgroundSize = 'cover';
                videoBackground.style.backgroundPosition = 'center';
            }
        }
    }
});
