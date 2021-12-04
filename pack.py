import pickle
import os

def save_obj(obj, name ):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)

while True:
    file_list_objects = input('LIST FILE: ')
    try:
        file_objects = (open('objects/'+file_list_objects+'.list', 'r', encoding="utf-8").read()).split('\n') #
        break
    except:
        print('ERROR READ LIST FILE')
        continue

class file_code():
    def __init__(self):
        self.files = []
        self.code = ''

file = file_code()

# получаем названия файлов с нужными объктами
for i in range(len(file_objects)-1): #
    file.files.append([file_objects[i], 0])
    print('IMPORT: ' + file_objects[i])

# чтение файлов содержащих в себе классы
for i in range(len(file.files)): #
    file_objects = open('objects/' + file.files[i][0], 'r', encoding="utf-8") #
    file.code += file_objects.read() + '\n' #
    file.files[i][1] = len(file.code.split('\n')) #
    file_objects.close() #

print('STRING: '  +str(len(file.code.split('\n')))) #
#os.system('pyinstaller main.py --icon=app.ico --onefile')
save_obj(file, file_list_objects)
