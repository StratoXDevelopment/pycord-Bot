import discord
from discord.ext import commands, bridge
from discord import ApplicationContext

class Bans(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bridge.bridge_command(name="bans",description="Shows a list of every banned users in the server")
    async def bans(self, ctx: ApplicationContext):
        bans = [entry async for entry in ctx.guild.bans(limit=100)]
        if not bans:
            return await ctx.respond("The guild has no banned users.")
        ban_entries = []
        for ban in bans:
            user = ban.user
            reason = ban.reason if ban.reason else "No reason provided"
            ban_entries.append(f"**{user.name}#{user.discriminator}** (ID: {user.id})\nReason: {reason}\n")
        ban_list_text = "\n".join(ban_entries)
        if len(ban_list_text) > 4000:
            await ctx.respond(f"Ban list too long. Showing first 100 bans:\n{ban_list_text[:4000]}...")
        else:
            embed = discord.Embed(
                    title="Server Ban List",
                    description=ban_list_text,
                    color=discord.Colour.blurple()
                    )
            embed.set_footer(text=f"Total bans shown: {len(bans)}")
            await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(Bans(bot))
