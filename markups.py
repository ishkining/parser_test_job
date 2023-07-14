from telebot import types


def start_markup():
    btn_start = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_keyboard = types.KeyboardButton("/start")
    btn_start.add(btn_keyboard)
    return btn_start


def btn_yes_no():
    btn_choice = types.InlineKeyboardMarkup()
    btn_yes = types.InlineKeyboardButton("Да", callback_data="Да")
    btn_choice.add(btn_yes)
    btn_no = types.InlineKeyboardButton("Нет", callback_data="Нет")
    btn_choice.add(btn_no)
    return btn_choice
