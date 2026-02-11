"""
Copyright © Krypton 2019-Present - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized Discord bot in Python

Version: 6.5.0
"""

import json
import logging
import os
import platform
import random

import aiosqlite
import discord
from discord import app_commands
from discord.ext import commands, tasks
from dotenv import load_dotenv

load_dotenv()

# ================= INTENTS =================

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

# ================= LOGGING =================

class LoggingFormatter(logging.Formatter):
    COLORS = {
        logging.DEBUG: "\x1b[38m",
        logging.INFO: "\x1b[34m",
        logging.WARNING: "\x1b[33m",
        logging.ERROR: "\x1b[31m",
        logging.CRITICAL: "\x1b[31;1m",
    }

    def format(self, record):
        log_color = self.COLORS.get(record.levelno, "")
        formatter = logging.Formatter(
            f"{log_color}[{{asctime}}] [{{levelname}}] {{message}}\x1b[0m",
            "%Y-%m-%d %H:%M:%S",
            style="{",
        )
        return formatter.format(record)


logger = logging.getLogger("discord_bot")
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setFormatter(LoggingFormatter())
logger.addHandler(console_handler)

# ================= DIEM DATA =================

diem_data = {}

# ================= SLASH COMMAND =================

@app_commands.describe(
    user="Người cần xem/chỉnh điểm",
    so_diem="Số điểm",
    hanh_dong="xem / cong / tru"
)
@app_commands.choices(hanh_dong=[
    app_commands.Choice(name="xem", value="xem"),
    app_commands.Choice(name="cong", value="cong"),
    app_commands.Choice(name="tru", value="tru"),
])
async def diem(
    interaction: discord.Interaction,
    hanh_dong: app_commands.Choice[str],
    user: discord.Member,
    so_diem: int = 0
):
    uid = user.id
    diem_data.setdefault(uid, 0)

    if hanh_dong.value == "xem":
        await interaction.response.send_message(
            f"📊 Điểm của {user.mention}: {diem_data[uid]}"
        )

    elif hanh_dong.value == "cong":
        diem_data[uid] += so_diem
        await interaction.response.send_message(
            f"✅ Đã cộng {so_diem} điểm cho {user.mention}"
        )

    elif hanh_dong.value == "tru":
        diem_data[uid] -= so_diem
        await interaction.response.send_message(
            f"➖ Đã trừ {so_diem} điểm của {user.mention}"
        )

# ================= BOT CLASS =================

class DiscordBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="!",
            intents=intents,
            help_command=None,
        )

    async def setup_hook(self):
        logger.info("Bot đang khởi động...")

        # Add slash command
        self.tree.add_command(diem)

        # Sync command
        await self.tree.sync()

        logger.info("Slash command đã sync xong!")

    async def on_ready(self):
        logger.info(f"Đã đăng nhập: {self.user}")

# ================= RUN BOT =================

bot = DiscordBot()
bot.run(os.getenv("TOKEN"))
