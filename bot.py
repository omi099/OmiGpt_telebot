import os
import asyncio
from pathlib import Path
from dotenv import dotenv_values
from telebot.async_telebot import AsyncTeleBot
from revChatGPT.V1 import Chatbot

# get config
parent_dir = Path(__file__).resolve().parent
config = dotenv_values(f"{parent_dir}/.env")

# init telegram bot
BOT_TOKEN = config["BOT_TOKEN"]
bot = AsyncTeleBot(BOT_TOKEN)

# init chatbot
chatbot = Chatbot(config={
    "email": config["CHATGPT_EMAIL"],
    "password": config["CHATGPT_PASSWORD"]
})

print("Chatbot & TeleBot initialized ")

# define a message handler to send a message when the command /start is issued
@bot.message_handler(commands=["start", "hello"])
async def send_welcome(message):
    await bot.reply_to(message, "Hello, how are you doing?")


# define a message handler to send a message when the command /gpt is issued
@bot.message_handler(commands=["gpt"])
async def send_gpt(message):
    print("Working with chatgpt")
    await bot.send_message(message.chat.id, "Working with chatgpt. Gimme a sec...")

    # generate response using Chatbot
    response = ""
    for data in chatbot.ask(message.text.replace("/gpt", "")):
        response += data["message"] + "\n"

    await bot.reply_to(message, response)


# run the bot
asyncio.run(bot.polling())
