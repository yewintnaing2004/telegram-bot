import telebot
from telebot import types

# Bot Token ကို ထည့်သွင်းထားပါသည်
BOT_TOKEN = "9169151678:AAEbPtkAThVTd_TngxpbSufQRNj9JzlA3gg"
bot = telebot.TeleBot(BOT_TOKEN)

# သိမ်းဆည်းရန် ယာယီနေရာ (User State)
user_states = {}

# /start နှိပ်သည့်အခါ ငွေသွင်း သို့မဟုတ် ငွေထုတ် ရွေးချယ်ခိုင်းရန်
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_deposit = types.InlineKeyboardButton("📥 ငွေသွင်းမည်", callback_data="deposit")
    btn_withdraw = types.InlineKeyboardButton("📤 ငွေထုတ်မည်", callback_data="withdraw")
    markup.add(btn_deposit, btn_withdraw)
    
    welcome_text = (
        "✨ မင်္ဂလာပါရှင် 🙏✨\n\n"
        "KBZPay ငွေသွင်း/ငွေထုတ် ဝန်ဆောင်မှုမှ ကြိုဆိုပါတယ်။\n"
        "ပြုလုပ်လိုသော ဝန်ဆောင်မှုကို အောက်ပါခလုတ်များမှ ရွေးချယ်ပေးပါရှင် 👇"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup, parse_mode="Markdown")

# ခလုတ်နှိပ်မှုကို လက်ခံစစ်ဆေးခြင်း
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    chat_id = call.message.chat.id
    if call.data == "deposit":
        user_states[chat_id] = "waiting_deposit_id"
        bot.answer_callback_query(call.id)
        bot.send_message(chat_id, "📥 **ငွေသွင်းခြင်း** အတွက် ကျေးဇူးပြု၍ သင်၏ **1xBet ID** လေးကို ပို့ပေးပါရှင် 💬", parse_mode="Markdown")
    
    elif call.data == "withdraw":
        user_states[chat_id] = "waiting_withdraw_id"
        bot.answer_callback_query(call.id)
        bot.send_message(chat_id, "📤 **ငွေထုတ်ခြင်း** အတွက် ပထမဦးစွာ သင်၏ **1xBet ID** လေးကို ပို့ပေးပါရှင် 💬", parse_mode="Markdown")

# စာ သို့မဟုတ် ပုံ ပို့လာသည့်အခါ အခြေအနေအလိုက် တုံ့ပြန်ခြင်း
@bot.message_handler(content_types=['text', 'photo'])
def handle_messages(message):
    chat_id = message.chat.id
    state = user_states.get(chat_id)
    
    # 1) ငွေသွင်းရန် ID တောင်းနေစဉ်
    if state == "waiting_deposit_id":
        user_states[chat_id] = "waiting_deposit_slip"
        bot.reply_to(message, (
            "ကျေးဇူးတင်ပါတယ်ရှင် 🙏\n\n"
            "💳 **ငွေလွှဲရန် အကောင့်အချက်အလက်**\n"
            "• KBZPay နံပါတ်: **09682379570**\n"
            "• အကောင့်အမည်: **Ma Kay Thi Nwe**\n\n"
            "ငွေလွှဲပြီးပါက Screenshot (သို့မဟုတ်) ငွေလွှဲရောက်ရှိကြောင်း အချက်အလက်ကို ပို့ပေးပါရှင် 📸"
        ), parse_mode="Markdown")
    
    # 2) ငွေသွင်းရန် စလစ်ပုံ သို့မဟုတ် အချက်အလက် ပို့သည့်အခါ
    elif state == "waiting_deposit_slip":
        user_states.pop(chat_id, None)
        bot.reply_to(message, "✅ ငွေလွှဲချက် လက်ခံရရှိပါပြီရှင်။ စစ်ဆေးပြီး အမြန်ဆုံး ဖြည့်တင်းပေးပါမယ်နော် ✨")

    # 3) ငွေထုတ်ရန် ID ရပြီးပါက ထုတ်မယ့်ပမာဏ တောင်းခံရန်
    elif state == "waiting_withdraw_id":
        user_states[chat_id] = f"waiting_withdraw_amount_{message.text}"
        bot.reply_to(message, "💰 ထုတ်ယူလိုသည့် ပမာဏ (ငွေပမာဏ) ကို ထပ်မံ ပို့ပေးပါရှင် ✍️")

    # 4) ငွေထုတ်မယ့်ပမာဏ ရရှိသွားပါက လွှဲရန်အချက်အလက်ပေးပြီး စစ်ဆေးရန်
    elif state and state.startswith("waiting_withdraw_amount_"):
        user_states.pop(chat_id, None)
        bot.reply_to(message, (
            "✅ ထုတ်ယူရန် အချက်အလက်များကို လက်ခံရရှိပါပြီရှင်။\n\n"
            "ကျေးဇူးပြု၍ လွှဲပြောင်းပေးရမည့် အောက်ပါအကောင့်သို့ ငွေလွှဲပေးပါရန် 🔽\n"
            "• KBZPay နံပါတ်: **09682379570**\n"
            "• အကောင့်အမည်: **Ma Kay Thi Nwe**\n\n"
            "ငွေလွှဲပြီးပါက စလစ် (သို့) အချက်အလက် ပို့ပေးပါ၊ စစ်ဆေးပြီး ငွေထုတ်ပေးပါမည်ရှင် 🔍✨"
        ), parse_mode="Markdown")
    
    else:
        # ပုံမှန် အနေအထား (သို့မဟုတ်) /start ပြန်စရန်
        bot.reply_to(message, "စတင်ရန် `/start` ကို နှိပ်ပေးပါရှင် 😊", parse_mode="Markdown")

# Bot အမြဲတမ်း အလုပ်လုပ်နေစေရန်
print("Bot is running smoothly...")
bot.infinity_polling()
