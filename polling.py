from tg_bot_config import bot


@bot.message_handler(content_types=['text'])
def bot_send_message(message):
    print("\n", "-" * 50,
          "\nuser_id", message.from_user.id,
          "\nlogin", message.from_user.username,
          "\nusername", message.from_user.first_name,
          "\ntext", message.text)
    if message.text == 'error':
        x = 100 + 'dima'
        print('Dima')

    bot.send_message(message.chat.id, message.text)
bot.polling()
