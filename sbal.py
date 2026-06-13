import requests
import xml.etree.ElementTree as ET
import pandas as pd
import csv
import os
import json
from datetime import datetime
# ---------- FETCH LEDGER BALANCES ----------
TALLY_URL = "http://localhost:9008"


tally_xml = """
<ENVELOPE>
  <HEADER>
    <VERSION>1</VERSION>
    <TALLYREQUEST>EXPORT</TALLYREQUEST>
    <TYPE>COLLECTION</TYPE>
    <ID>Remote Ledger Coll</ID>
  </HEADER>
  <BODY>
    <DESC>
      <STATICVARIABLES>
        <SVEXPORTFORMAT>$$SysName:XML</SVEXPORTFORMAT>
      </STATICVARIABLES>
      <TDL>
        <TDLMESSAGE>
          <COLLECTION NAME="Remote Ledger Coll" ISINITIALIZE="Yes">
            <TYPE>Ledger</TYPE>
            <FETCH>Name,OpeningBalance,ClosingBalance</FETCH>
            <BELONGSTO>Yes</BELONGSTO>
            <ISACTIVE>Yes</ISACTIVE>
          </COLLECTION>
        </TDLMESSAGE>
      </TDL>
    </DESC>
  </BODY>
</ENVELOPE>
"""

response = requests.post(TALLY_URL, data=tally_xml.encode('utf-8'), headers={'Content-Type': 'application/xml'})

ledger_data = []

if response.status_code == 200:
    root = ET.fromstring(response.text)
    print("9000 Connected")
    for ledger in root.findall(".//LEDGER"):
        name = ledger.attrib.get("NAME", "N/A")
        opening_balance_elem = ledger.find("OPENINGBALANCE")
        opening_balance = opening_balance_elem.text.strip() if opening_balance_elem is not None else "0.00"
        closing_balance_elem = ledger.find("CLOSINGBALANCE")
        closing_balance = closing_balance_elem.text if closing_balance_elem is not None else "0.00"

#        print(f"Ledger: {name}, Opening Balance: {opening_balance}, Closing Balance: {closing_balance}")
        ledger_data.append([name, opening_balance, closing_balance])

    with open("ledger_balances.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Ledger Name", "Opening Balance", "Closing Balance"])
        writer.writerows(ledger_data)

#    print("Ledger balance data saved to ledger_balances.csv")

    # Push to Google Sheet via Apps Script
    APPS_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbyqWmhjLFtc1g8tJiFoNju8_o7NIBupPEE6e69pqysFRPupGnXCt-RCR_ELypUBPuui/exec"
    payload = {
        "action": "updateLedger",
        "rows": ledger_data
    }
    try:
        gs_resp = requests.post(APPS_SCRIPT_URL, json=payload)
        print("GS Response:", gs_resp.text)
    except Exception as e:
        print("Failed to push to Google Sheet:", e)
else:
    print(f"Failed to connect to Tally for ledger balances. Status Code: {response.status_code}")

#-------------------------------------------------------------------------------------------------------------

