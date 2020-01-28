from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

# web app 共識

# 網站其實就是一個伺服器 python主流:flask小規模架設伺服器;django大規模有畫面網頁
# tolen權杖 asses存取秘密 只有我可以操控這個機器人 高度加密元素 很難猜 
line_bot_api = LineBotApi('X8+cXgsL+ZCMdQCvsX8NVnX4DphfDyI1j0sahpTAtoYLIDL9edQ0OyQ46kX1U/a5qFmFAMDz+kJ6/c+FeHPD4GaZPkUq7hGc9+dAIgHpClE+9yo2ADjRnuQ/Aje8yb//EAnbXMo/MJ4axyc96cMCfQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('8698f8664c36024aad67198c780ea9cc')

# 有人用遊覽器去這個網址www.line-bot.com/callback callback是被觸發的事件
# line_bot receive message then transfer to our server 進而觸發callback 再觸發handle來處理訊息
@app.route("/callback", methods=['POST'])	# route:路徑
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

# 處理訊息:回覆訊息也要權杖 只有我們設定可以回
# 依原樣 使用者傳hi, line_bot reply hi
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    r = 'Sorry, what do you mean?'

    if msg in ['hi', 'Hi']:
        r = 'Hi'
    elif msg == 'Do you have meal?':
        r = 'not yet'
    elif msg == 'Who are you':
        r = "I'm a robot"
    elif 'reserve' in msg:
        r = 'You want to reserve, right?'

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))

# main function: 寫這一行表示 如果這個app.py是直接被執行而不是被載入 才執行
# 確保直接被執行 而不是被載入
if __name__ == "__main__":
    app.run()
