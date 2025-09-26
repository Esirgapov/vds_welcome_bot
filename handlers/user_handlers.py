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


@router.message(CommandStart())
async def start_message(message: Message):
    await message.answer(
        text="I am Welcome Bot, that welcomes new members of the group!\n"
             "Here how it reacts to new members in the group: \n\n"
             "Please welcome our newest amazing volunteer, (name)! (username) please send your photo and bio in the same message. Thanks and welcome to our family😊🤗 \n\nWho added (name) to our big team?"
    )

@router.message(Command(commands='help'))
async def help_message(message: Message):
    await message.answer(text='If you have some problems with the bot or questions, please contact @simple_urm\n')

@router.message(F.new_chat_members)
async def welcome_new_members(message: Message):
    for user in message.new_chat_members:
        name = user.full_name
        username = f"@{user.username}" if user.username else name
        text = f"Please welcome our newest amazing volunteer, {name}! {username} please send your photo and bio in the same message. Thanks and welcome to our family😊🤗 \n\nWho added {name} to our big team?"
        await message.answer(text)

EXCEPTIONS = {}

def is_valid_name(full_name: str) -> bool:
    if full_name in EXCEPTIONS:
        return True
    parts = full_name.strip().split()
    if len(parts) != 2:
        return False
    return all(p[0].isupper() for p in parts)

@router.message(Command("check_names"))
async def check_names_handler(message: Message):
    chat_type = message.chat.type
    chat_id = message.chat.id

    await message.answer(f"ℹ️ Тип чата: <b>{chat_type}</b>\n🆔 Chat ID: <code>{chat_id}</code>", parse_mode="HTML")

    if chat_type != "supergroup":
        return await message.answer("❌ Эта команда работает только в супергруппах. Переведи группу в супергруппу.")

    await message.answer("🔍 Проверяю имена участников...")

    try:
        admins = await message.bot.get_chat_administrators(chat_id)
    except Exception:
        return await message.answer("❌ Не могу получить список участников. Бот должен быть админом.")

    invalid_users = []
    checked_ids = set()

    for admin in admins:
        user = admin.user
        if user.id in checked_ids or user.is_bot:
            continue
        checked_ids.add(user.id)

        name = user.full_name
        if not is_valid_name(name):
            invalid_users.append(f"{name} (@{user.username or 'без юзернейма'})")

    if not invalid_users:
        await message.answer("✅ Все имена соответствуют формату Имя Фамилия.")
    else:
        text = "⚠️ Участники с неправильным форматом имени:\n" + "\n".join(invalid_users)
        await message.answer(text)

