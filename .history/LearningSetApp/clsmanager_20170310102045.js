var target = "";
document.addEventListener('click', function(e) {
    e = e || window.event;
    target = e.target || e.srcElement,
        text = target.textContent || text.innerText;   
}, false);

var wn = window.open("chrome-extension://popup.html", "_blank", 
                        "height=300, width=500");
var node = wn.document.getElementById('elementcode');
console.log(node.id);
node.innerHTML(target);
console.log("isitgood?");

/*
chrome.browserAction.onClicked.addListener(function(tab) {
  chrome.tabs.executeScript({
    code: 'document.body.style.backgroundColor="red"'
  });
});*/