[].forEach.call(document.querySelectorAll('a[data-img-src]'), function(link) {
    var img = link.parentElement.parentElement.lastElementChild.children[0];
    link.onmouseover = function() {
        preview = link.getAttribute("data-img-src").replace("front", "90_126");
        img.setAttribute('src', preview);
    };

    img.parentElement.onclick = function(){
        preview = link.getAttribute("data-img-src").replace("front", "90_126");
        img.setAttribute('src', preview);
    }
});

document.getElementById('toggleHelp').onclick = function() {
    document.getElementById('help').classList.toggle('hide');
}
