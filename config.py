# config.py
# Safe, minimal-change replacement for your original config.py
# Keeps defaults (including LOGGER_ID = -1002936649318)

import re
import os
from os import getenv
from dotenv import load_dotenv
from pyrogram import filters

load_dotenv()

# ---------- helper parsers ----------
def _getenv_raw(name: str, default=None):
    v = os.getenv(name, None)
    if v is None:
        return default
    v = v.strip()
    # remove accidental surrounding quotes
    if (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")):
        v = v[1:-1].strip()
    if v == "":
        return default
    return v

def parse_int_env(name: str, default=None):
    raw = _getenv_raw(name, None)
    if raw is None:
        return default
    try:
        return int(raw)
    except (ValueError, TypeError):
        return default

def parse_chat_env(name: str, default=None):
    """
    Returns:
      - int (for -100... style chat IDs) if parseable
      - str (for @channelusername) if not integer
      - default if env missing/empty
    """
    raw = _getenv_raw(name, None)
    if raw is None:
        return default
    try:
        return int(raw)
    except (ValueError, TypeError):
        return raw  # keep username string like '@channelname'

def parse_bool_env(name: str, default=False):
    raw = _getenv_raw(name, None)
    if raw is None:
        return default
    low = str(raw).lower()
    if low in ("1", "true", "yes", "y", "on"):
        return True
    if low in ("0", "false", "no", "n", "off"):
        return False
    return default

# ---------- core credentials ----------
# Get this value from my.telegram.org/apps
API_ID = parse_int_env("API_ID", None)
API_HASH = _getenv_raw("API_HASH", None)

# Get your token from @BotFather on Telegram.
BOT_TOKEN = _getenv_raw("BOT_TOKEN", None)

# Get your bot username without '@'
BOT_USERNAME = _getenv_raw("BOT_USERNAME", None)

# Get your mongo url from cloud.mongodb.com
MONGO_DB_URI = _getenv_raw("MONGO_DB_URI", None)

# duration limit minutes (string env or number acceptable)
DURATION_LIMIT_MIN = parse_int_env("DURATION_LIMIT", 60000)

# Chat id of a group for logging bot's activities
DEFAULT_LOGGER_ID = -1002936649318
LOGGER_ID = parse_chat_env("LOGGER_ID", DEFAULT_LOGGER_ID)

# LOGGER_ID Id Also Use No Problem
BOTADDLOGS = parse_chat_env("BOTADDLOGS", DEFAULT_LOGGER_ID)

# Get this value from @FallenxBot on Telegram by /id
OWNER_ID = parse_int_env("OWNER_ID", 6995317382)

## Fill these variables if you're deploying on heroku.
# Your heroku app name
HEROKU_APP_NAME = _getenv_raw("HEROKU_APP_NAME", None)
# Get it from http://dashboard.heroku.com/account
HEROKU_API_KEY = _getenv_raw("HEROKU_API_KEY", None)

UPSTREAM_REPO = _getenv_raw(
    "UPSTREAM_REPO",
    "https://github.com/arfin03/ryo-music-v2",
)
UPSTREAM_BRANCH = _getenv_raw("UPSTREAM_BRANCH", "master")
GIT_TOKEN = _getenv_raw("GIT_TOKEN", None)

SUPPORT_CHANNEL = _getenv_raw("SUPPORT_CHANNEL", "https://t.me/padukaanos")
SUPPORT_CHAT = _getenv_raw("SUPPORT_CHAT", "https://t.me/gc_animecommunity")

ANIMES = _getenv_raw("ANIMES", "https://t.me/gc_animecommunity")

# Set this to True if you want the assistant to automatically leave chats after an interval
AUTO_LEAVING_ASSISTANT = parse_bool_env("AUTO_LEAVING_ASSISTANT", True)

# Get this credentials from https://developer.spotify.com/dashboard
SPOTIFY_CLIENT_ID = _getenv_raw("SPOTIFY_CLIENT_ID", "22b6125bfe224587b722d6815002db2b")
SPOTIFY_CLIENT_SECRET = _getenv_raw("SPOTIFY_CLIENT_SECRET", "c9c63c6fbf2f467c8bc68624851e9773")

# Maximum limit for fetching playlist's track from youtube, spotify, apple links.
PLAYLIST_FETCH_LIMIT = parse_int_env("PLAYLIST_FETCH_LIMIT", 60)

# Telegram audio and video file size limit (in bytes)
TG_AUDIO_FILESIZE_LIMIT = parse_int_env("TG_AUDIO_FILESIZE_LIMIT", 104857600)
TG_VIDEO_FILESIZE_LIMIT = parse_int_env("TG_VIDEO_FILESIZE_LIMIT", 1073741824)
# Checkout https://www.gbmb.org/mb-to-bytes for converting mb to bytes

# Get your pyrogram v2 session from @StringFatherBot on Telegram
STRING1 = _getenv_raw("STRING_SESSION", None)
STRING2 = _getenv_raw("STRING_SESSION2", None)
STRING3 = _getenv_raw("STRING_SESSION3", None)
STRING4 = _getenv_raw("STRING_SESSION4", None)
STRING5 = _getenv_raw("STRING_SESSION5", None)

BANNED_USERS = filters.user()
adminlist = {}
lyrical = {}
votemode = {}
autoclean = []
confirmer = {}

START_IMG_URL = _getenv_raw(
    "START_IMG_URL", "https://f.uguu.se/KJpKMnzR.mp4"
)
PING_IMG_URL = _getenv_raw(
    "PING_IMG_URL", "https://telegra.ph/file/6ecedcea37c0e827ed809.jpg"
)
PLAYLIST_IMG_URL = "https://telegra.ph/file/9806820d661b377f7fb4f.jpg"
STATS_IMG_URL = "https://telegra.ph/file/9806820d661b377f7fb4f.jpg"
TELEGRAM_AUDIO_URL = "https://telegra.ph/file/9806820d661b377f7fb4f.jpg"
TELEGRAM_VIDEO_URL = "https://telegra.ph/file/9806820d661b377f7fb4f.jpg"
STREAM_IMG_URL = "https://telegra.ph/file/9806820d661b377f7fb4f.jpg"
SOUNCLOUD_IMG_URL = "https://telegra.ph/file/9806820d661b377f7fb4f.jpg"
YOUTUBE_IMG_URL = "https://telegra.ph/file/9806820d661b377f7fb4f.jpg"
SPOTIFY_ARTIST_IMG_URL = "https://telegra.ph/file/9806820d661b377f7fb4f.jpg"
SPOTIFY_ALBUM_IMG_URL = "https://telegra.ph/file/9806820d661b377f7fb4f.jpg"
SPOTIFY_PLAYLIST_IMG_URL = "https://telegra.ph/file/9806820d661b377f7fb4f.jpg"

def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60**i for i, x in enumerate(reversed(stringt.split(":"))))

DURATION_LIMIT = int(time_to_seconds(f"{DURATION_LIMIT_MIN}:00"))

if SUPPORT_CHANNEL:
    if not re.match("(?:http|https)://", SUPPORT_CHANNEL):
        raise SystemExit(
            "[ERROR] - Your SUPPORT_CHANNEL url is wrong. Please ensure that it starts with https://"
        )

if SUPPORT_CHAT:
    if not re.match("(?:http|https)://", SUPPORT_CHAT):
        raise SystemExit(
            "[ERROR] - Your SUPPORT_CHAT url is wrong. Please ensure that it starts with https://"
        )

# For debugging: quick snapshot (avoid printing tokens)
def as_dict():
    return {
        "API_ID": API_ID,
        "API_HASH_set": bool(API_HASH),
        "BOT_TOKEN_set": bool(BOT_TOKEN),
        "BOT_USERNAME": BOT_USERNAME,
        "LOGGER_ID": LOGGER_ID,
        "BOTADDLOGS": BOTADDLOGS,
        "OWNER_ID": OWNER_ID,
        "HEROKU_APP_NAME": HEROKU_APP_NAME is not None,
        "AUTO_LEAVING_ASSISTANT": AUTO_LEAVING_ASSISTANT,
        "DURATION_LIMIT_MIN": DURATION_LIMIT_MIN,
    }
