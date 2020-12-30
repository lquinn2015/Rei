from discord.ext import commands
import discord
from server import server



class debug(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  async def admin_check(self, ctx):

    if ctx.author.id in server.admin_ids:
      await ctx.channel.send("Sure I trust you ^.^")
      return True
    
    for r in ctx.author.roles:
      if r.name in server.admin_role_names:
        await ctx.channel.send("Sure I trust you ^.^")
        return True

    await ctx.channel.send("I'm sorry but a lot of people have broken my heart so I just cant trust you >.<")
    return False


  @commands.command(
    name='test',
  )
  async def debug_terminal(self, ctx):
    
    admin = await self.admin_check(ctx)
    if not admin:
      return 

    args = ctx.message.content.split(' ')[2:]
    print(args)
    
    try:
      function = getattr(locals()['self'], args[0])
      await function(args[1:])
    except:
      await ctx.channel.send("Well that failed")

  async def ping_channel(self, args):
    channel = discord.utils.get(self.bot.get_all_channels(), name=args[0])
    await channel.send(' '.join(args[1:]))

  async def get_channel(self, channel_name):
    channel = discord.utils.get(self.bot.get_all_channels(), name=channel_name[0])
    print(channel.id)
    return

  async def change_nickname(self, args):
    
    args = ' '.join(args).split(',')
    
    guild = self.bot.get_guild(server.server_id)
    member = guild.get_member_named(args[0])
    
    ret = await member.edit(nick=args[1])
    print(ret)

  

def setup(bot):
  mod = debug(bot)
  bot.add_cog(mod)

