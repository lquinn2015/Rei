from discord.ext import commands
import math, aiohttp, asyncio, discord
from alliance import alliance
from server import server 
import pymongo
import os,urllib.parse
import time
import MessageTempletes as MT

class pwn(commands.Cog):

  def __init__(self, bot):
    self.bot = bot
    self.db = None
  

  @commands.command(
    name='status',
  )
  async def status(self,ctx):
    await ctx.send("I am doing alright ^.^")
  
  @commands.command(
    name='amiadmin'
  )
  async def admin_check_stub(self, ctx):
    admin = await server.admin_check(ctx)
  
  
  @commands.command(
    name='amialliance'
  )
  async def alliance_check_stub(self, ctx):
    aa = await server.alliance_member_check(ctx)


  @commands.command(
    name='register'
  )
  async def register_user(self, ctx):

    
    alliance_check = await server.alliance_member_check(ctx)
    if not alliance_check:
      return

    args = ctx.message.content.split()[2:]
    print(args)
    if not ( ("<" in ctx.message.content) and len(args) == 2):
      await ctx.send("Sorry please do rei, register @member link")

    if "http" not in args[1]:
      await ctx.send("Sorry please do rei, register @member link")

    memId = int(args[0].replace("!", "")[2:-1])
    member = discord.utils.find(lambda m: m.id == memId, ctx.guild.members)
 
    if("!" not in args[0]):
      args[0] = args[0][0:2] + "!" + args[0][2:]

    print(args[0])
    await self.insert_nationlink(args[0], args[1])
    name = member.nick
    if name is None:
      name = member.name
    await ctx.send("I registered " + name + " to nation " + str(args[1]) )

  @commands.command(
    name='lookup'
  )
  async def lookup_nationlink(self, ctx):

    alliance_check = await server.alliance_member_check(ctx, "")
    if not alliance_check:
      return

    args = ctx.message.content.split()[2:]
    if not ( ("<" in ctx.message.content) and len(args) == 1):
      await ctx.send("Sorry please do rei, lookup @member ")
      return 

    if("!" not in args[0]):
      args[0] = args[0][0:2] + "!" + args[0][2:]

    record = await self.get_nationlink(args[0])
    if record is None:
      return await ctx.send("I'm not sure i'm really sorry :(")

    memId = int(args[0][3:-1])
    member = self.bot.get_user(memId)

    member = discord.utils.find(lambda m: m.id == memId, ctx.message.guild.members)
    name = member.nick
    if name is None:
      name = member.name
    await ctx.send("I found " + str(name) + " to be " + str(record))

  @commands.command(
    name='purgewars'
  )
  async def purge_wars(self, ctx):

    ffmsg = "What you are not allowed to do that! >.<"
    ssmsg = "Ayi Ayi Captain"
    admin_check = await server.admin_check(ctx,fmsg=ffmsg, smsg=ssmsg)
    
    if not admin_check:
      return 
    
    wars_to_prune = await self.get_current_wars()

    for x in wars_to_prune:
      await self.prune_war(x)

  

  @commands.command(
    name="audit"
  )
  async def audit(self, ctx):

    admin = await server.alliance_member_check(ctx)
    if not admin:
      return

    totalUri = 0
    totalFood = 0
    alliance_data = await self.get_alliance()
    members = alliance_data['member_id_list']
    for x in members:  
      nation = await self.get_nation(x)
      uranium_demand = math.ceil(math.ceil(nation["totalinfrastructure"]/1000)*8.4)
      if nation["offensivewars"] + nation["defensivewars"] == 0:
        food_demand = int(nation["population"])/1000 + int(nation["soldiers"])/750
      else:
        food_demand = int(nation["population"])/1000 + int(nation["soldiers"])/500
      
      food_demand = math.ceil(food_demand) * 7

      totalUri += uranium_demand 
      totalFood += food_demand

      msg = f"{nation['name']} needs: {food_demand} food and {uranium_demand} uranium this week."
     
      # embeb these later
      await ctx.send(msg)

    msg = f"Total Food: {totalFood} \nTotal Uranium: {totalUri}"
    await ctx.send(msg)
    
  async def radar(self):
    await self.bot.wait_until_ready()

    while True:
      
      print("radar active")

      alliance_data = await self.get_alliance()
      members = alliance_data['member_id_list']
   
      active_wars = []

      for member_id in members:
        
        #get nations wars
        nation = await self.get_nation(member_id)

        #get wars we have logged
        curr_wars = await self.get_current_wars()
      
        owars = nation["offensivewar_ids"]
        dwars = nation["defensivewar_ids"]
        

        print(nation['name'])
        print(owars)
        print(dwars)
        
        #report unlogged and add them to new logged list
        for war_id in owars:
          
          if war_id not in curr_wars:
            war = await self.get_war(war_id)
            
            enemy_id = war['war'][0]['defender_id']
            enemy = await self.get_nation(enemy_id)
            await self.report_war_msg(nation, enemy, False)
            await self.insert_war(war, war_id)
          
          active_wars.append(war_id)

        for war_id in dwars:
          if war_id not in curr_wars:
            war = await self.get_war(war_id)
            enemy_id = war['war'][0]['aggressor_id']
            enemy = await self.get_nation(enemy_id)
            await self.report_war_msg(enemy, nation, True)
            await self.insert_war(war, war_id)

          active_wars.append(war_id)
        
      # serialize wars in case of crash
      stored_wars = await self.get_current_wars() 
      wars_to_prune = []

      for war_id in stored_wars:
        if war_id not in active_wars:
          wars_to_prune.append(war_id)
      
      for x in wars_to_prune:
        await self.prune_war(x)

      await asyncio.sleep(server.watchtower_scan_timer)  

  async def report_war_msg(self,attacker, defender, defensive):

    channel = self.bot.get_channel(server.watchtower_id)
    if int(attacker['allianceid']) == server.pnw_id:
      if int(defender['allianceid']) == 0:
        colour = 0x79c8fd
      else:
        colour = 0xF1C40F
    else:
      if int(attacker['allianceid']) == 0:
        colour = 0x9B59B6
      else:
        colour = 0xff0000
    
    embed = discord.Embed(title="New war Declaration", description=f"""{attacker['alliance']} is attacking {defender['alliance']}""", color = colour)

    ascore = float(attacker['score'])
    dscore = float(defender['score'])

    embed.set_thumbnail(url="https://politicsandwar.com/uploads/ded131b45a77f67b7714b8cdd637041c914c8ba4911.png")
    embed.add_field(name="Aggressor", value=f"""{attacker["name"]}""", inline=False)
    embed.add_field(name="Soldiers", value=f"""{attacker["soldiers"]}""", inline=True)
    embed.add_field(name="Tanks", value=f"""{attacker["tanks"]}""", inline=True)
    embed.add_field(name="Aircraft", value=f"""{attacker["aircraft"]}""", inline=True)
    embed.add_field(name="Ships", value=f"""{attacker["ships"]}""", inline=True)
    embed.add_field(name="Missiles/Nukes", value=f"""{attacker["missiles"]}/{attacker["nukes"]}""", inline=True)
    embed.add_field(name="Counter Range", value=f"{(ascore/1.75):.2f} - {((ascore/3)*4):.2f}", inline=True)

    embed.add_field(name="Defender", value=f"""{defender["name"]}""", inline=False)
    embed.add_field(name="Soldiers", value=f"""{defender["soldiers"]}""", inline=True)
    embed.add_field(name="Tanks", value=f"""{defender["tanks"]}""", inline=True)
    embed.add_field(name="Aircraft", value=f"""{defender["aircraft"]}""", inline=True)
    embed.add_field(name="Ships", value=f"""{defender["ships"]}""", inline=True)
    embed.add_field(name="Missiles/Nukes", value=f"""{defender["missiles"]}/{defender["nukes"]}""", inline=True)
    embed.add_field(name="Counter Range", value=f"{(dscore/1.75):.2f} - {((dscore/3)*4):.2f}", inline=True)

    await channel.send(embed=embed)
    

  async def get_war(self, war_id):
    key = alliance.get_api_key()
    url = f"{alliance.baseurl}war/{war_id}/&key={key}"
    return await self.get_json(url)

  async def get_nation(self, nation_id):
    key = alliance.get_api_key()
    url = f"{alliance.baseurl}nation/id={nation_id}&key={key}"
    return await self.get_json(url)

  async def get_alliance(self, targetID=alliance.pnw_id):
    key = alliance.get_api_key()
    url = f"{alliance.baseurl}alliance/id={targetID}&key={key}"
    return await self.get_json(url)



  @commands.command(
    name='spytestalliance',
    help="rei, spytestalliance targetID pages_per_frame"
  )
  async def spy_test_alliance(self, ctx, BatchSize=7):

    status = await server.alliance_role_check_by_name(ctx,"Military Command (P&W)") 
    
    status |= await server.admin_check(ctx, smsg="I trust you ^.^")

    status = True

    if status is False:
      return await ctx.channel.send("This is a really privilleged command and makes me do quite a bit of work so I can't just slave myself out to anyone sorry")

    await ctx.channel.send("This is very intensive in api keys and cpu usage please be gentle with me!")

    args = ctx.message.content.split(' ')[2:]
    if len(args) < 1:
      await ctx.channel.send("Remember arguments are TargetID NationsPerFrame")
      return
    try:
        if len(args) == 2:
            BatchSize = int(args[1])
    except:
        pass

    alliance_data = await self.get_alliance(args[0])
    members = alliance_data['member_id_list']
    f = open("battlereport.csv", "wb+")
    f.write(b"nationlink, number Of spies, name, city count, score, min range, max range, offensive wars count, defensive wars count, vmode, beige turns left\n")
    
    while True:
      embed = None
      pages = []
      f = open("battlereport.csv", "wb+")
      f.write(b"nationlink, number Of spies, name, city count, score, min range, max range, offensive wars count, defensive wars count, vmode, beige turns left\n")
      try:
        counter = 1
        for i, nationID in enumerate(members):
          if i % BatchSize == 0:
            if embed != None:
                pages.append(embed)
            embed = discord.Embed()
            embed.title = "Spytest"
            embed.description = " Spytest for %s (%d/%d)" % (alliance_data["name"], counter, math.ceil(len(members)/BatchSize))
            counter += 1

          nationAPIData = await self.get_nation(nationID)

          spyresults = await self.spy_test(ctx, nationID, nationData=nationAPIData)

          nationName = nationAPIData['name']
          score = nationAPIData['score']
          cities =  nationAPIData['cities']
          vmode = nationAPIData['vmode']
          offensivewarsCount = nationAPIData['offensivewar_ids']
          defensivewarsCount = nationAPIData['defensivewar_ids']
          beige_turns_left = nationAPIData['beige_turns_left']

          str_data = "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % ("https://politicsandwar.com/nation/id="+str(nationID), str(spyresults[0]), str(nationName), str(cities), str(score), str(float(score)*.5), str(float(score)*2), str(offensivewarsCount), str(defensivewarsCount), str(vmode), str(beige_turns_left))
          byte_data = str_data.encode()
          f.write(byte_data)

          embed = await self.append_nation_to_embed(embed, "https://politicsandwar.com/nation/id="+str(nationID), str(spyresults[0]), str(nationName), str(cities), str(score), str(float(score)*.5), str(float(score)*2), str(offensivewarsCount), str(defensivewarsCount), str(vmode), str(beige_turns_left), spyresults[3])
          print(len(embed))
        f.close()
        pages.append(embed)

        break
      except discord.errors.HTTPException:
        BatchSize -= 1
        f.close()

    await ctx.channel.send(file=discord.File('battlereport.csv'))    
    await MT.paginator(self.bot, ctx, pages, timeout=360)


  async def append_nation_to_embed(self, embed, nation_link, spies, nationName, cities, score, min_score, max_score, offensive_wars, defensivewars, vmode, beige_turns_left, arcane_active):
    embed.add_field(name=nationName + " || spies=" + spies, value=nation_link, inline=False)
    #embed.add_field(name="cities", value=cities, inline=True)
    #embed.add_field(name="score", value=score, inline=True)
    #embed.add_field(name="min score", value=score, inline=True)
    #embed.add_field(name="max score", value=score, inline=True)
    # if arcane_active:
    #   embed.add_field(name="spies", value=spies + " with arcane", inline=True)
    # else:  
    #   embed.add_field(name="spies", value=spies, inline=True)
    #embed.add_field(name="vmode turns", value=vmode, inline=True)
    #embed.add_field(name="Beige turns", value=beige_turns_left, inline=True)
    
    #embed.add_field(name="Offesnsive war Ids", value=str(offensive_wars), inline=False)
    #embed.add_field(name="Defensive War ids", value=str(defensivewars), inline=False)
    return embed



  @commands.command(
    name='spytest'
  )
  async def spy_test_msg(self, ctx):
     
    args = ctx.message.content.split(' ')[2:]
    if len(args) != 1:
      await ctx.channel.send("Remember arguments are TargetID")
      return
    
    ret = await self.spy_test(ctx, args[0]) 
    if ret[3] == 1:
        await ctx.channel.send("Arcane Detected")
    await ctx.channel.send("Odds are ~50% at safety level " + str(ret[1]) + " : spi#" + str(ret[2]))
    await ctx.channel.send("They have " + str(ret[0]) + " spies")

    

  # return = (numberOfspys, matchingSafetyLV, requireSpiesFor50%)
  async def spy_test(self, ctx, targetID, nationData=None):

    attacker = nationData
    if nationData is None:
      attacker = await self.get_nation(targetID)
    #defender = await self.get_nation(id2)
    defender = attacker
    #attacker powers
    covert_active = 0
    
    #defender powers
    tactician_active = 0
    arcane_active = 0 

    if "overt" in attacker['war_policy']: 
      covert_active = 1
    
    if "actician" in defender['war_policy']:
      tactician_active = 1

    if "rcane" in defender['war_policy']:
      arcane_active = 1
    
    safetylv = 1
    mins = 1
    currs = 1
    maxs = 60

    attempts = 0
    while maxs - mins > 0 and attempts < 8:
      attempts += 1
      currs = (maxs + mins)/2
      #print(currs)
      ret = await self.ping_spys(targetID,safetylv,currs)
      if "Low" in ret:
        mins = currs
      else:
        maxs = currs
    
    if maxs == 60:
      safetylv = 2
      mins = 1
      currs = 1
      maxs = 60

      attempts = 0
      while maxs - mins > 0 and attempts < 8:
        attempts += 1
        currs = (maxs + mins)/2
        ret = await self.ping_spys(targetID,safetylv,currs)
        if "Low" in ret:
          mins = currs
        else:
          maxs = currs

    
    #await ctx.channel.send("Odds are ~50% at safety level " + str(safetylv) + " : spi#" + str(currs))
    # we have estimated odds slightly higher than 50% so floor?

    #advanced formula
    policy_modifier = 1 + .15 * tactician_active - .15 * arcane_active + .15 * covert_active

    #print(policy_modifier)
    #admissible i think
    #print(maxs)
    #print(currs)
    #print(safetylv)
    e = math.floor((1/3) *  (100 * maxs / (50/policy_modifier - safetylv*25)) - 1/3)
    e = min(60, e)

    #e = math.floor((100*maxs) / (4*((50/policy_modifier) - 25) + 1/3))
    
    #await ctx.channel.send("They have " + str(e) + " spies")

    #basic formula
    #e = math.floor((maxs * 4)/(3) - 1/3)
    
    return (e, safetylv, currs, arcane_active)
  
  async def ping_spys(self, agroID, safetyLV, spies):
    url = "https://politicsandwar.com/war/espionage_get_odds.php?id1=%s&id2=%s&id3=0&id4=%d&id5=%d&_=%d" % (agroID,agroID, safetyLV, spies, time.time())    
    #print(url) 

    return await self.get_resp(url)
  
  
  async def get_resp(self, url):
    session = aiohttp.ClientSession()
    resp = await session.get(url)
    text = await resp.text()
    await session.close()
    return text

  async def get_json(self, url):
    session = aiohttp.ClientSession()
    resp = await session.get(url)
    data = await resp.json()
    await session.close()
    return data

  async def get_guardian_db(self):
    if self.db is None:
      uname = urllib.parse.quote_plus(os.environ["pymongouname"])
      password = urllib.parse.quote_plus(os.environ["pymongopass"])
      uri = "mongodb+srv://%s:%s@guardian-api-uobki.gcp.mongodb.net/test?retryWrites=true&w=majority" % (uname, password)
      client = pymongo.MongoClient(uri)
      self.db = client.guardian
    return self.db

  async def get_current_wars(self):
    db = await self.get_guardian_db()
    wars = []
    cursor = db.wars.find()
    if cursor.count() == 0:
      return []
    for war in cursor:
      wars.append(war['war_id'])
    return wars 

  async def get_nationlink(self, player):
    user = {"id":player}
    db = await self.get_guardian_db()
    cursor = db.users.find(user)
    if cursor.count() == 0:
      return None
    for player in cursor:
      return player["link"]
    return None

  async def insert_nationlink(self, player, nationlink):
    user = {"id":player, "link":nationlink}
    db = await self.get_guardian_db()
    db.users.insert_one(user)
  
  async def prune_nationlink(self, player):
    db = await self.get_guardian_db()
    db.users.delete_one({"id":player})

  async def insert_war(self, war, war_id):
    war['war_id'] = war_id
    db = await self.get_guardian_db()
    db.wars.insert_one(war)
    
  async def prune_war(self, war_id):
    db = await self.get_guardian_db()
    db.wars.delete_one({"war_id":war_id})


def setup(bot):
  mod = pwn(bot)
  bot.add_cog(mod)
  if server.radar_on:
    bot.loop.create_task(mod.radar())
