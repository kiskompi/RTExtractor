$(document).click(function(event) {
    var text = $(event.target).text();
    alert(text);
    console.log(text);
});
chrome.tabs.executeScript(null, {file: "content_script.js"});