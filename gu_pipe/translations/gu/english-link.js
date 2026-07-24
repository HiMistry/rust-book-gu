(function () {
  var page = location.pathname.split('/').pop();
  if (!page || page === 'index.html' || page === '') return;
  var enUrl = 'https://doc.rust-lang.org/stable/book/' + page;
  var el = document.createElement('p');
  el.id = 'english-link';
  el.innerHTML = 'Original page: <a href="' + enUrl + '" target="_blank">' + enUrl + '</a>';
  el.style.cssText = 'font-size:0.85em;color:#888;margin:0 0 12px 0';
  var main = document.querySelector('main');
  if (main) {
    main.parentNode.insertBefore(el, main);
  }
})();
