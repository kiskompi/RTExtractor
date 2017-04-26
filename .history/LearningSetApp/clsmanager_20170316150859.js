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

  // This function gets all the id of the elements that have a class name X and 
// returns them in a string separated by ",".
function getId(className) {
   // I get all elements containing className
   var elements = document.getElementsByClassName(className);   

   // Creating array with id of the elements
   var idElements= new Array();
   for (var i = 0; i < elements.length; i++) {
    idElements[i]=elements[i].id;
   }

   // Concatenate all id
   var list = idElements.join(" , ");
   return list;
}

var result=getId("classNameTest");