(function () {
  'use strict';
  const menuButton = document.getElementById('menuButton');
  const nav = document.getElementById('primaryNav');
  if (!menuButton || !nav) return;
  menuButton.addEventListener('click', () => {
    const open = nav.classList.toggle('open');
    menuButton.setAttribute('aria-expanded', String(open));
  });
  nav.addEventListener('click', () => {
    nav.classList.remove('open');
    menuButton.setAttribute('aria-expanded', 'false');
  });
})();
