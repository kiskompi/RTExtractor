  //  Inserting javascript code
  chrome.tabs.executeScript(null, {file: "clsmanager.js"});  

  // Sending request
  chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
    chrome.tabs.sendMessage(tabs[0].id, {greeting: "hello"}, function(response) {
    document.getElementById("elementcode").innerHTML(response.farewell);
    });
  }); 