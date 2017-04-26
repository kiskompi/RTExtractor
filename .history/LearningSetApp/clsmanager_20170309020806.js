document.addEventListener('click', function(e) {
    e = e || window.event;
    var target = e.target || e.srcElement,
        text = target.textContent || text.innerText;   
}, false);

var wn = window.open("example.html", "_blank", "height=300, width=500");
wn.document.write("")