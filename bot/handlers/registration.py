from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from bot.states.registration_state import RegistrationState
from bot.utils.file_manager import save_to_csv
from aiogram.filters import Command
from datetime import datetime

router = Router()

@router.message(Command("start"))
async def start_registration(message: Message, state: FSMContext):
    state_data = await state.get_data()
    if state_data.get("registered"):
        await message.answer("Вы уже зарегистрированы! Используйте /menu для просмотра доступных команд.")
        return

    await message.answer("Привет! Данный бот поможет вам в тренировках йоги. Для начала давайте зарегистрируемся. Как вас зовут?")
    await state.set_state(RegistrationState.name)

@router.message(RegistrationState.name)
async def ask_experience(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Спасибо! Теперь, расскажите немного о вашем опыте йоги (выберите один из вариантов, пишите с маленькой буквы - новичок, средний, продвинутый):")
    await state.set_state(RegistrationState.experience)

@router.message(RegistrationState.experience)
async def ask_level(message: Message, state: FSMContext):
    await state.update_data(experience=message.text)
    await message.answer("Отлично! Теперь выберите ваш предпочтительный уровень тренировки (выберите один из вариантов, пишите с маленькой буквы - новичок, средний, продвинутый):")
    await state.set_state(RegistrationState.level)

@router.message(RegistrationState.level)
async def save_data(message: Message, state: FSMContext):
    data = await state.get_data()
    name = data.get("name")
    experience = data.get("experience")
    level = message.text
    user_id = message.from_user.id
    registration_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    save_to_csv(user_id, name, experience, level, registration_date)

    await message.answer(f"Регистрация завершена, {name}! Теперь вы можете начать тренировки. Используйте /menu для просмотра доступных команд.")
    await state.clear()
