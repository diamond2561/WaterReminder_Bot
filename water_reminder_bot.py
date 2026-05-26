"""
💧 WaterReminderBot — Напоминалка пить воду
Первый бот в портфолио. Простой, полезный, рабочий.

Установка:
    pip install pyTelegramBotAPI schedule

Запуск:
    python water_bot.py

Перед запуском замени BOT_TOKEN на токен от @BotFather
"""

import telebot
import schedule
import time
import threading
import random
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# ── Настройки ──────────────────────────────────────────────
import os
BOT_TOKEN = os.getenv("BOT_TOKEN")# Получить у @BotFather

bot = telebot.TeleBot(BOT_TOKEN)

# ── Хранилище пользователей (в памяти, без БД) ─────────────
# Формат: { user_id: { "interval": 60, "active": True, "name": "Иван" } }
users = {}

# ── Фразы-напоминания ──────────────────────────────────────
REMINDERS = [
    "💧 Время выпить стакан воды! Твоё тело скажет спасибо.",
    "🌊 Не забывай про воду! Стакан прямо сейчас — и продолжай день.",
    "💦 Пора попить! Вода = энергия + концентрация.",
    "🥛 Стакан воды за 30 минут до еды — отличная привычка!",
    "🌿 Пьёшь достаточно воды? Один стакан прямо сейчас!",
    "⚡ Вода = топливо для мозга. Заправляйся!",
    "🏃 Если чувствуешь усталость — выпей воды. Это помогает!",
]

# ── Нормы воды по весу ──────────────────────────────────────
def calc_water(weight_kg: int) -> float:
    """Рекомендуемое количество воды в литрах."""
    return round(weight_kg * 0.033, 1)


# ── Клавиатуры ──────────────────────────────────────────────
def main_menu():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("▶️ Включить напоминания", callback_data="start_remind"),
        InlineKeyboardButton("⏸ Остановить",           callback_data="stop_remind"),
        InlineKeyboardButton("⏱ Изменить интервал",    callback_data="change_interval"),
        InlineKeyboardButton("💧 Моя норма воды",       callback_data="my_norm"),
        InlineKeyboardButton("ℹ️ О боте",               callback_data="about"),
    )
    return kb

def interval_menu():
    kb = InlineKeyboardMarkup(row_width=3)
    kb.add(
        InlineKeyboardButton("30 мин",  callback_data="interval_30"),
        InlineKeyboardButton("60 мин",  callback_data="interval_60"),
        InlineKeyboardButton("90 мин",  callback_data="interval_90"),
        InlineKeyboardButton("2 часа",  callback_data="interval_120"),
        InlineKeyboardButton("3 часа",  callback_data="interval_180"),
    )
    return kb


# ── Команды ─────────────────────────────────────────────────
@bot.message_handler(commands=["start"])
def cmd_start(message):
    user_id = message.from_user.id
    name = message.from_user.first_name or "друг"

    # Регистрируем пользователя если новый
    if user_id not in users:
        users[user_id] = {"interval": 60, "active": False, "name": name}

    text = (
        f"Привет, {name}! 👋\n\n"
        "Я помогу тебе не забывать пить воду 💧\n\n"
        "Обезвоживание — частая причина усталости, головной боли и плохой концентрации. "
        "Я буду напоминать тебе в нужное время!\n\n"
        "Выбери действие:"
    )
    bot.send_message(message.chat.id, text, reply_markup=main_menu())


@bot.message_handler(commands=["help"])
def cmd_help(message):
    text = (
        "📖 *Как пользоваться ботом:*\n\n"
        "▶️ *Включить* — начать получать напоминания\n"
        "⏸ *Остановить* — приостановить напоминания\n"
        "⏱ *Интервал* — как часто напоминать (30–180 мин)\n"
        "💧 *Моя норма* — рассчитать сколько воды нужно тебе\n\n"
        "Команды:\n"
        "/start — главное меню\n"
        "/help — эта справка\n"
        "/status — текущий статус"
    )
    bot.send_message(message.chat.id, text, parse_mode="Markdown")


@bot.message_handler(commands=["status"])
def cmd_status(message):
    user_id = message.from_user.id
    if user_id not in users:
        bot.send_message(message.chat.id, "Сначала нажми /start")
        return

    u = users[user_id]
    status = "✅ активны" if u["active"] else "⏸ остановлены"
    text = (
        f"📊 *Твой статус:*\n\n"
        f"Напоминания: {status}\n"
        f"Интервал: каждые {u['interval']} минут"
    )
    bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=main_menu())


# ── Обработчик кнопок ───────────────────────────────────────
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id

    # Убираем "часики" на кнопке
    bot.answer_callback_query(call.id)

    # Авторегистрация
    if user_id not in users:
        users[user_id] = {"interval": 60, "active": False, "name": call.from_user.first_name}

    u = users[user_id]

    # ── Включить напоминания
    if call.data == "start_remind":
        u["active"] = True
        bot.send_message(
            chat_id,
            f"✅ Напоминания включены! Буду писать каждые {u['interval']} минут.\n\n"
            "💡 Совет: поставь бота на видное место в уведомлениях.",
            reply_markup=main_menu()
        )

    # ── Остановить напоминания
    elif call.data == "stop_remind":
        u["active"] = False
        bot.send_message(
            chat_id,
            "⏸ Напоминания остановлены. Не забывай пить воду самостоятельно!\n"
            "Чтобы возобновить — нажми «Включить напоминания».",
            reply_markup=main_menu()
        )

    # ── Изменить интервал
    elif call.data == "change_interval":
        bot.send_message(
            chat_id,
            "⏱ Выбери как часто напоминать:",
            reply_markup=interval_menu()
        )

    # ── Установка интервала
    elif call.data.startswith("interval_"):
        minutes = int(call.data.split("_")[1])
        u["interval"] = minutes
        u["active"] = True
        bot.send_message(
            chat_id,
            f"✅ Отлично! Буду напоминать каждые {minutes} минут.",
            reply_markup=main_menu()
        )

    # ── Норма воды
    elif call.data == "my_norm":
        msg = bot.send_message(
            chat_id,
            "Введи свой вес в кг (например: 70):"
        )
        bot.register_next_step_handler(msg, process_weight)

    # ── О боте
    elif call.data == "about":
        bot.send_message(
            chat_id,
            "💧 *WaterReminderBot*\n\n"
            "Простой бот-напоминалка для тех, кто забывает пить воду.\n\n"
            "Средний человек выпивает на 30% меньше нормы. "
            "Этот бот помогает исправить привычку.\n\n"
            "Сделан как первый бот в портфолио 🤖",
            parse_mode="Markdown",
            reply_markup=main_menu()
        )


def process_weight(message):
    """Обработка введённого веса."""
    try:
        weight = int(message.text.strip())
        if weight < 20 or weight > 300:
            raise ValueError
        liters = calc_water(weight)
        glasses = int(liters * 1000 / 250)  # стаканов по 250 мл
        bot.send_message(
            message.chat.id,
            f"💧 *Твоя норма воды:*\n\n"
            f"При весе {weight} кг — примерно *{liters} литра* в день\n"
            f"Это около *{glasses} стаканов* по 250 мл\n\n"
            f"💡 Распредели равномерно в течение дня — и я помогу не забыть!",
            parse_mode="Markdown",
            reply_markup=main_menu()
        )
    except (ValueError, AttributeError):
        bot.send_message(
            message.chat.id,
            "❌ Введи число от 20 до 300 (например: 70)",
            reply_markup=main_menu()
        )


# ── Фоновый поток: рассылка напоминаний ────────────────────
def send_reminders():
    """Проверяет каждую минуту и отправляет напоминания нужным пользователям."""
    # Счётчик минут для каждого пользователя
    if not hasattr(send_reminders, "counters"):
        send_reminders.counters = {}

    for user_id, data in list(users.items()):
        if not data["active"]:
            continue

        # Инициализируем счётчик
        if user_id not in send_reminders.counters:
            send_reminders.counters[user_id] = 0

        send_reminders.counters[user_id] += 1

        # Пора отправить?
        if send_reminders.counters[user_id] >= data["interval"]:
            send_reminders.counters[user_id] = 0
            reminder = random.choice(REMINDERS)
            try:
                bot.send_message(user_id, reminder, reply_markup=main_menu())
            except Exception:
                # Пользователь заблокировал бота — убираем
                users.pop(user_id, None)


def run_scheduler():
    """Запуск фонового планировщика."""
    schedule.every(1).minutes.do(send_reminders)
    while True:
        schedule.run_pending()
        time.sleep(1)


# ── Запуск ──────────────────────────────────────────────────
if __name__ == "__main__":
    print("💧 WaterReminderBot запущен!")
    print("Нажми Ctrl+C для остановки\n")

    # Запускаем планировщик в отдельном потоке
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()

    # Запускаем бота (бесконечный polling)
    bot.infinity_polling(timeout=10, long_polling_timeout=5)