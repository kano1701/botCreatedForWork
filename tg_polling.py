from tg_bot_config import bot
from datetime import datetime
# from functions import qrcode_scaner
import json
from dispatcher import dispatcher


@bot.message_handler(content_types=['text'])
def bot_send_message(message):
    print("\n", "-" * 50,
          "\nuser_id", message.from_user.id,
          "\nlogin", message.from_user.username,
          "\nusername", message.from_user.first_name,
          "\ndate", datetime.today(),
          "\ntext", message.text)
    new = dispatcher(message.from_user.id, message.text)
    new.dispatcher()



# @bot.message_handler(content_types=['photo'])
# def bot_send_photo(message):
#     print("\n", "-" * 50,
#           "\nuser_id", message.from_user.id,
#           "\nlogin", message.from_user.username,
#           "\nusername", message.from_user.first_name,
#           "\ndate", datetime.today(),
#           "\ntext", message.text)
#     length = len(message.photo) - 1
#     file_info = bot.get_file(message.photo[length].file_id)
#     downloaded_file = bot.download_file(file_info.file_path)
#     src = 'qrcode/' + str(message.from_user.id) + '.jpg'
#     with open(src, 'wb') as new_file:
#         new_file.write(downloaded_file)
#     result_qrcode = qrcode_scaner.qrcode_scan(src)
#     print(result_qrcode)
#     try:
#         data = result_qrcode.decode('utf-8')
#         print(data)
#         data = json.loads(data)
#         print(data)
#         data = data['coupon']
#         print(data)
#     except:
#         data = 'error'
#     new = dispatcher(message.from_user.id, data)
#     new.dispatcher()


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    print("\n----------------------------------------------------------------",
          "\nuser_id", call.from_user.id,
          "\nlogin", call.from_user.username,
          "\nusername", call.from_user.first_name,
          "\ndate", datetime.today(),
          "\ntext", call.data)
    new = dispatcher(call.from_user.id, call.data, call.message.message_id)
    new.dispatcher()


bot.polling()
