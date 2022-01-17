import telebot
import os
import time
from time import sleep
import ftplib

from win10toast import ToastNotifier
n = ToastNotifier()
title_message = 'Помошник'
time_of_show = 10
icon_path = 'logo.ico'



os.system('cls')
#######################################################################
#######################################################################
bot = telebot.TeleBot("ТОКЕН")
#######################################################################
#######################################################################
def debug(text):
    print(f'Дебаг - {text}')
#######################################################################
#######################################################################
def get_sec():
    sec = str(time.localtime().tm_sec)
    debug(sec)
    return sec
#######################################################################
#######################################################################
print(f'тест функции get_sec. Результат: {get_sec()}')
#######################################################################

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, '''
Приветсвую тебя!
Для начала работы ознакомся с инструкцией:

1 - отправь сообщение с номером документа.
2 - сделай PDF со всеми фотографиями.
3 - после перешли в бота.
Всё! И заного =)

p.s по всем вопросам просьба обращаться в телеграм @palapalaru
        ''')


#######################################################################
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    global client
    client = message.text
    debug(client)
    debug(message.from_user.id)
    debug(message.from_user.first_name)
    debug(message.from_user.last_name)
    debug(message.from_user.username)

    mess = f'{message.from_user.username} работает над документом {client}'
    n.show_toast(title_message, mess, duration = time_of_show, icon_path =icon_path)

    bot2 = telebot.TeleBot("ТОКЕН")
    bot2.send_message('ID в telegram', mess)

    if len(client) > 1:
        if client.isdigit():
            bot.reply_to(message, f'Работаем с договором {client}')
            sleep(1)
            bot.reply_to(message, f'Теперь жду сообщение с файлом для дальнейшей работы.')
        else:
            bot.reply_to(message, 'Я же говорил введите цифры! Заного...')
    else:
            bot.reply_to(message, 'Что-то пошло не так... Активируйте заного бота и начните сначала!')
##############################################################################################################################################
##############################################################################################################################################
##############################################################################################################################################
##############################################################################################################################################
@bot.message_handler(content_types=['photo'])
def photo(message):
    print('message.photo =', message.photo)
    fileID = message.photo[-1].file_id
    print('fileID =', fileID)
    file_info = bot.get_file(fileID)
    print('file.file_path =', file_info.file_path)
    downloaded_file = bot.download_file(file_info.file_path)

    with open("image.jpg", 'wb') as new_file:
        new_file.write(downloaded_file)

    debug(client)    
    currect_pic = f'{client}.jpg'
    debug(currect_pic)
    
    os.rename('image.jpg', currect_pic)
    

    session = ftplib.FTP('IP FTP сервера', 'ЛОГИН', 'ПАРОЛЬ')

    with session as ftp:

        x=[]
        session.dir('-d', lambda L:x.append(L.split()[-1]))
        print(x)
        
        if client not in x:

            session.sendcmd('cwd from_telegram_bot')
            session.mkd(client)
            session.sendcmd(f'cwd {client}')

            

            filename = currect_pic
            filepath = r'C:\\{}'.format(filename)
            file_object = open(filepath, 'rb')
    
           
            session.storbinary(f'STOR {filename}', file_object)
            session.close()
            bot.reply_to(message, f'Папка создана для клиента {client}, фото загруженно. Можете работать дальше. Спасибо!')

            file_object.close()
            path = filepath
            os.remove(path)


            

        else:

            new_cl = f'{get_sec()} - {currect_pic}'

            os.rename(currect_pic, new_cl)

            filename = new_cl
            filepath = r'C:\\{}'.format(filename)
            file_object = open(filepath, 'rb')


            bot.reply_to(message, f'Папка {client} уже есть, сейчас добавим файл в данную папку.')
            session.sendcmd(f'cwd {client}')
            
            session.storbinary(f'STOR {filename}', file_object)
            session.close()
            bot.reply_to(message, f'Фото загружены. Можете работать дальше. Спасибо!')
            

            file_object.close()   
            path = filepath
            os.remove(path)
##############################################################################################################################################
##############################################################################################################################################
##############################################################################################################################################
##############################################################################################################################################
@bot.message_handler(content_types=['document'])
def handle_file(message):
    try:
        chat_id = message.chat.id
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        src = message.document.file_name;
        with open(f'{client}.pdf', 'wb') as new_file:
            new_file.write(downloaded_file)
        bot.reply_to(message, "Ваш файл принят в обработку.")

        session = ftplib.FTP('IP FTP сервера', 'ЛОГИН', 'ПАРОЛЬ')

        with session as ftp:

            session.sendcmd('cwd from_telegram_bot')

            x=[]
            session.dir('-d', lambda L:x.append(L.split()[-1]))
            print(x)

            if client not in x:

                session.mkd(client)

                session.sendcmd(f'cwd {client}')

                filename = f'{client}.pdf'
                filepath = r'C:\\{}'.format(filename)
                file_object = open(filepath, 'rb')

                y=[]
                session.dir('-d', lambda L:y.append(L.split()[-1]))
                print(y)
                
                if filename not in y:

                    session.storbinary(f'STOR {filename}', file_object)
                    session.close()
                    bot.reply_to(message, f'Папка создана для клиента {client}, файл загружен. Можете работать дальше. Спасибо!')

                    file_object.close()
                    path = filepath
                    os.remove(path)

                else:

                    rename = f'{get_sec()} - {client}.pdf'

                    os.rename(f'{client}.pdf', rename)

                    filename = rename
                    filepath = r'C:\\{}'.format(filename)
                    file_object = open(filepath, 'rb')

                    session.storbinary(f'STOR {filename}', file_object)
                    session.close()

                    file_object.close()
                    path = filepath
                    os.remove(path)
                    bot.reply_to(message, f'Файл уже есть с таким названием, файл переименновали и загрузили. Можете работать дальше. Спасибо!')


            else:

                session.sendcmd(f'cwd {client}')

                z=[]
                session.dir('-d', lambda L:z.append(L.split()[-1]))
                print(z)

                filename = f'{client}.pdf'
                filepath = r'C:\\{}'.format(filename)
                file_object = open(filepath, 'rb')

                if filename not in z:

                    session.storbinary(f'STOR {filename}', file_object)
                    session.close()
                    bot.reply_to(message, f'Папка уже была создана для клиента {client}, файл загружен. Можете работать дальше. Спасибо!')

                    file_object.close()
                    path = filepath
                    os.remove(path) 

                else:
                    file_object.close()
                    rename = f'{get_sec()} - {client}.pdf'

                    os.rename(f'{client}.pdf', rename)

                    filename = rename
                    filepath = r'C:\\{}'.format(filename)
                    file_object = open(filepath, 'rb')

                    session.storbinary(f'STOR {filename}', file_object)
                    session.close()

                    file_object.close()
                    path = filepath
                    os.remove(path)
                    bot.reply_to(message, f'Папка уже была создана для клиента {client}, файл переименновали и загрузили. Можете работать дальше. Спасибо!')

    except Exception as e:
        bot.reply_to(message, e)


##############################################################################################################################################      
##############################################################################################################################################
##############################################################################################################################################
##############################################################################################################################################
if __name__ == '__main__':
    bot.polling(none_stop=True)