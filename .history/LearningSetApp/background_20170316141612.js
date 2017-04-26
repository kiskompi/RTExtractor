document.addEventListener("click", function(tab) {
  chrome.tabs.executeScript({
    code: 'document.body.style.backgroundColor="red"'
  });
  alert("kaki");
});