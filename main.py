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
                start_time = datetime.strptime(object_person['date'] + ' ' + object_person['time'], '%m/%d/%y %H:%M:%S')
                end_time = start_time + timedelta(minutes=object_person['answerTime'])
                print(end_time)
                if datetime.now() > end_time:
                    print('Yes')
                    sheety_params = {
                        'sheet1': {
                            'answerTime': 'Ignored',
                        }
                    }
                    response_sheety = requests.put(url=sheety_endpoint + '/' + str(object_person['id']),
                                                   json=sheety_params, headers=headers_sheety)
                    # call to manager
                    message_to_manager = object_person['test'] + ' ' + str(object_person['telId']) + ' Ignored'
                    bot.send_message(MANAGER_TEL_ID, message_to_manager, reply_markup=start_markup())

                if object_person['answerTime'] not in ['Send', 'Ignored']:
                    message_to_user = object_person['test'] + ' ' + object_person['date'] + ' ' + object_person[
                        'time'] + ' ' + str(object_person['answerTime'])
                    bot.send_message(int(object_person['telId']), message_to_user,
                                     reply_markup=btn_yes_no(object_person['id']))
                    sheety_params = {
                        'sheet1': {
                            'answerTime': 'Send',
                        }
                    }
                    response_sheety = requests.put(url=sheety_endpoint + '/' + str(object_person['id']),
                                                   json=sheety_params,
                                                   headers=headers_sheety)
        time.sleep(10)


@bot.callback_query_handler(func=lambda call: True)
def function(call):
    splitted_data = call.data.split(' ')
    id_data = splitted_data[0]
    answer = splitted_data[1]

    response_sheety = requests.get(url=sheety_endpoint, headers=headers_sheety)
    notification_array = response_sheety.json()['sheet1']
    message_to_manager = ''
    for object_person in notification_array:
        if object_person['id'] == id_data:
            message_to_manager = object_person['test'] + ' ' + str(object_person['telId'])

    if answer == 'YES':
        sheety_params = {
            'sheet1': {
                'answerTime': 'Done',
            }
        }
        message_to_manager += ' Done'
    elif answer == 'NO':
        sheety_params = {
            'sheet1': {
                'answerTime': 'Not Done',
            }
        }
        message_to_manager += ' Not Done'

    response_sheety = requests.put(url=sheety_endpoint + '/' + id_data, json=sheety_params,
                                   headers=headers_sheety)
    # call to manager
    bot.send_message(MANAGER_TEL_ID, message_to_manager, reply_markup=start_markup())


# while True:
#     try:
bot.polling(none_stop=True)
# except Exception as e:
#     print(e)
#     continue
