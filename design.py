import telebot
from telebot import types
from utils import *

bot = telebot.TeleBot('...') #bot token

# State variable to keep track of user's state and storage variables for data
USER_STATE = "initial"
pnumber = None
username = None
email = None
ip_address = None
website = None
phish_website = None
name = None
lastname = None
id = None
terrorists = None
rand_person = None
start_num = None
end_num = None
rkey = None
tr_text = None

@bot.message_handler(commands=['start'])
def start_message(message):
    global USER_STATE
    if USER_STATE == "initial":
        markup = types.ReplyKeyboardMarkup(row_width=1)
        itembtn1 = types.KeyboardButton('📞📞 Search by phone number 📞📞')
        itembtn2 = types.KeyboardButton('☠️💀 Check a gmail/email being pwned ☠️💀')
        itembtn3 = types.KeyboardButton('👻👻 Generate name 👻👻')
        itembtn4 = types.KeyboardButton('👻👻 Generate user 👻👻')
        itembtn5 = types.KeyboardButton('0️⃣🔢 Generate numbers 🔢0️⃣')
        itembtn6 = types.KeyboardButton("🔀🔀 Generate any else('Phone', 'Email Address') 🔀🔀")
        itembtn7 = types.KeyboardButton('📚📚 Translate to english 📚📚')
        markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn6, itembtn7)
        bot.send_message(message.chat.id, "Choose an option:", reply_markup=markup)
    else:
        prev_button = types.KeyboardButton('Previous page')
        markup = types.ReplyKeyboardMarkup(row_width=1)
        markup.add(prev_button)
        bot.send_message(message.chat.id, "You are already in a search state. If you want to go back, use 'Previous page' button to go back.", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    global USER_STATE, pnumber, username, email, ip_address, website, phish_website, name, lastname, id, terrorists, rand_person, start_num, end_num, rkey, tr_text
    if message.text == 'Previous page':
        USER_STATE = "initial"
    try:
        if message.text == '☠️💀 Check a gmail/email being pwned ☠️💀':
            bot.reply_to(message,"Please,send me target gmail/email")
            USER_STATE = 'check_gmail'
        elif USER_STATE == 'check_gmail':
            email = message.text
            bot.reply_to(message, check_email_pwned(email))
            USER_STATE = "initial"
        elif message.text == '💻💻 Get all gmails connected with domain 💻💻':
            bot.reply_to(message,"Please,send me target domain")
            USER_STATE = 'domain_gmail'
        elif USER_STATE == 'domain_gmail':
            website = message.text
            bot.reply_to(message, email_search_by_url(website))
            USER_STATE = "initial"
        elif message.text == '👻👻 Generate name 👻👻':
            bot.reply_to(message, "Please, send me gender, name set and country. Must choose here.")
            bot.reply_to(message, rand_name_chooses())
            bot.reply_to(message, 'Example: Random, Australian, Australia')
            USER_STATE = 'rName'
        elif USER_STATE == 'rName':
            rand_person = message.text.split(', ')
            g, s, n = rand_person
            info = name_gen(g, s ,n)
            info_l = []
            for key in info:
                info_l.append(f"{key}: {info[key]}")
            bot.reply_to(message, '\n'.join(info_l))
            USER_STATE = "initial"
        elif message.text == '👻👻 Generate user 👻👻':
            bot.reply_to(message, f'{user_gen()}')
            USER_STATE = "initial"
        elif message.text == '0️⃣🔢 Generate numbers 🔢0️⃣':
            bot.reply_to(message, "Please, write start and end numbers. \nExample (first is start, second is end number)_ \n5 15")
            USER_STATE = 'rNum'
        elif USER_STATE == 'rNum':
            start_num, end_num = message.text.split(' ')
            bot.reply_to(message, f'{rand_num(int(start_num), int(end_num))}')
            USER_STATE = "initial"    
        elif message.text == "🔀🔀 Generate any else('Phone', 'Email Address') 🔀🔀":
            bot.reply_to(message, "Please, write what you want to search, phone or email.  \nFor phone number must write: Phone \nFor email address must write: Email Address")
            USER_STATE = 'rkey'
        elif USER_STATE == 'rkey':
            rkey = message.text
            bot.reply_to(message, f'{rand_any(rkey)}')
            USER_STATE = "initial"
        elif message.text == '📚📚 Translate to english 📚📚':
            bot.reply_to(message, "Please, send me text for translate")
            USER_STATE = 'tr_text'
        elif USER_STATE == 'tr_text':
            tr_text = message.text
            bot.reply_to(message, translate_text(tr_text))
            USER_STATE = "initial"
    except:
        bot.reply_to(message, "Please, try again.")
    start_message(message)

bot.polling()