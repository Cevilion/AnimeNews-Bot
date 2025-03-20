import aiohttp
import asyncio
import time 
import datetime
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import subprocess
import threading
import pymongo
import feedparser
from config import API_ID, API_HASH, BOT_TOKEN, NEWS_FEED_URLS, STICKER_ID, START_PIC, MONGO_URI

#from webhook import start_webhook
from modules.formatting import format_post
from modules.rss.rss import news_feed_loop
from pyrogram.errors import FloodWait


BOT_START_TIME = time.time()  # Track bot's start time

mongo_client = pymongo.MongoClient(MONGO_URI)
db = mongo_client["telegram_bot_db"]
user_settings_collection = db["user_settings"]
global_settings_collection = db["global_settings"]

app = Client("GenToolBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

#webhook_thread = threading.Thread(target=start_webhook, daemon=True)
#webhook_thread.start()


async def send_message_to_user(chat_id: int, message: str, image_url: str = None):
    try:
        if not message or len(message.strip()) == 0:
            print("❗ Empty message detected. Skipping post...")
            return

        if image_url:
            await app.send_photo(chat_id, image_url, caption=message)
        else:
            await app.send_message(chat_id, message)

        # Send sticker only after message success
        if STICKER_ID:
            try:
                await app.send_sticker(chat_id, STICKER_ID)
            except Exception as e:
                print(f"⚠️ Sticker error: {e}")
    except Exception as e:
        print(f"❌ Error sending message: {e}")


@app.on_message(filters.command("start"))
async def start(client, message):
    chat_id = message.chat.id
    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("ᴍᴀɪɴ ʜᴜʙ", url="https://telegram.dog/piras_official"),
            InlineKeyboardButton("Anime Channel", url="https://telegram.dog/animes_piras"),
        ],
        [
            InlineKeyboardButton("News Net", url="https://t.me/AnimeNews_Network"),
        ],
    ])

    photo_url = START_PIC

    await app.send_photo(
        chat_id, 
        photo_url,
        caption=(
            f"**ʙᴀᴋᴋᴀᴀᴀ {message.from_user.first_name}!!!**\n"
            f"**ɪ ᴀᴍ ᴀɴ ᴜᴩʟᴏᴀᴅ ᴛᴏᴏʟ ʙᴏᴛ.**\n"
            f"**ɪ ᴡᴀs ᴄʀᴇᴀᴛᴇᴅ ᴛᴏ ᴍᴀᴋᴇ ʟɪғᴇ ᴇᴀsɪᴇʀ...**\n"
            f"**ɪ ᴀᴍ sᴛɪʟʟ ɪɴ ʙᴇᴛᴀ ᴛᴇsᴛɪɴɢ ᴠᴇʀsɪᴏɴ...**"
        ),
        reply_markup=buttons
    )

@app.on_message(filters.command("stats"))
async def stats_command(client, message):
    current_time = time.time()
    uptime = str(datetime.timedelta(seconds=int(current_time - BOT_START_TIME)))

    start_time = time.time()
    ping_message = await message.reply_text("📊 **Calculating...**")
    ping_time = round((time.time() - start_time) * 1000, 2)

    await ping_message.edit_text(
        f"📊 **Bot Statistics:**\n"
        f"🔹 **Uptime:** `{uptime}`\n"
        f"🔹 **Ping:** `{ping_time} ms`"
    )

@app.on_message(filters.command("ping"))
async def ping_command(client, message):
    start_time = time.time()
    reply = await message.reply_text("🏓 **Pinging...**")
    ping_time = round((time.time() - start_time) * 1000, 2)

    await reply.edit_text(f"🏓 **Pong!** ✅\n`{ping_time} ms`")

@app.on_message(filters.command("news"))
async def connect_news(client, message):
    chat_id = message.chat.id
    if len(message.text.split()) == 1:
        await app.send_message(chat_id, "❗ **Please provide a channel ID or username (without @).**")
        return

    channel = " ".join(message.text.split()[1:]).strip().replace("@", "")
    global_settings_collection.update_one({"_id": "config"}, {"$set": {"news_channel": channel}}, upsert=True)
    await app.send_message(chat_id, f"✅ **News channel set to:** @{channel}")

@app.on_message(filters.command("help"))
async def help_command(client, message):
    chat_id = message.chat.id

    help_text = (
        "**🛠️ Available Commands:**\n\n"
        "✅ `/start` - Start the bot and view welcome message.\n"
        "✅ `/news <channel_id>` - Set the news channel for auto-posting.\n"
        "✅ `/testpost` - Send a sample news post to check formatting.\n"
        "✅ `/help` - Display this help message.\n"
        "✅ `/ping` - Check the bot's response time.\n"
        "✅ `/stats` - Show the bot's uptime and ping details.\n\n"
        "**Note:** Commands must be used in the appropriate chat context for proper functionality.\n\n"
        "📣 *Powered by DOT NeWZ*"
    )

    await app.send_message(chat_id, help_text)


@app.on_message(filters.command("testpost"))
async def test_post(client, message):
    chat_id = message.chat.id

    # Sample news data for testing
    demo_news = {
        "title": "Demo Post - Testing News Format",
        "summary": "This is a test post to verify that the news format and sticker are working correctly.",
        "link": "https://example.com/test-news",
        "date": "Today",
        "studio": "Test Studio",
        "category": "Anime Release"
    }

    # Format and send the post
    post, _ = format_post(demo_news, STICKER_ID)

    # Send the formatted post with sticker
    await send_message_to_user(chat_id, post)

    await message.reply_text("✅ Test post sent successfully!")


# Example news item
demo_news = {
    "title": "Attack on Titan Final Season Part 4 Announced!",
    "summary": "The epic conclusion to the series is set for Fall 2025.",
    "link": "https://example.com/aot-news",
    "date": "Fall 2025",
    "studio": "MAPPA",
    "category": "Anime Release"
}

post, sticker_id = format_post(demo_news, STICKER_ID)
print(post)
print(f"Sticker ID: {sticker_id}")

if __name__ == "__main__":
    print("Bot is starting...")

    async def start_bot():
        await app.start()
        print("✅ Bot started successfully!")

        # Start the news loop safely inside the running event loop
        asyncio.create_task(news_feed_loop(app, db, global_settings_collection, NEWS_FEED_URLS))

        await asyncio.Event().wait()  # Correct method for PyroFork to keep the bot running indefinitely

    asyncio.run(start_bot())

