import discord
from discord.ext import commands

class Nuke(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # @commands.Cog.listener()
    # async def on_ready(self):
    #     print('Nuke is ready!')

    @commands.command(name='nuke', aliases=['clear'])
    @commands.has_permissions(administrator=True)
    async def nuke(self, ctx, amount: int = 100):
        try:
            amount = max(1, min(amount, 1000))

            await ctx.channel.purge(limit=amount)
            await ctx.send(f"Nuke successful! Deleted {amount} messages.")
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

    @nuke.error
    async def nuke_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have the required permissions to use the nuke command.")

async def setup(bot):
    await bot.add_cog(Nuke(bot))