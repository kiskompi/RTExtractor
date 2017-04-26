  //  Inserting javascript code
  chrome.tabs.executeScript(null, {file: "scripts/content.js"});  

  // Sending request
  chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
    chrome.tabs.sendMessage(tabs[0].id, {greeting: "hello"}, function(response) {
    document.write(response.farewell);
    });
  }); 