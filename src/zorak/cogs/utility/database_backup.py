"""
The database backup commands.
"""
from __future__ import annotations

from discord.ext import commands


class Backup(commands.Cog):
    """
    Handles automatic points based on activity.
    """

    def __init__(self, bot):
        if not hasattr(bot, "db_client"):
            raise Exception("Database client not found.")
        self.bot = bot


# TODO: Fix the backup command.
@commands.slash_command()
@commands.has_any_role("Staff", "Sudo", "Project Manager")
async def backup_db(self, ctx):
    """Backup the MongoDB instance."""
    self.bot.db_client.backup_db()
    await ctx.respond("Database backed up.")


def setup(bot):
    """required"""
    bot.add_cog(Backup(bot))
