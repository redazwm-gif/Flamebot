import discord
from discord.ext import commands
import os
from PIL import Image, ImageDraw, ImageFont

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

data = {}

# ================= FORM =================
class DiemModal(discord.ui.Modal, title="Nhập thông tin trận đấu"):

    id_custom = discord.ui.TextInput(label="ID Custom")
    id_game = discord.ui.TextInput(label="ID Game")
    kill = discord.ui.TextInput(label="Số Kill")
    top = discord.ui.TextInput(label="Top")

    async def on_submit(self, interaction: discord.Interaction):

        custom = self.id_custom.value
        game = self.id_game.value

        try:
            kill = int(self.kill.value)
            top = int(self.top.value)
        except:
            await interaction.response.send_message(
                "❌ Kill và Top phải là số!",
                ephemeral=True
            )
            return

        top_points = {
            1: 12, 2: 9, 3: 8, 4: 7, 5: 6,
            6: 5, 7: 4, 8: 3, 9: 2, 10: 1
        }

        diem = kill + top_points.get(top, 0)

        if custom not in data:
            data[custom] = {
                "point": 0,
                "match": 0
            }

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
@bot.tree.command(name="bxh", description="Xem bảng xếp hạng ảnh")
async def bxh(interaction: discord.Interaction):

    if not data:
        await interaction.response.send_message("Chưa có dữ liệu.")
        return

    await interaction.response.defer()

    sorted_data = sorted(
        data.items(),
        key=lambda x: x[1]["point"],
        reverse=True
    )

    # ===== MỞ ẢNH NỀN =====
    try:
        img = Image.open("retouch_2026021117323495.png").convert("RGB")
    except:
        await interaction.followup.send("❌ Không tìm thấy background.png")
        return

    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("arial.ttf", 30)
    except:
        font = ImageFont.load_default()

    y = 200
    rank = 1

    for custom, info in sorted_data:
        text = f"{rank}. {custom} - {info['point']} điểm ({info['match']} trận)"
        draw.text((150, y), text, fill="white", font=font)
        y += 60
        rank += 1

    img_path = "bxh.png"
    img.save(img_path)

    await interaction.followup.send(file=discord.File(img_path))

# ================= READY =================
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Đã đăng nhập: {bot.user}")

bot.run(TOKEN)
