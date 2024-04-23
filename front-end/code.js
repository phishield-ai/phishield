function onOpen(e) {
  DocumentApp.getUi().createAddonMenu()
    .addItem('Start', 'showSidebar')
    .addToUi();
}

function showSidebar() {
  var html = HtmlService.createTemplateFromFile('sidebar').evaluate().setTitle("Add-On PhishShield");
  DocumentApp.getUi().showSidebar(html);
}

function openSettings() {
  var html = HtmlService.createTemplateFromFile('settings').evaluate().setTitle("Settings")
  DocumentApp.getUi().showSidebar(html);
}