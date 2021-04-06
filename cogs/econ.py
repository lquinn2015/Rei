from discord.ext import commands
import discord
from server import server
import functools
import asyncio
import MessageTempletes as MT


class econ(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.guild = self.bot.get_guild(server.server_id)


    def econ_cmds(name=None, help=None):
        def deco(func):
            func.econ_cmds=True
            func.cmd_name=name
            func.cmd_help=help
            @functools.wraps(func)
            def wrapper(*args,**kwargs):
                return func(*args, **kwargs)
            return wrapper
        return deco


    @commands.command(
      name = "econ",
      help = "\"rei, econ help\" for more information"
    )
    async def cli_econ(self, ctx):
        await self.help(ctx)

    @econ_cmds(
        name = "help",
        help = "econ help <cmd> to get help with a command"
    )
    async def help(self, ctx):
        functions = [x for x in self.get_econ_cmds()]
        command_pages = []
        help_fields = []

        for f in functions:
            data = dict()
            
            data["tilte"] = f.cmd_name
            help_info = dict()
            help_info["name"] = f.cmd_name
            help_info["value"] = f.cmd_help
            data["fields"] = [help_info]
            
            command_pages.append(discord.Embed.from_dict(data))
            help_main = dict()
            help_main["name"] = "Command"
            help_main["value"] = f.cmd_name
            help_fields.append(help_main)
        
        # now paginate with the help command first
        help_main = dict()
        help_main["tilte"] = "Econ Help"
        help_main["color"] = discord.Colour.green().value
        help_main["fields"] = help_fields
        help_embed = discord.Embed.from_dict(help_main)
        pages = [help_embed] + command_pages + ["Random text here hello lossi"]

        await MT.paginator(self.bot, ctx, pages)

            

    def get_econ_cmds(self):
        for x in econ.__dict__.values():
            if hasattr(x, "econ_cmds"):
                yield x


    @econ_cmds(
      name = "info",
      help = """
          exclusive options must select 1
          -a alliance_id
          -n nation_id
      """
    )
    async def info(ctx, nation_id=None, city_id=None):
        pass



def setup(bot):
  mod = econ(bot)
  bot.add_cog(mod)
