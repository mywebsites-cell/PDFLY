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

// -------- Block ad network redirects and pop-ups --------
(function() {
  // Prevent ads from redirecting users away from the page and block overlay pop-ups
  
  const blockedDomains = [
    'highperformanceformat.com',
    'ads.google.com',
    'googleads.com',
    'doubleclick.net',
    'adnxs.com'
  ];
  
  // Monitor and block pop-ups/overlays
  const originalOpen = window.open;
  window.open = function(url, name, specs) {
    console.log('Blocked pop-up attempt:', url);
    return null;
  };
  
  // Block overlay creation
  const originalCreateElement = document.createElement;
  document.createElement = function(tagName) {
    const element = originalCreateElement.call(document, tagName);
    
    // Intercept before appendChild to block full-screen overlays
    const originalAppendChild = element.appendChild;
    element.appendChild = function(child) {
      if (child && (child.style?.position === 'fixed' || child.style?.position === 'absolute')) {
        // Check if it looks like an overlay
        if ((child.style?.zIndex > 9000) || (child.style?.width === '100%' && child.style?.height === '100%')) {
          console.log('Blocked overlay element');
          return child;
        }
      }
      return originalAppendChild.call(this, child);
    };
    
    return element;
  };
  
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

// -------- Inject Help & Tips on tool pages (SEO-friendly) --------
(function() {
  // Skip home and simple info pages
  const path = (window.location.pathname || '').toLowerCase();
  const isHome = path === '/' || path === '/home' || path.endsWith('/index.html');
  const infoPages = ['/about', '/contact', '/privacy'];
  if (isHome || infoPages.some(p => path.includes(p))) return;

  // Map of tips per tool (fallback to generic)
  const tipsMap = {
    'word-to-pdf': [
      'Upload DOCX, DOC, RTF or ODT (up to 200MB).',
      'Best fidelity with DOCX; preserves layout, fonts and images.',
      'Server-side conversion; files are auto-deleted after processing.'
    ],
    'pdf-to-word': [
      'Works best for digitally-created PDFs (not photos of documents).',
      'For scans, use OCR first to improve text extraction quality.',
      'Keep complex PDFs under 200MB for faster conversion.'
    ],
    'image-to-pdf': [
      'Add multiple JPG/PNG images; drag to reorder before saving.',
      'For print-quality, start with high-resolution images.',
      'All processing happens client-side in your browser.'
    ],
    'pdf-to-image': [
      'Export pages as PNG; higher DPI yields sharper results.',
      'Ideal for sharing page previews or thumbnails.',
      'Large PDFs may take longer; be patient during processing.'
    ],
    'merge-pdf': [
      'Drag and drop files; reorder before merging.',
      'Merging is client-side—your PDFs stay on your device.',
      'Use clear filenames to keep track after merge.'
    ],
    'split-pdf': [
      'Split all pages or select ranges (e.g., 1-3,5,7-9).',
      'Client-side processing; no uploads required.',
      'Great for extracting just the pages you need.'
    ],
    'compress-pdf': [
      'Best for image-heavy PDFs—adjust quality for smaller size.',
      'Try medium quality first; balance size and readability.',
      'Preview output to ensure text remains legible.'
    ],
    'rotate-pdf': [
      'Rotate pages by 90/180/270 degrees as needed.',
      'Process locally in your browser; privacy-friendly.',
      'Save the rotated version to keep changes.'
    ],
    'reorder-pages': [
      'Drag and drop to change page order.',
      'Use keyboard for fine control if supported.',
      'Export the new sequence when done.'
    ],
    'lock-pdf': [
      'Add a password to restrict opening the PDF.',
      'Use strong passwords; store them safely.',
      'Server-side operation; files are auto-deleted.'
    ],
    'unlock-pdf': [
      'Remove password protection from PDFs you own.',
      'Only use with documents you have the right to modify.',
      'Server-side operation; files are auto-deleted.'
    ],
    'excel-to-pdf': [
      'Upload XLSX/XLS; preserves tables and formatting.',
      'Check page breaks in Excel for ideal PDF layout.',
      'Use landscape orientation for wide sheets.'
    ],
    'extract-images': [
      'Extract embedded images from your PDF as PNG files.',
      'Ideal for reusing graphics or figures.',
      'Large PDFs may take longer to process.'
    ],
    'add-page-numbers': [
      'Add page numbers to header or footer positions.',
      'Choose start number and style (e.g., 1, 1/10).',
      'Review placement to avoid overlapping content.'
    ],
    'add-watermark': [
      'Apply text watermark at chosen position and opacity.',
      'Use light opacity for readability; avoid covering content.',
      'Preview before saving to confirm placement.'
    ],
    'qr-code-pdf': [
      'Generate QR codes and export to PDF for printing.',
      'Use high contrast for reliable scanning.',
      'Test with a phone camera before distribution.'
    ]
  };

  function getToolKey() {
    // Normalize pathname to match keys regardless of .html or clean URL
    const keys = Object.keys(tipsMap);
    for (const key of keys) {
      if (path.includes(key)) return key;
    }
    return null;
  }

  function buildTipsSection(toolKey) {
    const section = document.createElement('section');
    section.className = 'help';
    const h2 = document.createElement('h2');
    h2.textContent = 'Help & Tips';
    const ul = document.createElement('ul');

    const tips = tipsMap[toolKey] || [
      'Fast, private tools—client-side where possible.',
      'Server tasks auto-delete files after processing.',
      'Use clear filenames and reasonable sizes for best results.'
    ];

    tips.forEach(text => {
      const li = document.createElement('li');
      const strong = document.createElement('strong');
      // Add a short label where helpful
      strong.textContent = '';
      li.appendChild(document.createTextNode(text));
      ul.appendChild(li);
    });

    section.appendChild(h2);
    section.appendChild(ul);
    return section;
  }

  function injectTips() {
    const toolKey = getToolKey();
    if (!toolKey) return; // unknown page; skip

    // Prevent duplicate injection
    if (document.querySelector('section.help')) return;

    const section = buildTipsSection(toolKey);

    // Prefer placing above bottom banner ad inside ad-content if present
    const adContent = document.querySelector('.ad-content') || document.querySelector('main.container');
    const bottomAd = document.querySelector('.ad-bottom-banner');
    if (bottomAd && bottomAd.parentElement) {
      bottomAd.parentElement.insertBefore(section, bottomAd);
    } else if (adContent) {
      adContent.appendChild(section);
    } else {
      document.body.appendChild(section);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', injectTips);
  } else {
    injectTips();
  }
})();