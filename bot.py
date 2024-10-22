import os
import asyncio
import argparse
import logging
import sys
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

import llm

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
LLM_TOKEN = os.getenv('LLM_TOKEN')

dp = Dispatcher()
llm = llm.Client(LLM_TOKEN)

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    msg = (f'Hey, {message.from_user.full_name} this bot helps you control '
           'your calories of your food. To see all commands print /help'
    )
    await message.answer(msg)


@dp.message(Command('help'))
async def command_help_handler(message: Message) -> None:
    msg = '''
    Available commands:
        /help - show help
        /start - start bot
        /vote - vote to teacher
    '''
    await message.answer(msg)

@dp.message(Command('vote'))
async def command_vote_handler(message: Message) -> None:
    msg = 'Start vote'
    await message.answer(msg)
    

@dp.message()
async def echo_handler(message: Message) -> None:
    response = await llm.generate(message.text)
    texts = [c.text for c in response.content]
    logging.info('Response from LLM: ', texts)
    try:
        await message.answer(texts[0])
    except TypeError:
        await message.answer("Nice try!")


async def main(TOKEN) -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)
    
    
parser = argparse.ArgumentParser()
parser.add_argument(
    '-v', '--verbose',
    type=str,
    default='INFO',
    help='Logging level, for example: DEBUG or WARNING.')
parser.add_argument(
    '-t', '--token',
    type=str,
    required=False,
    help='Provides Telegram bot token')


if __name__ == "__main__":
    args = parser.parse_args()
    TOKEN = args.token or BOT_TOKEN
    logging.basicConfig(level=args.verbose, stream=sys.stdout)
    asyncio.run(main(TOKEN))