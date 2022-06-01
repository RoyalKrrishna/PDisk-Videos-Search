# (c) @AbirHasan2005

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
from core.search_video import search_xdisk_videos

if os.path.exists("configs.env"):
    load_dotenv("configs.env")


class Configs(object):
    API_ID = int(os.environ.get("API_ID", 0))
    API_HASH = os.environ.get("API_HASH", "")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
    XDISK_USERNAME = os.environ.get("XDISK_USERNAME", "")
    XDISK_PASSWORD = os.environ.get("XDISK_PASSWORD", "")
    MAX_RESULTS = int(os.environ.get("MAX_RESULTS", 5))
    AUTH_CHATS = list(set(int(x) for x in os.environ.get("AUTH_CHATS", "0").split()))
    # Which XDisk Domain?
    XDISK_DOMAINS = [
        "https://www.xdisk.in/"
    ]
    XDISK_DOMAIN = os.environ.get("XDISK_DOMAIN", XDISK_DOMAINS[2])


XDiskBot = Client(
    session_name=":memory:",
    api_id=Configs.API_ID,
    api_hash=Configs.API_HASH,
    bot_token=Configs.BOT_TOKEN
)

if (not Configs.AUTH_CHATS) or (Configs.AUTH_CHATS == [0]):
    filters_markup = filters.command("request", prefixes=["#", "/"]) & ~filters.edited
else:
    filters_markup = filters.command("request", prefixes=["#", "/"]) & filters.chat(Configs.AUTH_CHATS) & ~filters.edited


@XDiskBot.on_message(filters.command("start") & ~filters.edited)
async def start_handler(_, m: Message):
    await m.reply_text("Hi, I am Alive!\n\nSearch using /request command.", quote=True)


@XDiskBot.on_message(filters_markup, group=-1)
async def text_handler(_, m: Message):
    if len(m.command) < 2:
        return await m.reply_text("Search Query Missing!")
    editable = await m.reply_text("Please Wait ...", quote=True)
    response = await search_xdisk_videos(m.text.split(" ", 1)[-1], Configs.XDISK_USERNAME, Configs.XDISK_PASSWORD)
    if isinstance(response, Exception):
        traceback.print_exc()
        try: await editable.edit("Failed to search!",
                                 reply_markup=InlineKeyboardMarkup([
                                     [InlineKeyboardButton("Sumpot Group", url="https://t.me/JoinOT")]
                                 ]))
        except MessageNotModified: pass
    elif not response["data"]["list"]:
        try: await editable.edit("Not Found!")
        except MessageNotModified: pass
    else:
        data = response["data"]["list"]
        text = ""
        count = 0
        for i in range(len(data)):
            if count > Configs.MAX_RESULTS:
                break
            count += 1
            text += f"**Title:** `{data[i]['title']}`\n" \
                    f"**Description:** `{data[i]['description']}`\n" \
                    f"**XDisk Link:** {Configs.XDISK_DOMAIN + 'share-video?videoid=' + data[i]['share_link'].split('=', 1)[-1]}\n\n"
        try: await editable.edit(text, disable_web_page_preview=True)
        except MessageNotModified: pass


async def run():
    await XDiskBot.start()
    print("\n\nBot Started!\n\n")
    await idle()
    await XDiskBot.stop()
    print("\n\nBot Stopped!\n\n")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(run())
