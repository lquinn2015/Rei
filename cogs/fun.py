from discord.ext import commands
import discord
from server import server
import json, requests


class fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.guild = self.bot.get_guild(server.server_id)

    @commands.command()
    async def yui(self, ctx):
        embed = discord.Embed(color=discord.Color.Purple(), title = "Yui")
        yui_user = await ctx.guild.fetch_member(178752448809271296)
        embed.set_image(url = yui_user.avatar)
        await ctx.send(embed=embed)

    @commands.command()
    async def cake(self, ctx):
        if len(ctx.mentions) > 0 and (ctx.mentions[0].id != ctx.author.id):
            await ctx.send(f"<@{ctx.author.id}> sends <@{ctx.mentions[0].id}> some cake :cake:")
        elif ctx.mentions[0].id == ctx.author.id:
            await ctx.send("Send it to someone else!")
        else:
            await ctx.send("Remember to mention someone!")

    @commands.command(name = "avatar")
    async def avatar_cmd(self, ctx):
        member = ctx.guild.get_member(ctx.message.mentions[0].id if len(ctx.message.mentions) > 0 else ctx.author.id)
        embed = discord.Embed(title=f"{member}s Avatar:")
        embed.set_image(url=member.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name = "pat")
    async def headpat_cmd(self, ctx):
        embed = discord.Embed(description="*You hear a distant purring*")
        if len(ctx.message.mentions) > 0:
            embed.title = f"*{ctx.message.mentions[0]} gets patted by {ctx.author}*"
        else:
            embed.title = f"*{ctx.author} gets patted by the Blankie Consigliere*"
        embed.set_image(url=requests.get("https://some-random-api.ml/animu/pat").json()['link'])
        await ctx.send(embed=embed)

    @commands.command(name = "wink")
    async def wink_cmd(self, ctx):
        embed = discord.Embed()
        if len(ctx.message.mentions) > 0:
            embed.title = f"*{ctx.message.mentions[0]} gets winked at by {ctx.author}*"
        else:
            embed.title = f"*The Blankie Consigliere winks at {ctx.author}*"
        embed.set_image(url=requests.get("https://some-random-api.ml/animu/wink").json()['link'])
        await ctx.send(embed=embed)

    @command.command(name = "boop")
    async def boop_cmd(self, ctx):
        embed = discord.Embed()
        if len(ctx.message.mentions) > 0:
            embed.title = f"*{ctx.author} boops {ctx.message.mentions[0]}*"
        else:
            embed.title = f"*{ctx.author} is booped by the Blankie Consigliere*"
        embed.set_image(url=requests.get("https://api.tenor.com/v1/search?q=boop+anime&key=LIVDSRZULELA&limit=25").json()['results'][random.randint(0, 24)]['media'][0]['gif']['url'])
        await ctx.send(embed=embed)

    @command.command(name = "slap")
    async def slap_cmd(self, ctx):
        embed = discord.Embed()
        if len(ctx.message.mentions) > 0:
            embed.title = f"*{ctx.message.mentions[0]} gets slapped by {ctx.author}*"
        else:
            embed.title = f"*{ctx.author} gets slapped by the Blankie Consigliere*"
        embed.set_image(url=requests.get("https://api.tenor.com/v1/search?q=slap+anime&key=LIVDSRZULELA&limit=25").json()['results'][random.randint(0, 24)]['media'][0]['gif']['url'])
        await ctx.send(embed=embed)

    @command.command(name = "dance")
    async def dance_cmd(self, ctx):
        embed = discord.Embed()
        if len(ctx.message.mentions) > 0:
            embed.title = f"*{ctx.author} dances with {ctx.message.mentions[0]}*"
        else:
            embed.title = f"*{ctx.author} dances*"
        embed.set_image(url=requests.get("https://api.tenor.com/v1/search?q=dance+anime&key=LIVDSRZULELA&limit=15").json()['results'][random.randint(0, 14)]['media'][0]['gif']['url'])
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(fun(bot))
