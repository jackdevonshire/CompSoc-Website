var baseUrl = "https://localhost:8080/api";
var authToken = "A SECURE TOKEN HERE";

function onOpen() {
  var ui = SpreadsheetApp.getUi();
  ui.createMenu('CompSoc Menu')
      .addItem('Update Website', 'updateWebsite')
      .addToUi();
}

function checkFeatured(featuredValue) {
  if (featuredValue == "Yes") {
    return 1;
  }
  return 0;
}

function updateWebsite() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var linksSheet = ss.getSheetByName("Links");
  var eventsSheet = ss.getSheetByName("Events");

  var links = linksSheet.getRange("A2:E11").getValues();
  var events = eventsSheet.getRange("A2:D11").getValues();

  var linksJson = []
  links.forEach(function(row) {
    if (row[0] != "") {
      linksJson.push({
        "icon": row[0],
        "title": row[1],
        "description": row[2],
        "link": row[3],
        "featured": checkFeatured(row[4])
      })
    }
  });

  var eventsJson = []
  events.forEach(function(row) {
    if (row[0] != "") {
      eventsJson.push({
        "date": row[0],
        "description": row[1],
        "link": row[2],
        "featured": checkFeatured(row[3])
      })
    }
  });

  var payload = {
    "token": authToken,
    "links": linksJson,
    "events": eventsJson
  }

  var options = { 
    'method' : 'post',
    'contentType': 'application/json',
    'headers': {},
    'payload': JSON.stringify(payload)
  };

  var response = UrlFetchApp.fetch(baseUrl+"/content", options);
  SpreadsheetApp.getUi().alert(response);
}
