from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters
from telegram.ext import Updater
from PIL import Image
import io
from novel_creator import *
import re

TOKEN = '2108061637:AAGLdTnmw5LACFQPeGjehC2U0JJDr2q9IsU'

user_dict = {}

def start(update: Update, context: CallbackContext):
    user_dict[update.effective_chat.id] = SceneData(update.effective_chat.id)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Привет! Я бот, который сделает вам сцену из визуальной новеллы. \n" +
                                                                    "Для этого пришлите мне 2 фотографии (без сжатия): \n" +
                                                                    "Фон с текстом в сообщении 'background' (ориентируйтесь на 1920x1080); \n" +
                                                                    "Персонажа с текстом в сообщении 'character' \n" +
                                                                    "После этого напишите 'make <текст_для_сцены>' ")
                                                                    

def set_background(update: Update, context: CallbackContext):
    file_image = context.bot.get_file(update.message.document)
    background_image = Image.open(io.BytesIO(file_image.download_as_bytearray()))
    user_dict[update.effective_chat.id].background = background_image
    context.bot.send_message(chat_id=update.effective_chat.id, text="Фон загружен.")

def set_character(update: Update, context: CallbackContext):
    file_image = context.bot.get_file(update.message.document)
    character_image = Image.open(io.BytesIO(file_image.download_as_bytearray()))
    user_dict[update.effective_chat.id].character = character_image
    context.bot.send_message(chat_id=update.effective_chat.id, text="Персонаж загружен.")

def make(update: Update, context: CallbackContext):
    text_search = re.search('^make (.*)', update.message.text, re.IGNORECASE)
    user_dict[update.effective_chat.id].text = text_search.group(1)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Ваш результат: ")
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=user_dict[update.effective_chat.id].createNovelScene())

def unknown(update: Update, context: CallbackContext):
    context.bot.sendMessage(chat_id=update.message.chat_id, text="Извините, я не понял команду.")

if __name__ == "__main__":
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    start_handler = CommandHandler('start', start)
    handler1 = MessageHandler(Filters.document & Filters.caption_regex("background"), set_background)
    handler2 = MessageHandler(Filters.document & Filters.caption_regex("character"), set_character)
    handler4 = MessageHandler(Filters.regex("^make (.*)"), make)
    handler_default = MessageHandler(Filters.command, unknown)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(handler1)
    dispatcher.add_handler(handler2)
    dispatcher.add_handler(handler4)
    dispatcher.add_handler(handler_default)

    updater.start_polling()

