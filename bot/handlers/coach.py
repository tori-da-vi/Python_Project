import aiohttp
import logging
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_gigachat.chat_models import GigaChat

# Инициализируем логирование
logging.basicConfig(level=logging.INFO)

GIGACHAT_API_URL = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
GIGACHAT_API_KEY = "MDVhZjBkMWEtYjJjZS00ZmJjLTkzZjUtMjVlOGUwODdmNmY4OmYwYTI0NDNlLWU0NWItNGU1MS04NTg5LWYzNGY2ZDY1ZTBhMQ=="

# Инициализация модели GigaChat
llm = GigaChat(
    credentials=GIGACHAT_API_KEY,
    scope="GIGACHAT_API_PERS",
    model="GigaChat",
    verify_ssl_certs=False,  # Отключаем SSL сертификаты
    streaming=False,
)

# Создаем роутер
router = Router()

# Сохраняем историю сообщений в списке
messages = [
    SystemMessage(content="Ты профессиональный йог-наставник, который консультирует своих учеников только в сфере йоги.")
]


# Обработчик команды /coach
@router.message(Command("coach"))
async def coach(message: Message):
    user_name = message.from_user.full_name
    await message.answer(
        f"Здравствуй, {user_name}! Меня зовут Пабло, я твой гуру йог! Готов ответить на все интересующие тебя вопросы!")
    await message.answer("Напиши мне свой вопрос:")


# Обработчик сообщений для чата с ИИ
@router.message()
async def handle_message(message: Message):
    user_input = message.text

    # Добавляем сообщение пользователя в историю
    messages.append(HumanMessage(content=user_input))

    # Получаем ответ от GigaChat
    try:
        res = llm.invoke(messages)
        # Добавляем ответ ИИ в историю
        messages.append(res)
        # Отправляем ответ пользователю
        await message.answer(res.content)
    except Exception as e:
        logging.error(f"Ошибка при получении ответа от GigaChat: {str(e)}")
        await message.answer("Произошла ошибка при получении ответа. Пожалуйста, попробуйте снова.")
