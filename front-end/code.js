function onOpen(e) {
  DocumentApp.getUi().createAddonMenu()
    .addItem('Start', 'showSideBar')
    .addToUi();
}

function showSideBar() {
  var html = HtmlService.createTemplateFromFile('sidebar').evaluate().setTitle("Add-On PhishShield");
  DocumentApp.getUi()
    .showSidebar(html);
}

function showSettings() {
  var html = HtmlService.createTemplateFromFile('settings').evaluate().setTitle("Settings");
  DocumentApp.getUi()
    .showSettings(html);
}