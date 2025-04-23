from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

router = Router()


@router.message(CommandStart())
async def start_message(message: Message):
    await message.answer(
        text="I am Welcome Bot, that welcomes new members of the group!\n"
             "Here how it reacts to new members in the group: \n\n"
             "Please welcome our newest volunteer, (Name), (@Nickname) please tell about yourself and add a pic, welcome to the family!"
    )

@router.message(Command(commands='help'))
async def help_message(message: Message):
    await message.answer(text='If you have some problems with the bot or questions, please contact @simple_urm\n')

@router.message(F.new_chat_members)
async def welcome_new_members(message: Message):
    for user in message.new_chat_members:
        name = user.full_name
        username = f"@{user.username}" if user.username else name
        text = f"Please welcome our newest volunteer, {name}, {username} please tell about yourself and add a pic, welcome to the family!"
        await message.answer(text)


