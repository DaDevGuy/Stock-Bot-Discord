import discord 
from discord.ext import commands

class ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(activity=discord.Game(name=".help | Gen"))
        print('Logged in as Wynx!')
        print("______________")


    @commands.command()
    async def ping(self, ctx):
        await ctx.send("Pong!")



async def setup(bot):
    await bot.add_cog(ping(bot))