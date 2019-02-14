import sys
from subprocess import call
import datetime

while True:
    try:
        print("\n\nвремя запуска", datetime.datetime.now())
        call([sys.executable, 'polling.py'], start_new_session=True)
    except KeyboardInterrupt:
        print("\n\nвремя ручного выключения", datetime.datetime.now())
        break
    else:
        print('\nперезапуск', datetime.datetime.now())
