/* Enhanced Documentation JavaScript for QoL Features */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all QoL features
    initThemeToggle();
    initEnhancedSearch();
    initCopyButtons();
    initTableOfContents();
    initCollapsibleSections();
    initBreadcrumbs();
    initEditOnGithub();
    initRelatedSections();
    initScrollSpy();
});

// Theme Toggle Functionality
function initThemeToggle() {
    const toggleButton = document.createElement('button');
    toggleButton.className = 'theme-toggle';
    toggleButton.innerHTML = '🌙';
    toggleButton.title = 'Toggle Dark/Light Theme';
    document.body.appendChild(toggleButton);

    // Load saved theme
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
    updateThemeIcon(savedTheme);

    toggleButton.addEventListener('click', function() {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        
        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        updateThemeIcon(newTheme);
    });

    function updateThemeIcon(theme) {
        toggleButton.innerHTML = theme === 'dark' ? '☀️' : '🌙';
    }
}

// Enhanced Search with Filters and Suggestions
function initEnhancedSearch() {
    const searchContainer = document.querySelector('.search') || document.querySelector('#searchbox');
    if (!searchContainer) return;

    // Create enhanced search structure
    const enhancedSearch = document.createElement('div');
    enhancedSearch.className = 'enhanced-search';
    
    enhancedSearch.innerHTML = `
        <div class="search-container">
            <div style="position: relative;">
                <input type="text" class="search-input" placeholder="Search documentation..." id="enhanced-search-input">
                <div class="search-suggestions" id="search-suggestions"></div>
            </div>
            <div class="search-filters">
                <button class="search-filter active" data-filter="all">All</button>
                <button class="search-filter" data-filter="classes">Classes</button>
                <button class="search-filter" data-filter="functions">Functions</button>
                <button class="search-filter" data-filter="modules">Modules</button>
                <button class="search-filter" data-filter="examples">Examples</button>
            </div>
        </div>
    `;

    searchContainer.appendChild(enhancedSearch);

    // Search functionality
    const searchInput = document.getElementById('enhanced-search-input');
    const suggestions = document.getElementById('search-suggestions');
    const filters = document.querySelectorAll('.search-filter');
    
    let searchIndex = [];
    buildSearchIndex();

    searchInput.addEventListener('input', debounce(handleSearch, 300));
    searchInput.addEventListener('focus', handleFocus);
    document.addEventListener('click', handleClickOutside);
    
    filters.forEach(filter => {
        filter.addEventListener('click', function() {
            filters.forEach(f => f.classList.remove('active'));
            this.classList.add('active');
            if (searchInput.value.trim()) {
                handleSearch();
            }
        });
    });

    function buildSearchIndex() {
        // Build search index from page content
        const elements = document.querySelectorAll('h1, h2, h3, h4, .class, .function, .method, dt');
        elements.forEach(el => {
            const text = el.textContent.trim();
            const link = el.id ? '#' + el.id : getElementLink(el);
            const type = getElementType(el);
            
            if (text && link) {
                searchIndex.push({
                    text: text,
                    link: link,
                    type: type,
                    element: el
                });
            }
        });
    }

    function handleSearch() {
        const query = searchInput.value.toLowerCase().trim();
        const activeFilter = document.querySelector('.search-filter.active').dataset.filter;
        
        if (query.length < 2) {
            suggestions.style.display = 'none';
            return;
        }

        const results = searchIndex.filter(item => {
            const matchesQuery = item.text.toLowerCase().includes(query);
            const matchesFilter = activeFilter === 'all' || item.type === activeFilter;
            return matchesQuery && matchesFilter;
        }).slice(0, 10);

        displaySuggestions(results, query);
    }

    function displaySuggestions(results, query) {
        if (results.length === 0) {
            suggestions.style.display = 'none';
            return;
        }

        suggestions.innerHTML = results.map(result => `
            <div class="search-suggestion" onclick="navigateToResult('${result.link}')">
                <strong>${highlightMatch(result.text, query)}</strong>
                <small style="display: block; color: var(--accent-color);">${result.type}</small>
            </div>
        `).join('');

        suggestions.style.display = 'block';
    }

    function highlightMatch(text, query) {
        const regex = new RegExp(`(${escapeRegex(query)})`, 'gi');
        return text.replace(regex, '<mark>$1</mark>');
    }

    function handleFocus() {
        if (searchInput.value.trim().length >= 2) {
            suggestions.style.display = 'block';
        }
    }

    function handleClickOutside(e) {
        if (!enhancedSearch.contains(e.target)) {
            suggestions.style.display = 'none';
        }
    }

    function getElementType(el) {
        if (el.classList.contains('class')) return 'classes';
        if (el.classList.contains('function') || el.classList.contains('method')) return 'functions';
        if (el.tagName.startsWith('H')) return 'modules';
        return 'all';
    }

    function getElementLink(el) {
        let current = el;
        while (current && !current.id) {
            current = current.parentElement;
        }
        return current ? '#' + current.id : '';
    }
}

function navigateToResult(link) {
    document.getElementById('search-suggestions').style.display = 'none';
    if (link.startsWith('#')) {
        document.querySelector(link)?.scrollIntoView({ behavior: 'smooth' });
    } else {
        window.location.href = link;
    }
}

// Copy to Clipboard Buttons
function initCopyButtons() {
    const codeBlocks = document.querySelectorAll('.highlight pre, .codehilite pre');
    
    codeBlocks.forEach(block => {
        const wrapper = block.closest('.highlight, .codehilite');
        if (!wrapper) return;
        
        const button = document.createElement('button');
        button.className = 'copy-button';
        button.textContent = 'Copy';
        button.title = 'Copy to clipboard';
        
        wrapper.style.position = 'relative';
        wrapper.appendChild(button);
        
        button.addEventListener('click', function() {
            const code = block.textContent;
            navigator.clipboard.writeText(code).then(function() {
                button.textContent = 'Copied!';
                button.classList.add('copied');
                setTimeout(function() {
                    button.textContent = 'Copy';
                    button.classList.remove('copied');
                }, 2000);
            }).catch(function() {
                // Fallback for older browsers
                const textArea = document.createElement('textarea');
                textArea.value = code;
                document.body.appendChild(textArea);
                textArea.select();
                document.execCommand('copy');
                document.body.removeChild(textArea);
                
                button.textContent = 'Copied!';
                button.classList.add('copied');
                setTimeout(function() {
                    button.textContent = 'Copy';
                    button.classList.remove('copied');
                }, 2000);
            });
        });
    });
}

// Interactive Table of Contents
function initTableOfContents() {
    const headings = document.querySelectorAll('h1, h2, h3, h4');
    if (headings.length < 3) return; // Only show TOC if there are enough headings
    
    const tocContainer = document.createElement('div');
    tocContainer.className = 'toc-container';
    tocContainer.id = 'toc-container';
    
    const tocToggle = document.createElement('button');
    tocToggle.className = 'toc-toggle';
    tocToggle.textContent = 'TOC';
    tocToggle.title = 'Toggle Table of Contents';
    
    document.body.appendChild(tocToggle);
    document.body.appendChild(tocContainer);
    
    // Build TOC
    let tocHTML = '<h3>Table of Contents</h3><ul>';
    headings.forEach(heading => {
        if (!heading.id) {
            heading.id = heading.textContent.toLowerCase().replace(/[^\\w\\s]/gi, '').replace(/\\s+/g, '-');
        }
        
        const level = parseInt(heading.tagName.substring(1));
        const indent = level > 2 ? 'style="margin-left: ' + ((level - 2) * 15) + 'px;"' : '';
        
        tocHTML += `<li ${indent}><a href="#${heading.id}" class="toc-link">${heading.textContent}</a></li>`;
    });
    tocHTML += '</ul>';
    
    tocContainer.innerHTML = tocHTML;
    
    // Toggle functionality
    tocToggle.addEventListener('click', function() {
        const isVisible = tocContainer.style.display === 'block';
        tocContainer.style.display = isVisible ? 'none' : 'block';
        tocToggle.textContent = isVisible ? 'TOC' : 'Hide';
    });
    
    // Smooth scrolling for TOC links
    const tocLinks = tocContainer.querySelectorAll('.toc-link');
    tocLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            const target = document.getElementById(targetId);
            if (target) {
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
}

// Collapsible Sections
function initCollapsibleSections() {
    const sections = document.querySelectorAll('.section');
    
    sections.forEach(section => {
        const heading = section.querySelector('h2, h3, h4');
        if (!heading || section.classList.contains('no-collapse')) return;
        
        const button = document.createElement('button');
        button.className = 'collapsible';
        button.textContent = heading.textContent;
        
        const content = document.createElement('div');
        content.className = 'collapsible-content';
        
        // Move all content after heading into collapsible container
        let nextSibling = heading.nextElementSibling;
        while (nextSibling && !nextSibling.matches('h1, h2, h3, h4')) {
            const current = nextSibling;
            nextSibling = nextSibling.nextElementSibling;
            content.appendChild(current);
        }
        
        heading.parentNode.insertBefore(button, heading);
        heading.parentNode.insertBefore(content, heading.nextSibling);
        heading.style.display = 'none';
        
        // Initially expanded
        content.style.maxHeight = content.scrollHeight + 'px';
        button.classList.add('active');
        
        button.addEventListener('click', function() {
            this.classList.toggle('active');
            if (content.style.maxHeight === '0px' || !content.style.maxHeight) {
                content.style.maxHeight = content.scrollHeight + 'px';
            } else {
                content.style.maxHeight = '0px';
            }
        });
    });
}

// Breadcrumb Navigation
function initBreadcrumbs() {
    const main = document.querySelector('main, .document, .body');
    if (!main) return;
    
    const breadcrumb = document.createElement('nav');
    breadcrumb.className = 'breadcrumb';
    
    const pathParts = window.location.pathname.split('/').filter(part => part);
    const breadcrumbItems = ['<a href="/">Home</a>'];
    
    let currentPath = '';
    pathParts.forEach((part, index) => {
        currentPath += '/' + part;
        const isLast = index === pathParts.length - 1;
        const displayName = part.replace(/[-_]/g, ' ').replace(/\\b\\w/g, l => l.toUpperCase());
        
        if (isLast) {
            breadcrumbItems.push(`<span>${displayName}</span>`);
        } else {
            breadcrumbItems.push(`<a href="${currentPath}">${displayName}</a>`);
        }
    });
    
    breadcrumb.innerHTML = breadcrumbItems.join('<span class="breadcrumb-separator">›</span>');
    main.insertBefore(breadcrumb, main.firstChild);
}

// Edit on GitHub Integration
function initEditOnGithub() {
    const main = document.querySelector('main, .document, .body');
    if (!main) return;
    
    const currentPath = window.location.pathname;
    const githubUrl = `https://github.com/eytangut/manim/edit/main/docs${currentPath.endsWith('/') ? currentPath + 'index.rst' : currentPath + '.rst'}`;
    
    const editLink = document.createElement('a');
    editLink.className = 'edit-github';
    editLink.href = githubUrl;
    editLink.target = '_blank';
    editLink.innerHTML = '📝 Edit on GitHub';
    
    main.appendChild(editLink);
}

// Related/See Also Sections
function initRelatedSections() {
    const functions = document.querySelectorAll('.function, .method, .class');
    
    functions.forEach(func => {
        const funcName = func.querySelector('dt')?.textContent || '';
        const related = findRelatedItems(funcName);
        
        if (related.length > 0) {
            const relatedSection = document.createElement('div');
            relatedSection.className = 'related-section';
            relatedSection.innerHTML = `
                <h4>See Also</h4>
                <div class="related-links">
                    ${related.map(item => `<a href="${item.link}" class="related-link">${item.name}</a>`).join('')}
                </div>
            `;
            
            func.appendChild(relatedSection);
        }
    });
}

function findRelatedItems(itemName) {
    // Simple related item finding based on naming patterns
    const related = [];
    const allItems = document.querySelectorAll('.function dt, .method dt, .class dt');
    
    allItems.forEach(item => {
        const name = item.textContent;
        if (name !== itemName && isRelated(itemName, name)) {
            const link = item.id ? '#' + item.id : getElementLink(item);
            if (link) {
                related.push({ name: name, link: link });
            }
        }
    });
    
    return related.slice(0, 5); // Limit to 5 related items
}

function isRelated(name1, name2) {
    // Simple heuristic for finding related items
    const base1 = name1.replace(/[^a-zA-Z]/g, '').toLowerCase();
    const base2 = name2.replace(/[^a-zA-Z]/g, '').toLowerCase();
    
    // Check for common prefixes or shared words
    const words1 = base1.split(/(?=[A-Z])/).filter(w => w.length > 2);
    const words2 = base2.split(/(?=[A-Z])/).filter(w => w.length > 2);
    
    return words1.some(w1 => words2.some(w2 => w1.includes(w2) || w2.includes(w1)));
}

// Scroll Spy for Navigation
function initScrollSpy() {
    const tocLinks = document.querySelectorAll('.toc-link');
    if (tocLinks.length === 0) return;
    
    const headings = Array.from(document.querySelectorAll('h1, h2, h3, h4')).filter(h => h.id);
    
    function updateActiveSection() {
        const scrollTop = window.pageYOffset;
        const windowHeight = window.innerHeight;
        
        let activeHeading = null;
        
        for (let i = headings.length - 1; i >= 0; i--) {
            const heading = headings[i];
            const rect = heading.getBoundingClientRect();
            
            if (rect.top <= windowHeight * 0.3) {
                activeHeading = heading;
                break;
            }
        }
        
        // Update TOC active states
        tocLinks.forEach(link => {
            link.classList.remove('active');
            if (activeHeading && link.getAttribute('href') === '#' + activeHeading.id) {
                link.classList.add('active');
            }
        });
    }
    
    window.addEventListener('scroll', debounce(updateActiveSection, 100));
    updateActiveSection(); // Initial call
}

// Utility Functions
function debounce(func, wait) {
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

function escapeRegex(string) {
    return string.replace(/[.*+?^${}()|[\\]\\\\]/g, '\\\\$&');
}

// Auto-save user preferences
function saveUserPreferences() {
    const prefs = {
        theme: document.documentElement.getAttribute('data-theme'),
        tocVisible: document.getElementById('toc-container')?.style.display === 'block'
    };
    localStorage.setItem('docPreferences', JSON.stringify(prefs));
}

function loadUserPreferences() {
    const prefs = JSON.parse(localStorage.getItem('docPreferences') || '{}');
    
    if (prefs.theme) {
        document.documentElement.setAttribute('data-theme', prefs.theme);
    }
    
    if (prefs.tocVisible && document.getElementById('toc-container')) {
        document.getElementById('toc-container').style.display = 'block';
        document.querySelector('.toc-toggle').textContent = 'Hide';
    }
}

// Save preferences on page unload
window.addEventListener('beforeunload', saveUserPreferences);

// Load preferences on page load
document.addEventListener('DOMContentLoaded', loadUserPreferences);