import os
import logging
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove
)
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler,
)

# === НАСТРОЙКИ ИЗ ПЕРЕМЕННЫХ ОКРУЖЕНИЯ ===
BOT_TOKEN = os.getenv('BOT_TOKEN', '7975067288:AAFTla7aHo16IZdTEUtGTlgfsyDxpG0FGi0')
ADMIN_CHAT_ID = int(os.getenv('ADMIN_CHAT_ID', '7302368349'))
TECH_SUPPORT_USERNAME = os.getenv('TECH_SUPPORT_USERNAME', '@Jishsl')
WEBSITE_URL = os.getenv('WEBSITE_URL', 'https://lidush2006.github.io/-_-/')

# Состояния анкеты
NAME, PHONE, RENT_TYPE, ADDRESS, ROOMS, DESCRIPTION, PRICE, PHOTOS = range(8)

# Логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


# Старт и главное меню
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [KeyboardButton("📝 Добавить объявление")],
        [KeyboardButton("🛠 Техподдержка"), KeyboardButton("🌐 Сайт")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    welcome_text = (
        "Здравствуйте, этот официальный бот сайта Рощинский Дом.\n\n"
        "Бот создан для удобного размещения ваших объявления с фотографией квартир "
        "на сайте Рощинский Дом. А также для обратной связи с администрацией сайта.\n\n"
        "Выберите необходимое вам действие:"
    )

    await update.message.reply_text(welcome_text, reply_markup=reply_markup)


# Обработка главного меню
async def main_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "📝 Добавить объявление":
        await update.message.reply_text(
            "👤 *Ваше имя (не обязательно можете поставить -)*\n_Пример: Иван_",
            parse_mode='Markdown',
            reply_markup=ReplyKeyboardRemove()
        )
        return NAME

    elif text == "🛠 Техподдержка":
        await update.message.reply_text(
            f"📞 Свяжитесь с нашей техподдержкой: {TECH_SUPPORT_USERNAME}\n"
            "Мы ответим вам в ближайшее время.",
            reply_markup=ReplyKeyboardMarkup([
                [KeyboardButton("📝 Добавить объявление")],
                [KeyboardButton("🛠 Техподдержка"), KeyboardButton("🌐 Сайт")]
            ], resize_keyboard=True)
        )
        return ConversationHandler.END

    elif text == "🌐 Сайт":
        await update.message.reply_text(
            f"🌐 Наш сайт: {WEBSITE_URL}",
            reply_markup=ReplyKeyboardMarkup([
                [KeyboardButton("📝 Добавить объявление")],
                [KeyboardButton("🛠 Техподдержка"), KeyboardButton("🌐 Сайт")]
            ], resize_keyboard=True)
        )
        return ConversationHandler.END

    else:
        await update.message.reply_text("Пожалуйста, используйте кнопки меню.")
        return ConversationHandler.END


# Шаг 1: Имя
async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['name'] = update.message.text
    await update.message.reply_text(
        "📞 *Ваш номер телефона*\n_Пример: +7 XXX XXX XX XX_",
        parse_mode='Markdown'
    )
    return PHONE


# Шаг 2: Телефон
async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['phone'] = update.message.text

    keyboard = [[KeyboardButton("🏠 Посуточно"), KeyboardButton("📅 Длительно")]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "🏠 *Как вы сдаете квартиру?*",
        parse_mode='Markdown',
        reply_markup=reply_markup
    )
    return RENT_TYPE


# Шаг 3: Тип аренды
async def get_rent_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['rent_type'] = update.message.text
    await update.message.reply_text(
        "📍 *Напишите адрес квартиры (не обязательно можете поставить -)*\n_Пример: Дом.13, кв.4_",
        parse_mode='Markdown',
        reply_markup=ReplyKeyboardRemove()
    )
    return ADDRESS


# Шаг 4: Адрес
async def get_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['address'] = update.message.text

    keyboard = [
        [KeyboardButton("1 комнатная"), KeyboardButton("2-х комнатная")],
        [KeyboardButton("3-х комнатная"), KeyboardButton("4-х комнатная")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "🛏 *Количество комнат*",
        parse_mode='Markdown',
        reply_markup=reply_markup
    )
    return ROOMS


# Шаг 5: Комнаты
async def get_rooms(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['rooms'] = update.message.text
    await update.message.reply_text(
        "📝 *Напишите описание квартиры для пользователей*",
        parse_mode='Markdown',
        reply_markup=ReplyKeyboardRemove()
    )
    return DESCRIPTION


# Шаг 6: Описание
async def get_description(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['description'] = update.message.text
    await update.message.reply_text(
        "💰 *Напишите цену (если цена Договорная напишите это)*\n_Пример: 25000 руб/мес  / Договорная",
        parse_mode='Markdown'
    )
    return PRICE


# Шаг 7: Цена
async def get_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['price'] = update.message.text
    await update.message.reply_text(
        "📸 *Отправьте фотографии квартиры*\n\n"
        "Можно отправить несколько фото. После отправки всех фото "
        "нажмите кнопку 'Готово'.",
        reply_markup=ReplyKeyboardMarkup([[KeyboardButton("✅ Готово")]], resize_keyboard=True)
    )
    return PHOTOS


# Шаг 8: Фотографии
async def get_photos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "✅ Готово":
        # Отправляем объявление админу
        return await send_to_admin(update, context)

    # Сохраняем фото
    if 'photos' not in context.user_data:
        context.user_data['photos'] = []

    if update.message.photo:
        # Берем самое большое фото
        photo_file = await update.message.photo[-1].get_file()
        context.user_data['photos'].append(photo_file.file_id)
        await update.message.reply_text("✅ Фото добавлено! Можно отправить еще или нажать 'Готово'.")

    return PHOTOS


# Отправка объявления админу
async def send_to_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = context.user_data

    # Формируем сообщение для админа
    message = (
        "🆕 *НОВОЕ ОБЪЯВЛЕНИЕ*\n\n"
        f"👤 *Имя:* {user_data['name']}\n"
        f"📞 *Телефон:* {user_data['phone']}\n"
        f"🏠 *Тип аренды:* {user_data['rent_type']}\n"
        f"📍 *Адрес:* {user_data['address']}\n"
        f"🛏 *Комнат:* {user_data['rooms']}\n"
        f"💰 *Цена:* {user_data['price']}\n"
        f"📝 *Описание:* {user_data['description']}\n\n"
        f"👤 *Отправитель:* @{update.effective_user.username or 'Нет username'}"
    )

    try:
        # Отправляем фото если есть
        if 'photos' in user_data and user_data['photos']:
            # Отправляем первое фото с описанием
            await context.bot.send_photo(
                chat_id=ADMIN_CHAT_ID,
                photo=user_data['photos'][0],
                caption=message,
                parse_mode='Markdown'
            )
            # Остальные фото без описания
            for photo_id in user_data['photos'][1:]:
                await context.bot.send_photo(chat_id=ADMIN_CHAT_ID, photo=photo_id)
        else:
            await context.bot.send_message(
                chat_id=ADMIN_CHAT_ID,
                text=message,
                parse_mode='Markdown'
            )

        # Сообщение пользователю
        success_message = (
            "✅ *Спасибо за объявление!*\n\n"
            "Мы уже отправили администрации сайта вашу анкету, "
            "в ближайшее время оно появится на нашем сайте.\n\n"
            "В случаи появления каких-нибудь проблем мы свяжемся с вами "
            "и сообщим об этом."
        )

        await update.message.reply_text(
            success_message,
            parse_mode='Markdown',
            reply_markup=ReplyKeyboardMarkup([
                [KeyboardButton("📝 Добавить объявление")],
                [KeyboardButton("🛠 Техподдержка"), KeyboardButton("🌐 Сайт")]
            ], resize_keyboard=True)
        )

    except Exception as e:
        logger.error(f"Ошибка отправки объявления: {e}")
        await update.message.reply_text(
            "❌ Произошла ошибка при отправке объявления. Попробуйте позже.",
            reply_markup=ReplyKeyboardMarkup([
                [KeyboardButton("📝 Добавить объявление")],
                [KeyboardButton("🛠 Техподдержка"), KeyboardButton("🌐 Сайт")]
            ], resize_keyboard=True)
        )

    # Очищаем данные пользователя
    context.user_data.clear()
    return ConversationHandler.END


# Отмена
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "❌ Создание объявления отменено.",
        reply_markup=ReplyKeyboardMarkup([
            [KeyboardButton("📝 Добавить объявление")],
            [KeyboardButton("🛠 Техподдержка"), KeyboardButton("🌐 Сайт")]
        ], resize_keyboard=True)
    )
    context.user_data.clear()
    return ConversationHandler.END


# Главная функция
def main():
    # Проверяем наличие токена
    if not BOT_TOKEN:
        print("❌ Ошибка: BOT_TOKEN не установлен!")
        return

    application = Application.builder().token(BOT_TOKEN).build()

    # ConversationHandler для создания объявления
    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.TEXT & filters.Regex("^📝 Добавить объявление$"), main_menu_handler)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
            RENT_TYPE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_rent_type)],
            ADDRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_address)],
            ROOMS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_rooms)],
            DESCRIPTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_description)],
            PRICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_price)],
            PHOTOS: [
                MessageHandler(filters.TEXT & filters.Regex("^✅ Готово$"), get_photos),
                MessageHandler(filters.PHOTO, get_photos)
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(conv_handler)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, main_menu_handler))

    print("✅ Бот запускается...")
    application.run_polling()


if __name__ == "__main__":
    main()