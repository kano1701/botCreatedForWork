from class_mysql import query
import locale
import calendar
import datetime
import qrcode


class menu():

    __result = {'text_of_message': [], 'keyboard': None, 'type': "inline_keyboard", 'button_text': None,
                "button_data": None, 'edit': False, 'photo': None}
    number_text = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣']
    number_data = ['/1', '/2', '/3', '/4', '/5']
    text_navi = ['⬅', '➡']
    data_navi = ['button_back', 'button_next']

    def __init__(self, user, data=None):
        self.user = user
        self.data = data

    def get_data(self):
        return self.data

    def get_lang(self):
        return query.select('language', 'user', 'cryptonex_id', self.user['cryptonex_id'])

    def get_status(self):
        return query.select('status', 'user', 'cryptonex_id', self.user['cryptonex_id'])

    def set_status(self, value):
        query.update('user', 'status', value, 'cryptonex_id', self.user['cryptonex_id'])

    def set_result(self, key, values):
        if key == 'text_of_message':
            if key == 'text_of_message' and values == None:
                self.__result['text_of_message'].clear()
            else:
                print('*'*20, 'set_result')
                self.__result['text_of_message'].append(values)
        elif key != 'text_of_message':
            self.__result[key] = values

    def get_result(self):
        return self.__result

    def send_calendar(self):

        today = datetime.datetime.today()
        lang = self.get_lang()
        year = query.select('year', 'user', 'cryptonex_id', self.user['cryptonex_id'])
        month = query.select('month', 'user', 'cryptonex_id', self.user['cryptonex_id'])
        result = {'text': None, 'data': None}
        start_week = None

        if lang == 'ru':
            locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
            start_week = 0

        this_month = calendar.Calendar(start_week)
        days = this_month.monthdayscalendar(year, month)
        days_text = []
        days_data = []

        for x in range(len(days)):
            text = []
            date = []
            for y in range(7):
                if days[x][y] == 0 or (month == today.month and days[x][y] < today.day):
                    text.append(' ')
                    date.append('ignore')
                else:
                    text.append(str(days[x][y]))
                    date.append(str(days[x][y]))
            days_text.append(text)
            days_data.append(date)

        result['text'] = [['<', calendar.month_name[month]+' '+str(year), '>']]
        result['data'] = [['button_back', 'ignore', 'button_next']]

        for loop in range(len(days)):
            result['text'].append(days_text[loop])
            result['data'].append(days_data[loop])

        return result

    def check_in_month(self, day, month, year):
        obj_month = calendar.monthrange(year, month)
        day_list = [i for i in range(obj_month[1])]
        return day in set(day_list)

    def buttons_for_list(self, input_list, method):
        offset = query.select('offset', 'user', 'cryptonex_id', self.user['cryptonex_id'])
        result = {'list': [], 'text': [], 'data': []}
        result['list'] = input_list['result'][method]

        if offset != 0:
            result['text'].append(self.text_navi[0])
            result['data'].append(self.data_navi[0])

        for i in range(len(result['list'])):
            result['text'].append(self.number_text[i])
            result['data'].append(self.number_data[i])

        if len(result['list']) == 5:
            result['text'].append(self.text_navi[1])
            result['data'].append(self.data_navi[1])

        return result

    def qrcode_generate(self, text):
        print("function qrcode_generate | text", text)
        img = qrcode.make(text)
        img.save('qr_code.png')

    def is_digit(self, data):
        number = data.lower()
        if number == 'nan' or number == 'inf' or number == '-inf':
            return False
        try:
            n = str(number).find(',')
            if n != -1:
                number = number[0:n:] + '.' + number[(n + 1)::]
            print(number)
            float(number)
            return True
        except:
            return False
