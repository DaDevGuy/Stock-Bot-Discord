import os
import discord
from discord.ext import commands
import datetime

class SubmissionsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.submissions_folder = "Submissions"

    @commands.command(name='listsub')
    async def listsub(self, ctx):
        try:
            submissions = []

            for filename in os.listdir(self.submissions_folder):
                if filename.endswith(".txt"):
                    service_name = filename[:-4]  
                    file_path = os.path.join(self.submissions_folder, filename)

                    with open(file_path, 'r') as file:
                        content = file.read()
                        submissions.append({"service": service_name, "content": content})

            embed = discord.Embed(title="Recent Submissions", color=0x00ff00, timestamp=datetime.datetime.now(datetime.UTC))

            for submission in submissions:
                embed.add_field(name=submission["service"], value=submission["content"], inline=False)

            embed.set_footer(text='\u200b', icon_url=ctx.message.author.display_avatar)

            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

async def setup(bot):
    await bot.add_cog(SubmissionsCog(bot))
