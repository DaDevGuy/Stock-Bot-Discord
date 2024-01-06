import discord
from discord.ext import commands
import gspread
import time
import datetime
from oauth2client.service_account import ServiceAccountCredentials

class VerificationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name('E:\\Wynx\\spreadsheet.json', self.scope)
        self.gc = gspread.authorize(self.credentials)

        self.sheet_url = 'REPLACE_WITH_DOCS_LINK_THINGY'

    def is_member_verified(self, member):
        try:
            sheet = self.gc.open_by_url(self.sheet_url).sheet1
            usernames = sheet.col_values(2)

            return member.name in usernames

        except Exception as e:
            print(f"Error checking verification: {e}")
            return False

    @commands.command(name='check')
    async def check_verification(self, ctx, member: discord.Member):
        if self.is_member_verified(member):
            embed1 = discord.Embed(title="Verified User", description=f"{member.mention} is a verified user!", color=discord.Colour.green(), timestamp=datetime.datetime.now(datetime.UTC))
            embed1.set_footer(text='\u200b', icon_url=member.display_avatar)
            await ctx.send(embed=embed1)
        else:
            embed = discord.Embed(title="Not Verified", description=f"{member.mention} is not a verified user!", color=discord.Colour.red(), timestamp=datetime.datetime.now(datetime.UTC))
            embed.set_footer(text='\u200b', icon_url=member.display_avatar)
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(VerificationCog(bot))
