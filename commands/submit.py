import discord
from discord.ext import commands
import os
import sqlite3
import datetime

class SubmitCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.submissions_folder = "Submissions"
        self.database_path = os.path.join(self.submissions_folder, "submissions.db")

        os.makedirs(self.submissions_folder, exist_ok=True)
        self._initialize_database()

    def _initialize_database(self):
        with sqlite3.connect(self.database_path) as conn:
            cursor = conn.cursor()

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS leaderboard (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    submitted_by TEXT,
                    count INTEGER
                )
            ''')

            conn.commit()

    @commands.command(name='submit')
    async def submit(self, ctx, *, account_details):
        try:
            
            submission_time = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M")

            with sqlite3.connect(self.database_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR IGNORE INTO leaderboard (submitted_by, count) VALUES (?, 0)
                ''', (ctx.author.name,))

                cursor.execute('''
                    UPDATE leaderboard SET count = count + 1 WHERE submitted_by = ?
                ''', (ctx.author.name,))

                conn.commit()


            file_path = os.path.join(self.submissions_folder, "submissions.txt")
            with open(file_path, 'a') as file:
                file.write(f"{account_details} | Submitted By {ctx.author.name} | {submission_time}\n")

            await ctx.send("Account submitted successfully!")

        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

    @commands.command(name='slb')
    async def submission_leaderboard(self, ctx):
        try:
            with sqlite3.connect(self.database_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT submitted_by, SUM(count) as total_count
                    FROM leaderboard
                    GROUP BY submitted_by
                ''')

                rows = cursor.fetchall()

            embed = discord.Embed(title="Submission Leaderboard", color=0x00ff00, timestamp=datetime.now(datetime.UTC))
            for user, count in rows:
                embed.add_field(name=user, value=f"{count} submissions", inline=False)
                embed.set_footer(text='\u200b', icon_url=ctx.author.display_avatar)

            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

async def setup(bot):
    await bot.add_cog(SubmitCog(bot))
