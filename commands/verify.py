import datetime
import discord
from discord.ext import commands
from discord.ui import Button, View


class Verify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def verify(self, ctx):
        button = Button(label="Click to Verify", style=discord.ButtonStyle.link, url="REPLACE_WITH_ACTUAL_LINK")

        view = View()
        view.add_item(button)

        embed = discord.Embed(
            title="How To Verify!",
            description="**Step 1:** Click on the button below. \n"
                        "**Step 2:** Fill out the form. \n"
                        "**Step 3:** Once you're done, ping a staff member.\n",
            color=discord.Colour.blurple(),
            timestamp=datetime.datetime.now(datetime.UTC),
        )
        embed.set_footer(text="\u200b", icon_url=ctx.message.author.display_avatar)
        await ctx.send(embed=embed, view=view)


async def setup(bot):
    await bot.add_cog(Verify(bot))
