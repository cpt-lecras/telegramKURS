from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

# START keyboard
mainmenu = [
    [KeyboardButton(text="Добавить студента"),KeyboardButton(text="Добавить предмет"),KeyboardButton(text="Добавить оценку")],
    [KeyboardButton(text="Вывести студентов"),KeyboardButton(text="Вывести предметы"),KeyboardButton(text="Вывести оценки ученика")]
]
mainmenu = ReplyKeyboardMarkup(keyboard=mainmenu,resize_keyboard=True)
