import datetime

from discord.ext import commands
import discord
import sqlite3
import time


class Vouch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.conn = sqlite3.connect('vouches.db')
        self.cursor = self.conn.cursor()
        self.setup_database()
        self.vouch_cooldowns = {} 

    def setup_database(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS vouches (user_id INTEGER PRIMARY KEY, vouch_count INTEGER)")
        self.conn.commit()

        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS vouch_logs (user_id INTEGER, vouch_type INTEGER, reason TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)")
        self.conn.commit()

    @commands.command(name="rep", aliases=["vouch"])
    @commands.cooldown(1, 1800, commands.BucketType.user)
    async def rep(self, ctx, user: discord.User = None, vouch_type: int = None, *, reason: str = "No reason provided"):
        """Vouch for a user. Use 1 for positive vouch, 0 for negative vouch."""
        if user is None or vouch_type is None:
            example_msg = "Example: `.rep @username 1 Reason for positive vouch`"
            return await ctx.send(f"Invalid command format. {example_msg}")

        if vouch_type not in [0, 1]:
            return await ctx.send("Invalid vouch type. Use 1 for positive vouch, 0 for negative vouch.")

        vouch_type_str = "Positive" if vouch_type == 1 else "Negative"
        color = discord.Color.green() if vouch_type == 1 else discord.Color.red()

        self.cursor.execute("INSERT OR IGNORE INTO vouches (user_id, vouch_count) VALUES (?, 0)", (user.id,))
        vouch_change = 1 if vouch_type == 1 else -1
        self.cursor.execute("UPDATE vouches SET vouch_count = vouch_count + ? WHERE user_id = ?",
                            (vouch_change, user.id))
        self.cursor.execute("INSERT INTO vouch_logs (user_id, vouch_type, reason) VALUES (?, ?, ?)",
                            (user.id, vouch_type, reason))
        self.conn.commit()

        vouch_count = self.get_vouch_count(user.id)
        vouch_type_str = "Positive" if vouch_type == 1 else "Negative"

        embed = discord.Embed(
            title=f"{vouch_type_str} Review Vouch",
            description=f"Thank you {ctx.author.mention} for providing a {vouch_type_str.lower()} vouch for {user.mention}!",
            color=color,
            timestamp=datetime.datetime.now(datetime.UTC)
        )
        embed.add_field(name="Reason", value=reason, inline=False)
        embed.set_footer(text='\u200b', icon_url=ctx.message.author.display_avatar)

        await ctx.send(embed=embed)

    @commands.command(name="repleaderboard", aliases=["replb", "vouchlb", "lb"])
    async def rep_leaderboard(self, ctx):
        """Show the vouch leaderboard."""
        leaderboard = self.get_vouch_leaderboard()

        if not leaderboard:
            return await ctx.send("No vouches recorded yet!")

        embed = discord.Embed(
            title="Vouch Leaderboard",
            color=discord.Color.gold(),
            timestamp=datetime.datetime.now(datetime.UTC)
        )

        for rank, (user_id, vouch_count) in enumerate(leaderboard, start=1):
            user = self.bot.get_user(user_id)

            if user is not None:  
                embed.add_field(name=f"{rank}. {user.name}", value=f"Vouch Count: {vouch_count}", inline=False)
                embed.set_footer(text='\u200b', icon_url=ctx.message.author.display_avatar)

        await ctx.send(embed=embed)

    @commands.command(name="profile")
    async def profile(self, ctx, user: discord.User = None):
        """View detailed profile of a user."""
        if not user:
            return await ctx.send("Please provide a user to view the profile.")

        vouch_count = self.get_vouch_count(user.id)
        if vouch_count is None:
            return await ctx.send(f"{user.mention} doesn't have a vouch profile yet.")

        positive_vouches, negative_vouches, latest_vouches = self.get_vouch_details(user.id)

        embed = discord.Embed(
            title=f"{user.name}'s Profile",
            color=discord.Color.blue(),
            timestamp=datetime.datetime.now(datetime.UTC)
        )

        embed.add_field(name="Positive Vouches", value=positive_vouches, inline=False)
        embed.add_field(name="Negative Vouches", value=negative_vouches, inline=False)
        embed.set_footer(text='\u200b', icon_url=ctx.message.author.display_avatar)

        if latest_vouches:
            for vouch in latest_vouches:
                vouch_type_str = "Positive" if vouch[1] == 1 else "Negative"
                embed.add_field(
                    name=f"{vouch_type_str} Vouch",
                    value=f"Reason: {vouch[2]}\nTimestamp: {vouch[3]}",
                    inline=False
                )

        await ctx.send(embed=embed)

    @commands.command(name="resetv")
    @commands.has_permissions(administrator=True)
    async def reset_vouch_profile(self, ctx, user: discord.User):
        """Reset a user's vouch profile. (Admin only)"""
        self.cursor.execute("DELETE FROM vouches WHERE user_id = ?", (user.id,))
        self.cursor.execute("DELETE FROM vouch_logs WHERE user_id = ?", (user.id,))
        self.conn.commit()
        await ctx.send(f"The vouch profile for {user.mention} has been reset.")

    @commands.command(name="resetc")
    @commands.has_permissions(administrator=True)
    async def reset_cooldown(self, ctx, user: discord.User):
        """Reset cooldown for a user. (Admin only)"""
        try:
            self.rep.reset_cooldown(ctx)
        except commands.CommandOnCooldown:
            pass

        if ctx.command.name in self.vouch_cooldowns:
            del self.vouch_cooldowns[ctx.command.name]
        await ctx.send(f"The cooldown for {user.mention} has been reset.")

    @rep.error
    @profile.error
    async def rep_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            cooldown_msg = f"This command is on cooldown. Please try again in {error.retry_after:.0f} seconds."
            await ctx.send(cooldown_msg)
            self.rep.reset_cooldown(ctx)
        elif isinstance(error, commands.MissingRequiredArgument):
            example_msg = "Example: `.rep @username 1 Reason for positive vouch`"
            await ctx.send(f"Invalid command format. {example_msg}")
        else:
            raise error

    def get_vouch_count(self, user_id):
        self.cursor.execute("SELECT vouch_count FROM vouches WHERE user_id = ?", (user_id,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def get_vouch_details(self, user_id):
        self.cursor.execute("SELECT COUNT(*) FROM vouch_logs WHERE user_id = ? AND vouch_type = 1", (user_id,))
        positive_vouches = self.cursor.fetchone()[0]

        self.cursor.execute("SELECT COUNT(*) FROM vouch_logs WHERE user_id = ? AND vouch_type = 0", (user_id,))
        negative_vouches = self.cursor.fetchone()[0]

        self.cursor.execute("SELECT * FROM vouch_logs WHERE user_id = ? ORDER BY timestamp DESC LIMIT 5", (user_id,))
        latest_vouches = self.cursor.fetchall()

        return positive_vouches, negative_vouches, latest_vouches

    def get_vouch_leaderboard(self):
        self.cursor.execute("SELECT * FROM vouches ORDER BY vouch_count DESC LIMIT 10")
        return self.cursor.fetchall()


async def setup(bot):
    await bot.add_cog(Vouch(bot))
