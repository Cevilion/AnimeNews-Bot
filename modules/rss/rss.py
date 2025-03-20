import asyncio
import random
import feedparser
from modules.formatting import format_post
from config import STICKER_ID

from PIL import Image, ImageDraw, ImageFont
import io
import aiohttp

async def fetch_and_send_news(app, db, global_settings_collection, urls):
    config = global_settings_collection.find_one({"_id": "config"})
    if not config or "news_channel" not in config:
        print("❗ No news channel configured.")
        return

    news_channel = "@" + config["news_channel"]

    for url in urls:
        print(f"🔎 Fetching RSS URL: {url}")
        feed = await asyncio.to_thread(feedparser.parse, url)

        if not feed.entries:
            print(f"❗ No new entries found in {url}")
            continue

        entries = list(feed.entries)[::-1]

        for entry in entries:
            entry_id = entry.get('id', entry.get('link'))
            title = entry.get('title', 'Untitled News')

            # Improved duplicate check: Check both entry_id & title
            if not db.sent_news.find_one({"$or": [{"entry_id": entry_id}, {"title": title}]}):
                news_item = {
                    "title": entry.title,
                    "summary": entry.get("summary", ""),
                    "link": entry.link,
                    "date": entry.get("published", "Unknown Date"),
                    "studio": entry.get("source", {}).get("title", "Unknown Studio"),
                    "category": "Anime Release" if "anime" in entry.title.lower() else "Industry News"
                }

                msg, sticker_id = format_post(news_item, STICKER_ID)
                thumbnail_url = entry.media_thumbnail[0]['url'] if 'media_thumbnail' in entry else None

                try:
                    await asyncio.sleep(random.randint(12, 18))  # Smart delay to avoid spam
                    if thumbnail_url:
                        await send_post_with_watermark(app, news_channel, thumbnail_url, msg)

                    else:
                        await app.send_message(chat_id=news_channel, text=msg)

                    await app.send_sticker(chat_id=news_channel, sticker=sticker_id)
                    db.sent_news.insert_one({"entry_id": entry_id, "title": entry.title, "link": entry.link})
                    print(f"✅ Sent news: {entry.title}")
                except Exception as e:
                    import traceback
                    print(f"❌ Error sending news message: {entry.title}")
                    print(f"➡️ Details: {traceback.format_exc()}")

async def add_watermark(image_url, watermark_text="DOT NeWZ"):
    async with aiohttp.ClientSession() as session:
        async with session.get(image_url) as resp:
            if resp.status == 200:
                image_bytes = await resp.read()
                image = Image.open(io.BytesIO(image_bytes))

                # Add watermark
                draw = ImageDraw.Draw(image)
                font = ImageFont.load_default()

                # Position watermark at bottom-right
                text_width, text_height = draw.textsize(watermark_text, font)
                position = (image.width - text_width - 10, image.height - text_height - 10)

                draw.text(position, watermark_text, font=font, fill="white")

                # Save modified image to bytes
                output_buffer = io.BytesIO()
                image.save(output_buffer, format="JPEG")
                output_buffer.seek(0)

                return output_buffer

async def send_post_with_watermark(app, news_channel, image_url, msg):
    try:
        watermark_image = await add_watermark(image_url)
        await app.send_photo(chat_id=news_channel, photo=watermark_image, caption=msg)
    except Exception as e:
        print(f"Error sending watermarked post: {e}")


async def news_feed_loop(app, db, global_settings_collection, urls):
    print("🔄 Starting news loop...")

    try:
        db.command("ping")  # MongoDB connection check
        print("✅ MongoDB connection confirmed!")
    except Exception as e:
        print(f"❗ MongoDB connection failed: {e}")
        return
    
    while True:
        try:
            print("🔍 Checking for new news entries...")
            await fetch_and_send_news(app, db, global_settings_collection, urls)
        except Exception as e:
            print(f"🚨 Error in news feed loop: {e}")
        await asyncio.sleep(60)
