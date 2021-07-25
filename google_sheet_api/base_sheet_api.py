"""
File:           base_sheet_api.py
Author:         Dibyaranjan Sathua
Created on:     25/07/21, 1:50 am
"""
from pathlib import Path
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

from google_sheet_api.exceptions import GoogleSheetError


class BaseSheetAPI:
    """ Base class for sheet reader and writer API """
    SCOPES = []

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
