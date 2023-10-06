"""
The user data handler for the whole server.
"""
from __future__ import annotations

import discord
import discord.abc
from discord.ext import commands


class Users(commands.Cog):
    """
    Handles user-database relations for the Users table.
    """

    def __init__(self, bot):
        if not hasattr(bot, "db_client"):
            raise Exception("Database client not found.")
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):  # pylint: disable=E1101
        """When a member joins, add them to the DB."""
        self.bot.db_client.add_user_to_table(member)

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):  # pylint: disable=E1101
        """When a member leaves, remove them from the DB."""
        self.bot.db_client.remove_user_from_table(member)

    @commands.slash_command()
    @commands.has_any_role("Admin", "Sudo", "Staff", "Project Manager")
    async def add_all_members_to_db(self, ctx):
        """Add all members to the database."""
        self.bot.db_client.create_table_from_members(ctx.guild.members)
        await ctx.respond("All members added to database.")


def setup(bot):
    """required"""
    bot.add_cog(Users(bot))
