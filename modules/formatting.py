from datetime import datetime
import pytz

def format_post(news_item, sticker_id):
    title = news_item.get("title", "No Title")
    summary = news_item.get("summary", "No summary available.")
    link = news_item.get("link", "#")
    date = news_item.get("date", "Unknown Date")
    studio = news_item.get("studio", "Unknown Studio")
    category = news_item.get("category", "General")

    # Convert date to IST format
    try:
        date_obj = datetime.strptime(date, "%a, %d %b %Y %H:%M:%S %z")
        date_ist = date_obj.astimezone(pytz.timezone("Asia/Kolkata")).strftime("%d %B %Y | %I:%M %p IST")
    except ValueError:
        date_ist = date

    # Category-specific styles
    if category == "Anime Release":
        formatted_post = (
            f"<b>🎬 Anime Release Alert!</b>\n\n"
            f"<blockquote>🔥 <b>{title}</b> 🔥</blockquote>\n\n"
            f"<i>📝 {summary}</i>\n\n"
            f"📅 <b>Release Date:</b> <u>{date_ist}</u>\n"
            f"🏢 <b>Studio/Publisher:</b> <u>{studio}</u>\n\n"
            f"🔗 <a href='{link}'>Read More</a>\n\n"
            f"#Anime #News #DOTNeWZ\n\n"
            f"📣 <i>Posted by DOT NeWZ</i>\n\n"
        )
    elif category == "Manga Update":
        formatted_post = (
            f"<b>📚 Manga Update!</b>\n\n"
            f"<blockquote>📖 <b>{title}</b> 📖</blockquote>\n\n"
            f"<i>📃 {summary}</i>\n\n"
            f"📅 <b>Release Date:</b> <u>{date_ist}</u>\n"
            f"✒️ <b>Publisher:</b> <u>{studio}</u>\n\n"
            f"🔗 <a href='{link}'>Read More</a>\n\n"
            f"#Manga #News #DOTNeWZ\n\n"
            f"📣 <i>Posted by DOT NeWZ</i>\n\n"
        )
    elif category == "Industry News":
        formatted_post = (
            f"<b>🗞️ Industry News!</b>\n\n"
            f"<blockquote>📰 <b>{title}</b> 📰</blockquote>\n\n"
            f"<i>💬 {summary}</i>\n\n"
            f"📅 <b>Date:</b> <u>{date_ist}</u>\n"
            f"🏢 <b>Source:</b> <u>{studio}</u>\n\n"
            f"🔗 <a href='{link}'>Read More</a>\n\n"
            f"#Industry #Anime #DOTNeWZ\n\n"
            f"📣 <i>Posted by DOT NeWZ</i>\n\n"
        )
    else:
        formatted_post = (
            f"<b>🌟 Latest News!</b>\n\n"
            f"<blockquote>✨ <b>{title}</b> ✨</blockquote>\n\n"
            f"<i>📝 {summary}</i>\n\n"
            f"📅 <b>Date:</b> <u>{date_ist}</u>\n"
            f"🏢 <b>Source:</b> <u>{studio}</u>\n\n"
            f"🔗 <a href='{link}'>Read More</a>\n\n"
            f"#Anime #News #DOTNeWZ\n\n"
            f"📣 <i>Posted by DOT NeWZ</i>\n\n"
        )

    return formatted_post, sticker_id
