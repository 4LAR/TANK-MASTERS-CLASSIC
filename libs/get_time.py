#
#
#
#

import time

# получить текущее время
def get_time():
    return time.strftime("%H:%M:%S|%d-%m-%y", time.localtime())
