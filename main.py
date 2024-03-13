import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Replace with your actual Telegram bot token
bot_token = "7018786698:AAGxexoRvLJlTh5bLnf63HFkQc-WvhgqgME"

def is_admin(update):
  chat_member = update.effective_chat.get_member(update.effective_user.id)
  return chat_member.can_restrict_members

def handle_restricted(update, context):
  update.message.reply_text("You don't have permission to use this command.")

def ban_user(update, context):
  if is_admin(update):
    chat_member = update.message.chat_member
    if chat_member is not None:
      user = chat_member.from_user
      chat = update.effective_chat

      try:
        # Ban the user
        telegram.ChatAction(chat.id, telegram.ChatAction.BAN_USER)
        update.message.reply_text(f"Banned {user.mention_html()}!")
      except telegram.error.ChatMemberCantBeEdited:
        update.message.reply_text("I don't have permission to ban users.")
  else:
    handle_restricted(update, context)

def kick_user(update, context):
  if is_admin(update):
    chat_member = update.message.chat_member
    if chat_member is not None:
      user = chat_member.from_user
      chat = update.effective_chat

      try:
        # Kick the user
        telegram.ChatAction(chat.id, telegram.ChatAction.KICK_USER)
        update.message.reply_text(f"Kicked {user.mention_html()}!")
      except telegram.error.ChatMemberCantBeEdited:
        update.message.reply_text("I don't have permission to kick users.")
  else:
    handle_restricted(update, context)

# ... other command handlers (admire, welcome, etc.)

# Create Updater and dispatcher
updater = Updater(bot_token)
dispatcher = updater.dispatcher

# Register handlers with admin check
dispatcher.add_handler(CommandHandler("ban", ban_user))
dispatcher.add_handler(CommandHandler("kick", kick_user))
# ... other command handlers

# Handle other messages
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

# Start the bot
updater.start_polling()
updater.idle()
