import datetime
import discord
from discord.ext import commands


class Pls(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def pls(self, ctx):
        embed = discord.Embed(
            title="Vouch Requested!",
            description="Hey there! Your opinion truly matters to us. If "
            "you've had an awesome experience with us, "
            "consider dropping a review or giving us a "
            "shout-out by typing `.vouch <mention staff who` "
            "`provided u acc> 1 <reason>` "
            "<review> in ⁠『✌』𝐕𝐨𝐮𝐜𝐡. Your words could "
            "inspire others to discover the same greatness "
            "you've found. Let's spread the positivity "
            "together!",
            color=discord.Colour.green(),
            timestamp=datetime.datetime.now(datetime.UTC),
        )
        embed.set_footer(text="\u200b", icon_url=ctx.message.author.display_avatar)
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Pls(bot))
