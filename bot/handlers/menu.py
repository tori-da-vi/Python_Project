import logging
from aiogram import Router
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command

# Настроим логирование
logging.basicConfig(level=logging.INFO)

router = Router()

# Обработчик команды /menu
@router.message(Command("menu"))
async def show_menu(message):
    logging.info("Команда /menu активирована")  # Логирование для проверки

    # Создаём кнопки с текстом
    button1 = KeyboardButton(text="/schedule")
    button2 = KeyboardButton(text="/workout")
    button3 = KeyboardButton(text="/workoutHistory")
    button4 = KeyboardButton(text="/feedback")
    button5 = KeyboardButton(text="/coach")

    # Создаём клавиатуру и добавляем кнопки
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [button1, button2],  # Строка с кнопками
            [button3, button4],  # Строка с кнопками
            [button5]  # Строка с кнопками
        ],
        resize_keyboard=True  # Автоматическое изменение размера клавиатуры
    )

    # Отправляем сообщение с клавиатурой
    await message.answer("Доступные команды:", reply_markup=keyboard)