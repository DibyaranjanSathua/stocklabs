"""
File:           sheet_reader.py
Author:         Dibyaranjan Sathua
Created on:     23/06/21, 9:20 pm
"""
from google_sheet_api.base_sheet_api import BaseSheetAPI


class SheetReader(BaseSheetAPI):
    """ Read data from google sheets """
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

    def __init__(self, token_file: str):
        super(SheetReader, self).__init__(token_file=token_file)

    def read(self, sheet_id: str, cells: str):
        """ Read cells value from the required sheet with sheet_id """
        service = self._get_service()
        sheet = service.spreadsheets()
        result = sheet.values().get(
            spreadsheetId=sheet_id,
            range=cells
        ).execute()
        values = result.get("values")
        print(values)
