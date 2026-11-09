import discord
from discord.ext import bridge, commands
import os
from dotenv import load_dotenv
from utils.log import info, error, success, banner
from utils.color import colorize

load_dotenv()

intents = discord.Intents.default()
intents.guilds = True
intents.message_content = True

bot = bridge.Bot(command_prefix="!", intents=intents, help_command=None)


async def ephemeral(ctx: discord.ApplicationContext, text: str):
    return await ctx.respond(text, ephemeral=True)
def env(key):
    return os.getenv(key)

banner()

@bot.event
async def on_application_command_error(ctx: discord.ApplicationContext, error: discord.DiscordException):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.respond("⏳ This commanf is currently on cooldown! Please wait a bit before trying again", ephemeral=True)
    elif isinstance(error, commands.MissingPermissions):
        await ephemeral(ctx, "🚫 You do not have the required permissions to run this command!")
    elif isinstance(error, commands.BotMissingPermissions):
        await ephemeral(ctx, "🚫 I do not have enough permissions to do this!")
    elif isinstance(error, commands.NSFWChannelRequired):
        await ephemeral(ctx, "🔞 This command can only be used in an NSFW channel!")
    elif isinstance(error, commands.errors.CommandNotFound):
        await ephemeral(ctx, "This command do not exist on my commands list.")
    else:
        await ephemeral(ctx, "❌ An unexpected error occured while processing this command.")
        raise error

@bot.event
async def on_bridge_command_error(ctx: bridge.BridgeContext, error: Exception):
    if isinstance(error, commands.MissingPermissions):
        await ctx.respond("❌ You're missing permissions to run this command.", ephemeral=True)
    elif isinstance(error, commands.BadArgument):
        await ctx.respond("❌ Invalid Argument Provided.", ephemeral=True)
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.respond("❌ You're missing a required argument `{error.param.name}`", ephemeral=True)
    else:
        await ctx.respond("❌ Something went wrong while processing this command.", ephemeral=True)

@bot.event
async def on_ready():
    success(f"{bot.user} is online and ready!")

def load_extensions(bot: discord.Bot, directory:str ="cogs"):
    for root, dirs, files in os.walk(directory):
        if root != "cogs" and not "__pycache__" in root:
            info(f"Module: {root}")
        for filename in files:
            if filename.endswith(".py"):
                ext_path = os.path.join(root, filename)
                module_name = ext_path.replace(os.sep, ".")[:-3]
                bot.load_extension(module_name)
                info(f" ↳ Command Loaded {module_name}")
    info(f"All Modules are loaded!")
    print(colorize(text="  ──────────────────────────────────────────────────────────────", fg="gray", bold=False))

load_extensions(bot)

bot.run(env("TOKEN"))
