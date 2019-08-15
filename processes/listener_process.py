import logging
import time

from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters

from config import config as cfg
from resources import examples
from utils.process_utils import DaemonProcess

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


class Messages:
    title_menu_main = 'Choose the option in main menu:'
    title_menu_add = 'Select resource to parse:'
    title_menu_resource = lambda x: f'Paste link on which you want to search items, e.g.: {x}'

    add_new_resource = 'Add new resource/page to parse'
    list_resources = 'List current resources'
    go_back = 'Go back'

    error_unknown_command = 'Sorry, I don\'t understand your command. Use /start to start'


def error_callback(bot, update, error):
    logging.error("Something wrong happened", error)


def get_chat_id(update):
    return (update.message or update.callback_query.message).chat_id


def main_menu_keyboard():
    keyboard = [[InlineKeyboardButton(Messages.add_new_resource, callback_data='m1')],
                [InlineKeyboardButton(Messages.list_resources, callback_data='m2')]]
    return InlineKeyboardMarkup(keyboard)


def add_menu_keyboard():
    keyboard = [[InlineKeyboardButton(name.upper(), callback_data=f'm1_{name}')] for i, name in enumerate(cfg.available_resources)]
    return InlineKeyboardMarkup(keyboard + [[InlineKeyboardButton(Messages.go_back, callback_data=f'main')]])


class ListenerProcess(DaemonProcess):
    def __init__(self):
        super(ListenerProcess, self).__init__(name="ListenerProcess")
        self.updater = None
        self.last_commands = {}

    def chat_start(self, update, context):
        context.bot.send_message(chat_id=get_chat_id(update), text=Messages.title_menu_main, reply_markup=main_menu_keyboard())

    def chat_add_menu(self, update, context):
        context.bot.send_message(chat_id=get_chat_id(update), text=Messages.title_menu_add, reply_markup=add_menu_keyboard())

    def chat_add_resource(self, update, context):
        resource_name = update.callback_query.data.split('_')[-1]
        chat_id = get_chat_id(update)
        self.last_commands[chat_id] = f'addresource_{resource_name}'
        context.bot.send_message(
            chat_id=chat_id,
            text=Messages.title_menu_resource(examples[resource_name]()),
            disable_web_page_preview=True
        )

    def chat_message(self, update, context):
        chat_id = get_chat_id(update)
        if self.last_commands.get(chat_id):
            command = self.last_commands[chat_id].split('_')[0]
            resource = self.last_commands[chat_id].split('_')[1]
            self.last_commands[chat_id] = None
            # add handling of different commands
            context.bot.send_message(chat_id=chat_id, text=f"Your command {command} on {resource}")
        else:
            context.bot.send_message(chat_id=chat_id, text=Messages.error_unknown_command)

    def target(self):
        self.updater = Updater(cfg.telegram_token, use_context=True)

        dispatcher = self.updater.dispatcher
        dispatcher.add_handler(CommandHandler('start', self.chat_start))
        dispatcher.add_handler(CallbackQueryHandler(self.chat_start, pattern='main'))
        dispatcher.add_handler(CallbackQueryHandler(self.chat_add_menu, pattern='^m1$'))
        dispatcher.add_handler(CallbackQueryHandler(self.chat_add_resource, pattern='m1_'))
        dispatcher.add_handler(MessageHandler(Filters.text, self.chat_message))
        dispatcher.add_error_handler(error_callback)
        self.updater.start_polling()

        while True:
            time.sleep(1)
