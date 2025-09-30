// ===============================
// MODERN UI JAVASCRIPT CONTROLLER
// ===============================

class MovieRecommendationUI {
    constructor() {
        this.init();
        this.setupEventListeners();
    }

    init() {
        // Initialize UI components
        this.loadingOverlay = document.getElementById('loadingOverlay');
        this.toastContainer = document.getElementById('toastContainer');
        this.currentSort = { column: null, direction: 'asc' };
        this.moviesData = [];
        
        // Add entrance animations
        this.addEntranceAnimations();
    }

    setupEventListeners() {
        // Form submission with loading state
        const form = document.querySelector('.recommendation-form form');
        if (form) {
            form.addEventListener('submit', (e) => {
                this.handleFormSubmission(e);
            });
        }

        // Sort button listeners
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('sort-btn')) {
                this.handleSort(e.target);
            }
        });

        // Table hover effects
        this.setupTableEffects();
        
        // Initialize tooltips and interactions
        this.initializeInteractions();
    }

    // ===============================
    // FORM HANDLING
    // ===============================

    handleFormSubmission(e) {
        const mood = document.getElementById('sentiment').value;
        const language = document.getElementById('language').value;

        if (!mood || !language) {
            this.showToast('Please select both mood and language', 'warning');
            e.preventDefault();
            return;
        }

        // Show loading state
        this.showLoading();
        
        // Show success message
        this.showToast(`Finding ${mood} movies in ${language}...`, 'info');
    }

    // ===============================
    // LOADING STATES
    // ===============================

    showLoading() {
        this.loadingOverlay.classList.add('active');
        document.body.style.overflow = 'hidden';
    }

    hideLoading() {
        this.loadingOverlay.classList.remove('active');
        document.body.style.overflow = '';
    }

    // ===============================
    // TOAST NOTIFICATIONS
    // ===============================

    showToast(message, type = 'info', duration = 4000) {
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        
        const icons = {
            success: 'fas fa-check-circle',
            warning: 'fas fa-exclamation-triangle',
            error: 'fas fa-times-circle',
            info: 'fas fa-info-circle'
        };

        toast.innerHTML = `
            <div class="toast-content">
                <i class="toast-icon ${icons[type]}"></i>
                <div class="toast-message">${message}</div>
                <button class="toast-close" onclick="this.parentElement.parentElement.remove()">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `;

        this.toastContainer.appendChild(toast);

        // Trigger show animation
        setTimeout(() => toast.classList.add('show'), 100);

        // Auto remove
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 300);
        }, duration);
    }

    // ===============================
    // TABLE SORTING
    // ===============================

    handleSort(button) {
        const column = button.dataset.sort;
        const table = document.querySelector('.movies-table tbody');
        
        if (!table) return;

        // Update sort direction
        if (this.currentSort.column === column) {
            this.currentSort.direction = this.currentSort.direction === 'asc' ? 'desc' : 'asc';
        } else {
            this.currentSort.column = column;
            this.currentSort.direction = 'asc';
        }

        // Update button states
        document.querySelectorAll('.sort-btn').forEach(btn => btn.classList.remove('active'));
        button.classList.add('active');
        
        // Update button text
        const icon = this.currentSort.direction === 'asc' ? 'fa-sort-up' : 'fa-sort-down';
        button.innerHTML = button.innerHTML.replace(/fa-sort[-\w]*/, icon);

        // Get and sort rows
        const rows = Array.from(table.querySelectorAll('tr'));
        const sortedRows = this.sortTableRows(rows, column, this.currentSort.direction);

        // Clear table and add sorted rows with animation
        table.innerHTML = '';
        sortedRows.forEach((row, index) => {
            row.style.animationDelay = `${index * 0.05}s`;
            row.classList.add('slide-in-up');
            table.appendChild(row);
        });

        this.showToast(`Sorted by ${column} (${this.currentSort.direction}ending)`, 'success', 2000);
    }

    sortTableRows(rows, column, direction) {
        return rows.sort((a, b) => {
            let aVal, bVal;

            switch (column) {
                case 'title':
                    aVal = a.querySelector('.movie-title').textContent.trim();
                    bVal = b.querySelector('.movie-title').textContent.trim();
                    break;
                    
                case 'rating':
                    aVal = parseFloat(a.querySelector('.movie-rating').textContent.trim()) || 0;
                    bVal = parseFloat(b.querySelector('.movie-rating').textContent.trim()) || 0;
                    break;
                    
                case 'popularity':
                    aVal = this.parsePopularity(a.querySelector('.movie-popularity').textContent.trim());
                    bVal = this.parsePopularity(b.querySelector('.movie-popularity').textContent.trim());
                    break;
                    
                default:
                    return 0;
            }

            if (typeof aVal === 'string') {
                aVal = aVal.toLowerCase();
                bVal = bVal.toLowerCase();
            }

            let result = 0;
            if (aVal < bVal) result = -1;
            if (aVal > bVal) result = 1;

            return direction === 'desc' ? -result : result;
        });
    }

    parsePopularity(popularityText) {
        // Parse popularity text like "1,234,567" or "N/A"
        if (popularityText === 'N/A' || !popularityText) return 0;
        return parseInt(popularityText.replace(/,/g, '')) || 0;
    }

    // ===============================
    // TABLE EFFECTS
    // ===============================

    setupTableEffects() {
        const table = document.querySelector('.movies-table');
        if (!table) return;

        // Add row hover effects
        const rows = table.querySelectorAll('tbody tr');
        rows.forEach((row, index) => {
            row.addEventListener('mouseenter', () => {
                this.highlightRow(row, true);
            });

            row.addEventListener('mouseleave', () => {
                this.highlightRow(row, false);
            });

            // Add click effect
            row.addEventListener('click', () => {
                this.selectRow(row);
            });
        });
    }

    highlightRow(row, highlight) {
        if (highlight) {
            row.style.transform = 'translateX(12px) scale(1.02)';
            row.style.boxShadow = 'inset 6px 0 0 #9d4edd, 0 4px 20px rgba(157, 78, 221, 0.4)';
            row.style.background = 'rgba(157, 78, 221, 0.15)';
        } else {
            row.style.transform = '';
            row.style.boxShadow = '';
            row.style.background = '';
        }
    }

    selectRow(row) {
        // Add pulse effect
        row.style.animation = 'pulse 0.3s ease';
        setTimeout(() => {
            row.style.animation = '';
        }, 300);

        // Show movie title in toast
        const title = row.querySelector('.movie-title').textContent;
        this.showToast(`Selected: ${title}`, 'info', 2000);
    }

    // ===============================
    // ANIMATIONS & INTERACTIONS
    // ===============================

    addEntranceAnimations() {
        // Add staggered animation to form elements
        const formGroups = document.querySelectorAll('.form-group');
        formGroups.forEach((group, index) => {
            group.style.animationDelay = `${0.1 + index * 0.1}s`;
            group.classList.add('fade-in');
        });

        // Add animation to buttons
        const buttons = document.querySelectorAll('.btn');
        buttons.forEach((button, index) => {
            button.style.animationDelay = `${0.3 + index * 0.1}s`;
            button.classList.add('fade-in');
        });
    }

    initializeInteractions() {
        // Add particle effect on button hover
        const buttons = document.querySelectorAll('.btn-primary');
        buttons.forEach(button => {
            button.addEventListener('mouseenter', () => {
                this.createParticleEffect(button);
            });
        });

        // Add form validation feedback
        const selects = document.querySelectorAll('.form-select');
        selects.forEach(select => {
            select.addEventListener('change', () => {
                this.validateFormField(select);
            });
        });

        // Add smooth scroll behavior
        const links = document.querySelectorAll('a[href^="#"]');
        links.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const target = document.querySelector(link.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth' });
                }
            });
        });
    }

    // ===============================
    // SHARE FUNCTIONALITY
    // ===============================

    async shareResults(title, text, url) {
        // Try native share API first
        if (navigator.share) {
            try {
                await navigator.share({
                    title: title,
                    text: text,
                    url: url
                });
                this.showToast('Shared successfully!', 'success');
                return;
            } catch (err) {
                if (err.name !== 'AbortError') {
                    console.log('Share failed:', err);
                }
            }
        }

        // Fallback: Copy to clipboard
        this.copyToClipboard(url);
    }

    async copyToClipboard(text) {
        try {
            await navigator.clipboard.writeText(text);
            this.showToast('Link copied to clipboard! 📋', 'success');
        } catch (err) {
            // Fallback for older browsers
            const textArea = document.createElement('textarea');
            textArea.value = text;
            textArea.style.position = 'fixed';
            textArea.style.left = '-999999px';
            document.body.appendChild(textArea);
            textArea.select();
            try {
                document.execCommand('copy');
                this.showToast('Link copied to clipboard! 📋', 'success');
            } catch (err) {
                this.showToast('Failed to copy link', 'error');
            }
            document.body.removeChild(textArea);
        }
    }

    openSocialShare(platform, url, text) {
        let shareUrl = '';
        const encodedUrl = encodeURIComponent(url);
        const encodedText = encodeURIComponent(text);

        switch (platform) {
            case 'twitter':
                shareUrl = `https://twitter.com/intent/tweet?url=${encodedUrl}&text=${encodedText}`;
                break;
            case 'facebook':
                shareUrl = `https://www.facebook.com/sharer/sharer.php?u=${encodedUrl}`;
                break;
            case 'whatsapp':
                shareUrl = `https://wa.me/?text=${encodedText}%20${encodedUrl}`;
                break;
            case 'linkedin':
                shareUrl = `https://www.linkedin.com/sharing/share-offsite/?url=${encodedUrl}`;
                break;
            case 'telegram':
                shareUrl = `https://t.me/share/url?url=${encodedUrl}&text=${encodedText}`;
                break;
        }

        if (shareUrl) {
            window.open(shareUrl, '_blank', 'width=600,height=400');
        }
    }

    createParticleEffect(element) {
        const rect = element.getBoundingClientRect();
        const particles = 6;

        for (let i = 0; i < particles; i++) {
            const particle = document.createElement('div');
            particle.style.cssText = `
                position: fixed;
                width: 4px;
                height: 4px;
                background: linear-gradient(45deg, #9d4edd, #c44569);
                border-radius: 50%;
                pointer-events: none;
                z-index: 1000;
                left: ${rect.left + rect.width / 2}px;
                top: ${rect.top + rect.height / 2}px;
                animation: particle-float 1s ease-out forwards;
                box-shadow: 0 0 10px rgba(157, 78, 221, 0.6);
            `;

            document.body.appendChild(particle);

            // Random direction
            const angle = (Math.PI * 2 * i) / particles;
            const velocity = 50 + Math.random() * 50;
            
            particle.style.setProperty('--dx', Math.cos(angle) * velocity + 'px');
            particle.style.setProperty('--dy', Math.sin(angle) * velocity + 'px');

            setTimeout(() => particle.remove(), 1000);
        }
    }

    validateFormField(field) {
        const isValid = field.value !== '';
        
        if (isValid) {
            field.style.borderColor = 'rgba(129, 255, 184, 0.5)';
            field.style.boxShadow = '0 0 0 3px rgba(129, 255, 184, 0.2), 0 4px 20px rgba(129, 255, 184, 0.1)';
        } else {
            field.style.borderColor = 'rgba(157, 78, 221, 0.5)';
            field.style.boxShadow = '0 0 0 3px rgba(157, 78, 221, 0.3), 0 4px 20px rgba(157, 78, 221, 0.2)';
        }

        setTimeout(() => {
            field.style.borderColor = '';
            field.style.boxShadow = '';
        }, 2000);
    }

    // ===============================
    // UTILITY METHODS
    // ===============================

    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    throttle(func, limit) {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }
}

// ===============================
// PARTICLE ANIMATION CSS
// ===============================

const particleCSS = `
@keyframes particle-float {
    0% {
        opacity: 1;
        transform: translate(0, 0) scale(0);
    }
    50% {
        opacity: 0.8;
        transform: translate(calc(var(--dx) * 0.5), calc(var(--dy) * 0.5)) scale(1);
    }
    100% {
        opacity: 0;
        transform: translate(var(--dx), var(--dy)) scale(0);
    }
}
`;

// Inject particle CSS
const style = document.createElement('style');
style.textContent = particleCSS;
document.head.appendChild(style);

// ===============================
// INITIALIZATION
// ===============================

// Initialize the UI when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.movieUI = new MovieRecommendationUI();
    
    // Hide loading overlay on page load
    setTimeout(() => {
        if (window.movieUI.loadingOverlay) {
            window.movieUI.hideLoading();
        }
    }, 500);
    
    // Show welcome message
    setTimeout(() => {
        if (document.querySelector('.hero-section')) {
            window.movieUI.showToast('Welcome to CineAI! Select your mood and language to get started.', 'info', 3000);
        }
    }, 1000);

    // Share dropdown functionality
    const shareButton = document.getElementById('shareButton');
    const shareMenu = document.getElementById('shareMenu');
    
    if (shareButton && shareMenu) {
        shareButton.addEventListener('click', (e) => {
            e.stopPropagation();
            shareMenu.classList.toggle('active');
        });

        // Close dropdown when clicking outside
        document.addEventListener('click', (e) => {
            if (!shareButton.contains(e.target) && !shareMenu.contains(e.target)) {
                shareMenu.classList.remove('active');
            }
        });

        // Close dropdown after selecting an option
        const shareOptions = shareMenu.querySelectorAll('.share-option');
        shareOptions.forEach(option => {
            option.addEventListener('click', () => {
                setTimeout(() => {
                    shareMenu.classList.remove('active');
                }, 300);
            });
        });
    }
});

// Handle page visibility changes
document.addEventListener('visibilitychange', () => {
    if (document.visibilityState === 'visible') {
        // Re-trigger animations when page becomes visible
        const animatedElements = document.querySelectorAll('.fade-in, .slide-in-up, .slide-in-left');
        animatedElements.forEach(el => {
            el.style.animation = 'none';
            el.offsetHeight; // Trigger reflow
            el.style.animation = null;
        });
    }
});

// Add keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Escape key to close loading overlay
    if (e.key === 'Escape' && window.movieUI.loadingOverlay.classList.contains('active')) {
        window.movieUI.hideLoading();
    }
    
    // Ctrl/Cmd + R to refresh recommendations
    if ((e.ctrlKey || e.metaKey) && e.key === 'r') {
        const form = document.querySelector('.recommendation-form form');
        if (form && document.querySelector('.results-section')) {
            e.preventDefault();
            form.submit();
        }
    }
});

// Export for global access
window.MovieRecommendationUI = MovieRecommendationUI;