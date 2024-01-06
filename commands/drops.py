import datetime

import discord
from discord.ext import commands

class DropCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.drop_active = False

    @commands.command(name='drop', aliases=['d'])
    async def drop(self, ctx, action=None):
        print(f"Command invoked: {ctx.message.content}")

        if action == 'start':
            if self.drop_active:
                await ctx.send('A drop is already active. Use `.drop stop` to end it before starting a new one.')
            else:
                embed = discord.Embed(title='Drop Started!', description='@everyone A new drop has started! Hurry up and get the drops!!', color=discord.Color.green(), timestamp=datetime.datetime.now(datetime.UTC))
                embed.set_footer(text='\u200b', icon_url=ctx.message.author.display_avatar)
                allowed_mentions = discord.AllowedMentions(everyone=True)
                await ctx.send(embed=embed, allowed_mentions=allowed_mentions)

                self.drop_active = True
        elif action == 'stop':
            if not self.drop_active:
                await ctx.send('No active drop to stop.')
            else:
                embed = discord.Embed(title='Drop Stopped!', description='The drop has ended. Better luck next time!', color=discord.Color.red(), timestamp=datetime.datetime.now(datetime.UTC))
                embed.set_footer(text='\u200b', icon_url=ctx.message.author.display_avatar)
                await ctx.send(embed=embed)
                self.drop_active = False
        else:
            await ctx.send('Invalid action. Use `.drop start` or `.drop stop`.')

async def setup(bot):
    await bot.add_cog(DropCog(bot))
