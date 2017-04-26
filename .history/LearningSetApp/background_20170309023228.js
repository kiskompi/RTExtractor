browser.contextMenus.create({
  id: "learn-page",
  title: "Learn this page"
});

browser.contextMenus.onClicked.addListener(function(info, tab) {
  if (info.menuItemId == "eat-page") {
    browser.tabs.executeScript({
      file: "page-eater.js"
    });
  }
});