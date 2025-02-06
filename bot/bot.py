import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from bot.config import TELEGRAM_BOT_TOKEN, WHITE_LIST  # Импорт конфигурации из папки bot
from api.config import IMEI_CHECK_API_TOKEN, IMEI_CHECK_API_URL, SERVICE_ID  # Импорт конфигурации из папки api

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

def check_imei(imei: str):
    headers = {
        "Authorization": f"Bearer {IMEI_CHECK_API_TOKEN}",
        "Accept-Language": "en",
        "Content-Type": "application/json"
    }
    data = {"deviceId": imei, "serviceId": SERVICE_ID}

    response = requests.post(IMEI_CHECK_API_URL, json=data, headers=headers)
    return response.json()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in WHITE_LIST:
        await update.message.reply_text("Вы не в белом списке!")
        return
    await update.message.reply_text("Отправьте IMEI для проверки.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in WHITE_LIST:
        await update.message.reply_text("Вы не в белом списке!")
        return

    imei = update.message.text.strip()
    if len(imei) != 15 or not imei.isdigit():
        await update.message.reply_text("Некорректный IMEI! Введите 15-значный номер.")
        return

    result = check_imei(imei)

    logger.info(f"Ответ от API: {result}")

    if "error" in result:
        await update.message.reply_text(f"Ошибка: {result['error']}")
    elif "id" in result:
        device_name = result.get("properties", {}).get("deviceName", "Неизвестно")
        model_desc = result.get("properties", {}).get("modelDesc", "Неизвестно")
        imei_info = result.get("properties", {}).get("imei", "Неизвестно")
        usa_block_status = result.get("properties", {}).get("usaBlockStatus", "Неизвестно")
        sim_lock = result.get("properties", {}).get("simLock", "Неизвестно")
        replacement_status = result.get("properties", {}).get("replacement", "Неизвестно")

        await update.message.reply_text(
            f"Проверка IMEI {imei} успешна!\n"
            f"ID проверки: {result['id']}\n"
            f"Статус: {result['status']}\n"
            f"Название устройства: {device_name}\n"
            f"Модель: {model_desc}\n"
            f"IMEI устройства: {imei_info}\n"
            f"Состояние блокировки в США: {usa_block_status}\n"
            f"SIM Lock: {'Да' if sim_lock else 'Нет'}\n"
            f"Статус замены: {'Да' if replacement_status else 'Нет'}\n"
            f"Изображение устройства: {result.get('properties', {}).get('image', 'Не доступно')}"
        )
    else:
        await update.message.reply_text("❌ Не удалось получить информацию по IMEI.")


def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
