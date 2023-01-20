import telebot

from app.config import settings
from app.exceptions import ItemNotFound
from app.shops import shops


bot = telebot.TeleBot(settings.telegram_token)
keyboard = telebot.types.ReplyKeyboardMarkup()
all_button = telebot.types.KeyboardButton("Все магазины")
keyboard.row(*[telebot.types.KeyboardButton(shop_name) for shop_name in shops])
keyboard.row(all_button)
hideBoard = telebot.types.ReplyKeyboardRemove()


@bot.message_handler(commands=["start"])
def start(message: telebot.types.Message):
    bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name}, я помощник для поиска товаров на 'полках' известных маркетплейсов!")
    bot.send_message(message.chat.id, f"Используй команду /shops для вывода доступных магазинов.")

@bot.message_handler(commands=["shops"])
def get_shops(message: telebot.types.Message, text="Выберите магазин для поиска:"):
    ans = bot.send_message(
        chat_id=message.chat.id,
        text=text,
        reply_markup=keyboard,
    )
    bot.register_next_step_handler(ans, request)

def request(message: telebot.types.Message):
    shop_name = message.text
    ans = bot.send_message(
        message.chat.id, 
        text="Что вы хотите найти? Введите поисковый запрос (например: iphone 13 pro):",
        reply_markup=hideBoard
    )
    bot.register_next_step_handler(message, get_items, shop_name=shop_name)

def all_shops(request):
    results = []
    for shop in shops.values():
        try:
            results.extend(shop.get_items(request, 2))
        except ItemNotFound:
            pass
    return results

def get_items(message, shop_name: str="Все магазины"):
    is_not_found = False
    request = message.text
    bot.send_message(message.chat.id, f"Вы выбрали: {shop_name}\nВаш запрос: {request}\nЧерез пару минут мы пришлем вам подходящие варианты...")
    if shop_name in shops:
        try:
            items = shops[shop_name].get_items(request, 5)
        except ItemNotFound:
            is_not_found = True
    else:
        items = all_shops(request)
        if not len(items):
            is_not_found = True
    if is_not_found:
        bot.send_message(message.chat.id, "К сожалению, мы не смогли найти ничего подходящего, попробуйте уточнить запрос!")
    else:
        for item in items:
            caption = f"Описание: {item.name}\nСсылка: {item.url}\nЦена: {item.price}"
            bot.send_photo(message.chat.id, item.picture_url, caption=caption)
    get_shops(message, text="Если хотите повторить поиск, снова выберите магазин:")

if __name__ == "__main__":
    bot.infinity_polling()