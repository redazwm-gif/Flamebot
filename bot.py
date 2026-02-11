"""
Copyright © Krypton 2019-Present - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized Discord bot in Python

Version: 6.5.0
"""

import logging
import os
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

# ================= INTENTS =================

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# ================= LOGGING =================

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("discord_bot")

# ================= DIEM DATA =================

diem_data = {}

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

        self.tree.add_command(diem)
        self.tree.add_command(bxh)

        await self.tree.sync()
        logger.info("Slash command đã sync xong!")

    async def on_ready(self):
        logger.info(f"Đã đăng nhập: {self.user}")

# ================= SLASH COMMAND DIEM =================

@app_commands.command(name="diem", description="Quản lý điểm")
@app_commands.describe(
    hanh_dong="xem / cong / tru",
    user="Chọn người",
    so_diem="Số điểm (nếu cộng/trừ)"
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
            f"✅ Đã cộng {so_diem} điểm cho {user.mention}\nTổng: {diem_data[uid]}"
        )

    elif hanh_dong.value == "tru":
        diem_data[uid] -= so_diem
        await interaction.response.send_message(
            f"➖ Đã trừ {so_diem} điểm của {user.mention}\nTổng: {diem_data[uid]}"
        )

# ================= SLASH COMMAND BXH =================

@app_commands.command(name="bxh", description="Xem bảng xếp hạng")
async def bxh(interaction: discord.Interaction):

    if not diem_data:
        await interaction.response.send_message("Chưa có dữ liệu điểm.")
        return

    sorted_users = sorted(diem_data.items(), key=lambda x: x[1], reverse=True)

    message = "🏆 **BẢNG XẾP HẠNG** 🏆\n\n"

    for i, (uid, score) in enumerate(sorted_users[:10], start=1):
        member = interaction.guild.get_member(uid)
        if member:
            message += f"{i}. {member.display_name} - {score} điểm\n"

    await interaction.response.send_message(message)

# ================= RUN BOT =================

bot = DiscordBot()
bot.run(os.getenv("TOKEN"))
