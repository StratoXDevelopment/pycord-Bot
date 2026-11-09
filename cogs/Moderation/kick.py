import discord
from discord.ext import bridge, commands
from discord import Embed

class Kick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bridge.bridge_command(name="kick", description="Kicks the mentioned member from the server.")
    @bridge.has_permissions(kick_members=True)
    @bridge.bridge_option(name="target", description="The member you wanted to kick.", required=True, default=None, input_type=discord.SlashCommandOptionType.user)
    async def kick(self, ctx: bridge.BridgeContext, member: discord.Member, *, reason: str = None):
        try:
            if not reason:
               await member.kick(reason="No reason provided")
               await ctx.respond(f"{ctx.author.mention} has kicked {member.display_name}")
            else:
               await member.kick(reason=reason)
               await ctx.respond(f"{ctx.author.mention} has kicked {member.display_name} for: {reason}")
        except discord.Forbidden:
            await ctx.respond("❌ I can't kick them (im missing permissions or they're above my top role).")
            return
        except discord.NotFound:
            await ctx.respond("❌ The member you mentioned is no longer in this server.")
            return
        except discord.HTTPException as e:
            await ctx.respond(f"Something went wrong while processing this command.")
            return

def setup(bot):
    bot.add_cog(Kick(bot))
