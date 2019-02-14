from class_mysql import query
from class_cnx_api import cnx_api
from functions.seach_in_dic import seach_in_dic
from dictionaries import menu
from menu.wallet import wallet
from menu.deposit import deposit
from menu.exchange import exchange
from menu.withdraw import withdraw
from menu.transactions import transactions
from menu.cards import cards
from menu.invoices import invoices
from menu.mining import mining
from menu.setting import setting
from status import status
from telebot import types
from send_message import telegram


class dispatcher():

    output = {'text_of_message': [], 'keyboard': None, 'type': "inline_keyboard", 'button_text': None,
                "button_data": None, 'edit': False, 'photo': None}
    user = {'cryptonex_id': None, 'public': None, 'secret': None, 'status': None, 'language': None}

    def __init__(self, tg_id, data, message_id=None):
        self.tg_id = tg_id
        self.data = data
        self.message_id = message_id

    def dispatcher(self):

        print('#' * 50, 'class DISPATCHER | def distribution', '#' * 50)

        self.user = query.info(self.tg_id)
        print(' user\n', self.user)
        print(' data\n', self.data)

        if self.user['cryptonex_id'] is None:
            self.registration()
        elif self.user['cryptonex_id'] is not None:
            self.main_keyboard()

        if self.data != '/start':

            if seach_in_dic(menu, self.data) is not False:
                self.press_menu()

            print(' status', self.user['status'])
            self.call_item()

        print(self.output)

        if self.output['button_text']:

            if self.output['type'] == 'inline_keyboard':
                self.output['keyboard'] = self.inline_keyboard()

            elif self.output['type'] == 'reply_keyboard':
                self.output['keyboard'] = self.reply_keyboard()

        print('\n user \n', self.user)
        print('\n output \n', self.output)

        send = telegram(self.user, self.output, self.message_id)
        send.distribution()

    def inline_keyboard(self):
        keyboard = types.InlineKeyboardMarkup()
        for line in range(len(self.output['button_text'])):
            buttons = []
            for key in range(len(self.output['button_text'][line])):
                # print("text button", self.output['button_text'][line][key])
                # print("text button", transactions_type(self.output['button_text'][line][key]))
                buttons.append(types.InlineKeyboardButton(text=self.output['button_text'][line][key],
                                                          callback_data=self.output['button_data'][line][key]))
                # print("list button", buttons)
            keyboard.row(*buttons)
        return keyboard

    def reply_keyboard(self):
        keyboard = types.ReplyKeyboardMarkup()
        for line in range(len(self.output['button_text'])):
            buttons = []
            for key in range(len(self.output['button_text'][line])):
                buttons.append(self.output['button_text'][line][key])
            keyboard.row(*buttons)
        return keyboard

    def call_item(self):

        print('->class dispatcher | def call_item')
        print(' status', self.user['status'])

        if self.user['status'] in status['wallet'].values():
            result = wallet(self.user)
            self.output = result.show_user()

        elif self.user['status'] in status['deposit'].values():
            result = deposit(self.user, self.data)
            self.output = result.distribution()

        elif self.user['status'] in status['invoices'].values():
            result = invoices(self.user, self.data)
            self.output = result.manager()

        elif self.user['status'] in status['exchange'].values():
            result = exchange(self.user, self.data)
            self.output = result.distribution()

        elif self.user['status'] in status['withdraw'].values():
            result = withdraw(self.user, self.data)
            self.output = result.distribution()

        elif self.user['status'] in status['transactions'].values():
            result = transactions(self.user, self.data)
            self.output = result.distribution()

        elif self.user['status'] in status['cards'].values():
            result = cards(self.user, self.data)
            self.output = result.distribution()

        elif self.user['status'] in status['mining'].values():
            result = mining(self.user, self.data)
            self.output = result.distribution()

        elif self.user['status'] in status['setting'].values():
            result = setting(self.user, self.data)
            self.output = result.manager()

    def press_menu(self):
        print('->class dispatcher | def press menu')

        menu_status = {
            'wallet': status['wallet']['wallet'],
            'setting': status['setting']['setting'],
            'invoices': status['invoices']['invoices'],
            'deposit': status['deposit']['currency'],
            'withdraw': status['withdraw']['withdraw'],
            'exchange': status['exchange']['exchange'],
            'transactions': status['transactions']['transactions'],
            'cards': status['cards']['cards'],
            'mining': status['mining']['mining']
        }
        item = seach_in_dic(menu, self.data)
        query.update('user', 'status', menu_status[item], 'telegram_id', self.tg_id)
        self.user['status'] = menu_status[item]

    def registration(self):
        print("class input_message_handler | def registration")
        print("user id =", self.tg_id)
        new = cnx_api.user_register_internal(str(self.tg_id))
        if 'error' not in new.keys():
            query.insert('user', 'telegram_id', self.tg_id)
            query.update('user', 'cryptonex_id', new['result']['user'], 'telegram_id', self.tg_id)
            query.update('user', 'public_key', new['result']['user_api_key'], 'telegram_id', self.tg_id)
            query.update('user', 'secret_key', new['result']['user_api_secret'], 'telegram_id', self.tg_id)
            query.update('user', 'status', status.START, 'telegram_id', self.tg_id)

    def main_keyboard(self):
        print('#' * 50, 'class DISPATCHER | def main_keyboard', '#' * 50)
        self.output['type'] = 'reply_keyboard'
        self.output['text_key'] = [
            [
                menu['wallet'][self.user['language']],
                menu['deposit'][self.user['language']],
                menu['withdraw'][self.user['language']]
            ],
            [
                menu['exchange'][self.user['language']],
                menu['transactions'][self.user['language']],
                menu['cards'][self.user['language']]
            ],
            [
                menu['mining'][self.user['language']],
                menu['invoices'][self.user['language']],
                menu['setting'][self.user['language']]
            ]
        ]
