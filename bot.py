from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ChatAction
import os, subprocess

BOT_TOKEN = os.environ.get("BOT_TOKEN")

def start(update, context):
    update.message.reply_text("👋 Send me any video link (YouTube, Terabox, Instagram, etc.) and I’ll fetch it!")

def handle_link(update, context):
    url = update.message.text.strip()
    update.message.reply_text("⏳ Processing video... please wait.")
    context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.UPLOAD_VIDEO)

    try:
        filename = "video.mp4"
        command = ["yt-dlp", "-o", filename, "-f", "mp4", url]
        subprocess.run(command, check=True)

        with open(filename, "rb") as f:
            update.message.reply_video(f, caption="✅ Here’s your video!")
        os.remove(filename)

    except Exception as e:
        update.message.reply_text(f"⚠️ Error: {str(e)}")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_link))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
