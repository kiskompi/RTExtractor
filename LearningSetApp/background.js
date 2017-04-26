// chrome.tabs.executeScript(null, {file: "clsmanager.js"});
$(document).click(function(event) {
    var text = $(event.target).text();
    alert(text);
    console.log(text);
});

chrome.browserAction.onClicked.addListener(function(tab) {
  chrome.tabs.executeScript({
    chrome.tabs.executeScript(null, {file: "clsmanager.js"});
  });
});