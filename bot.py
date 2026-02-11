import discord
from discord.ext import commands
import os

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# Lưu dữ liệu
data = {}

# ================= FORM POPUP =================
class DiemModal(discord.ui.Modal, title="Nhập thông tin trận đấu"):

    id_custom = discord.ui.TextInput(
        label="ID Custom",
        placeholder="VD: TT2"
    )

    id_game = discord.ui.TextInput(
        label="ID Game",
        placeholder="VD: 1"
    )

    kill = discord.ui.TextInput(
        label="Số Kill",
        placeholder="VD: 5"
    )

    top = discord.ui.TextInput(
        label="Top",
        placeholder="VD: 1"
    )

    async def on_submit(self, interaction: discord.Interaction):

        custom = self.id_custom.value
        game = self.id_game.value

        try:
            kill = int(self.kill.value)
            top = int(self.top.value)
        except:
            await interaction.response.send_message("❌ Kill và Top phải là số!", ephemeral=True)
            return

        # Công thức tính điểm (có thể chỉnh)
        diem = kill + (15 - top)

        if custom not in data:
            data[custom] = {"point": 0, "match": 0}

        data[custom]["point"] += diem
        data[custom]["match"] += 1

        await interaction.response.send_message(
            f"🔥 Custom: {custom}\n"
            f"🎮 Game: {game}\n"
            f"💥 Kill: {kill}\n"
            f"🏆 Top: {top}\n"
            f"⭐ Điểm trận: {diem}\n"
            f"📊 Tổng điểm: {data[custom]['point']}\n"
            f"🎮 Tổng trận: {data[custom]['match']}"
        )

# ================= LỆNH /tinhdiem =================
@bot.tree.command(name="tinhdiem", description="Nhập điểm bằng form popup")
async def tinhdiem(interaction: discord.Interaction):
    await interaction.response.send_modal(DiemModal())

# ================= LỆNH /bxh =================
@bot.tree.command(name="bxh", description="Xem bảng xếp hạng")
async def bxh(interaction: discord.Interaction):
    if not data:
        await interaction.response.send_message("Chưa có dữ liệu điểm.")
        return

    sorted_data = sorted(data.items(), key=lambda x: x[1]["point"], reverse=True)

    msg = "🏆 **BẢNG XẾP HẠNG** 🏆\n\n"

    medals = ["🥇", "🥈", "🥉"]

    for i, (custom, info) in enumerate(sorted_data):
        medal = medals[i] if i < 3 else f"{i+1}."
        msg += f"{medal} **{custom}**\n"
        msg += f"   ⭐ Điểm: {info['point']}\n"
        msg += f"   🎮 Số trận: {info['match']}\n\n"

    await interaction.response.send_message(msg)

# ================= READY =================
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Đã đăng nhập: {bot.user}")

bot.run(TOKEN)
