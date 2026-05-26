"""
💧 WaterReminderBot — Многоязычная напоминалка пить воду
Поддержка: 🇷🇺 Русский, 🇬🇧 English, 🇩🇪 Deutsch, 🇫🇷 Français, 🇸🇦 العربية
"""

import telebot
import schedule
import time
import threading
import random
import os
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

# ── Переводы ───────────────────────────────────────────────
TEXTS = {
    "ru": {
        "flag": "🇷🇺", "name": "Русский",
        "welcome": "Привет, {name}! 👋\n\nЯ помогу тебе не забывать пить воду 💧\n\nОбезвоживание — частая причина усталости и плохой концентрации.\n\nВыбери действие:",
        "reminders_on": "✅ Напоминания включены! Буду писать каждые {interval} минут.\n\n💡 Поставь бота на видное место в уведомлениях.",
        "reminders_off": "⏸ Напоминания остановлены.\nЧтобы возобновить — нажми «Включить напоминания».",
        "choose_interval": "⏱ Выбери как часто напоминать:",
        "interval_set": "✅ Буду напоминать каждые {interval} минут.",
        "enter_weight": "Введи свой вес в кг (например: 70):",
        "weight_result": "💧 *Твоя норма воды:*\n\nПри весе {weight} кг — примерно *{liters} литра* в день\nЭто около *{glasses} стаканов* по 250 мл\n\n💡 Распредели равномерно в течение дня!",
        "weight_error": "❌ Введи число от 20 до 300 (например: 70)",
        "about": "💧 *WaterReminderBot*\n\nПростой бот-напоминалка для тех, кто забывает пить воду.\n\nСредний человек выпивает на 30% меньше нормы.\n\nСделан как первый бот в портфолио 🤖",
        "status_active": "✅ активны",
        "status_paused": "⏸ остановлены",
        "status_text": "📊 *Твой статус:*\n\nНапоминания: {status}\nИнтервал: каждые {interval} минут",
        "choose_lang": "🌍 Выбери язык / Choose language:",
        "lang_set": "✅ Язык изменён на Русский 🇷🇺",
        "btn_start": "▶️ Включить",
        "btn_stop": "⏸ Остановить",
        "btn_interval": "⏱ Интервал",
        "btn_norm": "💧 Моя норма",
        "btn_about": "ℹ️ О боте",
        "btn_lang": "🌍 Язык",
        "reminders": [
            "💧 Время выпить стакан воды! Твоё тело скажет спасибо.",
            "🌊 Не забывай про воду! Стакан прямо сейчас — и продолжай день.",
            "💦 Пора попить! Вода = энергия + концентрация.",
            "🥛 Стакан воды за 30 минут до еды — отличная привычка!",
            "🌿 Пьёшь достаточно воды? Один стакан прямо сейчас!",
            "⚡ Вода = топливо для мозга. Заправляйся!",
            "🏃 Если чувствуешь усталость — выпей воды. Это помогает!",
        ],
    },
    "en": {
        "flag": "🇬🇧", "name": "English",
        "welcome": "Hello, {name}! 👋\n\nI'll help you remember to drink water 💧\n\nDehydration is a common cause of fatigue and poor concentration.\n\nChoose an action:",
        "reminders_on": "✅ Reminders enabled! I'll message you every {interval} minutes.\n\n💡 Pin me to your notifications!",
        "reminders_off": "⏸ Reminders stopped.\nTo resume — press «Enable reminders».",
        "choose_interval": "⏱ How often should I remind you?",
        "interval_set": "✅ I'll remind you every {interval} minutes.",
        "enter_weight": "Enter your weight in kg (e.g. 70):",
        "weight_result": "💧 *Your daily water norm:*\n\nFor {weight} kg — about *{liters} litres* per day\nThat's about *{glasses} glasses* of 250 ml\n\n💡 Spread it evenly throughout the day!",
        "weight_error": "❌ Please enter a number between 20 and 300 (e.g. 70)",
        "about": "💧 *WaterReminderBot*\n\nA simple reminder bot for those who forget to drink water.\n\nThe average person drinks 30% less than needed.\n\nBuilt as a portfolio project 🤖",
        "status_active": "✅ active",
        "status_paused": "⏸ paused",
        "status_text": "📊 *Your status:*\n\nReminders: {status}\nInterval: every {interval} minutes",
        "choose_lang": "🌍 Choose language:",
        "lang_set": "✅ Language changed to English 🇬🇧",
        "btn_start": "▶️ Enable",
        "btn_stop": "⏸ Stop",
        "btn_interval": "⏱ Interval",
        "btn_norm": "💧 My norm",
        "btn_about": "ℹ️ About",
        "btn_lang": "🌍 Language",
        "reminders": [
            "💧 Time to drink a glass of water! Your body will thank you.",
            "🌊 Don't forget to hydrate! A glass right now — then keep going.",
            "💦 Time to drink! Water = energy + focus.",
            "🥛 A glass of water 30 minutes before a meal is a great habit!",
            "🌿 Drinking enough water? One glass right now!",
            "⚡ Water = brain fuel. Fill up!",
            "🏃 Feeling tired? Drink some water. It helps!",
        ],
    },
    "de": {
        "flag": "🇩🇪", "name": "Deutsch",
        "welcome": "Hallo, {name}! 👋\n\nIch helfe dir, ans Wassertrinken zu denken 💧\n\nDehydration ist eine häufige Ursache für Müdigkeit und schlechte Konzentration.\n\nWähle eine Aktion:",
        "reminders_on": "✅ Erinnerungen aktiviert! Ich schreibe dir alle {interval} Minuten.\n\n💡 Pinne mich an deine Benachrichtigungen!",
        "reminders_off": "⏸ Erinnerungen gestoppt.\nZum Fortfahren — drücke «Erinnerungen aktivieren».",
        "choose_interval": "⏱ Wie oft soll ich dich erinnern?",
        "interval_set": "✅ Ich erinnere dich alle {interval} Minuten.",
        "enter_weight": "Gib dein Gewicht in kg ein (z.B. 70):",
        "weight_result": "💧 *Dein täglicher Wasserbedarf:*\n\nBei {weight} kg — ca. *{liters} Liter* pro Tag\nDas sind ca. *{glasses} Gläser* à 250 ml\n\n💡 Verteile es gleichmäßig über den Tag!",
        "weight_error": "❌ Bitte gib eine Zahl zwischen 20 und 300 ein (z.B. 70)",
        "about": "💧 *WaterReminderBot*\n\nEin einfacher Erinnerungsbot für alle, die vergessen Wasser zu trinken.\n\nDer Durchschnittsmensch trinkt 30% weniger als nötig.\n\nAls Portfolio-Projekt erstellt 🤖",
        "status_active": "✅ aktiv",
        "status_paused": "⏸ pausiert",
        "status_text": "📊 *Dein Status:*\n\nErinnerungen: {status}\nIntervall: alle {interval} Minuten",
        "choose_lang": "🌍 Sprache wählen:",
        "lang_set": "✅ Sprache auf Deutsch geändert 🇩🇪",
        "btn_start": "▶️ Aktivieren",
        "btn_stop": "⏸ Stoppen",
        "btn_interval": "⏱ Intervall",
        "btn_norm": "💧 Mein Bedarf",
        "btn_about": "ℹ️ Über den Bot",
        "btn_lang": "🌍 Sprache",
        "reminders": [
            "💧 Zeit, ein Glas Wasser zu trinken! Dein Körper wird es dir danken.",
            "🌊 Vergiss das Trinken nicht! Ein Glas jetzt — dann weiter.",
            "💦 Zeit zu trinken! Wasser = Energie + Konzentration.",
            "🥛 Ein Glas Wasser 30 Minuten vor dem Essen ist eine tolle Gewohnheit!",
            "🌿 Trinkst du genug? Jetzt ein Glas!",
            "⚡ Wasser = Gehirnkraftstoff. Auftanken!",
            "🏃 Müde? Trink Wasser. Es hilft!",
        ],
    },
    "fr": {
        "flag": "🇫🇷", "name": "Français",
        "welcome": "Bonjour, {name}! 👋\n\nJe t'aiderai à te souvenir de boire de l'eau 💧\n\nLa déshydratation est une cause fréquente de fatigue et de manque de concentration.\n\nChoisis une action:",
        "reminders_on": "✅ Rappels activés! Je t'écrirai toutes les {interval} minutes.\n\n💡 Épingle-moi dans tes notifications!",
        "reminders_off": "⏸ Rappels arrêtés.\nPour reprendre — appuie sur «Activer les rappels».",
        "choose_interval": "⏱ À quelle fréquence dois-je te rappeler?",
        "interval_set": "✅ Je te rappellerai toutes les {interval} minutes.",
        "enter_weight": "Entre ton poids en kg (ex: 70):",
        "weight_result": "💧 *Ta norme d'eau quotidienne:*\n\nPour {weight} kg — environ *{liters} litres* par jour\nC'est environ *{glasses} verres* de 250 ml\n\n💡 Répartis-le uniformément dans la journée!",
        "weight_error": "❌ Entre un nombre entre 20 et 300 (ex: 70)",
        "about": "💧 *WaterReminderBot*\n\nUn simple bot de rappel pour ceux qui oublient de boire de l'eau.\n\nLa personne moyenne boit 30% de moins que nécessaire.\n\nCréé comme projet de portfolio 🤖",
        "status_active": "✅ actifs",
        "status_paused": "⏸ en pause",
        "status_text": "📊 *Ton statut:*\n\nRappels: {status}\nIntervalle: toutes les {interval} minutes",
        "choose_lang": "🌍 Choisir la langue:",
        "lang_set": "✅ Langue changée en Français 🇫🇷",
        "btn_start": "▶️ Activer",
        "btn_stop": "⏸ Arrêter",
        "btn_interval": "⏱ Intervalle",
        "btn_norm": "💧 Ma norme",
        "btn_about": "ℹ️ À propos",
        "btn_lang": "🌍 Langue",
        "reminders": [
            "💧 Il est temps de boire un verre d'eau! Ton corps te remerciera.",
            "🌊 N'oublie pas de t'hydrater! Un verre maintenant — puis continue.",
            "💦 L'heure de boire! Eau = énergie + concentration.",
            "🥛 Un verre d'eau 30 minutes avant de manger — une excellente habitude!",
            "🌿 Tu bois assez? Un verre maintenant!",
            "⚡ L'eau = carburant pour le cerveau. Fais le plein!",
            "🏃 Tu te sens fatigué(e)? Bois de l'eau. Ça aide!",
        ],
    },
    "ar": {
        "flag": "🇸🇦", "name": "العربية",
        "welcome": "مرحباً، {name}! 👋\n\nسأساعدك على تذكر شرب الماء 💧\n\nالجفاف سبب شائع للتعب وضعف التركيز.\n\nاختر إجراءً:",
        "reminders_on": "✅ تم تفعيل التذكيرات! سأرسل لك كل {interval} دقيقة.\n\n💡 ثبّتني في إشعاراتك!",
        "reminders_off": "⏸ تم إيقاف التذكيرات.\nللاستئناف — اضغط «تفعيل التذكيرات».",
        "choose_interval": "⏱ كم مرة تريد أن أذكّرك؟",
        "interval_set": "✅ سأذكّرك كل {interval} دقيقة.",
        "enter_weight": "أدخل وزنك بالكيلوغرام (مثال: 70):",
        "weight_result": "💧 *كمية الماء اليومية الموصى بها:*\n\nلوزن {weight} كغ — حوالي *{liters} لتر* في اليوم\nأي حوالي *{glasses} كأس* سعة 250 مل\n\n💡 وزّعها على مدار اليوم!",
        "weight_error": "❌ أدخل رقماً بين 20 و 300 (مثال: 70)",
        "about": "💧 *WaterReminderBot*\n\nبوت تذكير بسيط لمن ينسى شرب الماء.\n\nالشخص العادي يشرب 30% أقل مما يحتاج.\n\nتم إنشاؤه كمشروع في المحفظة 🤖",
        "status_active": "✅ مفعّل",
        "status_paused": "⏸ متوقف",
        "status_text": "📊 *حالتك:*\n\nالتذكيرات: {status}\nالفاصل: كل {interval} دقيقة",
        "choose_lang": "🌍 اختر اللغة:",
        "lang_set": "✅ تم تغيير اللغة إلى العربية 🇸🇦",
        "btn_start": "▶️ تفعيل",
        "btn_stop": "⏸ إيقاف",
        "btn_interval": "⏱ الفاصل الزمني",
        "btn_norm": "💧 كميتي",
        "btn_about": "ℹ️ عن البوت",
        "btn_lang": "🌍 اللغة",
        "reminders": [
            "💧 حان وقت شرب كأس ماء! جسمك سيشكرك.",
            "🌊 لا تنسَ الترطيب! كأس الآن — ثم تابع يومك.",
            "💦 وقت الشرب! الماء = طاقة + تركيز.",
            "🥛 كأس ماء قبل 30 دقيقة من الأكل — عادة رائعة!",
            "🌿 هل تشرب كافياً؟ كأس واحدة الآن!",
            "⚡ الماء = وقود الدماغ. امتلئ!",
            "🏃 تشعر بالتعب؟ اشرب ماء. يساعد!",
        ],
    },
}

# ── Хранилище пользователей ────────────────────────────────
# { user_id: { "interval": 60, "active": False, "lang": "ru" } }
users = {}

def get_lang(user_id):
    return users.get(user_id, {}).get("lang", "ru")

def t(user_id, key, **kwargs):
    lang = get_lang(user_id)
    text = TEXTS[lang].get(key, TEXTS["ru"][key])
    return text.format(**kwargs) if kwargs else text


# ── Клавиатуры ──────────────────────────────────────────────
def main_menu(user_id):
    lang = get_lang(user_id)
    tx = TEXTS[lang]
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton(tx["btn_start"],    callback_data="start_remind"),
        InlineKeyboardButton(tx["btn_stop"],     callback_data="stop_remind"),
        InlineKeyboardButton(tx["btn_interval"], callback_data="change_interval"),
        InlineKeyboardButton(tx["btn_norm"],     callback_data="my_norm"),
        InlineKeyboardButton(tx["btn_about"],    callback_data="about"),
        InlineKeyboardButton(tx["btn_lang"],     callback_data="change_lang"),
    )
    return kb

def interval_menu(user_id):
    kb = InlineKeyboardMarkup(row_width=3)
    kb.add(
        InlineKeyboardButton("30 min",  callback_data="interval_30"),
        InlineKeyboardButton("60 min",  callback_data="interval_60"),
        InlineKeyboardButton("90 min",  callback_data="interval_90"),
        InlineKeyboardButton("2 h",     callback_data="interval_120"),
        InlineKeyboardButton("3 h",     callback_data="interval_180"),
    )
    return kb

def lang_menu():
    kb = InlineKeyboardMarkup(row_width=2)
    for code, data in TEXTS.items():
        kb.add(InlineKeyboardButton(
            f"{data['flag']} {data['name']}",
            callback_data=f"setlang_{code}"
        ))
    return kb


# ── Команды ─────────────────────────────────────────────────
@bot.message_handler(commands=["start"])
def cmd_start(message):
    user_id = message.from_user.id
    name = message.from_user.first_name or "friend"
    if user_id not in users:
        users[user_id] = {"interval": 60, "active": False, "lang": "ru"}
    bot.send_message(
        message.chat.id,
        t(user_id, "welcome", name=name),
        reply_markup=main_menu(user_id)
    )

@bot.message_handler(commands=["help"])
def cmd_help(message):
    user_id = message.from_user.id
    bot.send_message(message.chat.id, t(user_id, "about"), parse_mode="Markdown")

@bot.message_handler(commands=["status"])
def cmd_status(message):
    user_id = message.from_user.id
    if user_id not in users:
        bot.send_message(message.chat.id, "Use /start first")
        return
    u = users[user_id]
    status = t(user_id, "status_active") if u["active"] else t(user_id, "status_paused")
    bot.send_message(
        message.chat.id,
        t(user_id, "status_text", status=status, interval=u["interval"]),
        parse_mode="Markdown",
        reply_markup=main_menu(user_id)
    )


# ── Обработчик кнопок ───────────────────────────────────────
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    bot.answer_callback_query(call.id)

    if user_id not in users:
        users[user_id] = {"interval": 60, "active": False, "lang": "ru"}
    u = users[user_id]

    if call.data == "start_remind":
        u["active"] = True
        bot.send_message(chat_id, t(user_id, "reminders_on", interval=u["interval"]), reply_markup=main_menu(user_id))

    elif call.data == "stop_remind":
        u["active"] = False
        bot.send_message(chat_id, t(user_id, "reminders_off"), reply_markup=main_menu(user_id))

    elif call.data == "change_interval":
        bot.send_message(chat_id, t(user_id, "choose_interval"), reply_markup=interval_menu(user_id))

    elif call.data.startswith("interval_"):
        minutes = int(call.data.split("_")[1])
        u["interval"] = minutes
        u["active"] = True
        bot.send_message(chat_id, t(user_id, "interval_set", interval=minutes), reply_markup=main_menu(user_id))

    elif call.data == "my_norm":
        msg = bot.send_message(chat_id, t(user_id, "enter_weight"))
        bot.register_next_step_handler(msg, process_weight)

    elif call.data == "about":
        bot.send_message(chat_id, t(user_id, "about"), parse_mode="Markdown", reply_markup=main_menu(user_id))

    elif call.data == "change_lang":
        bot.send_message(chat_id, t(user_id, "choose_lang"), reply_markup=lang_menu())

    elif call.data.startswith("setlang_"):
        lang_code = call.data.split("_")[1]
        if lang_code in TEXTS:
            u["lang"] = lang_code
            bot.send_message(chat_id, TEXTS[lang_code]["lang_set"], reply_markup=main_menu(user_id))


def process_weight(message):
    user_id = message.from_user.id
    try:
        weight = int(message.text.strip())
        if weight < 20 or weight > 300:
            raise ValueError
        liters = round(weight * 0.033, 1)
        glasses = int(liters * 1000 / 250)
        bot.send_message(
            message.chat.id,
            t(user_id, "weight_result", weight=weight, liters=liters, glasses=glasses),
            parse_mode="Markdown",
            reply_markup=main_menu(user_id)
        )
    except (ValueError, AttributeError):
        bot.send_message(message.chat.id, t(user_id, "weight_error"), reply_markup=main_menu(user_id))


# ── Фоновый поток: рассылка напоминаний ────────────────────
def send_reminders():
    if not hasattr(send_reminders, "counters"):
        send_reminders.counters = {}

    for user_id, data in list(users.items()):
        if not data["active"]:
            continue
        if user_id not in send_reminders.counters:
            send_reminders.counters[user_id] = 0
        send_reminders.counters[user_id] += 1

        if send_reminders.counters[user_id] >= data["interval"]:
            send_reminders.counters[user_id] = 0
            lang = data.get("lang", "ru")
            reminder = random.choice(TEXTS[lang]["reminders"])
            try:
                bot.send_message(user_id, reminder)
            except Exception:
                users.pop(user_id, None)

def run_scheduler():
    schedule.every(1).minutes.do(send_reminders)
    while True:
        schedule.run_pending()
        time.sleep(1)


# ── Запуск ──────────────────────────────────────────────────
if __name__ == "__main__":
    print("💧 WaterReminderBot (multilingual) запущен!")
    print("Языки: 🇷🇺 🇬🇧 🇩🇪 🇫🇷 🇸🇦")
    print("Нажми Ctrl+C для остановки\n")
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()
    bot.infinity_polling(timeout=10, long_polling_timeout=5)