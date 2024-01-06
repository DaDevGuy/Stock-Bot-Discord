import discord
from discord.ext import commands
import sqlite3

class SendCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.conn = sqlite3.connect('accounts.db')
        self.cursor = self.conn.cursor()

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def send(self, ctx, user: discord.User, category=None, service=None):
        if category is None or service is None:
            await ctx.send('Please provide the category, service, and mention the user. Example: `.send @username basic netflix`')
            return

        if not self.has_available_accounts(category, service):
            await ctx.send(f'No available accounts for {service} in the {category} category.')
            return
        
        self.cursor.execute('''
            SELECT id, email, password FROM accounts
            WHERE category = ? AND service = ?
            ORDER BY RANDOM() LIMIT 1
        ''', (category, service))
        account_result = self.cursor.fetchone()

        if account_result:
            account_id, email, password = account_result

            self.cursor.execute('''
                DELETE FROM accounts
                WHERE id = ?
            ''', (account_id,))
            self.conn.commit()

            await user.send(
                f'Account details for {service} ({category}):\nEmail: {email}\nPassword: {password}'
            )

            await ctx.send(f'Successfully sent account details to {user.mention}!')
        else:
            await ctx.send(f'No accounts available for the specified category and service.')
    @send.error
    async def send_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permissions to run this command!")


    def has_available_accounts(self, category, service):
        self.cursor.execute('''
            SELECT COUNT(*) FROM accounts
            WHERE category = ? AND service = ?
        ''', (category, service))
        count = self.cursor.fetchone()[0]
        return count > 0


async def setup(bot):
    await bot.add_cog(SendCog(bot))
