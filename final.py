import os
import asyncio
from pathlib import Path
from dotenv import dotenv_values
from telebot.async_telebot import AsyncTeleBot
from revChatGPT.V1 import Chatbot
import aiohttp

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

# define a message handler to send a message when the bot receives any message
@bot.message_handler(func=lambda message: True)
async def send_gpt(message):
    print("Working with chatgpt")
    await bot.send_chat_action(message.chat.id, "typing")
    
    try:
        # generate response using Chatbot
        response = ""
        for data in chatbot.ask(message.text):
            response = data["message"]

        await bot.reply_to(message, response)
    except (aiohttp.ClientError, asyncio.TimeoutError):
        # if request fails, retry after 5 seconds
        print("Chatbot API request failed, retrying...")
        await asyncio.sleep(5)
        await send_gpt(message)

async def main():
    while True:
        try:
            await bot.polling(timeout=10*60)
        except Exception as e:
            print(f"Exception occurred during polling: {e}")
            await asyncio.sleep(5)

asyncio.run(main())
