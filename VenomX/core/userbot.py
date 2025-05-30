# All rights reserved.
#
import asyncio
import sys

from pyrogram import Client
from pyrogram.errors import ChatWriteForbidden
import config

from VenomX.logger_config import LOGGER

assistants = []
assistantids = []


class Userbot(Client):
    def __init__(self):
        self.clients = []
        # ✅ Ensure session(s) is always a list
        self.sessions = config.STRING_SESSIONS if isinstance(config.STRING_SESSIONS, list) else [config.STRING_SESSIONS]

        for i, session in enumerate(self.sessions, start=1):
            client = Client(
                f"VenomString{i}",
                api_id=config.API_ID,
                api_hash=config.API_HASH,
                in_memory=True,
                no_updates=True,
                session_string=session.strip(),
            )
            self.clients.append(client)

    async def _start(self, client, index):
        LOGGER(__name__).info("Starting Assistant Clients")
        try:
            await client.start()
            assistants.append(index)
            try:
                await client.send_message(config.LOGGER_ID, "Assistant Started")
            except ChatWriteForbidden:
                try:
                    await client.join_chat(config.LOGGER_ID)
                    await client.send_message(config.LOGGER_ID, "Assistant Started")
                except Exception:
                    LOGGER(__name__).error(
                        f"Assistant Account {index} has failed to send message in Loggroup. Make sure you have added assistant in Loggroup."
                    )
                    sys.exit(1)

            get_me = await client.get_me()
            client.username = get_me.username
            client.id = get_me.id
            client.mention = get_me.mention
            assistantids.append(get_me.id)
            client.name = f"{get_me.first_name} {get_me.last_name or ''}".strip()

        except Exception as e:
            LOGGER(__name__).error(
                f"Assistant Account {index} failed with error: {str(e)}."
            )
            sys.exit(1)

    async def start(self):
        tasks = []
        for i, client in enumerate(self.clients, start=1):
            task = self._start(client, i)
            tasks.append(task)
        await asyncio.gather(*tasks)

    async def stop(self):
        tasks = [client.stop() for client in self.clients]
        await asyncio.gather(*tasks)
    
    def __getattr__(self, name):
        if not self.clients:
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")
        first_client = self.clients[0]
        if hasattr(first_client, name):
            return getattr(first_client, name)
        raise AttributeError(f"'{type(first_client).__name__}' object has no attribute '{name}'")
