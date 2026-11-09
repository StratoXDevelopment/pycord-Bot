import discord
from discord.ext import commands, bridge
from cogs.Tickets.database import delete_ticket_config, set_ticket_config, get_ticket_config, increment_ticket_count, setup_tables
from utils.embed import Embed 
import asyncio

# delete and get _ticket_config takes only guildId and get returns the config 
# set_ticket_config asks for guild_id, panel_channel_id, staff_role_id, category_id, embed_message_id

async def roleCheck(i: discord.Interaction):
    config = await get_ticket_config(i.guild.id)
    role = i.guild.get_role(config['staff_role_id'])
    if role in i.user.roles:
        return True
    await i.response.send_message("You don't have permissions to use this button.", ephemeral=True)
    return False

class AddUserMenu(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)

    @discord.ui.user_select(placeholder="Select a member to add")
    async def select(self, select: discord.ui.Select, i: discord.Interaction):
        user = select.values[0]
        await i.channel.set_permissions(
                user,
                read_messages=True,
                send_messages=True,
                view_channel=True
                )
        await i.channel.send(f"{i.user.mention} added {user.mention} to the ticket.")
        await i.response.send_message(f"Added {user.mention} to the ticket.", ephemeral=True)

class RemoveUserMenu(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)

    @discord.ui.user_select(placeholder="Select a member to remove")
    async def remove(self, select: discord.ui.Select, i: discord.Interaction):
        user = select.values[0]
        await i.channel.set_permissions(user, overwrite=None)
        await i.channel.send(f"{i.user.mention} removed {user.mention} from the ticket.")
        await i.response.send_message(f"Removed {user.mention} from the ticket.", ephemeral=True)

class Controls(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Close", style=discord.ButtonStyle.red, custom_id="ticket_close")
    async def close(self, button: discord.Button, i: discord.Interaction):
        check = await roleCheck(i)
        if not check:
            return
        config = await get_ticket_config(i.guild.id)
        if not config:
            return
        msg = await i.response.send_message(embed=discord.Embed(title="Closing...", description="This channel will be deleted in 5seconds.", color=discord.Color.red()))
        await asyncio.sleep(5)
        await i.channel.delete()

    @discord.ui.button(label="Add", style=discord.ButtonStyle.gray, custom_id="ticket_add")
    async def add(self, button: discord.Button, i: discord.Interaction):
        check = await roleCheck(i)
        if not check:
            return
        await i.response.send_message("Select a member to add:", view=AddUserMenu(), ephemeral=True)

    @discord.ui.button(label="Remove", style=discord.ButtonStyle.gray, custom_id="ticket_remove")
    async def remove(self, button: discord.Button, i: discord.Interaction):
        role = await roleCheck(i)
        if not role:
            return
        await i.response.send_message("Select a member to remove:", view=RemoveUserMenu(), ephemeral=True)


class CreateTicket(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Create a ticket", style=discord.ButtonStyle.gray, custom_id="ticket_create", emoji="🎫")
    async def create(self, button: discord.Button, i: discord.Interaction):
        config = await get_ticket_config(i.guild.id)
        if not config:
            return
        await i.response.defer(ephemeral=True)
        try:
            ticket_count = await increment_ticket_count(i.guild.id)
            category = i.guild.get_channel(config['category_id'])
            supporter = i.guild.get_role(config['staff_role_id'])
            overwrites = {
                    i.guild.default_role: discord.PermissionOverwrite(view_channel=False),
                    supporter: discord.PermissionOverwrite(view_channel=True, send_messages=True),
                    i.user: discord.PermissionOverwrite(view_channel=True, send_messages=True)
                    }
            channel = await i.guild.create_text_channel(name=f"ticket-{i.user.name}-{ticket_count}", category=category, overwrites=overwrites)
            closureEmbed = discord.Embed(title="Ticket staff controls", description="The buttons below can only be used by the support team.", color=None)
            closureEmbed.add_field(name="close", value="Closes the ticket and deletes the channel in 5s")
            closureEmbed.add_field(name="add", value="Add a user to the ticket channel.")
            closureEmbed.add_field(name="remove", value="Remove a user from the ticket channel.")
            closureEmbed.add_field(name="More options comming soon", value="There will be more options comming in new updates.")
            await channel.send(f"{i.user.mention} {supporter.mention}", embed=closureEmbed, view=Controls())
            await i.followup.send(f"Ticket Created: {channel.mention}", ephemeral=True)
        except Exception as error:
            await i.followup.send("Something went wrong while creating the ticket channel.", ephemeral=True)
            return

class Ticket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(CreateTicket())
        self.bot.add_view(Controls())

    @bridge.bridge_group(invoke_without_command=True)
    @bridge.map_to("help")
    async def ticket(self, ctx: bridge.Context):
        embed = Embed(title="Ticket Commands Help", description=f"Below are all the commands this module have.")
        embed.field(name="ticket setup", value="Use this command to setup the ticket module", inline=True)
        embed.field(name="ticket disable", value="This command disables the ticket module.", inline=True)
        embed.field(name="ticket info", value="This command shows the information about ticket system such as how many tickets are created, support role etc.")
        embed.field(name="ticket add", value="This command adds the mentioned member to the ticket channel.")
        embed.field(name="ticket remove", value="This command removes the mentioned member from the ticket (will warn if you try to remove the ticket owner)")
        await ctx.respond(embed=embed)

    @ticket.command()
    async def setup(self, ctx: bridge.Context, channel: bridge.BridgeOption(input_type=discord.TextChannel, description="The channel where ticket panel goes to", required=True), category: bridge.BridgeOption(input_type=discord.CategoryChannel, description="The category where the ticket channels will be created", required=True), role: bridge.BridgeOption(input_type=discord.Role, description="The role you want to give access to manage tickets", required=True)):
        config = await get_ticket_config(ctx.guild.id)
        if config:
            await ctx.respond(embed=discord.Embed(title="Module already enabled", description="This server already has tickets module enabled, You can use `/ticket disable` to disable the tickets module.", color=discord.Color.red()))
            return
        embed = Embed(title="Ticket Panel", description="Use the button below to create a ticket.", color=None)
        embed.set_footer(text=f"Powered by {self.bot.user.name or ctx.guild.name}", icon_url=ctx.guild.icon.url if ctx.guild.icon else self.bot.user.display_avatar.url)
        message = await channel.send(embed=embed, view=CreateTicket())
        await set_ticket_config(
                guild_id=ctx.guild.id,
                panel_channel_id=channel.id,
                category_id=category.id,
                staff_role_id=role.id,
                embed_message_id=message.id
                )
        await ctx.respond(embed=discord.Embed(title="Tickets is configured", description="The tickets module is configured successfully", color=discord.Color.green()))

    @ticket.command()
    async def disable(self, ctx: bridge.Context):
        guildid = ctx.guild.id   
        config = await get_ticket_config(guildid)
        if not config:
            await ctx.respond("The ticket module is disabled, You cant disable the module that is already disabled")
            return
        # Extra: We will add a system to get the embed_message_id and delete it
        await delete_ticket_config(guildid)
        await ctx.respond(embed=Embed(title="Ticket Module Disabled", description="Successfully disabled the ticket module for this server."))

    @ticket.command()
    async def add(self, ctx: bridge.Context, user: bridge.BridgeOption(input_type=discord.Member, description="The user you want to add in the ticket channel", required=True)):
        channel = ctx.channel
        if not "ticket-" in channel.name:
            await ctx.respond("This isnt a ticket channel.")
            return
        await ctx.respond("The user you want to add:", view=AddUserMenu())

    @ticket.command()
    async def remove(self, ctx: bridge.context, user: bridge.BridgeOption(input_type=discord.Member, description="The user you want to remove from the ticket channel.", required=True)):
        if not "ticket-" in ctx.channel.name:
            await ctx.respond("This isnt a ticket channel")
            return
        await ctx.respond("The user you want to remove from the ticket:", view=RemoveUserMenu())

def setup(bot):
    bot.add_cog(Ticket(bot))
