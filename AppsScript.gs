// Google Apps Script — deploy as Web App
// Go to Extensions > Apps Script in your sheet, paste this, deploy as Web App

const SHEET_ID = '1LZtsBP5irE0_t8vowQFG9bxjiQgoZ1R3hVL3gWAo1zQ';

function doPost(e) {
  try {
    const data = JSON.parse(e.postData.contents);
    const action = data.action;
    const sheet = SpreadsheetApp.openById(SHEET_ID);

    if (action === 'addCategory') {
      const s = sheet.getSheetById(334012384);
      s.appendRow([data.category, '']);
      return json({ success: true, msg: 'Category added' });
    }

    if (action === 'removeCategory') {
      const s = sheet.getSheetById(334012384);
      const rows = s.getDataRange().getValues();
      for (let i = rows.length - 1; i >= 0; i--) {
        if (rows[i][0] === data.category) s.deleteRow(i + 1);
      }
      return json({ success: true, msg: 'Category removed' });
    }

    if (action === 'addItem') {
      const s = sheet.getSheetById(334012384);
      s.appendRow([data.category, data.item]);
      return json({ success: true, msg: 'Item added' });
    }

    if (action === 'removeItem') {
      const s = sheet.getSheetById(334012384);
      const rows = s.getDataRange().getValues();
      for (let i = rows.length - 1; i >= 1; i--) {
        if (rows[i][0] === data.category && rows[i][1] === data.item) {
          s.deleteRow(i + 1);
          break;
        }
      }
      return json({ success: true, msg: 'Item removed' });
    }

    return json({ success: false, msg: 'Unknown action' });
  } catch (err) {
    return json({ success: false, msg: err.toString() });
  }
}

function doGet(e) {
  return doPost({ postData: { contents: JSON.stringify({ action: e.parameter.action, category: e.parameter.category, item: e.parameter.item }) } });
}

function json(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}
