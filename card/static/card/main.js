[].forEach.call(document.querySelectorAll('a[data-img-src]'), function(link) {
  const img = link.parentElement.parentElement.lastElementChild.children[0];
  link.onmouseover = function() {
    preview = link.getAttribute('data-img-src').replace('front', '90_126');
    img.setAttribute('src', preview);
  };

  img.parentElement.onclick = function() {
    preview = link.getAttribute('data-img-src').replace('front', '90_126');
    img.setAttribute('src', preview);
  };
});

document.getElementById('toggleHelp').onclick = function() {
  document.getElementById('help').classList.toggle('hide');
};

document.addEventListener('DOMContentLoaded', (event) => {
  const url = new URL(window.location.href);
  const sortID = new URLSearchParams(
      document.getElementById('sort-id').getAttribute('href'));
  const sortDiff = new URLSearchParams(
      document.getElementById('sort-diff').getAttribute('href'));
  for (const p of url.searchParams) {
    sortID.append(p[0], p[1]);
    sortDiff.append(p[0], p[1]);
  }
  sortID.set('sort', 'id');
  sortDiff.set('sort', 'diff');
  document.getElementById('sort-id').setAttribute(
      'href', '?' + sortID.toString());
  document.getElementById('sort-diff').setAttribute(
      'href', '?' + sortDiff.toString());
});
