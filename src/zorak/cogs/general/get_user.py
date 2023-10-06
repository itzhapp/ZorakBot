"""
Get some user data.
"""
from __future__ import annotations

import discord
import discord.abc
from discord.ext import commands


class GetUser(commands.Cog):
    """
    Handles user-database relations for the Users table.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def get_user(self, ctx, user):
        """Returns info on the selected user."""
        user_data = self.bot.db_client.get_one_user(user.id)
        await ctx.respond(user_data)


def setup(bot):
    """required"""
    bot.add_cog(GetUser(bot))