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
    const BACKEND_BASE = 'https://pdfly-7vu5.onrender.com';
    if (!BACKEND_BASE) return;
    window.addEventListener('load', function() {
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
    const blockedDomains = [
      'highperformanceformat.com',
      'ads.google.com',
      'googleads.com',
      'doubleclick.net',
      'adnxs.com'
    ];

    const originalOpen = window.open;
    window.open = function(url, name, specs) {
      console.log('Blocked pop-up attempt:', url);
      return null;
    };

    const originalCreateElement = document.createElement;
    document.createElement = function(tagName) {
      const element = originalCreateElement.call(document, tagName);
      const originalAppendChild = element.appendChild;
      element.appendChild = function(child) {
        if (child && (child.style?.position === 'fixed' || child.style?.position === 'absolute')) {
          if ((child.style?.zIndex > 9000) || (child.style?.width === '100%' && child.style?.height === '100%')) {
            console.log('Blocked overlay element');
            return child;
          }
        }
        return originalAppendChild.call(this, child);
      };
      return element;
    };

    document.addEventListener('click', function(e) {
      const target = e.target.closest('a');
      if (!target) return;
      const href = target.getAttribute('href') || '';
      const iframeParent = e.target.closest('iframe, [id*="ad"], [class*="ad"]');
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

    const originalSetLocation = Object.getOwnPropertyDescriptor(Window.prototype, 'location')?.set;
    if (originalSetLocation) {
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
    }
  })();

  // -------- Inject Help & Tips on tool pages (SEO-friendly) --------
  (function() {
    const path = (window.location.pathname || '').toLowerCase();
    const isHome = path === '/' || path === '/home' || path.endsWith('/index.html');
    const infoPages = ['/about', '/contact', '/privacy'];
    if (isHome || infoPages.some(p => path.includes(p))) return;

    const tipsMap = {
      'word-to-pdf': [
        { label: 'Formats', text: 'Upload DOCX, DOC, RTF or ODT (≤200MB).' },
        { label: 'Fonts', text: 'Embed fonts in Word to preserve exact appearance in PDF.' },
        { label: 'Page Setup', text: 'Set page size/margins in Word (A4/Letter) before converting.' },
        { label: 'Images', text: 'Use high‑resolution images for print‑quality output.' },
        { label: 'Privacy', text: 'Server‑side conversion; files auto‑delete. ', link: { text: 'Privacy Policy', url: '/privacy' }, suffix: '.' }
      ],
      'pdf-to-word': [
        { label: 'Best Input', text: 'Digitally‑created PDFs convert better than photos/scans.' },
        { label: 'OCR', text: 'Run OCR on scanned PDFs to extract editable text.' },
        { label: 'Tables', text: 'Complex tables may need manual touch‑ups after conversion.' },
        { label: 'Fonts', text: 'Missing fonts can affect layout; install originals for fidelity.' },
        { label: 'Privacy', text: 'Files processed on server; auto‑deleted. ', link: { text: 'Learn more', url: '/privacy' }, suffix: '.' }
      ],
      'image-to-pdf': [
        { label: 'Multiple', text: 'Add JPG/PNG files; drag to reorder pages.' },
        { label: 'Fit', text: 'Choose fit/center options to control page padding.' },
        { label: 'Quality', text: 'Use high‑resolution images for crisp PDFs.' },
        { label: 'Order', text: 'Rename files or drag to keep desired sequence.' },
        { label: 'Privacy', text: 'Runs entirely client‑side in your browser.' }
      ],
      'pdf-to-image': [
        { label: 'DPI', text: 'Higher DPI yields sharper images; balance vs. file size.' },
        { label: 'Format', text: 'PNG for quality/transparency; JPG for smaller size.' },
        { label: 'Ranges', text: 'Export specific page ranges to save time.' },
        { label: 'Performance', text: 'Very large PDFs may render slowly—be patient.' },
        { label: 'Use', text: 'Ideal for previews, thumbnails, and sharing online.' }
      ],
      'merge-pdf': [
        { label: 'Reorder', text: 'Drag files to set merge order before combining.' },
        { label: 'Local', text: 'Merging is client‑side—files stay on your device.' },
        { label: 'Naming', text: 'Use clear filenames to track post‑merge content.' },
        { label: 'Size', text: 'Avoid merging extremely large files to keep outputs manageable.' },
        { label: 'Support', text: 'Questions? ', link: { text: 'Contact us', url: '/contact' }, suffix: '.' }
      ],
      'split-pdf': [
        { label: 'Modes', text: 'Split all pages or choose ranges (e.g., 1‑3,5,7‑9).' },
        { label: 'Local', text: 'Runs client‑side; no uploads required.' },
        { label: 'Targeted', text: 'Extract only the sections you need.' },
        { label: 'Naming', text: 'Name outputs clearly for quick identification.' },
        { label: 'Privacy', text: 'Client‑side processing keeps files local.' }
      ],
      'compress-pdf': [
        { label: 'Images', text: 'Compression helps most on image‑heavy PDFs.' },
        { label: 'Balance', text: 'Try medium quality for size vs. readability.' },
        { label: 'Preview', text: 'Check pages to ensure text remains legible.' },
        { label: 'Version', text: 'Newer PDF versions may compress more efficiently.' },
        { label: 'Limits', text: 'Text‑only PDFs often see minimal gains.' }
      ],
      'rotate-pdf': [
        { label: 'Angles', text: 'Rotate by 90/180/270 degrees as needed.' },
        { label: 'Pages', text: 'Apply rotation to selected pages or all pages.' },
        { label: 'Local', text: 'Edits occur in‑browser; nothing uploaded.' },
        { label: 'Save', text: 'Export the rotated version when finished.' },
        { label: 'Backup', text: 'Keep originals in case you need to revert.' }
      ],
      'reorder-pages': [
        { label: 'Drag', text: 'Drag thumbnails to change page order.' },
        { label: 'Zoom', text: 'Zoom in for precise identification of pages.' },
        { label: 'Groups', text: 'Reorder in batches for long documents.' },
        { label: 'Export', text: 'Save when done to apply the new sequence.' },
        { label: 'Local', text: 'Runs client‑side for speed and privacy.' }
      ],
      'lock-pdf': [
        { label: 'Passwords', text: 'Add a password to restrict opening.' },
        { label: 'Strength', text: 'Use strong, unique passwords; store safely.' },
        { label: 'Sharing', text: 'Share passwords securely—not via plain text.' },
        { label: 'Limits', text: 'Some viewers handle encryption differently; test outputs.' },
        { label: 'Privacy', text: 'Server‑side; files auto‑delete. ', link: { text: 'Privacy Policy', url: '/privacy' }, suffix: '.' }
      ],
      'unlock-pdf': [
        { label: 'Rights', text: 'Only unlock PDFs you are authorized to modify.' },
        { label: 'Limits', text: 'Strong encryption or policy locks may not be removable.' },
        { label: 'Legal', text: 'Respect licenses and terms when modifying PDFs.' },
        { label: 'Alternate', text: 'If unlock fails, try “Print to PDF” as a workaround.' },
        { label: 'Privacy', text: 'Server‑side; files auto‑delete. ', link: { text: 'Privacy Policy', url: '/privacy' }, suffix: '.' }
      ],
      'excel-to-pdf': [
        { label: 'Layouts', text: 'Preserves tables and formatting from XLSX/XLS.' },
        { label: 'Breaks', text: 'Set page breaks for ideal pagination.' },
        { label: 'Fit', text: 'Use “Fit to page” scaling for wide sheets.' },
        { label: 'Orientation', text: 'Landscape works better for wide tables.' },
        { label: 'Print Area', text: 'Define print area to include only desired cells.' }
      ],
      'extract-images': [
        { label: 'Output', text: 'Extract embedded images as PNG/JPG files.' },
        { label: 'DPI', text: 'Higher DPI yields better quality for reuse.' },
        { label: 'Reuse', text: 'Ideal for graphics, figures, and illustrations.' },
        { label: 'Performance', text: 'Large PDFs may take longer to process.' },
        { label: 'Naming', text: 'Outputs are numbered—rename for clarity.' }
      ],
      'add-page-numbers': [
        { label: 'Placement', text: 'Choose header or footer positions.' },
        { label: 'Formats', text: 'Styles like “1”, “1/10”, or “Page 1”.' },
        { label: 'Style', text: 'Set font size/color for readability.' },
        { label: 'Start', text: 'Start numbering at a specific page if needed.' },
        { label: 'Safety', text: 'Avoid overlapping content—preview before saving.' }
      ],
      'add-watermark': [
        { label: 'Opacity', text: 'Use light opacity to keep text readable.' },
        { label: 'Position', text: 'Center/diagonal placements are common.' },
        { label: 'Font', text: 'Choose clear, professional fonts for text marks.' },
        { label: 'Size', text: 'Scale watermark appropriately for page size.' },
        { label: 'Preview', text: 'Check placement before saving final PDF.' }
      ],
      'qr-code-pdf': [
        { label: 'Contrast', text: 'High contrast improves scan reliability.' },
        { label: 'Size', text: 'Use ≥2cm code size for printed materials.' },
        { label: 'Quiet Zone', text: 'Leave padding around the code for scanners.' },
        { label: 'Testing', text: 'Test with a phone camera before publishing.' },
        { label: 'Content', text: 'Store URLs, Wi‑Fi, contacts (vCard), or text.' }
      ]
    };

    function getToolKey() {
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

      const fallback = [
        { label: 'Privacy', text: 'Client-side where possible; server tasks auto-delete files.' },
        { label: 'Performance', text: 'Use sensible file sizes for faster processing.' },
        { label: 'Support', text: 'See About/Contact for help and feedback.' }
      ];

      const tips = tipsMap[toolKey] || fallback;

      tips.forEach(item => {
        const li = document.createElement('li');
        if (item.label) {
          const strong = document.createElement('strong');
          strong.textContent = item.label + ': ';
          li.appendChild(strong);
        }
        li.appendChild(document.createTextNode(item.text));
      if (item.link) {
        const a = document.createElement('a');
        a.href = item.link.url;
        a.textContent = item.link.text;
        a.style.color = 'var(--primary)';
        a.style.textDecoration = 'underline';
        li.appendChild(a);
      }
      if (item.suffix) {
        li.appendChild(document.createTextNode(item.suffix));
      }
    function injectTips() {
      const toolKey = getToolKey();
      if (!toolKey) return;
      if (document.querySelector('section.help')) return;
      const section = buildTipsSection(toolKey);
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