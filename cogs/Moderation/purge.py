import discord
from discord import Embed
from discord import ApplicationContext, Option
from discord.ext import commands, bridge
import time

class Purge(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bridge.bridge_command(name="purge", description="Purges the given amount of messages from the current channel", aliases=["clear"])
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx: ApplicationContext, amount: bridge.BridgeOption(int, "Number of messages to delete", required=True)):
        if amount <= 0:
            return await ctx.respond("Please specify a positive number of messages to delete.", ephemeral=True)
        elif amount > 100:
            return await ctx.respond("Please specify a number between (1-100).")
       
        await ctx.message.delete()
        deleted = await ctx.channel.purge(limit=amount)
        msg = await ctx.channel.send(embed=discord.Embed(title=f"Purged {len(deleted)} Message(s)",description=f"Deleted {len(deleted)} message(s).", color=discord.Colour.blurple()))
        time.sleep(2)
        await msg.delete()

def setup(bot):
    bot.add_cog(Purge(bot))
