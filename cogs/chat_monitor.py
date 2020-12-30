from discord.ext import commands
import discord
from server import server

class chat_monitor(commands.Cog):


  def __init__(self, bot):
    self.bot = bot


  @commands.command(
    name="online"
  )
  async def is_user_on(self, ctx, name):

    if ctx.guild == None:
      return False
    

    for member in ctx.guild.members:
      if member.id == server.known_users_by_name[name]:
       
        return "online" in member.status
    return False
  

  @commands.Cog.listener()
  async def on_message(self, message):

    user = message.author
    content = message.content.casefold()
  

    # if "nini rei" in content:
    #   await message.channel.send("Nini")
    #   await message.channel.send('<:goodnight:702268658180947988>')

    emmyActive = await self.is_user_on(message,"emmy")
    if emmyActive:
      return

    if type(message.channel) == discord.channel.DMChannel: ## no PM processing here
      return



    for x in server.curse_filter:
      if x in content:
        await message.channel.send("Language!")
        break
    
    for aliases in server.mention_listener:
      for name in aliases:
        if name in content:
          user = self.bot.get_user(server.known_users_by_name[aliases[0]])
          msg = f'{message.author.name} mentioned you in {message.channel.guild}/{message.channel.name}. \n they said: "{message.content}"'
          await user.send(msg)

    for x in server.user_specfic:
      if x in content:
        if message.author.id == server.user_specfic[x][0]:
          await message.channel.send(server.user_specfic[x][1])

  @commands.Cog.listener()
  async def on_member_join(self, member):

    # emmyActive = await self.is_user_on(member,"emmy")
    # if emmyActive:
    #   return

    if member.guild.id == server.server_id:
      channel = self.bot.get_channel(server.server_general)
      await channel.send(f"Welcome to the Chocolate Castle discord server {member.mention}\nEnjoy your stay ^.^")

      guild = self.bot.get_guild(server.server_id)
      role = guild.get_role(server.server_roles['visitor'])
      print(role)
      await member.add_roles(role)
  
  @commands.Cog.listener()
  async def on_member_remove(self, member):

    # emmyActive = await self.is_user_on(member,"emmy")
    # if emmyActive:
    #   return

    if member.guild.id == server.server_id:
      channel = self.bot.get_channel(server.server_general)
      await channel.send(f"Bai {member.mention}")
  

def setup(bot):
  bot.add_cog(chat_monitor(bot))
  
