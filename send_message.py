from tg_bot_config import bot
from telebot import types

class telegram():

    def __init__(self, user, output, message_id):
        self.user = user
        self.result = output
        self.message_id = message_id

    def distribution(self):

        print('#' * 50, 'class TELEGRAM | def distribution', '#' * 50)
        print('user\n', self.user)
        print('result\n', self.result)

        if self.result['edit'] is False:
            self.send_message()

        elif self.result['edit'] is True:
            self.edit_message()

    def send_message(self):

        for send in range(len(self.result['text_of_message'])):
            
            if self.result['keyboard'] is None:
                bot.send_message(self.user['telegram_id'], self.result['text_of_message'][send])
    
            elif self.result['keyboard'] is not None:
                print("\n\n", self.user['telegram_id'])
                print('message_id', self.message_id)
                bot.send_message(self.user['telegram_id'], self.result['text_of_message'][send],
                                 reply_markup=self.result['keyboard'])
    
            if self.result['photo'] is not None:
                bot.send_photo(self.user['telegram_id'], photo=self.result['photo'])

    def edit_message(self):

        for send in range(len(self.result['text_of_message'])):
            
            if self.result['keyboard'] is None:
                bot.edit_message_text(self.user['telegram_id'], self.message_id, self.result['text_of_message'][send])
    
            elif self.result['keyboard'] is not None:
                print("\n\n", self.user['telegram_id'])
                print('message_id', self.message_id)
                bot.edit_message_text(self.user['telegram_id'], self.message_id, self.result['text_of_message'][send],
                                 reply_markup=self.result['keyboard'])
    
            if self.result['photo'] is not None:
                bot.send_photo(self.user['telegram_id'], photo=self.result['photo'])