"""
File:           google_sheet_api.py
Author:         Dibyaranjan Sathua
Created on:     23/06/21, 9:35 pm
"""
from google_sheet_api import SheetReader, SheetWriter

def test_sheet_reader():
    """ Testing google sheet reading """
    token_file = "/Users/dibyaranjan/Stocks/stocklabs/google_token/token.json"
    sheet_id = "1JRleMts93cmRHcpNjl-Id9IA9enIn3IfvCd9FeFuEIE"
    cells = "Sheet1!B1:D2"
    reader = SheetReader(token_file=token_file)
    reader.read(sheet_id=sheet_id, cells=cells)


def test_sheet_writer():
    """ Testing google sheet reading """
    token_file = "/Users/dibyaranjan/Stocks/stocklabs/google_token/token.json"
    sheet_id = "1JRleMts93cmRHcpNjl-Id9IA9enIn3IfvCd9FeFuEIE"
    cells = "Sheet1!E1:G2"
    writer = SheetWriter(token_file=token_file)
    # values = [
    #     [
    #         # Cell values ...
    #     ],
    #     # Additional rows ...
    # ]
    values = [
        [1, 2, 3], [4, 5, 6]
    ]
    writer.write(sheet_id=sheet_id, cells=cells, values=values)


if __name__ == "__main__":
    test_sheet_reader()
    test_sheet_writer()
