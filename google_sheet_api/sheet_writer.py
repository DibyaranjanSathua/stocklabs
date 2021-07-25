"""
File:           sheet_writer.py
Author:         Dibyaranjan Sathua
Created on:     25/07/21, 1:59 am
"""
from typing import List
from google_sheet_api.base_sheet_api import BaseSheetAPI


class SheetWriter(BaseSheetAPI):
    """ Write data from google sheets """
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    def __init__(self, token_file: str):
        super(SheetWriter, self).__init__(token_file=token_file)

    def write(self, sheet_id: str, cells: str, values: List):
        """ Write cells value from the required sheet with sheet_id """
        service = self._get_service()
        sheet = service.spreadsheets()
        body = {
            "values": values
        }
        result = sheet.values().update(
            spreadsheetId=sheet_id,
            range=cells,
            valueInputOption="USER_ENTERED",
            body=body
        ).execute()
        print(f"{result.get('updatedCells')} cells updated.")
