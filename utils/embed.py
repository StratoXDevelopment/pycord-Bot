import discord
from .log import warn

def create_embed(title: str, description: str, color: str = "#7655E8"):
    embed = discord.Embed(title=title, description=description, color=color)
    return embed

def new_field(embed: discord.Embed, name: str, value: str, inline: bool = False):
    embed.add_field(name=name, value=value, inline=inline)
    return embed

def add_images(embed: discord.Embed, image_url: str = None, thumbnail_url: str = None):
    if not image_url and thumbnail_url:
        embed.set_thumbnail(url=thumbnail_url)
        return embed
    elif not thumbnail_url and image_url:
        embed.set_image(url=image_url)
        return embed
    else:
        warn("You have to provide either image_url or thumbnail_url.")

class Embed(discord.Embed):
    def __init__(self, *, title: str, description: str, color: int = 0x7655E8, **kwargs):
        super().__init__(title=title, description=description, color=color, **kwargs)

    def field(self, name: str, value: str, inline: bool = False):
        self.add_field(name=name, value=value, inline=inline)

    def footer(self, text: str, icon_url: str):
        if not icon_url:
            self.set_footer(text=text)
        else:
            self.set_footer(text=text, icon_url=icon_url)

    def images(iurl: str = None, turl: str = None):
        add_images(self, image_url=iurl, thumbnail_url=turl)

    def author(self, text: str, icon_url: str = None):
        if not icon_url:
            self.set_author(name=text)
        else:
            self.set_author(name=text, icon_url=icon_url)

