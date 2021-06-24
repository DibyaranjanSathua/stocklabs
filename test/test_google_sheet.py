"""
File:           google_sheet_api.py
Author:         Dibyaranjan Sathua
Created on:     23/06/21, 9:35 pm
"""
from google_sheet_api.sheet_reader import SheetReader


def test_sheet_reader():
    """ Testing google sheet reading """
    token_file = "/Users/dibyaranjan/Stocks/stocklabs/google_token/token.json"
    sheet_id = "1JRleMts93cmRHcpNjl-Id9IA9enIn3IfvCd9FeFuEIE"
    cells = "Sheet1!B1:D2"
    reader = SheetReader(token_file=token_file)
    reader.read(sheet_id=sheet_id, cells=cells)


if __name__ == "__main__":
    test_sheet_reader()
