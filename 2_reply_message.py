# import flask related
from flask import Flask, request, abort
from urllib.parse import parse_qsl
# import linebot related
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    LocationSendMessage, ImageSendMessage, StickerSendMessage,
    VideoSendMessage, TemplateSendMessage, ButtonsTemplate, PostbackAction, MessageAction, URIAction,
    PostbackEvent, ConfirmTemplate, CarouselTemplate, CarouselColumn,
    ImageCarouselTemplate, ImageCarouselColumn, FlexSendMessage
)
import json

# create flask server
app = Flask(__name__)
line_bot_api = LineBotApi('ydbR7tlDs0awKhF6dOc3M6NKdQ3vQGsztN1eDWTkGuEMOT7sM17ZhHLAuUtvl269KllY0embWZt3yTotI1N00VzWj5/oJNAKc2wjKzhc+2ksLiER9MuydqtZf6vhBvZQDnfxr4TWlG0IVA16VjYOoAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('58b85082aeb6b5190f1fa81b0d083adf')

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        print('receive msg')
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
    return 'OK'

# handle msg
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # get user info & message
    user_id = event.source.user_id
    msg = event.message.text
    user_name = line_bot_api.get_profile(user_id).display_name
    
    # get msg details
    print('msg from [', user_name, '](', user_id, ') : ', msg)

    line_bot_api.reply_message(event.reply_token, TextSendMessage(text = "小胖: "+msg))

# run app
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5566, debug=True)