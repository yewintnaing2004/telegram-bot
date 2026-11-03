import telebot

# Bot Token ကို ထည့်သွင်းထားပါသည်
BOT_TOKEN = "9169151678:AAEbPtkAThVTd_TngxpbSufQRNj9JzlA3gg"
bot = telebot.TeleBot(BOT_TOKEN)

# /start ခေါ်ဆိုသည့်အခါ ပြန်မည့် စာသား
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "မင်္ဂလာပါရှင်။ 1xBet ငွေသွင်း/ငွေထုတ် လုပ်ငန်းများအတွက်\n\n"
        "KBZPay: **09682379570** (Ma Kay Thi Nwe) သို့ ငွေလွှဲပြီး "
        "Screenshot (သို့မဟုတ်) ငွေလွှဲရောက်ရှိကြောင်း အချက်အလက်များကို ပို့ပေးပါ။"
    )
    bot.reply_to(message, welcome_text, parse_mode="Markdown")

# ပုံ သို့မဟုတ် စာ ပို့လာပါက အလိုအလျောက် ပြန်မည့် စာသား
@bot.message_handler(content_types=['photo', 'text'])
def handle_incoming_messages(message):
    reply_text = "ငွေလွှဲချက် လက်ခံရရှိပါသည်။ စစ်ဆေးနေပါပြီ ခင်ဗျာ။"
    bot.reply_to(message, reply_text)

# Bot အမြဲတမ်း အလုပ်လုပ်နေစေရန်
print("Bot is running...")
bot.infinity_polling()
