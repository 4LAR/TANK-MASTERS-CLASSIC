#
#
#
#

import pickle

# сохранение объекта в файл
def save_obj(obj, name):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

# загрузка объекта из файла
def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)
