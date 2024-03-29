import discord
from discord.ext import commands
import os
import heartbeat
from dotenv import load_dotenv

load_dotenv()


cogs = ['cogs.pnw', 'cogs.debug', 'cogs.chat_monitor', 'cogs.fun']

def get_prefix(bot, msg):

    if(os.environ["debug"] == "True"):
        prefixs = ["test, ", "rei-test, ", "rtest, ", "rt, "]        
    else:
        prefixs = ["Rachel, ", "rachel, ","Rei, ", "rei, "]

    return commands.when_mentioned_or(*prefixs)(bot, msg)

intents = discord.Intents.all()#(messages=True, members=True, guilds=True)

bot = commands.Bot(
  command_prefix = get_prefix,
  descripton='Emmy is for testing',
  owner_id=314877704396734465,
  case_insensitive=True,
  intents = intents
)

@bot.event
async def on_ready():
  print(f'Logged in as {bot.user.name} - {bot.user.id}')
  # bot.remove_command('help')
  bot.custom_name = "Emmy"
  for cog in cogs:
    bot.load_extension(cog)
    print(f"{cog} spinning up")
  return

from discord.ext import commands
@bot.command(
  name="hallu"
)
async def hallu(ctx):
  await ctx.send("test")

#heartbeat.start()
bot.run(os.environ["token"], bot=True, reconnect=True)
