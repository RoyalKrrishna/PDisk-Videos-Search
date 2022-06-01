# (c) @AbirHasan2005

from core.login import xdisk_login

XDisk_DB = {}


async def get_cookies(username: str, password: str) -> str:
    if not XDisk_DB:
        user_id, cookies = await xdisk_login(username, password)
        XDisk_DB["cookies"] = cookies
        XDisk_DB["user_id"] = user_id
        XDisk_DB["username"] = username
        XDisk_DB["password"] = password

    return XDisk_DB["cookies"]


async def set_cookies(data: dict):
    XDisk_DB["username"] = data["username"]
    XDisk_DB["password"] = data["password"]
    XDisk_DB["user_id"] = data["user_id"]
    XDisk_DB["cookies"] = data["cookies"]
