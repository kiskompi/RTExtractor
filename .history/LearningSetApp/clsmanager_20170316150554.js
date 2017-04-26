$(document).click(function(event) {
    var text = $(event.target).text();
    alert(text);
    console.log(text);
});

// Listening for message from popup.js
chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse) {
    if (request.greeting == "hello")
      sendResponse({farewell: result});
  });