(function() {
    "use strict"; // Start of use strict
  
    var mainNav = document.querySelector('#mainNav');
  
    if (mainNav) {
  
      // Collapse Navbar
      var collapseNavbar = function() {
  
        var scrollTop = (window.pageYOffset !== undefined) ? window.pageYOffset : (document.documentElement || document.body.parentNode || document.body).scrollTop;
  
        if (scrollTop > 100) {
          mainNav.classList.add("navbar-shrink");
        } else {
          mainNav.classList.remove("navbar-shrink");
        }
      };
  
      // Collapse now if page is not at top
      collapseNavbar();
      // Collapse the navbar when page is scrolled
      document.addEventListener("scroll", collapseNavbar);
  
      // Close responsive menu when a scroll trigger link is clicked
      var navbarToggler = document.querySelector('.navbar-toggler');
      var responsiveNavItems = [].slice.call(
        document.querySelectorAll('#navcol-1 .nav-link')
      );
  
      responsiveNavItems.map(function(responsiveNavItem) {
        responsiveNavItem.addEventListener('click', function() {
          if (window.getComputedStyle(navbarToggler).display !== 'none') {
            navbarToggler.click();
          }
        });
      });
  
      // Highlight the active navigation link
      var currentPath = window.location.pathname;
      responsiveNavItems.forEach(function(navItem) {
        if (navItem.getAttribute('href') === currentPath) {
          navItem.classList.add('active');
        }
      });
    }
  
  })(); // End of use strict
  