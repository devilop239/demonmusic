# All rights reserved.
import importlib
import sys
import os

# ✅ Fix for relative imports on Render
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall

from config.config import BANNED_USERS
import config.config as config
from VenomX import HELPABLE, app, userbot
from VenomX.core.call import Ayush
from VenomX.plugins import ALL_MODULES
from VenomX.utils.database import get_banned_users, get_gbanned
from VenomX.logger_config import LOGGER


async def init():
    if len(config.STRING_SESSIONS) == 0:
        LOGGER("VenomX").error("No Assistant Clients Vars Defined!.. Exiting Process.")
        return

    if not config.SPOTIFY_CLIENT_ID and not config.SPOTIFY_CLIENT_SECRET:
        LOGGER("VenomX").warning(
            "No Spotify Vars defined. Your bot won't be able to play Spotify queries."
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
        imported_module = importlib.import_module(all_module)
        if hasattr(imported_module, "__MODULE__") and imported_module.__MODULE__:
            if hasattr(imported_module, "__HELP__") and imported_module.__HELP__:
                HELPABLE[imported_module.__MODULE__.lower()] = imported_module

    LOGGER("VenomX.plugins").info("Successfully Imported All Modules")

    await userbot.start()
    await Ayush.start()
    LOGGER("VenomX").info("Assistant Started Successfully")

    try:
        await Ayush.stream_call(
            "http://docs.evostream.com/sample_content/assets/sintel1m720p.mp4"
        )
    except NoActiveGroupCall:
        LOGGER("VenomX").error("Please ensure the voice call in your log group is active.")
        exit()

    await Ayush.decorators()
    LOGGER("VenomX").info("VenomX Started Successfully")

    await idle()

    await app.stop()
    await userbot.stop()


if __name__ == "__main__":
    app.run(init())
