(function () {
  'use strict';
  function theme(id) {
    if (/^veterinary-/.test(id)) return 'veterinary';
    if (/^(animal-behavior|animal-cognition|anthrozoology)$/.test(id)) return 'behavior';
    if (/^(animal-welfare|animal-science|zoo-aquarium-science)$/.test(id)) return 'care';
    if (/^(wildlife-|conservation-|ecology|marine-|environmental-)/.test(id)) return 'wildlife';
    return 'biology';
  }
  function results(count, label, prefix) {
    if (!count) return '';
    return `<div class="search-results-note" role="status"><img src="${prefix || ''}images/curious-fox.svg" alt="" width="56" height="48"><p>${count} ${label}${count === 1 ? '' : 's'} to explore</p></div>`;
  }
  function empty(message, prefix) {
    return `<div class="friendly-empty" role="status"><img src="${prefix || ''}images/curious-fox.svg" alt="" width="84" height="72"><div><strong>No matches yet</strong><p>${message}</p></div></div>`;
  }
  window.ANIMAL_DETAILS = { theme, results, empty };
})();
