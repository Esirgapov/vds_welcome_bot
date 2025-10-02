from aiogram import F, Router
from aiogram.filters import Command, CommandStart
# from aiogram.filters.command import CommandObject
# from aiogram.types.chat_member import ChatMember
# from aiogram.utils.chat_action import ChatActionSender
from aiogram.types import Message

router = Router()


# @router.message(F.text.startswith('/'), F.chat.type.in_({"group", "supergroup"}))
# async def block_commands_for_non_admins(message: Message, bot):
#     member = await bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)
#     if member.status not in {"administrator", "creator"}:
#         await message.delete()

@router.message(CommandStart(), F.chat.type == "private")
async def start_message(message: Message):
    await message.answer(
        text="I am Welcome Bot, that welcomes new members of the group!\n"
             "Here how it reacts to new members in the group: \n\n"
             "Please welcome our newest amazing volunteer, (name)! (username) please send your photo and bio in the same message. Thanks and welcome to our family😊🤗 \n\n"
    )

@router.message(Command(commands='help'), F.chat.type == "private")
async def help_message(message: Message):
    await message.answer(text='If you have some problems with the bot or questions, please contact @simple_urm\n')

@router.message(F.new_chat_members)
async def welcome_new_members(message: Message):
    for user in message.new_chat_members:
        name = user.full_name
        username = f"@{user.username}" if user.username else name
        text = f"Please welcome our newest amazing volunteer, {name}! {username} please send your photo and bio in the same message. Thanks and welcome to our family😊🤗"
        await message.answer(text)

