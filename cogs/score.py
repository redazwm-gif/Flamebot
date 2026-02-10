from discord.ext import commands

class Score(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="diem")
    async def diem(self, ctx, kill: int, hang: int):
        # ví dụ: 1 kill = 1 điểm, hạng 1 = 12 điểm
        hang_diem = {
            1: 12, 2: 9, 3: 8, 4: 7, 5: 6,
            6: 5, 7: 4, 8: 3, 9: 2, 10: 1
        }

        tong = kill + hang_diem.get(hang, 0)
        await ctx.send(f"🔥 **Tổng điểm:** `{tong}`")

async def setup(bot):
    await bot.add_cog(Score(bot))
