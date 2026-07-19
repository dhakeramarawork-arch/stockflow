/* ============================================================
   StockFlow — Main JavaScript
   ============================================================ */

// Sidebar toggle for both mobile and desktop
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebarOverlay');
    
    // For mobile and tablet
    if (window.innerWidth < 992) {
        if (sidebar) sidebar.classList.toggle('show');
        if (overlay) overlay.classList.toggle('show');
    } 
    // For desktop (collapse/expand)
    else {
        document.body.classList.toggle('sidebar-collapsed');
    }
}

// Auto-dismiss toasts after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.toast').forEach(toast => {
        setTimeout(() => {
            const bs = bootstrap.Toast.getOrCreateInstance(toast);
            bs.hide();
        }, 5000);
    });

    // Add loading spinner to form submissions
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function() {
            if (this.checkValidity()) {
                showSpinner();
            }
        });
    });
});

// Loading spinner helpers
function showSpinner() {
    let overlay = document.querySelector('.spinner-overlay');
    if (!overlay) {
        overlay = document.createElement('div');
        overlay.className = 'spinner-overlay';
        overlay.innerHTML = '<div class="spinner-border text-primary" style="width:3rem;height:3rem;" role="status"></div>';
        document.body.appendChild(overlay);
    }
    overlay.classList.add('show');
}

// ... keep existing code ...

// Scroll reveal animations
window.addEventListener('scroll', function() {
    // Navbar background change
    const nav = document.getElementById('mainNav');
    if (nav) {
        if (window.scrollY > 50) {
            nav.classList.add('scrolled');
        } else {
            nav.classList.remove('scrolled');
        }
    }
    
    // Reveal elements on scroll
    const reveals = document.querySelectorAll('.reveal');
    reveals.forEach(element => {
        const elementTop = element.getBoundingClientRect().top;
        const elementVisible = 150;
        if (elementTop < window.innerHeight - elementVisible) {
            element.classList.add('active');
        }
    });
});

// Trigger initial reveal on load
window.addEventListener('load', function() {
    const reveals = document.querySelectorAll('.reveal');
    reveals.forEach(element => {
        const elementTop = element.getBoundingClientRect().top;
        const elementVisible = 150;
        if (elementTop < window.innerHeight - elementVisible) {
            element.classList.add('active');
        }
    });
});

function hideSpinner() {
    const overlay = document.querySelector('.spinner-overlay');
    if (overlay) overlay.classList.remove('show');
}