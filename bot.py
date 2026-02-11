import discord
from discord.ext import commands
import os

TOKEN = os.getenv("TOKEN")

if TOKEN is None:
    raise ValueError("❌ Chưa set TOKEN trong Environment Variables")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

data = {}

# ================= FORM =================
class DiemModal(discord.ui.Modal, title="Nhập thông tin trận đấu"):

    team = discord.ui.TextInput(label="Tên Team")
    game = discord.ui.TextInput(label="ID Game")
    kill = discord.ui.TextInput(label="Số Kill")
    top = discord.ui.TextInput(label="Top")

    async def on_submit(self, interaction: discord.Interaction):

        team_name = self.team.value.strip()

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

        diem_tran = kill + top_points.get(top, 0)

        if team_name not in data:
            data[team_name] = {"point": 0, "match": 0}

        data[team_name]["point"] += diem_tran
        data[team_name]["match"] += 1

        embed = discord.Embed(
            title="🔥 KẾT QUẢ TRẬN",
            color=discord.Color.orange()
        )

        embed.add_field(name="🎮 Team", value=team_name, inline=False)
        embed.add_field(name="💥 Kill", value=kill)
        embed.add_field(name="🏆 Top", value=top)
        embed.add_field(name="⭐ Điểm trận", value=diem_tran)
        embed.add_field(name="📊 Tổng điểm", value=data[team_name]["point"])
        embed.add_field(name="🎮 Tổng trận", value=data[team_name]["match"])

        await interaction.response.send_message(embed=embed)

# ================= /tinhdiem =================
@bot.tree.command(name="tinhdiem", description="Nhập điểm bằng form popup")
async def tinhdiem(interaction: discord.Interaction):
    await interaction.response.send_modal(DiemModal())

# ================= /bxh =================
@bot.tree.command(name="bxh", description="Xem bảng xếp hạng")
async def bxh(interaction: discord.Interaction):

    if not data:
        await interaction.response.send_message("❌ Chưa có dữ liệu.")
        return

    sorted_data = sorted(
        data.items(),
        key=lambda x: x[1]["point"],
        reverse=True
    )

    embed = discord.Embed(
        title="🏆 BẢNG XẾP HẠNG 🏆",
        color=discord.Color.gold()
    )

    medals = ["🥇", "🥈", "🥉"]

    for index, (team, info) in enumerate(sorted_data):

        if index < 3:
            rank_icon = medals[index]
        else:
            rank_icon = f"{index+1}️⃣"

        embed.add_field(
            name=f"{rank_icon} {team}",
            value=f"⭐ Điểm: {info['point']}\n🎮 Số trận: {info['match']}",
            inline=False
        )

    await interaction.response.send_message(embed=embed)

# ================= RESET =================
@bot.tree.command(name="resetbxh", description="Reset toàn bộ điểm")
async def resetbxh(interaction: discord.Interaction):
    data.clear()
    await interaction.response.send_message("✅ Đã reset bảng xếp hạng.")

# ================= READY =================
@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"✅ Đã sync {len(synced)} slash command")
    except Exception as e:
        print(e)

    print(f"🔥 Bot đã đăng nhập: {bot.user}")

bot.run(TOKEN)
