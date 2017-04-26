
  // This function gets all the id of the elements that have a class name X and 
// returns them in a string separated by ",".
function getId(className) {
   // I get all elements containing className
    $(document).click(function(event) {
        var text = $(event.target).text();
        alert(text);
        console.log(text);
    });
   return text;
}

var result=getId("classNameTest");


// Listening for message from popup.js
chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse) {
    if (request.greeting == "hello")
      sendResponse({farewell: result});
  });
