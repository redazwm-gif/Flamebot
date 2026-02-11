import discord
from discord.ext import commands
import os

TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise ValueError("❌ Chưa set TOKEN trong Environment Variables")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Lưu dữ liệu
data = {}

# ================= FORM NHẬP ĐIỂM =================
class DiemModal(discord.ui.Modal, title="Nhập thông tin trận đấu"):

    team = discord.ui.TextInput(label="Tên Team", required=True)
    game = discord.ui.TextInput(label="ID Game", required=True)
    kill = discord.ui.TextInput(label="Số Kill", required=True)
    top = discord.ui.TextInput(label="Top", required=True)

    async def on_submit(self, interaction: discord.Interaction):

        team_name = self.team.value.strip()

        # Kiểm tra số
        try:
            kill = int(self.kill.value)
            top = int(self.top.value)
        except ValueError:
            await interaction.response.send_message(
                "❌ Kill và Top phải là số!",
                ephemeral=True
            )
            return

        # Bảng điểm top
        top_points = {
            1: 12, 2: 9, 3: 8, 4: 7, 5: 6,
            6: 5, 7: 4, 8: 3, 9: 2, 10: 1
        }

        diem_tran = kill + top_points.get(top, 0)

        # Nếu team chưa có thì tạo mới
        if team_name not in data:
            data[team_name] = {
                "point": 0,
                "match": 0
            }

        data[team_name]["point"] += diem_tran
        data[team_name]["match"] += 1

        # Embed kết quả
        embed = discord.Embed(
            title="🔥 KẾT QUẢ TRẬN 🔥",
            color=discord.Color.orange()
        )

        embed.add_field(name="🎮 Team", value=team_name, inline=False)
        embed.add_field(name="🆔 Game ID", value=self.game.value, inline=False)
        embed.add_field(name="💥 Kill", value=str(kill))
        embed.add_field(name="🏆 Top", value=str(top))
        embed.add_field(name="⭐ Điểm trận", value=str(diem_tran), inline=False)
        embed.add_field(name="📊 Tổng điểm", value=str(data[team_name]["point"]))
        embed.add_field(name="🎮 Tổng trận", value=str(data[team_name]["match"]))

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
            rank = medals[index]
        else:
            rank = f"{index+1}."

        embed.add_field(
            name=f"{rank} {team}",
            value=f"⭐ Điểm: {info['point']}\n🎮 Trận: {info['match']}",
            inline=False
        )

    await interaction.response.send_message(embed=embed)


# ================= /resetbxh =================
@bot.tree.command(name="resetbxh", description="Reset toàn bộ bảng xếp hạng (Admin)")
async def resetbxh(interaction: discord.Interaction):

    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message(
            "❌ Bạn không có quyền dùng lệnh này.",
            ephemeral=True
        )
        return

    data.clear()
    await interaction.response.send_message("✅ Đã reset toàn bộ bảng xếp hạng.")


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
