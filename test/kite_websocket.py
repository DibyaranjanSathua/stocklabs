"""
File:           kite_websocket.py
Author:         Dibyaranjan Sathua
Created on:     02/10/21, 5:07 pm
"""
from urllib.parse import quote_plus
import websocket
import time

address = "wss://ws.zerodha.com/"
api_key = "kitefront"
user_id = "TW1320"
enctoken = "Qq7CI8lNICFWiwUgDUZwQtdV/nINsaveefvgFw6G1x3sTDRCf86kvSuv33j+Z7CYJ+7WZzvNypT706EWvjYZQS+b2AjxkfPY6byTlnl4XS0HJqpWSFLPew=="
version = "2.9.3"
uid = "1633182958536"
enctoken = "Qq7CI8lNICFWiwUgDUZwQtdV%2FnINsaveefvgFw6G1x3sTDRCf86kvSuv33j%2BZ7CYJ%2B7WZzvNypT706EWvjYZQS%2Bb2AjxkfPY6byTlnl4XS0HJqpWSFLPew%3D%3D"

ws_url = f"{address}?api_key={api_key}&user_id={user_id}&enctoken={enctoken}" \
         f"&uid={uid}&user-agent=kite3-web&version={version}"
print(ws_url)

def on_open(ws):
    print("On Open called")


def on_close(ws, close_status_code, close_msg):
    print("On Close called")


def on_message(ws, message):
    print("On Message called")
    print(message)


# websocket.enableTrace(True)
# ws = websocket.WebSocketApp(
#             url=ws_url,
#             on_open=on_open,
#             on_close=on_close,
#             on_message=on_message
#         )
#
# ws.run_forever()
#
# time.sleep(30)

def encode_uri_component(string):
    return quote_plus(string, safe="*").replace("~", "%7E").replace("%00", "\0")

test_string = "ajs23827325hbaxa.x\']d  \(\)qamxkhudha\/,m12!@#$%^&*()_+bahqbh`"
pyencode = encode_uri_component(test_string)
jsencode = "ajs23827325hbaxa.x%27%5Dd++%28%29qamxkhudha%2F%2Cm12%21%40%23%24%25%5E%26*%28%29_%2Bbahqbh%60"
print(test_string)
print(pyencode)
print(jsencode)
print(pyencode == jsencode)

test_string = r"!@#$%^&*()_+-="
pyencode = encode_uri_component(test_string)
jsencode = "%21%40%23%24%25%5E%26*%28%29_%2B-%3D"
print(test_string)
print(pyencode)
print(jsencode)
print(pyencode == jsencode)

test_string = '[];\',./{}|:"<>?`~'
pyencode = encode_uri_component(test_string)
jsencode = "%5B%5D%3B%27%2C.%2F%7B%7D%7C%3A%22%3C%3E%3F%60%7E"
print(test_string)
print(pyencode)
print(jsencode)
print(pyencode == jsencode)
