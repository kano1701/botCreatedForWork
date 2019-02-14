import pymysql

MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASS = 'ubuntu'
MYSQL_DB = 'CNX'

class mysql():

    def __init__(self, HOST, USER, PASSWORD, DATABASE):
        self._host = HOST
        self._user = USER
        self._password = PASSWORD
        self._database = DATABASE

    def query(self, typeSQL, textSQL):
        print('->class MYSQL | def query')
        print("  textSQL", textSQL)
        connect = pymysql.connect(host=self._host, user=self._user, password=self._password,
                                  db=self._database, charset='utf8')
        sql = connect.cursor()
        sql.execute(textSQL)
        if typeSQL == 'select':
            return sql.fetchall()
        elif typeSQL == 'update' or typeSQL == 'insert':
            connect.commit()

    def select(self, entry, table, obj, obj_value):
        textSQL = 'SELECT {} FROM {} WHERE {} = {}'
        result = self.query('select', textSQL.format(entry, table, obj, obj_value))
        try:
            result[0][0]
            if entry == '*':
                return True
            elif entry != '*':
                return result[0][0]
        except:
            return False

    def update(self, table, column, column_value, obj, obj_value):
        textSQL = 'UPDATE {} SET {} = "{}" WHERE {} = {}'
        self.query('update', textSQL.format(table, column, column_value, obj, obj_value))

    def insert(self, table, columns, values):
        textSQL = 'INSERT INTO {} ({}) VALUES ({})'
        self.query('insert', textSQL.format(table, columns, values))

    def info(self, tg_id):
        print('class mysql | def info')
        textSQL = 'SELECT cryptonex_id, public_key, secret_key, status, language, telegram_id FROM user WHERE telegram_id = {}'
        print(textSQL.format(tg_id))
        result = self.query('select', textSQL.format(tg_id))
        if len(result) > 0:
            return {
                        'cryptonex_id': result[0][0],  'public': result[0][1], 'secret': result[0][2],
                        'status': result[0][3], 'language': result[0][4], 'telegram_id': result[0][5]
                    }


query = mysql(MYSQL_HOST, MYSQL_USER, MYSQL_PASS, MYSQL_DB)  # type: mysql