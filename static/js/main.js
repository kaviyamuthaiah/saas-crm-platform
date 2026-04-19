/* main.js – SaaS Platform frontend utilities */

(function () {
  'use strict';

  // ── Sidebar toggle (mobile) ─────────────────────────────────
  const sidebarToggle = document.getElementById('sidebarToggle');
  const sidebar       = document.getElementById('sidebar');
  const mainWrapper   = document.getElementById('mainWrapper');

  if (sidebarToggle && sidebar) {
    sidebarToggle.addEventListener('click', function () {
      sidebar.classList.toggle('open');
      // Desktop: collapse sidebar by shifting main content
      if (window.innerWidth > 768) {
        const isCollapsed = sidebar.style.width === '0px';
        if (isCollapsed) {
          sidebar.style.width = '';
          mainWrapper.style.marginLeft = '';
        } else {
          sidebar.style.width = '0px';
          mainWrapper.style.marginLeft = '0px';
        }
      }
    });

    // Close sidebar when clicking outside on mobile
    document.addEventListener('click', function (e) {
      if (window.innerWidth <= 768 &&
          sidebar.classList.contains('open') &&
          !sidebar.contains(e.target) &&
          e.target !== sidebarToggle) {
        sidebar.classList.remove('open');
      }
    });
  }

  // ── Auto-dismiss alerts after 5 seconds ────────────────────
  const alerts = document.querySelectorAll('.alert.alert-dismissible');
  alerts.forEach(function (alert) {
    setTimeout(function () {
      const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
      if (bsAlert) bsAlert.close();
    }, 5000);
  });

  // ── Confirm dangerous actions ───────────────────────────────
  // Any button/link with data-confirm attribute will prompt first
  document.addEventListener('click', function (e) {
    const el = e.target.closest('[data-confirm]');
    if (el) {
      const msg = el.dataset.confirm || 'Are you sure?';
      if (!window.confirm(msg)) {
        e.preventDefault();
        e.stopPropagation();
      }
    }
  });

  // ── Tooltips (Bootstrap) ────────────────────────────────────
  const tooltipEls = document.querySelectorAll('[data-bs-toggle="tooltip"]');
  tooltipEls.forEach(function (el) {
    new bootstrap.Tooltip(el);
  });

  // ── Active nav highlighting fallback ────────────────────────
  // Already handled in the template with inline conditionals,
  // but this covers any dynamic cases.
  const currentPath = window.location.pathname;
  document.querySelectorAll('.nav-item').forEach(function (item) {
    const href = item.getAttribute('href');
    if (href && href !== '/' && currentPath.startsWith(href)) {
      item.classList.add('active');
    }
  });

})();
