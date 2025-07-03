import telebot
from deep_translator import GoogleTranslator
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


TOKEN = 'token'

bot = telebot.TeleBot(TOKEN)


SUPPORTED_LANGS_DICT  = {
    'uz': 'Uzbek',
    'en': 'English',
    'ru': 'Russian',
    'es': 'Spanish',
    'fr': 'French',
    'de': 'German',
    'zh-CN': 'Chinese (Simplified)',
    'ar': 'Arabic',
    'hi': 'Hindi',
    'ja': 'Japanese'
}

logging.info(f"Qo'lda yuklangan tillar soni: {len(SUPPORTED_LANGS_DICT)}")





@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    """Bot ishga tushganda yoki /help buyrug'i berilganda xabar yuborish"""
    bot.reply_to(message,
                 "Assalomu alaykum! Men Tarjimon botiman. Menga istalgan matnni yuboring, men uni boshqa tilga tarjima qilaman.\n"
                 "Ishlatish tartibi:\n"
                 "1. Matnni yuboring.\n"
                 "2. Agar tarjima tilini ko'rsatmoqchi bo'lsangiz, matndan keyin defis (-) bilan til kodini kiriting.\n"
                 "   Misol: Salom dunyo -en (o'zbekchadan inglizchaga tarjima qilish)\n"
                 "   Misol: Hello world -uz (inglizchadan o'zbekchaga tarjima qilish)\n"
                 "3. Agar til ko'rsatilmasa, men avtomatik ravishda ingliz tiliga tarjima qilaman.\n"
                 "Mavjud tillar uchun /tillar buyrug'ini bering.")


@bot.message_handler(commands=['tillar'])
def list_languages(message):
    """Qo'llab-quvvatlanadigan tillar ro'yxatini ko'rsatish"""

    lang_list = []
    for code, name in SUPPORTED_LANGS_DICT.items():
        lang_list.append(f"{code}: {name}")


    lang_list.sort()

    bot.reply_to(message,
                 "Qo'llab-quvvatlanadigan tillar (tarjima_qiladigan_so'zinggiz -til masalan salom -en):\n" + "\n".join(
                     lang_list))





@bot.message_handler(func=lambda message: True)
def translate_text(message):
    """Matnni tarjima qilish"""
    text_to_translate = message.text
    target_lang = 'en'
    source_lang = 'auto'

    if ' -' in text_to_translate:
        parts = text_to_translate.rsplit(' -', 1)
        text_to_translate = parts[0].strip()
        lang_code_input = parts[1].strip().lower()



        if lang_code_input == 'zh-cn':
            lang_code_input = 'zh-CN'

        if lang_code_input in SUPPORTED_LANGS_DICT:
            target_lang = lang_code_input
        else:
            bot.reply_to(message, "Kechirasiz, noto'g'ri til kodi. Avtomatik ravishda ingliz tiliga tarjima qilaman.\n"
                                  "Mavjud tillar uchun /tillar buyrug'ini bering.")
            logging.warning(f"Noto'g'ri til kodi kiritildi: {lang_code_input}")

    try:

        translator = GoogleTranslator(source=source_lang, target=target_lang)
        translated_text = translator.translate(text_to_translate)

        bot.reply_to(message, f"Tarjima (avtomatik aniqlangan til -> {target_lang}):\n\n{translated_text}")

    except Exception as e:
        bot.reply_to(message, f"Tarjima qilishda xatolik yuz berdi: {e}\n"
                              "Iltimos, matnni tekshirib qayta urinib ko'ring. Ehtimol internet aloqasi yo'qdir yoki tarjima xizmati vaqtincha ishlamayapti.")
        logging.error(f"Tarjima qilishda xato: {e}", exc_info=True)


bot.polling(none_stop=True)