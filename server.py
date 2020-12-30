"""
This is a stateless class and simply contains data used for the CC server its mean to be imported to different classes. This data is final do not change it outside of this class
"""



class server(object):
  def __init__(self):
    pass

  def reverse_dict(self, dic):
    ret = {}
    for x in dic:
      ret[dic[x]] = x
    return ret

  async def admin_check(self, ctx, smsg=None, fmsg=None):

    if ctx.author.id in server.admin_ids:
      if smsg != None:
        await ctx.channel.send(smsg)
      else:  
        await ctx.channel.send("Sure I trust you ^.^")
      return True
    
    for r in ctx.author.roles:
      if r.name in server.admin_role_names:
        await ctx.channel.send("Sure I trust you ^.^")
        return True

    if fmsg != None:
      await ctx.channel.send(fmsg) 
    else:
      await ctx.channel.send("I'm sorry but a lot of people have broken my heart so I just cant trust you >.<")
    return False

  async def alliance_member_check(self, ctx, custom=None):


    for r in ctx.author.roles:
      if r.id in server.alliance_role_ids:
        if(custom == None):
          await ctx.channel.send("Sure I trust you ^.^")
        elif (len(custom) > 0):
          await ctx.channel.send(custom)
        return True
    
    await ctx.channel.send("I'm sorry but a lot of people have broken my heart so I just cant trust you >.<")
    return False

  async def alliance_role_check_by_name(self, ctx, role_txt):
    for r in ctx.author.roles:
      if r.id == server.alliance_role_names[role_txt]:
        return True
      else:
        return False


  

server = server()

#Names of people you use a lot 
server.known_users_by_name = {
  "menny":513841949946675201,
  "lossi":202893949843668992,
  "xphos":314877704396734465,
  "emmy":660669670675841044
}

Debug = True

if Debug:
  ###########DEBUG_SERVER_SPECFIC_###############################################################
  #server ID
  server.server_id = 338810201429770242 
  #dictionary of command role ids we use
  server.server_roles = {"visitor":451214014362550274, "milcom":684893938326306841} # K=role name, V=[role ids list or singular]

  #specfic chat rooms
  server.server_general = 698637841663656006
  server.watchtower_id = 698637841663656006
  server.admin_room = 698637841663656006
  server.watchtower_scan_timer = 99999999
  server.radar_on = False

  #identity controls
  server.admin_role_names = ["Emmys Friend"]
  server.admin_ids = [server.known_users_by_name['menny'],server.known_users_by_name['xphos']]
  server.alliance_role_names = {"Emmys Friend":707677404772040735}
  server.alliance_role_ids = server.reverse_dict(server.alliance_role_names)
  ###########DEBUG_SERVER_SPECFIC_###############################################################


#alliance specfic
server.pnw_id=7346

if not Debug:
  ###########CHOCOLATE_CASTLE_SPECFIC###############################################################
  #server ID
  server.server_id = 675868982414278656 
  #dictionary of command role ids we use
  server.server_roles = {"visitor":675870214314917927} # K=role name, V=[role ids list or singular]

  #specfic chat rooms
  server.server_general = 675868982414278660
  server.watchtower_id = 681937121015234565
  server.admin_room = 734514010522779679
  server.watchtower_scan_timer = 3600/4
  server.radar_on = True

  #identity controls
  server.admin_role_names = ["Emmys Friend"]
  server.admin_ids = [server.known_users_by_name['menny'],server.known_users_by_name['xphos']]

  # this is two way map the second is auto generated
  server.alliance_role_names = {"Holy Knight (P&W)":684887560736342087, "Shieldmaiden (P&W)":684887475272941608, "Companion (P&W)":684887828982923302, "Admin Team":681930028405096462, "Popess":675869137276370945, "Queen":675869131307745312, "Internal Affairs (P&W)":684894044094332929,"Military Command (P&W)":684893938326306841, "Caretaker (P&W)":686198339892412419, "Economic Affairs":684897908167802891}
  server.alliance_role_ids = server.reverse_dict(server.alliance_role_names)

  ###########CHOCOLATE_CASTLE_SPECFIC###############################################################




# Chat monitor specific should move this to the chat monitor
server.curse_filter = ['fuck','bitch','cunt','hershey', 'shit']
server.user_specfic = {
  #"jawn":(329379649132167168, "language"),
  "lewd":(server.known_users_by_name["xphos"],"Indeed\n*nods in disappointment*")
  }

server.mention_listener = [["menny","menhera"], ["xphos","melon","watermelon"]] #["lossi", "rosey"]

