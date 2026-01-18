# AnonXMusic/core/bot.py
from pyrogram import Client, errors
from pyrogram.enums import ChatMemberStatus, ParseMode

import config

from ..logging import LOGGER


class Anony(Client):
    def __init__(self):
        # start log (ke console/logger)
        LOGGER(__name__).info("Starting Bot...")
        super().__init__(
            name="siyaxbot",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            in_memory=True,
            parse_mode=ParseMode.HTML,
            max_concurrent_transmissions=7,
        )
        # keep a reference logger for convenience
        self._log = LOGGER(__name__)

    async def _safe_init_logger_chat(self):
        """
        Try to send a startup message to the configured LOGGER_ID.
        If anything goes wrong (bad format, bot not in channel, etc) we
        gracefully disable logger id (set config.LOGGER_ID = None) so
        the bot won't crash and can continue running.
        """
        self._log.info("Resolved LOGGER_ID: %r (type=%s)", config.LOGGER_ID, type(config.LOGGER_ID).__name__)

        if not config.LOGGER_ID:
            self._log.warning("LOGGER_ID is falsy/None; skipping log group/channel setup.")
            return

        try:
            # Try to send a message to the LOGGER_ID to verify access
            await self.send_message(
                chat_id=config.LOGGER_ID,
                text=(
                    f"<u><b>» {self.me.mention} ʙᴏᴛ sᴛᴀʀᴛᴇᴅ :</b><u>\n\n"
                    f"ɪᴅ : <code>{self.id}</code>\n"
                    f"ɴᴀᴍᴇ : {self.me.first_name} {self.me.last_name or ''}\n"
                    f"ᴜsᴇʀɴᴀᴍᴇ : @{self.me.username if self.me.username else 'None'}"
                ),
            )
            self._log.info("Startup message sent to LOGGER_ID successfully.")
        except (errors.ChannelInvalid, errors.PeerIdInvalid) as e:
            self._log.error(
                "Bot failed to access the log group/channel (ChannelInvalid/PeerIdInvalid). "
                "Disabling LOGGER_ID to avoid crash. Error: %s", repr(e), exc_info=True
            )
            config.LOGGER_ID = None
            return
        except ValueError as ve:
            # Handles bad types like int("") or other casting issues if they bubble up
            self._log.error(
                "ValueError while trying to send startup message to LOGGER_ID=%r. Disabling LOGGER_ID. Error: %s",
                config.LOGGER_ID, repr(ve), exc_info=True
            )
            config.LOGGER_ID = None
            return
        except Exception as ex:
            # Any other exception (bot not in chat, banned, network error, etc)
            self._log.error(
                "Unexpected error while accessing log group/channel for LOGGER_ID=%r. Disabling LOGGER_ID. "
                "Exception: %s", config.LOGGER_ID, repr(ex), exc_info=True
            )
            config.LOGGER_ID = None
            return

        # If we get here, the send_message succeeded. Now double-check admin status.
        try:
            member = await self.get_chat_member(config.LOGGER_ID, self.id)
            if member.status != ChatMemberStatus.ADMINISTRATOR:
                self._log.error(
                    "Bot is not an administrator in the log group/channel (LOGGER_ID=%r). "
                    "Promote the bot if you want full logging functionality. Continuing without admin privileges.",
                    config.LOGGER_ID
                )
                # do not disable LOGGER_ID — just warn. If the bot needs admin perms, some features may be limited.
            else:
                self._log.info("Bot is administrator in the log group/channel.")
        except Exception as ex:
            # If checking member status fails, log and disable logger id to avoid crashes later
            self._log.error(
                "Failed to verify bot's admin status in LOGGER_ID=%r. Disabling LOGGER_ID to avoid crash. Error: %s",
                config.LOGGER_ID, repr(ex), exc_info=True
            )
            config.LOGGER_ID = None

    async def start(self):
        # start the pyrogram client
        await super().start()

        # assign some useful attrs
        self.id = self.me.id
        self.name = self.me.first_name + " " + (self.me.last_name or "")
        self.username = self.me.username
        self.mention = self.me.mention

        # Try safe logger initialization (will not crash bot)
        await self._safe_init_logger_chat()

        # If LOGGER_ID got disabled above, we skip the strict admin check.
        if config.LOGGER_ID:
            # at this point we've already attempted get_chat_member in _safe_init_logger_chat,
            # but do a harmless recheck if desired. We wrap in try/except to avoid crash.
            try:
                a = await self.get_chat_member(config.LOGGER_ID, self.id)
                if a.status != ChatMemberStatus.ADMINISTRATOR:
                    self._log.error(
                        "Please promote your bot as an admin in your log group/channel (LOGGER_ID=%r). "
                        "Continuing without admin privileges.",
                        config.LOGGER_ID
                    )
                else:
                    self._log.info("Logger channel setup verified.")
            except Exception:
                # We already logged details in _safe_init_logger_chat; ignore here.
                pass
        else:
            # LOGGER_ID is disabled / not configured
            self._log.warning("Logger channel is not configured or was disabled during init. Continuing without it.")

        self._log.info(f"Music Bot Started as {self.name}")

    async def stop(self):
        await super().stop()
