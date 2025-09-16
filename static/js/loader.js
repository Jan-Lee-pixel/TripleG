/**
 * Triple G BuildHub Loading Screen - Enhanced Version
 * A robust loading screen component with Lottie animation, progress tracking,
 * and comprehensive error handling
 */
class TripleGLoader {
    constructor() {
        this.progress = 0;
        this.minLoadTime = 3000; // Minimum display time (ms)
        this.maxLoadTime = 8000; // Maximum time before force complete
        this.loaderContainer = null;
        this.progressBar = null;
        this.startTime = null;
        this.initiated = false;
        this.lottieInstance = null;
        this.lottieContainer = null;
        this.loadingMessage = null;
        this.pageLoaded = false;
        this.lottieLoaded = false;
        this.fallbackUsed = false;
        this.retryCount = 0;
        this.maxRetries = 2;
        this.animationPaths = [
            // Determine paths based on current location
            window.location.pathname.includes('SiteDiary/') ? 
                '../json/Color-scheme-remix.json' : './json/Color-scheme-remix.json', // Primary path
            '/json/Color-scheme-remix.json',  // Absolute path as fallback
            window.location.pathname.includes('SiteDiary/') ? 
                '../json/Color-scheme-[remix].json' : './json/Color-scheme-[remix].json', // Try with brackets
            '/json/Color-scheme-[remix].json' // Absolute path with brackets
        ];
    }

    /**
     * Initialize the loading screen
     */
    init() {
        if (this.initiated) return;
        this.initiated = true;
        this.startTime = performance.now();

        this.createLoaderUI();
        this.setupEventListeners();
        
        // Start both Lottie and progress systems in parallel
        this.loadLottieAnimation();
        this.startProgressSystem();
        
        // Safety timeout in case something hangs
        this.safetyTimeout = setTimeout(() => {
            if (!this.pageLoaded) {
                console.warn('Loader timeout reached - forcing completion');
                this.completeLoading();
            }
        }, this.maxLoadTime);
    }

    /**
     * Create all loader DOM elements
     */
    createLoaderUI() {
        // Main container
        this.loaderContainer = document.createElement('div');
        this.loaderContainer.className = 'tripleG-loader-container';
        document.body.appendChild(this.loaderContainer);

        // Background
        const gradientBg = document.createElement('div');
        gradientBg.className = 'gradient-background';
        this.loaderContainer.appendChild(gradientBg);

        // Logo container
        const logoContainer = document.createElement('div');
        logoContainer.className = 'tripleG-logo-container';
        
        // Logo image
        const logoImg = document.createElement('img');
        logoImg.className = 'tripleG-logo';
        
        // Determine correct path based on current URL
        const isSubdirectory = window.location.pathname.includes('SiteDiary/');
        logoImg.src = isSubdirectory ? '../css/images/logostick.png' : './css/images/logostick.png';
        
        logoImg.alt = 'Triple G Logo';
        logoImg.onerror = () => {
            // Try alternative paths if the first one fails
            if (logoImg.src.includes('./css/')) {
                logoImg.src = '../css/images/logostick.png';
            } else if (logoImg.src.includes('../css/')) {
                logoImg.src = './css/images/logostick.png';
            } else {
                // Final fallback
                logoImg.src = '/css/images/logostick.png';
            }
        };
        logoContainer.appendChild(logoImg);
        
        // Logo text
        const logoText = document.createElement('div');
        logoText.className = 'tripleG-logo-text';
        
        const title = document.createElement('h1');
        title.textContent = 'TRIPLE G';
        
        const subtitle = document.createElement('p');
        subtitle.textContent = 'DESIGN STUDIO + CONSTRUCTION';
        
        logoText.appendChild(title);
        logoText.appendChild(subtitle);
        logoContainer.appendChild(logoText);
        this.loaderContainer.appendChild(logoContainer);

        // Lottie container
        this.lottieContainer = document.createElement('div');
        this.lottieContainer.className = 'tripleG-lottie-container';
        this.loaderContainer.appendChild(this.lottieContainer);

        // Progress bar
        const progressContainer = document.createElement('div');
        progressContainer.className = 'tripleG-progress-container';
        
        this.progressBar = document.createElement('div');
        this.progressBar.className = 'tripleG-progress-bar';
        
        progressContainer.appendChild(this.progressBar);
        this.loaderContainer.appendChild(progressContainer);
        
        // Loading message
        this.loadingMessage = document.createElement('div');
        this.loadingMessage.className = 'tripleG-loading-message';
        this.loadingMessage.textContent = 'Loading creative assets...';
        this.loaderContainer.appendChild(this.loadingMessage);
        
        // Lock body scroll
        document.body.style.overflow = 'hidden';
    }

    /**
     * Set up event listeners
     */
    setupEventListeners() {
        window.addEventListener('load', () => {
            this.pageLoaded = true;
            this.checkCompletion();
        });

        document.addEventListener('DOMContentLoaded', () => {
            this.updateLoadingMessage('Preparing experience...');
        });
    }

    /**
     * Load Lottie animation with fallback handling
     */
    async loadLottieAnimation() {
        // Check if Lottie is already loaded
        if (window.lottie) {
            this.initLottieAnimation();
            return;
        }

        try {
            await this.loadLottieLibrary();
            this.initLottieAnimation();
        } catch (error) {
            console.error('Lottie failed to load:', error);
            this.useFallbackAnimation();
        }
    }

    /**
     * Load Lottie library
     */
    loadLottieLibrary() {
        return new Promise((resolve, reject) => {
            if (window.lottie) {
                resolve();
                return;
            }

            const script = document.createElement('script');
            script.src = 'https://cdnjs.cloudflare.com/ajax/libs/lottie-web/5.10.2/lottie.min.js';
            script.async = true;
            
            script.onload = () => {
                console.log('Lottie loaded successfully');
                resolve();
            };
            
            script.onerror = () => {
                console.error('Lottie script failed to load');
                reject(new Error('Lottie script load failed'));
            };
            
            document.head.appendChild(script);
            
            // Timeout fallback
            setTimeout(() => {
                if (!window.lottie) {
                    reject(new Error('Lottie load timeout'));
                }
            }, 3000);
        });
    }

    /**
     * Initialize Lottie animation with retry logic
     */
    initLottieAnimation(retryIndex = 0) {
        if (!window.lottie || !this.lottieContainer) {
            console.warn('Lottie not available for initialization');
            this.useFallbackAnimation();
            return;
        }

        if (retryIndex >= this.animationPaths.length) {
            console.warn('All animation paths failed - using fallback');
            this.useFallbackAnimation();
            return;
        }

        try {
            this.lottieInstance = lottie.loadAnimation({
                container: this.lottieContainer,
                renderer: 'svg',
                loop: true,
                autoplay: true,
                path: this.animationPaths[retryIndex],
                rendererSettings: {
                    progressiveLoad: true,
                    preserveAspectRatio: 'xMidYMid meet'
                }
            });

            this.lottieInstance.addEventListener('data_ready', () => {
                console.log('Lottie animation loaded successfully');
                this.lottieLoaded = true;
                this.updateLoadingMessage('Almost there...');
                this.checkCompletion();
            });

            this.lottieInstance.addEventListener('data_failed', () => {
                console.warn(`Lottie load failed for path: ${this.animationPaths[retryIndex]}`);
                this.lottieInstance.destroy();
                this.initLottieAnimation(retryIndex + 1);
            });

        } catch (error) {
            console.error('Lottie initialization error:', error);
            this.initLottieAnimation(retryIndex + 1);
        }
    }

    /**
     * Fallback animation when Lottie fails
     */
    useFallbackAnimation() {
        this.fallbackUsed = true;
        this.lottieContainer.innerHTML = `
            <div class="fallback-animation">
                <div class="spinner"></div>
            </div>
        `;
        this.updateLoadingMessage('Loading content...');
        this.lottieLoaded = true; // Mark as loaded to continue progress
        this.checkCompletion();
    }

    /**
     * Start the progress tracking system
     */
    startProgressSystem() {
        this.updateProgress(0);
        
        // Simulate progress updates
        this.progressInterval = setInterval(() => {
            const elapsed = performance.now() - this.startTime;
            const targetProgress = Math.min(0.9, elapsed / (this.minLoadTime * 0.8));
            
            if (this.progress < targetProgress) {
                this.updateProgress(this.progress + 0.01);
            }
            
            // Check if we should complete based on load state
            this.checkCompletion();
        }, 50);
    }

    /**
     * Update progress bar and related UI
     */
    updateProgress(value) {
        this.progress = Math.min(1, Math.max(0, value));
        this.progressBar.style.width = `${this.progress * 100}%`;
        
        // Update loading message based on progress
        if (this.progress < 0.3) {
            this.updateLoadingMessage('Initializing...');
        } else if (this.progress < 0.6) {
            this.updateLoadingMessage('Loading assets...');
        } else if (this.progress < 0.9) {
            this.updateLoadingMessage('Finalizing...');
        }
    }

    /**
     * Update the loading message text
     */
    updateLoadingMessage(text) {
        if (this.loadingMessage) {
            this.loadingMessage.textContent = text;
        }
    }

    /**
     * Check if loading should complete
     */
    checkCompletion() {
        const elapsed = performance.now() - this.startTime;
        const minTimeReached = elapsed >= this.minLoadTime;
        const resourcesReady = this.pageLoaded && this.lottieLoaded;
        
        if (minTimeReached && resourcesReady) {
            this.completeLoading();
        } else if (this.progress >= 0.99) {
            // Emergency completion if progress somehow reaches end
            this.completeLoading();
        }
    }

    /**
     * Complete the loading process
     */
    completeLoading() {
        clearInterval(this.progressInterval);
        clearTimeout(this.safetyTimeout);
        
        // Quickly fill any remaining progress
        this.updateProgress(1);
        
        // Hide the loader
        setTimeout(() => {
            this.hideLoader();
        }, 500);
    }

    /**
     * Hide the loader with transition
     */
    hideLoader() {
        if (!this.loaderContainer) return;
        
        this.loaderContainer.classList.add('tripleG-loader-hidden');
        
        // Clean up Lottie if used
        if (this.lottieInstance) {
            this.lottieInstance.destroy();
        }
        
        // Remove from DOM after transition
        setTimeout(() => {
            if (this.loaderContainer && this.loaderContainer.parentNode) {
                this.loaderContainer.parentNode.removeChild(this.loaderContainer);
            }
            document.body.style.overflow = '';
        }, 600);
    }

    /**
     * Force hide the loader in emergency situations
     */
    forceHide() {
        clearInterval(this.progressInterval);
        clearTimeout(this.safetyTimeout);
        this.hideLoader();
    }
}

// Initialize loader
const tripleGLoader = new TripleGLoader();

// Start loader based on document state
if (document.readyState === 'complete') {
    tripleGLoader.init();
} else {
    document.addEventListener('DOMContentLoaded', () => tripleGLoader.init());
    window.addEventListener('load', () => tripleGLoader.init());
}

// Export for debugging
window.tripleGLoader = tripleGLoader;