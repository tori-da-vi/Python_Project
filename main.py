import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from bot.handlers import registration, schedule, workout, workout_history, feedback  # Импортируем другие роутеры
from bot.middleware.registration_middleware import RegistrationMiddleware
from bot.handlers.menu import router as menu_router
from bot.handlers.coach import router as coach_router

# Настроим логирование
logging.basicConfig(level=logging.INFO)

API_TOKEN = "8172487665:AAF_1slvsHesQEPdWbkDCpqgf43PmgL2ffs"

async def main():
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    dp.message.middleware(RegistrationMiddleware())  # Подключаем middleware для проверки регистрации

    # Регистрируем роутеры
    dp.include_router(registration.router)
    dp.include_router(schedule.router)
    dp.include_router(workout.router)
    dp.include_router(workout_history.router)
    dp.include_router(feedback.router)
    dp.include_router(menu_router)
    dp.include_router(coach_router)

    logging.info("Бот запущен и слушает команды.")

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
