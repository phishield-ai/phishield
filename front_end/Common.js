/**
 * Callback for rendering the homepage card.
 * @return {CardService.Card} The card to show to the user.
 */
function onHomepage(e) {
  var message = 'Welcome to PhishShield!';

  // Create a card with a welcome message.
  return createPhishingCard(message, true);
}

/**
 * Creates a card with an image of a phishing shield, overlayed with the text.
 * @param {String} text The text to overlay on the image.
 * @param {Boolean} isHomepage True if the card created here is a homepage;
 *      false otherwise. Defaults to false.
 * @return {CardService.Card} The assembled card.
 */
function createPhishingCard(text, isHomepage) {
  // Use a phishing shield image.
  var imageUrl = 'https://ffd04feb3264e31cbca5add4d0281514c77e1025ec87ae866efdad4-apidata.googleusercontent.com/download/storage/v1/b/phishshield/o/phish-shield-logo.png?jk=ASOpP9ic7zO6XmV0s53oiE8N-ZKGd8OtCs6czY73B3vQpkRNWLnjoP1aiUtFaQUKIPot2MF7B73wIvfFsTohtvAfqt1tSXe89xNE3dt6Qje_z-E4PFaTvngrZsRD8KbWceEgkcgJqKNVs2Wwz9XTmnJGuYQ97ECEwUfivJsPGFqqke_0uc6yhjWDn2rf-26ht8mWIe7N6FNvGII-j2sBvm7bVHt5lrUQQcR-RgSGoJ_AjgQNnLX5dtCP-z8gV8-ATzNPivMR1YCwxfK_4o6eJ9bYR2NnaRxNaONG7C_25quolKhRwNVZNBS9DfnTWYuOC1cn5Oa8RQ_m9fsekpr9aMi8qncL9L11067B7-cwh_lDl93qJPMm7rO4bzVP5BuelERbDVh3f5ZBQTMvrlrfUS7w-sd8sx36gf3VvqzKOIC0SBTSFq29g5oMQXufA6T4pvRV3_A6SXQ7on8gvxd1CvpSnUplz3D54n5Y_SgPif4qyHzLOqtaW0JjMypvJ80HWzwsk5hwRk0edxNDbG_FcEEapphQZePUkCQxRIKzufGPkeHDYXzBF7e3x-ttc9mA_MxrSuK102sVwtHl6KXhVvAx9UxSXe-6evYQrzZZiCQQNWMbDDJacnBT7-1fMMVERwKuPaG9GVrBmCSopJApsBg5M6_58uxgP326uTTpcE4PeXJDMVEqL3IwhNCVbsFQEJ0XslWRnIND8e8KR4eDl8jippzMc0O1O7TXgCu0X6ZKS2llc5UhotaU0PNaNcXjTuXHY2RDd6PIYySH6ItlvcWWxOwK-tV1v7r5oPQzzSCnTsK9Y4B_31n9-Kpy84Fr0wYCDHWGCJJ5L_MsLH4ZhYcn_LUvpe8RaAji-Zp3y1PRqe_ZCVLrgy9A4H7FVCHM_VtlnrxfFdDLwIrN2_RT2p5gpADx6ziDPSGberdc2YwliRQIzHuwdQDs-7pP6sTBmEj7768VVDmono4df9ElpwxPOO0eu3eB6_ACBhSb8onC6X0YMFoItVonbG_ktGdvXz2HLgMyoF72TT4aNPS0SG28zZJuFytOvRgf_sjj4We2QGdr0m2kfhO8heEDIgCUw-l4PgBrO7axXNGhGKVOxmXK9Jk95iS33LP4t8DpABaOXjQW1HCxcpGqwWKSI2fC7nlqax0-zuQigGaePwT7wZX5KX-LsG1N&isca=1';

  var image = CardService.newImage()
      .setImageUrl(imageUrl)
      .setAltText('PhishShield Image');

  // Create headline and subheadline
  var headline = CardService.newDecoratedText()
      .setTopLabel("PhishShield")

  var subheadline = CardService.newTextParagraph()
      .setText('Protecting your inbox from phishing attacks')

  // Create button 1: Report Phishing Detection
  var reportDetectionAction = CardService.newAction()
    .setFunctionName('openModal')
    .setParameters({type: 'report_detection'});
  var reportDetectionButton = CardService.newTextButton()
    .setText('Report Phishing Detection')
    .setOnClickAction(reportDetectionAction)
    .setTextButtonStyle(CardService.TextButtonStyle.FILLED);

  // Create button 2: Report Phishing Email
  var reportEmailAction = CardService.newAction()
    .setFunctionName('openModal')
    .setParameters({type: 'report_email'});
  var reportEmailButton = CardService.newTextButton()
    .setText('Report Phishing Email')
    .setOnClickAction(reportEmailAction)
    .setTextButtonStyle(CardService.TextButtonStyle.FILLED);

  // Create button 3: Open Settings
  var openSettingsAction = CardService.newAction()
    .setFunctionName('onSettingsOpen')
    .setParameters({type: 'open_settings'});
  var openSettingsButton = CardService.newTextButton()
    .setText('Open Settings')
    .setOnClickAction(openSettingsAction)
    .setTextButtonStyle(CardService.TextButtonStyle.FILLED);

  // Create a button set with the three buttons
  var buttonSet = CardService.newButtonSet()
    .addButton(reportDetectionButton)
    .addButton(reportEmailButton)
    .addButton(openSettingsButton);

  // Create a footer with a link to your product.
  var footer = CardService.newFixedFooter()
      .setPrimaryButton(CardService.newTextButton()
          .setText('Powered by PhishShield')
          .setOpenLink(CardService.newOpenLink()
              .setUrl('https://www.phishshield.com')));

  // Assemble the widgets and return the card.
  var section = CardService.newCardSection()
      .addWidget(image)
      .addWidget(headline) // Add the headline
      .addWidget(subheadline) // Add the subheadline
      .addWidget(buttonSet);
  var card = CardService.newCardBuilder()
      .addSection(section)
      .setFixedFooter(footer);

  // Set peek header only for non-homepage cards.
  if (!isHomepage) {
    var peekHeader = CardService.newCardHeader()
      .setTitle('Contextual Phishing Shield')
      .setImageUrl('https://example.com/peek-header-image.png')
      .setSubtitle(text);
    card.setPeekCardHeader(peekHeader);
  }

  return card.build();
}
function onSettingsOpen(e) {
  var header = CardService.newCardHeader()
      .setTitle('Settings');

  // Load the user's saved option or set a default value
  var savedOption = getUserOption(); // Implement this function to retrieve the user's saved option
  var defaultOption = savedOption || 'enable'; // Set a default option if none is saved

  // Create radio option for selection of email notifications
  var radio = CardService.newSelectionInput()
      .setType(CardService.SelectionInputType.RADIO_BUTTON)
      .setTitle('Enable email notification')
      .setFieldName('options')
      .addItem('Enable', 'enable', defaultOption === 'enable')
      .addItem('Disable', 'disable', defaultOption === 'disable');

  // Create dropdowns to mimic a slider for the detection threshold
  var thresholdDropdown = CardService.newSelectionInput()
      .setType(CardService.SelectionInputType.DROPDOWN)
      .setTitle('Detection Threshold')
      .setFieldName('threshold')
      .setOnChangeAction(CardService.newAction().setFunctionName('saveSettings'));
  
  // Add threshold values to the dropdown
  var thresholdValues = [];
  for (var i = 0; i <= 100; i += 10) {
    thresholdDropdown.addItem(i.toString(), i.toString(), false);
  }

  // Create a button that saves the selected option and threshold
  var action = CardService.newAction()
      .setFunctionName('saveSettings');
  var button = CardService.newTextButton()
      .setText('Save settings')
      .setOnClickAction(action)
      .setTextButtonStyle(CardService.TextButtonStyle.FILLED);
  var buttonSet = CardService.newButtonSet()
      .addButton(button);

  // Assemble the widgets and return the card.
  var section = CardService.newCardSection()
      .addWidget(radio)
      .addWidget(thresholdDropdown)
      .addWidget(buttonSet);
  var card = CardService.newCardBuilder()
      .setHeader(header)
      .addSection(section);
  return card.build();
}

/**
 * Saves the selected option.
 */
function saveSettings(e) {
  var selectedOption = e.formInput.options;
  setUserOption(selectedOption); // Implement this function to save the selected option
}

/**
 * Retrieves the user's saved option from Properties Service.
 * @return {string|null} The user's saved option, or null if not found.
 */
function getUserOption() {
  var userProperties = PropertiesService.getUserProperties();
  return userProperties.getProperty('selectedOption');
}

/**
 * Saves the selected option into Properties Service.
 * @param {string} option The selected option to save.
 */
function setUserOption(option) {
  var userProperties = PropertiesService.getUserProperties();
  userProperties.setProperty('selectedOption', option);
}

/**
 * Retrieves the user's saved threshold from Properties Service.
 * @return {string|null} The user's saved threshold, or null if not found.
 */
function getUserThreshold() {
  var userProperties = PropertiesService.getUserProperties();
  return userProperties.getProperty('selectedThreshold');
}

/**
 * Saves the selected threshold into Properties Service.
 * @param {string} threshold The selected threshold to save.
 */
function setUserThreshold(threshold) {
  var userProperties = PropertiesService.getUserProperties();
  userProperties.setProperty('selectedThreshold', threshold);
}