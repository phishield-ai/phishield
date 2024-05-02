/**
 * Callback for rendering the homepage card.
 * @return {CardService.Card} The card to show to the user.
 */
function onHomepage(e) {
  var message = 'Welcome to PhiShield!';

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
  var imageUrl = 'https://i.imgur.com/mIFYKtG.png';

  var image = CardService.newImage()
      .setImageUrl(imageUrl)
      .setAltText('PhiShield Image');

  // Create headline and subheadline
  var headline = CardService.newDecoratedText()
      .setTopLabel("PhiShield")

  var subheadline = CardService.newTextParagraph()
      .setText('Protecting your inbox from phishing attacks')

  // Create button 1: Analyze Email
  var analyzeEmailAction = CardService.newAction()
    .setFunctionName('analyzeEmail')
    .setParameters({type: 'analyze_email'});
  var analyzeEmailButton = CardService.newTextButton()
    .setText('Analyze Email')
    .setOnClickAction(analyzeEmailAction)
    .setTextButtonStyle(CardService.TextButtonStyle.FILLED);

  // Create button 2: Report Email
  var reportEmailAction = CardService.newAction()
    .setFunctionName('reportEmail')
    .setParameters({type: 'report_email'});
  var reportEmailButton = CardService.newTextButton()
    .setText('Report Email')
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
    .addButton(analyzeEmailButton)
    .addButton(reportEmailButton)
    .addButton(openSettingsButton);

  // Create a footer with a link to your product.
  var footer = CardService.newFixedFooter()
      .setPrimaryButton(CardService.newTextButton()
          .setText('Powered by PhiShield')
          .setOpenLink(CardService.newOpenLink()
              .setUrl('https://www.phishield.dev')));

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
  return PropertiesService.getScriptProperties().getProperty('selectedThreshold');
  console.log('Retrieved threshold: ' + threshold);
  return threshold;
}

/**
 * Saves the selected threshold into Properties Service.
 * @param {string} threshold The selected threshold to save.
 */
function setUserThreshold(threshold) {
  return PropertiesService.getScriptProperties().setProperty('selectedThreshold', threshold);
  Logger.log('Saved threshold: ' + threshold);
}

/**
 * Report a phishing email.
 * @param {string} messageId The ID of the email message to report.
 */
function reportEmail() {
  var messageId = e.gmail.messageId;

  try {
    // Report the email as phishing using Gmail API
    var response = Gmail.Users.Messages.reportSpam('me', messageId);
    
    // Log the response
    console.log('Email reported as phishing:', response);
    
    // You can add further actions here based on the response if needed
  } catch (error) {
    // Handle any errors that occur during the reporting process
    console.error('Error reporting email as phishing:', error);
  }
}

function analyzeEmail(e) {
// Get the ID of the message the user has open.
var messageId = e.gmail.messageId;

// Get an access token scoped to the current message and use it for GmailApp
// calls.
var accessToken = e.gmail.accessToken;
GmailApp.setCurrentMessageAccessToken(accessToken);

// Get the subject of the email.
var message = GmailApp.getMessageById(messageId);

// Get the raw content of the email.
var rawContent = message.getRawContent();

// Transform raw email into bytes.
var bytes = Utilities.newBlob(rawContent).getBytes();

// Create the payload for the multipart request
var payload = {
  file: Utilities.newBlob(bytes).setName('email.eml') // Create a blob from bytes and set a name
};

// Construct the options for the request
var options = {
  method: 'post',
  'content-type': 'multipart/form-data',
  'boundary': 'X-GOOGLE',
  payload: payload
};

// Make the API call
try {
  var response = UrlFetchApp.fetch('https://api.phishield.dev/email/analysis', options);
  var responseData = JSON.parse(response.getContentText());
  
  // Create a card to display the API response
  var card = createResponseCard(responseData);
  
  // Return the card to display on the user's UI
  return card;
} catch (error) {
  console.error('Error making API call:', error);
}
}

// Function to create a card displaying the API response
function createResponseCard(responseData) {
var header = CardService.newCardHeader()
    .setTitle('Phishing Analysis Result')
    .setSubtitle('Here is the score and the suspicious elements.');

var content = responseData.data.content;

// Extract score and suspicious elements from the API response
var score = content.score;
var suspiciousElements = content.suspicious_elements;

// Create text paragraphs for score and suspicious elements
var scoreParagraph = CardService.newTextParagraph()
  .setText('Score: ' + score);

var suspiciousElementsParagraph = CardService.newTextParagraph()
  .setText('Suspicious Elements: ' + suspiciousElements);

// Create a section with the score and suspicious elements
var section = CardService.newCardSection()
  .addWidget(scoreParagraph)
  .addWidget(suspiciousElementsParagraph);

// Create the card
var card = CardService.newCardBuilder()
  .setHeader(header)
  .addSection(section)
  .build();

return card;
}