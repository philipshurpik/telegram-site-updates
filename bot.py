import logging

from telegram.ext import MessageHandler, Filters, Updater, CommandHandler


def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")


def add(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="Please type a link to search what you want")


def echo(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text=update.message.text)


def init():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    updater = Updater('913916073:AAHPhzjibVt_6lMdrhUJZsm5RA7rFMgadEc', use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    add_handler = CommandHandler('add', add)
    echo_handler = MessageHandler(Filters.text, echo)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(add_handler)
    dispatcher.add_handler(echo_handler)

    updater.start_polling()


if __name__ == '__main__':
    init()
