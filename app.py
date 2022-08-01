import telebot

from app import config as cfg


bot = telebot.TeleBot(cfg.TOKEN)


@bot.message_handler(content_types=["text"])
def echo(message: telebot.types.Message):
    bot.send_message(message.chat.id, message.text)


if __name__ == "__main__":
    bot.infinity_polling()