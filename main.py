# (c) @RoyalKrrishna

import os
import asyncio
import traceback
from dotenv import (
    load_dotenv
)
from pyrogram import (
    Client,
    filters,
    idle
)
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from pyrogram.errors import (
    MessageNotModified
)
from core.search_video import search_pdisk_videos

if os.path.exists("configs.env"):
    load_dotenv("configs.env")


class Configs(object):
    API_ID = int(os.environ.get("API_ID", 0))
    API_HASH = os.environ.get("API_HASH", "")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
    PDISK_USERNAME = os.environ.get("PDISK_USERNAME", "")
    PDISK_PASSWORD = os.environ.get("PDISK_PASSWORD", "")
    MAX_RESULTS = int(os.environ.get("MAX_RESULTS", 5))
    # Which PDisk Domain?
    PDISK_DOMAINS = [
        "https://www.cofilink.com/",
        "https://www.pdisk1.net/",
        "https://www.pdisk.net/"
    ]
    PDISK_DOMAIN = os.environ.get("PDISK_DOMAIN", PDISK_DOMAINS[2])


PDiskBot = Client(
    session_name=":memory:",
    api_id=Configs.API_ID,
    api_hash=Configs.API_HASH,
    bot_token=Configs.BOT_TOKEN
)


@PDiskBot.on_message(filters.command("start") & ~filters.edited)
async def start_handler(_, m: Message):
    await m.reply_photo("https://telegra.ph/file/f35d8b79281781574e6f4.jpg",
    caption="**Hey Dear! 😚\n\nWelcome to the largest movies and\nseries world on Telegram!🍿\n\nSend only movie name!**🎟️",
                                 reply_markup=InlineKeyboardMarkup([
                                     [InlineKeyboardButton("🍿 Join Our Channel 🍿", url="https://t.me/iPopcornMovie")],
                                     [InlineKeyboardButton("💬 Add Me To Your Groups 💬", url="http://t.me/iPopcornMovieSearchBot?startgroup=botstart")]
                                 ]))
                     

@PDiskBot.on_message(filters.text)
async def text_handler(_, m: Message):
    
    editable = await m.reply_text("**Searching Your Movie 🔍\n\nPlease Wait...⏳**", quote=True)
    response = await search_pdisk_videos(m.text.split(" ", 1)[-1], Configs.PDISK_USERNAME, Configs.PDISK_PASSWORD)
    if isinstance(response, Exception):
        traceback.print_exc()
        try: await editable.edit("**Bot will Be Offline For Some days\nGuys as Pdisk Has Stopped Their Service\nAnd Bot will have to be re-programmed to\nprovide further service.\n\nWe will Soon Update u Through The Bot ✌️\n\nJust hang on till we Find Something Else 🥲\n\n👇🏻👇🏻👇🏻👇🏻👇🏻👇🏻\n@FindYourMovieBot**",
                                 reply_markup=InlineKeyboardMarkup([
                                     [InlineKeyboardButton("Report", url="https://t.me/RoyalKrrishna")]
                                 ]))
        except MessageNotModified: pass
    elif not response["data"]["list"]:
        try: await editable.edit("**Not Found...⚠️\n\nTry Searching Correct Movie Name From Google.\n\nTry Searching The Main Word In The Movie Name.\n\nCheck Spelling On [Google](https://www.google.com/search?)** 🔍",
                                 reply_markup=InlineKeyboardMarkup([
                                     [InlineKeyboardButton("🎟️ Request Your Movie 🎟️", url="https://t.me/iPopcornMovieGroup")],
                                     [InlineKeyboardButton("🔎 How To Search Movie Here❓", url="https://t.me/c/1767951730/8")]
                                 ]))
        except MessageNotModified: pass
    else:
        data = response["data"]["list"]
        text = ""
        count = 0
        for i in range(len(data)):
            if count > Configs.MAX_RESULTS:
                break
            count += 1
            text += f"♻️ **{data[i]['title']}**\n" \
                    f"🔗 {Configs.PDISK_DOMAIN + 'share-video?videoid=' + data[i]['share_link'].split('=', 1)[-1]}\n\n╾╾╾╾╾╾╾╾╾╾╾╾╾╾╾╾╾╾╾╾╾╾╾\n\n"
        try: await editable.edit(text, disable_web_page_preview=True,
                                 reply_markup=InlineKeyboardMarkup([
                                     [InlineKeyboardButton("🎟️ Request Your Movie 🎟️", url="https://t.me/iPopcornMovieGroup")],
                                     [InlineKeyboardButton("🔎 How To Search Movie Here❓", url="https://t.me/c/1767951730/8")]
                                 ]))
        except MessageNotModified: pass
async def run():
    await PDiskBot.start()
    print("\n\nBot Started!\n\n")
    await idle()
    await PDiskBot.stop()
    print("\n\nBot Stopped!\n\n")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(run())
