def format_post(news_item, sticker_id):
    title = news_item.get("title", "No Title")
    summary = news_item.get("summary", "No summary available.")
    link = news_item.get("link", "#")
    date = news_item.get("date", "Unknown Date")
    studio = news_item.get("studio", "Unknown Studio")
    category = news_item.get("category", "General")

    # Category-specific styles
    if category == "Anime Release":
        formatted_post = (
            f"🎬 **Anime Release Alert!**\n\n"
            f"🔥 *{title}* 🔥\n\n"
            f"📝 {summary}\n\n"
            f"📅 *Release Date:* {date}\n"
            f"🏢 *Studio/Publisher:* {studio}\n\n"
            f"🔗 [Read More]({link})\n\n"
            f"#Anime #News #DOTNeWZ\n\n"
            f"📣 *Posted by DOT NeWZ*\n\n"
        )
    elif category == "Manga Update":
        formatted_post = (
            f"📚 **Manga Update!**\n\n"
            f"📖 *{title}* 📖\n\n"
            f"📃 {summary}\n\n"
            f"📅 *Release Date:* {date}\n"
            f"✒️ *Publisher:* {studio}\n\n"
            f"🔗 [Read More]({link})\n\n"
            f"#Manga #News #DOTNeWZ\n\n"
            f"📣 *Posted by DOT NeWZ*\n\n"
        )
    elif category == "Industry News":
        formatted_post = (
            f"🗞️ **Industry News!**\n\n"
            f"📰 **{title}** 📰\n\n"
            f"💬 {summary}\n\n"
            f"📅 *Date:* {date}\n"
            f"🏢 *Source:* {studio}\n\n"
            f"🔗 [Read More]({link})\n\n"
            f"#Industry #Anime #DOTNeWZ\n\n"
            f"📣 *Posted by DOT NeWZ*\n\n"
        )
    else:
        formatted_post = (
            f"🌟 **Latest News!**\n\n"
            f"✨ **{title}** ✨\n\n"
            f"📝 {summary}\n\n"
            f"📅 *Date:* {date}\n"
            f"🏢 *Source:* {studio}\n\n"
            f"🔗 [Read More]({link})\n\n"
            f"#Anime #News #DOTNeWZ\n\n"
            f"📣 *Posted by DOT NeWZ*\n\n"
        )

    return formatted_post, sticker_id
