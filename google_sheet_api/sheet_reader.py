"""
File:           sheet_reader.py
Author:         Dibyaranjan Sathua
Created on:     23/06/21, 9:20 pm
"""
from pathlib import Path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials

from google_sheet_api.exceptions import GoogleSheetError


class SheetReader:
    """ Read data from google sheets """
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

    def __init__(self, token_file: str):
        self._token_file: Path = Path(token_file)
        if not self._token_file.is_file():
            raise GoogleSheetError(
                f"Token file {self._token_file} for google sheet api doesn't exist"
            )

    def _get_service(self):
        """ Get the service object for executing spreadsheets methods """
        # Make sure that you have shared the google sheet with the client_email in token.json
        creds = Credentials.from_service_account_file(str(self._token_file), scopes=self.SCOPES)
        service = build('sheets', 'v4', credentials=creds)
        return service

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
