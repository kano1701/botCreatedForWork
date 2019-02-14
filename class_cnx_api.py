import json
import hashlib
import requests
import time


class cnx_api():

    def call_api(self, method, key=None, secret_key=None, add_params=None, login=None):
        print(key)
        print(secret_key)
        print(add_params)
        print(login)

        nonce = int(time.time())
        url = 'http://dev-backoffice.cryptonex.internal:5656/api'
        params = {}

        if key:
            url = 'http://dev-backoffice.cryptonex.internal:5959/api'
            sign = method + str(nonce)+secret_key
            sign = hashlib.sha256(sign.encode('utf-8')).hexdigest()
            default = {'key': key, 'sign': sign, 'nonce': nonce}
            params.update(default)

            if add_params:
                params.update(add_params)

        elif key == None:
            default={'login': login}
            params.update(default)

        header = {'X-Real-IP': '127.0.0.1'}
        payload = {'jsonrpc': '2.0', 'method': method, 'params': params, 'id': 2}
        print('payload', payload)
        result = requests.post(url, data=json.dumps(payload), headers=header)
        print(result.text)
        return json.loads(result.text)

    # Регистрация пользователя
    def user_register_internal(self, telegram_id):
            login = telegram_id + '@telegram.org'
            return self.call_api(method='user.register_internal', login=login)

    # Список кошельков
    def user_account_list(self, key, secret_key, max_count=None):
            add_params = None
            if max_count != None:
                add_params = {'max_count': max_count}
            return self.call_api(method='user.account_list', key=key, secret_key=secret_key, add_params=add_params)

    # Обмен валютами
    def currency_convert(self, key, secret_key, amount, from_currency, to_currency):
            add_params = {'amount': str(amount), 'from_currency': from_currency, 'to_currency': to_currency}
            return self.call_api(method='currency.convert', key=key, secret_key=secret_key, add_params=add_params)

    # Вывод средств
    def account_withdraw(self, key, secret_key, from_hash, to_hash, amount):
            add_params = {'from_hash': from_hash, 'to_hash': to_hash, 'amount': amount}
            return self.call_api(method='account.withdraw', key=key, secret_key=secret_key, add_params=add_params)

    # Список транзакций
    def transactions_list(self, key, secret_key, max_count=None, offset=None, type = None):
            if max_count == None:
                max_count = 15
            add_params = {'max_count': max_count}
            if type:
                new_params = {'transactions_type': type}
                add_params.update(new_params)
            if offset:
                new_params = {'offset': offset}
                add_params.update(new_params)
            return self.call_api(method='transaction.list', key=key, secret_key=secret_key, add_params=add_params)

    # Список рейтов
    def get_rate_list(self, key, secret_key, currency_one, currency_two):
        result = self.call_api(method='currency_pair.get_rate_list', key=key, secret_key=secret_key)
        print('\n GET RATE LIST')
        print('currency_one',currency_one)
        if currency_one == 'cnx':
            alias = str(currency_one) + '/' + str(currency_two)
            print('alias', alias)
            for loop in range(len(result['result']['rates'])):
                print('alias in result', result['result']['rates'][loop]['alias'])
                if result['result']['rates'][loop]['alias'].lower() == alias:
                    return result['result']['rates'][loop]['bid']
        print('currency_two',currency_two)
        if currency_two == 'cnx':
            alias = str(currency_two) + '/' + str(currency_one)
            print('alias', alias)
            for loop in range(len(result['result']['rates'])):
                print('alias in result',result['result']['rates'][loop]['alias'])
                if result['result']['rates'][loop]['alias'].lower() == alias:
                    return 1 / float(result['result']['rates'][loop]['ask'])

    # Список карт
    def coupon_list(self, key, secret_key, max_count=None, offset=None):
        add_params = {}
        if max_count:
            new_params = {'max_count' : max_count}
            add_params.update(new_params)
        if offset:
            new_params = {'offset' : offset}
            add_params.update(new_params)
        return self.call_api(method='coupon.list', key=key, secret_key=secret_key, add_params=add_params)

    # Пополнение карты
    def coupon_apply(self, key, secret_key, amount, coupon, currency):
        add_params = {'amount': amount, 'coupon': coupon, 'currency': currency}
        return self.call_api(method='coupon.apply', key=key, secret_key=secret_key, add_params=add_params)

    # Создание карты
    def coupon_create(self, key, secret_key, amount, currency, password=None, receiver=None, comment=None):
        add_params = {'amount': amount, 'currency': currency}
        if password:
            new_param = {'password': password}
            add_params.update(new_param)
        if receiver:
            new_param = {'receiver': receiver}
            add_params.update(new_param)
        if comment:
            new_param = {'comment': comment}
            add_params.update(new_param)
        return self.call_api(method='coupon.create', key=key, secret_key=secret_key, add_params=add_params)

    # Активировать карту
    def coupon_redeem(self, key, secret_key, coupon, password=None):
        add_params = {'coupon': coupon}
        if password:
            new_param = {'password': password}
            add_params.update(new_param)
        return self.call_api(method='coupon.redeem', key=key, secret_key=secret_key, add_params=add_params)

    # Проверка карты
    def coupon_check(self, key, secret_key, coupon):
        add_params = {'coupon': coupon}
        return self.call_api(method='coupon.check', key=key, secret_key=secret_key, add_params=add_params)

    # Список майнингов
    def mining_list(self, key, secret_key, max_count=None, offset=None):
        if max_count == None:
            max_count = 15
        add_params = {'max_count': max_count}
        if offset:
            new_param = {'offset': offset}
            add_params.update(new_param)
        return self.call_api(method='mining.list', key=key, secret_key=secret_key, add_params=add_params)

    # Создание майнинга
    def mining_create(self, key, secret_key, amount, hold=None, description=None):
        add_params = {'amount': amount, 'hold': False, 'description': description}
        if hold:
            new_param = {'hold': hold}
            add_params.update(new_param)
        return self.call_api(method='mining.create', key=key, secret_key=secret_key, add_params=add_params)

    # Отменить счет
    def invoice_cancel(self, key, secret_key, uuid):
        add_params = {'uuid': uuid}
        return self.call_api(method='invoice.cancel', key=key, secret_key=secret_key, add_params=add_params)

    # Оплатить счет
    def invoice_apply(self, key, secret_key, uuid):
        add_params = {'uuid': uuid}
        return self.call_api(method='invoice.apply', key=key, secret_key=secret_key, add_params=add_params)

    # Создание счета
    def invoice_create(self, key, secret_key, currency, amount, executor=None, description=None, expire_at=None):
        print("def invoice create",
              "\ncurrency", currency,
              "\namount", amount,
              "\nexecutor", executor,
              "\ndescription", description,
              "\nexpire_at", currency,)
        add_params = {'currency': currency, 'amount': amount}
        if executor:
            print(1)
            new_param = {'executor': executor}
            add_params.update(new_param)
        if description:
            print(2)
            new_param = {'description': description}
            add_params.update(new_param)
        if expire_at:
            print(3)
            new_param = {'expire_at': expire_at}
            add_params.update(new_param)
        return self.call_api(method='invoice.create', key=key, secret_key=secret_key, add_params=add_params)

    # Список счетов
    def invoice_list(self, key, secret_key, is_executor=False, max_count=None, offset=None):
        add_params = {'is_executor': is_executor}
        if max_count:
            print('if max_count')
            new_param = {'max_count': max_count}
            add_params.update(new_param)
        if offset:
            print('if offset')
            new_param = {'offset': offset}
            add_params.update(new_param)
        return self.call_api(method='invoice.list', key=key, secret_key=secret_key, add_params=add_params)

    # Информация о счете
    def invoice_get(self, key, secret_key, uuid):
        add_params = {'uuid': uuid}
        return self.call_api(method='invoice.get', key=key, secret_key=secret_key, add_params=add_params)




cnx_api = cnx_api()