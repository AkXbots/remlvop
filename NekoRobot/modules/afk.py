message.reply_to_message.from_user.id
        fst_name = message.reply_to_message.from_user.first_name
        check_afk(update, context, user_id, fst_name, userc_id)


def check_afk(update, context, user_id, fst_name, userc_id):
    if sql.is_afk(user_id):
        user = sql.check_afk_status(user_id)

if int(userc_id) == int(user_id):
            return
        if not user.reason:
            res = f"{fst_name} is afk"
            update.effective_message.reply_text(res)
        else:
            res = f"{html.escape(fst_name)} is afk.\nReason: <code>{html.escape(user.reason)}</code>"

            update.effective_message.reply_text(res, parse_mode="html")


AFK_HANDLER = DisableAbleCommandHandler("afk", afk, run_async=True)
AFK_REGEX_HANDLER = DisableAbleMessageHandler(
    Filters.regex(r"^(?i)brb(.*)$"), afk, friendly="afk"
)
NO_AFK_HANDLER = MessageHandler(
    Filters.all & Filters.chat_type.groups, no_longer_afk, run_async=True
)
AFK_REPLY_HANDLER = MessageHandler(
    Filters.all & Filters.chat_type.groups, reply_afk, run_async=True
)

NEKO_PTB.add_handler(AFK_HANDLER, AFK_GROUP)
NEKO_PTB.add_handler(AFK_REGEX_HANDLER, AFK_GROUP)
NEKO_PTB.add_handler(NO_AFK_HANDLER, AFK_GROUP)
NEKO_PTB.add_handler(AFK_REPLY_HANDLER, AFK_REPLY_GROUP)

mod_name = "Afk"
command_list = ["afk"]
handlers = [
    (AFK_HANDLER, AFK_GROUP),
    (AFK_REGEX_HANDLER, AFK_GROUP),
    (NO_AFK_HANDLER, AFK_GROUP),
    (AFK_REPLY_HANDLER, AFK_REP
