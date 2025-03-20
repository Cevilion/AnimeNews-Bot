from datetime import datetime
import pytz

def format_post(news_item, sticker_id):
    title = news_item.get("title", "No Title")
    summary = news_item.get("summary", "No summary available.")
    link = news_item.get("link", "#")
    date = news_item.get("date", "Unknown Date")
    source = news_item.get("studio", "Unknown Source")  # Changed from 'studio' to 'source'
    category = news_item.get("category", "General")

    # Convert date to IST format with fallback handling
try:
    if "GMT" in date:
        date_obj = datetime.strptime(date, "%a, %d %b %Y %H:%M:%S GMT")
        date_obj = date_obj.replace(tzinfo=pytz.utc).astimezone(pytz.timezone("Asia/Kolkata"))
    elif "T" in date and "Z" in date:
        date_obj = datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=pytz.utc).astimezone(pytz.timezone("Asia/Kolkata"))
    else:
        date_obj = datetime.strptime(date, "%a, %d %b %Y %H:%M:%S %z")

    date_ist = date_obj.strftime("%d %B %Y | %I:%M %p IST")
except ValueError:
    date_ist = date  # Use original date if conversion fails


    # Category-specific styles
    if category == "Anime Release":
        formatted_post = (
            f"━━━━━━━━━━━━━━━━━━━━━\n"
            f"<b>🎬 Anime Release Alert!</b>\n"
            f"<b>🔹 {title} 🔥</b>\n\n"
            f"<i>📝 {summary}</i>\n\n"
            f"📅 <b>Release Date:</b> <code>{date_ist}</code>\n"
            f"🏢 <b>Source:</b> <u>{source}</u>\n\n"
            f"🔗 <a href='{link}'>Read More</a>\n"
            f"━━━━━━━━━━━━━━━━━━━━━\n"
            f"#Anime #News #DOTNeWZ\n\n"
            f"📣 <i>Posted by DOT NeWZ</i>\n\n"
        )
    elif category == "Manga Update":
        formatted_post = (
            f"━━━━━━━━━━━━━━━━━━━━━\n"
            f"<b>📚 Manga Update!</b>\n"
            f"<b>🔹 {title} 📖</b>\n\n"
            f"<i>📃 {summary}</i>\n\n"
            f"📅 <b>Release Date:</b> <code>{date_ist}</code>\n"
            f"✒️ <b>Source:</b> <u>{source}</u>\n\n"
            f"🔗 <a href='{link}'>Read More</a>\n"
            f"━━━━━━━━━━━━━━━━━━━━━\n"
            f"#Manga #News #DOTNeWZ\n\n"
            f"📣 <i>Posted by DOT NeWZ</i>\n\n"
        )
    elif category == "Industry News":
        formatted_post = (
            f"━━━━━━━━━━━━━━━━━━━━━\n"
            f"<b>🗞️ Industry News!</b>\n"
            f"<b>🔹 {title} 📰</b>\n\n"
            f"<i>💬 {summary}</i>\n\n"
            f"📅 <b>Date:</b> <code>{date_ist}</code>\n"
            f"🏢 <b>Source:</b> <u>{source}</u>\n\n"
            f"🔗 <a href='{link}'>Read More</a>\n"
            f"━━━━━━━━━━━━━━━━━━━━━\n"
            f"#Industry #Anime #DOTNeWZ\n\n"
            f"📣 <i>Posted by DOT NeWZ</i>\n\n"
        )
    else:
        formatted_post = (
            f"━━━━━━━━━━━━━━━━━━━━━\n"
            f"<b>🌟 Latest News!</b>\n"
            f"<b>🔹 {title} ✨</b>\n\n"
            f"<i>📝 {summary}</i>\n\n"
            f"📅 <b>Date:</b> <code>{date_ist}</code>\n"
            f"🏢 <b>Source:</b> <u>{source}</u>\n\n"
            f"🔗 <a href='{link}'>Read More</a>\n"
            f"━━━━━━━━━━━━━━━━━━━━━\n"
            f"#Anime #News #DOTNeWZ\n\n"
            f"📣 <i>Posted by DOT NeWZ</i>\n\n"
        )

    return formatted_post, sticker_id if sticker_id else None
