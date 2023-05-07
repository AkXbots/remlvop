from typing import Optional

from telegram import Message, Update, Bot, User
from telegram import MessageEntity
from telegram.ext import Filters, MessageHandler, run_async

from NekoRobot import NEKO_PTB
from NekoRobot.modules.disable import DisableAbleCommandHandler, DisableAbleRegexHandler
from NekoRobot.modules.sql import afk_sql as sql
from NekoRobot.modules.users import get_user_id

AFK_GROUP = 7
AFK_REPLY_GROUP = 8


@run_async
def afk(bot: Bot, update: Update):
    args = update.effective_message.text.split(None, 1)
    if len(args) >= 2:
        reason = args[1]
    else:
        reason = ""

    sql.set_afk(update.effective_user.id, reason)
    update.effective_message.reply_text("{} is now AFK!".format(update.effective_user.first_name))


@run_async
def no_longer_afk(bot: Bot, update: Update):
    user = update.effective_user  # type: Optional[User]

    if not user:  # ignore channels
        return

    res = sql.rm_afk(user.id)
    if res:
        update.effective_message.reply_text("{} is no longer AFK!".format(update.effective_user.first_name))


@run_async
def reply_afk(bot: Bot, update: Update):
    message = update.effective_message  # type: Optional[Message]
    entities = message.parse_entities([MessageEntity.TEXT_MENTION, MessageEntity.MENTION])
    if message.entities and entities:
        for ent in entities:
            if ent.type == MessageEntity.TEXT_MENTION:
                user_id = ent.user.id
                fst_name = ent.user.first_name

            elif ent.type == MessageEntity.MENTION:
                user_id = get_user_id(message.text[ent.offset:ent.offset + ent.length])
                if not user_id:
                    # Should never happen, since for a user to become AFK they must have spoken. Maybe changed username?
                    return
                chat = bot.get_chat(user_id)
                fst_name = chat.first_name

            else:
                return

            check_afk(bot, update, user_id, fst_name)

    elif message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        fst_name = message.reply_to_message.from_user.first_name
        check_afk(bot, update, user_id, fst_name)

def check_afk(bot, update, user_id, fst_name):
    if sql.is_afk(user_id):
        user = sql.check_afk_status(user_id)
        if not user.reason:
            res = "{} is AFK!".format(fst_name)
        else:
            res = "{} is AFK! says its because of: \n{}".format(fst_name, user.reason)
        update.effective_message.reply_text(res)


        valid, reason = sql.check_afk_status(user_id)
        if valid:
            if not reason:
                res = "{} is AFK!".format(fst_name)
            else:
                res = "{} is AFK! says its because of:\n{}".format(fst_name, reason)
            message.reply_text(res)

__help__ = """
 - /afk <reason>: mark yourself as AFK.
 - brb <reason>: same as the afk command - but not a command.

When marked as AFK, any mentions will be replied to with a message to say you're not available!
"""

__mod_name__ = "AFK"

AFK_HANDLER = DisableAbleCommandHandler("afk", afk)
AFK_REGEX_HANDLER = DisableAbleRegexHandler("(?i)brb", afk, friendly="afk")
NO_AFK_HANDLER = MessageHandler(Filters.all & Filters.group , no_longer_afk)
AFK_REPLY_HANDLER = MessageHandler(Filters.all & Filters.group , reply_afk)

NEKO_PTB.add_handler(AFK_HANDLER, AFK_GROUP)
NEKO_PTB.add_handler(AFK_REGEX_HANDLER, AFK_GROUP)
NEKO_PTB.add_handler(NO_AFK_HANDLER, AFK_GROUP)
NEKO_PTB.add_handler(AFK_REPLY_HANDLER, AFK_REPLY_GROUP)
