import discord
from discord.ext import commands
import sqlite3
import random
import string

class PurchaseCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.conn = sqlite3.connect("purchase.db")  
        self.create_purchase_table()

    def create_purchase_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS purchases (
                purchase_id TEXT PRIMARY KEY,
                user_id INTEGER,
                notes TEXT
            )
        ''')
        self.conn.commit()

    def generate_purchase_id(self):
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(10))

    @commands.command(name='purchase')
    async def purchase_command(self, ctx, user: discord.User = None, *notes):
        if user is None or not notes:
            await ctx.send("Error: Please provide a username and notes for the purchase.")
            return

        notes_text = ' '.join(notes)

        purchase_id = self.generate_purchase_id()

        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO purchases (purchase_id, user_id, notes)
            VALUES (?, ?, ?)
        ''', (purchase_id, user.id, notes_text))
        self.conn.commit()

        await ctx.send(f"Purchase ID: {purchase_id} | User: {user.mention} | Notes: {notes_text}")

    @commands.command(name='valid')
    async def valid_command(self, ctx, purchase_id):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT user_id, notes FROM purchases WHERE purchase_id = ?
        ''', (purchase_id,))
        result = cursor.fetchone()

        if result is not None:
            user_id, notes = result
            user = self.bot.get_user(user_id)
            embed = discord.Embed(title="VALID!", description=f"Purchase ID: {purchase_id} is valid!")
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"Invalid! Purchase ID {purchase_id}.")


async def setup(bot):
    await bot.add_cog(PurchaseCog(bot))
