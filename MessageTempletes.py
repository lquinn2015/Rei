import asyncio
import discord


async def paginator(bot, ctx, pages, timeout=60):
      
    msg = None

    arrow_forward_emoji =  u'\U000027A1'
    arrow_backward_emoji = u'\U00002B05'

    def reaction_options(reaction, user):
        
        return user.id == ctx.author.id and msg.id == reaction.message.id and reaction.emoji in [arrow_forward_emoji, arrow_backward_emoji]
    

    idx = 0
    while True:

        if type(pages[idx]) == tuple:
            pages[idx] = await pages[idx][0](pages[idx][1:]) # evaluate a paging function we don't need to calcuate everything before hand but we do want to cache results 

        if msg == None:
            if(type(pages[idx]) == str):
                msg = await ctx.send(pages[idx])
            else:
                msg = await ctx.send(embed=pages[idx])
        else:
            if(type(pages[idx]) == str):
                await msg.edit(content=pages[idx], embed=None)
            else:
                await msg.edit(embed=pages[idx], content=None)

        await msg.add_reaction(arrow_backward_emoji)
        await msg.add_reaction(arrow_forward_emoji)

        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=timeout, check=reaction_options)

            if reaction.emoji == arrow_forward_emoji:
                idx = (idx + 1) % len(pages)
                await reaction.remove(user)
            if reaction.emoji == arrow_backward_emoji:
                idx = (idx - 1 + len(pages)) % len(pages)
                await reaction.remove(user)
            
            continue

        

        except asyncio.TimeoutError:
            await msg.clear_reaction(arrow_backward_emoji)
            await msg.clear_reaction(arrow_forward_emoji)
            break