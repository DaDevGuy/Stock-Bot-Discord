import datetime

import discord
from discord.ext import commands
import os
import random

class sendcookie(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def upload_file(self, user, file_path):
        # Create a Discord File object
        file = discord.File(file_path)

        # Get the user's DM channel or create one
        dm_channel = user.dm_channel or await user.create_dm()

        instructions = "Here's your cookie! Please download the file and enjoy."
        await dm_channel.send(instructions)

        # Send the file to the DM channel and get the message
        message = await dm_channel.send(file=file)

        # Return the download link
        return message.attachments[0].url

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def sendcookie(self, ctx, user: discord.User):
        try:
            if ctx.author.id == user.id:
                await ctx.reply("You can't send cookies to yourself!")
                return

            # Get a list of all files in the Cookies folder ending with ".txt"
            files = [file for file in os.listdir("Cookies") if file.endswith(".txt")]

            if files:
                # Select a random file from the list
                filename = random.choice(files)
                file_path = os.path.join("Cookies", filename)

                # Upload the file and get the link
                download_link = await self.upload_file(user, file_path)

                # Send the download link
                embed = discord.Embed(title="Success", description=f"Cookie sent to {user.mention} in their DMs!", color=discord.Colour.green(), timestamp=datetime.datetime.now(datetime.UTC))
                embed.set_footer(text='\u200b', icon_url=ctx.message.author.display_avatar)
                await ctx.send(embed=embed)

                # Delete the file
                os.remove(file_path)
            else:
                await ctx.send("No cookie files found in the Cookies folder.")
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")
async def setup(bot):
    await bot.add_cog(sendcookie(bot))
