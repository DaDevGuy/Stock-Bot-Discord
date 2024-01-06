import discord
from discord.ext import commands
import datetime

class HelpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        help_embed = discord.Embed(title="Help", description="Help Desk for Wynx!", color=discord.Color.purple(), timestamp=datetime.datetime.utcnow())
        help_embed.set_author(name="Wynxx")

        commands_list = [
            ("**.addacc**", "Adds account to a category"),
            ("**.bgen**", "Generates a basic account"),
            ("**.pgen**", "Generates a premium account :star:"),
            ("**.egen**", "Generates an extreme account :star:"),
            ("**.redeem**", "Redeem a code for a service"),
            ("**.sendcookie**", "Sends a cookie to a user"),
            ("**.submit**", "Submit Accounts"),
            ("**.drop**", ".drop `start/stop`"),
            ("**.nuke**", ".nuke (number of messages) `.nuke 100`"),
            ("**.slb**", "Shows submissions leaderboard"),
            ("**.help**", "Shows this message"),
            ("**.stock**", "Shows the number of accounts in each category"),
            ("**.rep**", "Vouch someone `.rep @username 0/1 Reason for vouch`"),
            ("**.profile**", "View vouch profile of a user"),
            ("**.lb**", "View vouch Leaderboard"),
            ("**.listsub**", "Shows recently submitted accounts"),
            ("**.check**", "Check if the user is verified"),
            ("**.verify**", "Request verification"),
            ("**.send**", "Send Accounts `.send @username (category) (service)!`"),
            ("**.pls**", "Request a vouch!"),
            ("**.verify**", "Request verification!"),
        ]

        for command, description in commands_list:
            help_embed.description += f"\n{command}: {description}"

        help_embed.set_footer(text='\u200b', icon_url=ctx.author.display_avatar)

        await ctx.send(embed=help_embed)


async def setup(bot):
    await bot.add_cog(HelpCommand(bot))
