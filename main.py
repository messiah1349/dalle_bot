import os
import openai
from dataclasses import dataclass
from typing import Any
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters


@dataclass
class Response:
    """every backend method should return response object"""
    status: int  # 0 status - everything is good, else - there is error
    answer: Any  # result


openai.api_key = os.environ["DALLE_KEY"]
token = os.environ["DALLE_BOT_TOKEN"]


def get_image(promt: str) -> Response:
    try:
        response = openai.Image.create(prompt=promt, n=1, size="512x512")
        image_url = response['data'][0]['url']
        return Response(0, image_url)
    except Exception as e:
        return Response(-1, str(e))


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    user_id = update.message.from_user.id
    text = update.message.text
    response = get_image(text)
    if response.status < 0:
        await context.bot.send_message(chat_id=user_id, text=response.answer)
    else:
        await context.bot.send_photo(chat_id=user_id, photo=response.answer)


def main():
    application = Application.builder().token(token).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == '__main__':
    main()
