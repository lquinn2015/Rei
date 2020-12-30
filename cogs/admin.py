from discord.ext import commands
import discord
from server import server

class admin(commands.Cog):

  def __init__(self, bot):
    self.bot = bot


  @commands.command(
    name="kick"
  )
  async def kick_user(self, ctx):  
    passport = await server.admin_check(ctx)
    if(not passport):
      return False

    args = ctx.message.content.split()[2:]
    print(args)

    memId = int(args[0][3:-1])
    member = self.bot.get_user(memId)

    member = discord.utils.find(lambda m: m.id == memId, ctx.message.guild.members)
    name = member.nick
    reason = args[1:]
    source = ctx.author.nick

    # print(name)
    # print(reason)
    # print(source)

    channel = self.bot.get_channel(server.admin_room)
    await ctx.guild.kick
    await channel.send("We are attempting to kick " + name + " " + " ".join(reason) + ". The admin was " + source)
    


  @commands.command(
    name="mute"
  )
  async def mute_user(self, ctx):  
    passport = await server.admin_check(ctx)
    if(not passport):
      return False

    args = ctx.message.content.split()[2:]
    print(args)

    memId = int(args[0][3:-1])
    member = self.bot.get_user(memId)

    member = discord.utils.find(lambda m: m.id == memId, ctx.message.guild.members)
    name = member.nick
    reason = args[1:]
    source = ctx.author.nick

    # print(name)
    # print(reason)
    # print(source)

    channel = self.bot.get_channel(server.admin_room)

    await channel.send("We are attempting to kick " + name + " " + " ".join(reason) + ". The admin was " + source)
    




def setup(bot):
  mod = admin(bot)
  bot.add_cog(mod)