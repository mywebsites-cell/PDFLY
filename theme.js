// theme.js - Theme toggle functionality & Mobile menu
(function() {
  const themeToggle = document.getElementById('themeToggle');
  
  // Load saved theme
  const savedTheme = localStorage.getItem('theme') || 'light';
  document.documentElement.setAttribute('data-theme', savedTheme);
  
  if (themeToggle) {
    themeToggle.textContent = savedTheme === 'dark' ? '☀️' : '🌙';
    
    themeToggle.addEventListener('click', function() {
      const currentTheme = document.documentElement.getAttribute('data-theme');
      const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
      
      document.documentElement.setAttribute('data-theme', newTheme);
      localStorage.setItem('theme', newTheme);
      themeToggle.textContent = newTheme === 'dark' ? '☀️' : '🌙';
    });
  }

  // Mobile Menu Toggle
  const mobileMenuToggle = document.getElementById('mobileMenuToggle');
  const mainNav = document.querySelector('.main-nav');
  
  if (mobileMenuToggle && mainNav) {
    mobileMenuToggle.addEventListener('click', function() {
      mainNav.classList.toggle('active');
      const isActive = mainNav.classList.contains('active');
      mobileMenuToggle.textContent = isActive ? '✕' : '⋮';
    });

    // Handle dropdown clicks in mobile menu
    const dropdowns = mainNav.querySelectorAll('.dropdown');
    dropdowns.forEach(dropdown => {
      const dropbtn = dropdown.querySelector('.dropbtn');
      const dropdownContent = dropdown.querySelector('.dropdown-content');
      
      if (dropbtn && dropdownContent) {
        dropbtn.addEventListener('click', function(e) {
          if (window.innerWidth <= 768) {
            e.preventDefault();
            dropdownContent.classList.toggle('active');
          }
        });
      }
    });

    // Close mobile menu when clicking outside
    document.addEventListener('click', function(e) {
      if (window.innerWidth <= 768) {
        if (!mainNav.contains(e.target) && !mobileMenuToggle.contains(e.target)) {
          mainNav.classList.remove('active');
          mobileMenuToggle.textContent = '⋮';
        }
      }
    });

    // Close mobile menu on window resize
    window.addEventListener('resize', function() {
      if (window.innerWidth > 768) {
        mainNav.classList.remove('active');
        mobileMenuToggle.textContent = '⋮';
      }
    });
  }

    // ------------------------------
    // Global download UI helpers
    // Provides `showDownloadButton({ containerSelector, filename, blobOrUrl, mime, text })`
    // and `removeDownloadButton()` on window so tools can show a download button after processing.
    // Works standalone (does not require `shared.js`).

    function triggerDownload(blobOrUrl, filename, mime) {
      // blobOrUrl may be a Blob/ArrayBuffer or a string URL
      if (!blobOrUrl) return;
      if (typeof blobOrUrl === 'string') {
        // remote URL
        const a = document.createElement('a');
        a.href = blobOrUrl;
        a.download = filename || '';
        document.body.appendChild(a);
        a.click();
        a.remove();
        return;
      }

      // assume Blob or ArrayBuffer
      const blob = blobOrUrl instanceof Blob ? blobOrUrl : new Blob([blobOrUrl], { type: mime || 'application/octet-stream' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = filename || 'download';
      document.body.appendChild(a);
      a.click();
      a.remove();
      setTimeout(() => URL.revokeObjectURL(url), 1500);
    }

    function showDownloadButton(opts) {
      opts = opts || {};
      const container = document.querySelector(opts.containerSelector || '.container') || document.body;

      // remove existing area if present
      removeDownloadButton();

      const area = document.createElement('div');
      area.className = 'download-area';
      area.id = 'globalDownloadArea';

      const btn = document.createElement('button');
      btn.className = 'btn';
      btn.type = 'button';
      btn.textContent = opts.text || 'Download';
      btn.addEventListener('click', function() {
        triggerDownload(opts.blobOrUrl, opts.filename || 'result.pdf', opts.mime || 'application/pdf');
      });

      area.appendChild(btn);

      if (opts.note) {
        const note = document.createElement('small');
        note.className = 'small-note';
        note.textContent = opts.note;
        area.appendChild(note);
      }

      // append after the main container for most tool pages; fallback to body
      container.appendChild(area);

      // return the element so caller can keep reference if needed
      return area;
    }

    function removeDownloadButton() {
      const prev = document.getElementById('globalDownloadArea');
      if (prev && prev.parentNode) prev.parentNode.removeChild(prev);
    }

    // expose globally
    window.showDownloadButton = showDownloadButton;
    window.removeDownloadButton = removeDownloadButton;
    window.triggerDownload = triggerDownload;
})();

// -------- AdSense loader (global) --------
(function() {
  const ADS_CLIENT = 'ca-pub-XXXXXXXXXXXX'; // replace with your AdSense client ID
  let adsScriptLoaded = false;

  function pushAds() {
    const slots = document.querySelectorAll('ins.adsbygoogle');
    slots.forEach(() => {
      try {
        (window.adsbygoogle = window.adsbygoogle || []).push({});
      } catch (e) {
        // ignore push errors
      }
    });
  }

  function loadAds() {
    if (!ADS_CLIENT || ADS_CLIENT.includes('XXXXXXXX')) return; // keep placeholder safe
    if (adsScriptLoaded) {
      pushAds();
      return;
    }
    const s = document.createElement('script');
    s.async = true;
    s.src = 'https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js';
    s.setAttribute('data-ad-client', ADS_CLIENT);
    s.onload = pushAds;
    document.head.appendChild(s);
    adsScriptLoaded = true;
  }

  document.addEventListener('DOMContentLoaded', loadAds);
})();

// -------- Warm-up Render backend to avoid cold start --------
(function() {
  // If frontend is on Vercel and backend on Render free tier,
  // ping the backend in the background so the first tool request is fast.
  const BACKEND_BASE = 'https://pdfly-7vu5.onrender.com';
  if (!BACKEND_BASE) return;
  window.addEventListener('load', function() {
    // Delay slightly to avoid blocking page paint
    setTimeout(() => {
      try {
        fetch(BACKEND_BASE + '/diagnostics', {
          method: 'GET',
          cache: 'no-store',
          mode: 'no-cors'
        }).catch(() => {});
      } catch (e) {}
    }, 500);
  });
})();

// -------- Block ad network redirects --------
(function() {
  // Prevent ads from redirecting users away from the page
  // Blocks redirects to ad networks and unwanted URLs
  
  const blockedDomains = [
    'highperformanceformat.com',
    'ads.google.com',
    'googleads.com',
    'doubleclick.net',
    'adnxs.com'
  ];
  
  // Monitor link clicks from ad containers
  document.addEventListener('click', function(e) {
    const target = e.target.closest('a');
    if (!target) return;
    
    const href = target.getAttribute('href') || '';
    const iframeParent = e.target.closest('iframe, [id*="ad"], [class*="ad"]');
    
    // If click originated from ad element and redirects to ad domain, prevent it
    if (iframeParent) {
      for (let domain of blockedDomains) {
        if (href.includes(domain)) {
          e.preventDefault();
          e.stopPropagation();
          console.log('Blocked ad redirect to:', href);
          return;
        }
      }
    }
  }, true);
  
  // Monitor window.location changes from ad scripts
  const originalSetLocation = Object.getOwnPropertyDescriptor(Window.prototype, 'location').set;
  Object.defineProperty(Window.prototype, 'location', {
    set: function(url) {
      const urlStr = String(url);
      for (let domain of blockedDomains) {
        if (urlStr.includes(domain)) {
          console.log('Blocked redirect to:', urlStr);
          return;
        }
      }
      originalSetLocation.call(this, url);
    },
    configurable: true
  });
})();