import importlib
import sys
import asyncio

from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall

import config
from config import BANNED_USERS
from WinxMusic import LOGGER, app, userbot
from WinxMusic.core.call import Winx
from WinxMusic.misc import sudo
from WinxMusic.plugins import ALL_MODULES
from WinxMusic.utils.database import get_banned_users, get_gbanned


async def init():
    if sys.version_info < (3, 9):
        LOGGER("WinxMusic").error(
            "WinxMusic is optimized for Python 3.9 or higher. Exiting..."
        )
        sys.exit(1)

    if len(config.STRING_SESSIONS) == 0:
        LOGGER("WinxMusic").error(
            "No Assistant Clients Vars Defined!.. Exiting Process."
        )
        return
    if not config.SPOTIFY_CLIENT_ID and not config.SPOTIFY_CLIENT_SECRET:
        LOGGER("WinxMusic").warning(
            "No Spotify Vars defined. Your bot won't be able to play spotify queries."
        )
    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except Exception:
        pass
    await app.start()
    for all_module in ALL_MODULES:
        importlib.import_module("WinxMusic.plugins" + all_module)
    LOGGER("WinxMusic.plugins").info("Necessary Modules Imported Successfully.")
    await userbot.start()
    await Winx.start()
    try:
        await Winx.stream_call("https://telegra.ph/file/b60b80ccb06f7a48f68b5.mp4")
    except NoActiveGroupCall:
        LOGGER("WinxMusic").error(
            "[ERROR] - \n\nTurn on group voice chat and don't put it off otherwise I'll stop working thanks."
        )
        sys.exit()
    except:
        pass
    await Winx.decorators()
    LOGGER("WinxMusic").info("Alexa Music Bot Started Successfully")
    await idle()
    await app.stop()
    await userbot.stop()
    LOGGER("WinxMusic").info("Stopping Alexa Music Bot...")


if __name__ == "__main__":
    asyncio.get_event_loop_policy().get_event_loop().run_until_complete(init())
    LOGGER("WinxMusic").info("Stopping WinxMusic! GoodBye")
