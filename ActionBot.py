from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
    ContextTypes,
)
import random

# Этапы диалога
CHARACTERISTIC, DIFFICULTY = range(2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Привет! Я помогу вам проверить, справится ли ваш персонаж с действием.\n"
        "Пожалуйста, введите число характеристики вашего персонажа (от 0 до 10):"
    )
    return CHARACTERISTIC

async def get_characteristic(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        characteristic = int(update.message.text)
        if characteristic < 0 or characteristic > 10:
            raise ValueError("Характеристика должна быть в диапазоне от 0 до 10.")
        context.user_data['characteristic'] = characteristic
        await update.message.reply_text(
            "Спасибо! Теперь укажите сложность действия: легко, средне или сложно."
        )
        return DIFFICULTY
    except ValueError as e:
        await update.message.reply_text(f"Ошибка: {e}. Пожалуйста, введите корректное число от 0 до 10.")
        return CHARACTERISTIC

async def get_difficulty(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    difficulty = update.message.text.lower()
    if difficulty not in ["легко", "средне", "сложно"]:
        await update.message.reply_text(
            "Пожалуйста, выберите сложность: легко, средне или сложно."
        )
        return DIFFICULTY

    characteristic = context.user_data['characteristic']
    random_number = random.randint(1, 10)
    total = characteristic + random_number

    # Условия успеха
    success_threshold = {
        "легко": 5,
        "средне": 10,
        "сложно": 15,
    }[difficulty]

    if total > success_threshold:
        await update.message.reply_text(
            f"У вас получилось! (Характеристика: {characteristic}, Рандом: {random_number}, Итог: {total})"
        )
    else:
        await update.message.reply_text(
            f"Вы не справились, сожалею. (Характеристика: {characteristic}, Рандом: {random_number}, Итог: {total})"
        )
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Диалог отменен. Если захотите попробовать снова, введите /start.")
    return ConversationHandler.END

def main():
    # Создаем приложение
    application = Application.builder().token("7887151978:AAHofrYjXOvrWNqaTDTnTl7KH5KQl5chOeE").build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHARACTERISTIC: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_characteristic)],
            DIFFICULTY: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_difficulty)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)

    application.run_polling()

if __name__ == "__main__":
    main()
