# AnonXMusic/core/userbot.py
from pyrogram import Client, errors
import traceback

import config
from ..logging import LOGGER

assistants = []
assistantids = []


def _is_set(value):
    """Return True if env-like value is set and not empty/None/"None"."""
    return value is not None and str(value).strip().lower() not in ("", "none")


async def _safe_send(client: Client, chat_id, text: str) -> bool:
    """
    Try to send a message safely. Returns True on success, False on any failure.
    Does not exit the process.
    """
    try:
        await client.send_message(chat_id=chat_id, text=text)
        return True
    except (errors.ChannelInvalid, errors.PeerIdInvalid) as e:
        LOGGER(__name__).error(
            "Send message failed: ChannelInvalid/PeerIdInvalid. chat_id=%r. Err: %s",
            chat_id, repr(e), exc_info=True,
        )
    except ValueError as ve:
        LOGGER(__name__).error(
            "Send message failed: ValueError (likely bad chat_id type). chat_id=%r. Err: %s",
            chat_id, repr(ve), exc_info=True,
        )
    except Exception as ex:
        LOGGER(__name__).error(
            "Send message unexpected failure for chat_id=%r. Err: %s\nTraceback:\n%s",
            chat_id, repr(ex), traceback.format_exc(), exc_info=True,
        )
    return False


async def _safe_join(client: Client, *chats):
    """
    Try to join a list of chat usernames/ids, ignore failures.
    """
    for c in chats:
        try:
            if not c:
                continue
            await client.join_chat(c)
        except Exception:
            # ignore join failures (private chat, already in, no permission, etc)
            LOGGER(__name__).debug("Could not join chat %r (ignored).", c, exc_info=True)


class Userbot:
    def __init__(self):
        # create assistant clients but don't start them yet
        self.one = Client(
            name="AnonXAss1",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING1) if config.STRING1 is not None else None,
            no_updates=True,
        )
        self.two = Client(
            name="AnonXAss2",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING2) if config.STRING2 is not None else None,
            no_updates=True,
        )
        self.three = Client(
            name="AnonXAss3",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING3) if config.STRING3 is not None else None,
            no_updates=True,
        )
        self.four = Client(
            name="AnonXAss4",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING4) if config.STRING4 is not None else None,
            no_updates=True,
        )
        self.five = Client(
            name="AnonXAss5",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING5) if config.STRING5 is not None else None,
            no_updates=True,
        )

    async def start(self):
        LOGGER(__name__).info("Starting Assistants...")

        # ASSISTANT 1
        if _is_set(config.STRING1):
            await self.one.start()
            LOGGER(__name__).info("Assistant 1 session loaded: id=%r username=%r",
                                   getattr(self.one.me, "id", None), getattr(self.one.me, "username", None))
            # try join chat(s) quietly
            await _safe_join(self.one, "PhoenixXsupport", "where_lucy")
            assistants.append(1)

            ok = await _safe_send(self.one, config.LOGGER_ID, "Assistant Started")
            if not ok:
                # Log warning but DO NOT exit -- keep running
                LOGGER(__name__).warning(
                    "Assistant Account 1 could not access the log group. Make sure assistant is in the log group and promoted as admin."
                )
                # disable logging target for safety for subsequent assistants? we keep config but continue
            # set attributes
            self.one.id = self.one.me.id
            self.one.name = self.one.me.mention
            self.one.username = self.one.me.username
            assistantids.append(self.one.id)
            LOGGER(__name__).info("Assistant Started as %s", self.one.name)

        # ASSISTANT 2
        if _is_set(config.STRING2):
            await self.two.start()
            LOGGER(__name__).info("Assistant 2 session loaded: id=%r username=%r",
                                   getattr(self.two.me, "id", None), getattr(self.two.me, "username", None))
            await _safe_join(self.two, "PhoenixXsupport", "where_lucy")
            assistants.append(2)

            ok = await _safe_send(self.two, config.LOGGER_ID, "Assistant Started")
            if not ok:
                LOGGER(__name__).warning(
                    "Assistant Account 2 could not access the log group. Check membership/admin status."
                )
            self.two.id = self.two.me.id
            self.two.name = self.two.me.mention
            self.two.username = self.two.me.username
            assistantids.append(self.two.id)
            LOGGER(__name__).info("Assistant Two Started as %s", self.two.name)

        # ASSISTANT 3
        if _is_set(config.STRING3):
            await self.three.start()
            LOGGER(__name__).info("Assistant 3 session loaded: id=%r username=%r",
                                   getattr(self.three.me, "id", None), getattr(self.three.me, "username", None))
            await _safe_join(self.three, "PhoenixXsupport", "where_lucy")
            assistants.append(3)

            ok = await _safe_send(self.three, config.LOGGER_ID, "Assistant Started")
            if not ok:
                LOGGER(__name__).warning(
                    "Assistant Account 3 could not access the log group. Check membership/admin status."
                )
            self.three.id = self.three.me.id
            self.three.name = self.three.me.mention
            self.three.username = self.three.me.username
            assistantids.append(self.three.id)
            LOGGER(__name__).info("Assistant Three Started as %s", self.three.name)

        # ASSISTANT 4
        if _is_set(config.STRING4):
            await self.four.start()
            LOGGER(__name__).info("Assistant 4 session loaded: id=%r username=%r",
                                   getattr(self.four.me, "id", None), getattr(self.four.me, "username", None))
            await _safe_join(self.four, "PhoenixXsupport", "where_lucy")
            assistants.append(4)

            ok = await _safe_send(self.four, config.LOGGER_ID, "Assistant Started")
            if not ok:
                LOGGER(__name__).warning(
                    "Assistant Account 4 could not access the log group. Check membership/admin status."
                )
            self.four.id = self.four.me.id
            self.four.name = self.four.me.mention
            self.four.username = self.four.me.username
            assistantids.append(self.four.id)
            LOGGER(__name__).info("Assistant Four Started as %s", self.four.name)

        # ASSISTANT 5
        if _is_set(config.STRING5):
            await self.five.start()
            LOGGER(__name__).info("Assistant 5 session loaded: id=%r username=%r",
                                   getattr(self.five.me, "id", None), getattr(self.five.me, "username", None))
            await _safe_join(self.five, "PhoenixXsupport", "where_lucy")
            assistants.append(5)

            ok = await _safe_send(self.five, config.LOGGER_ID, "Assistant Started")
            if not ok:
                LOGGER(__name__).warning(
                    "Assistant Account 5 could not access the log group. Check membership/admin status."
                )
            self.five.id = self.five.me.id
            self.five.name = self.five.me.mention
            self.five.username = self.five.me.username
            assistantids.append(self.five.id)
            LOGGER(__name__).info("Assistant Five Started as %s", self.five.name)

    async def stop(self):
        LOGGER(__name__).info("Stopping Assistants...")
        try:
            if _is_set(config.STRING1):
                await self.one.stop()
            if _is_set(config.STRING2):
                await self.two.stop()
            if _is_set(config.STRING3):
                await self.three.stop()
            if _is_set(config.STRING4):
                await self.four.stop()
            if _is_set(config.STRING5):
                await self.five.stop()
        except Exception:
            LOGGER(__name__).warning("Error while stopping assistants (ignored).", exc_info=True)
