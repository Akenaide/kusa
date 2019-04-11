[].forEach.call(document.querySelectorAll('a[data-img-src]'), function(link) {
    link.onmouseover = function() {

        var img = link.parentElement.parentElement.lastElementChild.children[0];
        preview = link.getAttribute("data-img-src").replace("front", "90_126");
        img.setAttribute('src', preview);
    };
});

document.getElementById('toggleHelp').onclick = function() {
    document.getElementById('help').classList.toggle('hide');
}
