browser.contextMenus.create({
  id: "learn-page",
  title: "Learn this page"
});

chrome.contextMenus.onClicked.addListener(function(info, tab) {
  if (info.menuItemId == "learn-page") {
    browser.tabs.executeScript({
      file: "clsmanager.js"
    });
  }
});