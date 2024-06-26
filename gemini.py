"""
Author: Yugraj Vishwakarma
Telegram: https://t.me/Scorpion_Yug
"""

import os
import io
import logging
import PIL.Image
import google.generativeai as genai
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode, ChatActions
from aiogram.utils import executor

os.system("pip install aiogram==2.25.1 Pillow google-generativeai")

# Create the bot object.
bot = Bot(token='6381398610:AAHwPW_jzTYW5ZOSkjxsn1LCu5l0zfz4QJQ')
dp = Dispatcher(bot)

# Use os.getenv for the Google API key
GOOGLE_API_KEY = os.getenv('AIzaSyADvbAVI3oETadDSBIzNbWfaIfj7h-DhSU')

# Configure the API key for Gemini
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-pro-vision')


@dp.message_handler(commands=['hacker, @SudoWORLD_bot, SudoWorld_Bot, chat, batao'])
async def gemi_handler(message: types.Message):
    loading_message = None  # Initialize loading_message outside the try block
    try:
        # Display a loading message
        loading_message = await message.answer("<b>Ruk jaa bhai de raha hu, tera jabab...</b>", parse_mode='html')

        # Check if there's a prompt or not
        if len(message.text.strip()) <= 5:  
            await message.answer("<b>Please provide a prompt after the command...</b>", parse_mode='html')
            return

        # Get the text following the /gemi command as the prompt
        prompt = message.text.split(maxsplit=1)[1:]

        # Example: Generate text from a prompt
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)

        response_text = response.text

        # Split the response if it's over 10000 characters
        if len(response_text) > 10000:
            # Split the response into parts
            parts = [response_text[i:i+10000] for i in range(0, len(response_text), 10000)]
            for part in parts:
                await message.answer(part, parse_mode='markdown')
        else:
            # Send the response as a single message
            await message.answer(response_text, parse_mode='markdown')

    except Exception as e:
        await message.answer(f"Sorry bhai system mein koi kharabi aai hai toh mein jabab nahi de sakta: {str(e)}")
    finally:
        # Delete the loading message regardless of whether an error occurred or not
        if loading_message:
            await bot.delete_message(chat_id=loading_message.chat.id, message_id=loading_message.message_id)


@dp.message_handler(commands=['image, dekho'])
async def generate_from_image(message: types.Message):
    user_id = message.from_user.id

    if message.reply_to_message and message.reply_to_message.photo:
        image = message.reply_to_message.photo[-1]
        prompt = message.get_args() or message.reply_to_message.caption or "Describe this image."

        processing_message = await message.answer("<b>Dekh raha hu bhai thhoda intezaar kar...</b>", parse_mode='html')

        try:
            # Fetch image from Telegram
            img_data = await bot.download_file_by_id(image.file_id)
            img = PIL.Image.open(io.BytesIO(img_data.getvalue()))

            # Generate content
            response = model.generate_content([prompt, img])
            response_text = response.text

            # Send the response as plain text
            await message.answer(response_text, parse_mode=None)
        except Exception as e:
            logging.error(f"Sorry bhai aankhen foot jaane ke karan mein tumhe ab jabab nahi de sakta 😭: {e}")
            await message.answer("<b>Sorry 😔 bro meri aankhein foot gyi 😭</b>", parse_mode='html')
        finally:
            await bot.delete_message(chat_id=processing_message.chat.id, message_id=processing_message.message_id)
    else:
        await message.answer("<b>Please reply to an image with this command.</b>", parse_mode='html')

os.system("python gemini.py")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
    
