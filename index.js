import discord
from discord import app_commands
from discord.ext import commands
import os

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

data = {}

class DiemModal(discord.ui.Modal, title="Nhập thông tin trận đấu"):

    id_custom = discord.ui.TextInput(label="ID Custom", placeholder="VD: TT2")
    id_game = discord.ui.TextInput(label="ID Game", placeholder="VD: 1")
    kill = discord.ui.TextInput(label="Số Kill", placeholder="VD: 5")
    top = discord.ui.TextInput(label="Top", placeholder="VD: 1")

    async def on_submit(self, interaction: discord.Interaction):
        custom = str(self.id_custom)
        game = str(self.id_game)
        kill = int(self.kill)
        top = int(self.top)

        diem = kill + (15 - top)

        if custom not in data:
            data[custom] = 0

        data[custom] += diem

        await interaction.response.send_message(
            f"✅ Custom: {custom}\n🎮 Game: {game}\n💥 Kill: {kill}\n🏆 Top: {top}\n⭐ Điểm trận: {diem}\n🔥 Tổng điểm custom: {data[custom]}"
        )

@bot.tree.command(name="tinhdiem", description="Nhập điểm bằng form popup")
async def tinhdiem(interaction: discord.Interaction):
    await interaction.response.send_modal(DiemModal())

@bot.tree.command(name="bxh", description="Xem bảng xếp hạng")
async def bxh(interaction: discord.Interaction):
    if not data:
        await interaction.response.send_message("Chưa có dữ liệu.")
        return

    msg = "🏆 BẢNG XẾP HẠNG:\n"
    for custom, diem in data.items():
        msg += f"{custom}: {diem} điểm\n"

    await interaction.response.send_message(msg)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print("Bot đã sẵn sàng!")

bot.run(TOKEN)
