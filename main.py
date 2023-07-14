import time
from datetime import datetime, timedelta
import requests
import telebot

from markups import *

token = '6340678324:AAEovBkPOIeDgBqsEuQ2UEW98lnBqusDlbU'
bot = telebot.TeleBot(token)

API_KEY_SHEETY = '8ed630f07c99b091084d4d43d4c23500'
NAME_OF_SHEET = 'testJobForParser'
headers_sheety = {
    'Authorization': 'Basic aXNoa2luaW5nOmlzaGtpbmluZw==',
}

MANAGER_TEL_ID = ''
sheety_endpoint = f'https://api.sheety.co/{API_KEY_SHEETY}/{NAME_OF_SHEET}/sheet1'


@bot.message_handler(commands=['start'])
def start(message):
    message_to_user = 'Добро пожаловать в бот напоминаниий!'
    bot.send_message(message.chat.id, message_to_user, reply_markup=start_markup())
    while True:
        response_sheety = requests.get(url=sheety_endpoint, headers=headers_sheety)
        notification_array = response_sheety.json()['sheet1']
        for object_person in notification_array:
            if object_person['answerTime'] not in ['Done', 'Not Done', 'Ignored']:
                print(object_person)
                start_time = datetime.strptime('07/14/23 13:55:26', '%m/%d/%y %H:%M:%S')
                end_time = start_time + timedelta(0, 60 * object_person['answerTime'])
                print(end_time)
                if datetime.now() > end_time:
                    print('Yes')
                    sheety_params = {
                        'sheet1': {
                            'answerTime': 'Ignored',
                        }
                    }
                    response_sheety = requests.put(url=sheety_endpoint + '/' + str(object_person['id']), json=sheety_params, headers=headers_sheety)
                    # call to manager
                    message_to_manager = object_person['test'] + ' ' + str(object_person['telId']) + ' Ignored'
                    bot.send_message(MANAGER_TEL_ID, message_to_manager, reply_markup=start_markup())

                message_to_user = object_person['test'] + ' ' + object_person['date'] + ' ' + object_person[
                    'time'] + ' ' + str(object_person['answerTime'])
                bot.send_message(int(object_person['telId']), message_to_user, reply_markup=btn_yes_no())
        time.sleep(10)


@bot.callback_query_handler(func=lambda call: True)
def function(call):
    if call.data == 'Да':
        message_to_user = 'Да!'
        bot.send_message(call.message.chat.id, message_to_user, reply_markup=start_markup())
    elif call.data == 'Нет':
        message_to_user = 'Нет!'
        bot.send_message(call.message.chat.id, message_to_user, reply_markup=start_markup())



# while True:
#     try:
bot.polling(none_stop=True)
# except Exception as e:
#     print(e)
#     continue
