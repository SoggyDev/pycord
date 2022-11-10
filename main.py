#-----------------------------------------------------------------Imports------------------------------------------------------------------------------------
import asyncio
from discord import emoji
from datetime import timedelta
import discord
from datetime import datetime
from discord.ext import commands
from discord import Option
from discord.ext.commands.errors import MissingPermissions
from discord.ext.commands import has_permissions
from discord.ext import tasks
from keep_alive import keep_alive
import os
import random
from discord import Embed
import json
import sqlite3
#-----------------------------------------------------------------Variables-----------------------------------------------------------------------------------
con = sqlite3.connect('level.db')
cur = con.cursor()
intents = discord.Intents.default()
intents.message_content = True
client = discord.Bot(command_prefix="!")
messages = discord.Message
token = os.environ['token']

#-----------------------------------------------------------------Commands-------------------------------------------------------------------------------------

@client.command(name="poll")
async def poll(ctx,*,message):
    embi=discord.Embed(title=" POLL", description=f"{message}")
    msg1=await ctx.channel.send(embed=embi)
    await msg1.add_reaction('👍')
    await msg1.add_reaction('👎')


@client.event  # responding to messages
async def on_message(message):
    message.content = (message.content.lower())  # makes all messages lowercase, from the bot's perspective
    if message.author == client.user:  # to not respond to bots
        return
    if "hello" in message.content:
        await message.channel.send("Hi!")  # response
    if "rickroll" in message.content:
        await message.channel.send("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    if "lol" in message.content:
        await message.channel.send("""Was that even funny?""")
    if "yes" in message.content:
        await message.channel.send("no")
    if "yo " in message.content:
        await message.channel.send("Yo!")
    if "helo" in message.content:
        await message.channel.send("Hey!")
    if "hi" in message.content:
        await message.channel.send("Hello There!")
    if "hru" in message.content:
        await message.channel.send("I'm good. What about you?")
    if "fine" in message.content:
        await message.channel.send("Noice")
    if "good" in message.content:
        await message.channel.send("Noice")
#------------------------------------------------------------------Moderation----------------------------------------------------------------------------------

@client.command()
async def gtn(ctx, guess:int):
    number = random.randint(1, 10)
    if guess == number:
        await ctx.send("You guessed it!")
    else:
        await ctx.send("Nope! Better luck next time :)")

@client.command(name='ban',description="bans a member from the server")
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: Option(discord.Member, description="Which member do you want to ban?", required=True),
              reason: Option(str, description='Why?', required=False)):
    if member.id == ctx.author.id:
        await ctx.respond("BRUH! You can't ban yourself!")
        if reason == None:
            reason == f'None provided by {ctx.author}.'
        await member.ban(reason=reason)
        await ctx.respond(f'<@{ctx.author.id}>, <@{member.id}> has been banned from the server. ✈️')


@client.command(name='announce',description='announce something', )
@commands.has_permissions(manage_messages=True)
async def announce(ctx, title: Option(str, description='Title regarding the announcement', required=True), announcement: Option(str, description='announcement', required=True)):
  textem = discord.Embed(title=f'{title}', color=discord.Color.blurple())
  textem.add_field(name='**Announcement:**', value=f'{announcement}')
  textem.set_image(url='https://i.imgur.com/4M7IWwP.gif')
  await ctx.respond(embed=textem)



@client.command(name='lock',description='Lock a channel', )
@commands.has_permissions(manage_channels=True)
async def lock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role,send_messages=False)
    await ctx.respond('Channel has been locked')



@client.command(name='unlock',description='Unlock a channel', )
@commands.has_permissions(manage_channels=True)
async def lock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role,send_messages=True)
    await ctx.respond('Channel has been unlocked')

@client.command(name='kick',description="Kicks a member from the server.")
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: Option(discord.Member, description="Who do you want to kick?", required=True),
               reason: Option(str, description="Why?", required=False)):
    if member.id == ctx.author.id:
        await ctx.respond("BRUH! You can't kick yourself!")
    elif member.guild_permissions.administrator:
        await ctx.respond("Stop trying to kick an admin :rolling_eyes:")
    else:
        if reason == None:
            reason = f'None provided by {ctx.author}.'
            await member.kick(reason=reason)
            await ctx.respond(f'<@{ctx.author.id}>, <@{member.id}> has been kicked from the server. ✈️')


@client.command(name='clear',description="clears a channel's messages")
@commands.has_permissions(manage_messages=True)
@commands.cooldown(1, 5, commands.BucketType.user)
async def clear(ctx, messages : Option(int, description='How many messages do you want to clear?', required=True)):
    await ctx.defer()
    z = await ctx.channel.purge(limit=messages)
    await ctx.respond(f'I have cleared {len(z)}')

#--------------------------------------------------------------Fun Commands------------------------------------------------------------------------------------


@client.command(name='mute',description = "mutes/timeouts a member")
@commands.has_permissions(moderate_members = True)
async def timeout(ctx, member: Option(discord.Member, required = True), reason: Option(str, required = False), days: Option(int, max_value = 27, default = 0, required = False), hours: Option(int, default = 0, required = False), minutes: Option(int, default = 0, required = False), seconds: Option(int, default = 0, required = False)): #setting each value with a default value of 0 reduces a lot of the code
    if member.id == ctx.author.id:
        await ctx.respond("You can't timeout yourself!")
        return
    if member.guild_permissions.moderate_members:
        await ctx.respond("You can't do this, this person is a moderator!")
        return
    duration = timedelta(days = days, hours = hours, minutes = minutes, seconds = seconds)
    if duration >= timedelta(days = 28): #added to check if time exceeds 28 days
        await ctx.respond("I can't mute someone for more than 28 days!", ephemeral = True) #responds, but only the author can see the response
        return
    if reason == None:
        await member.timeout_for(duration)
        await ctx.respond(f"<@{member.id}> has been timed out for {days} days, {hours} hours, {minutes} minutes, and {seconds} seconds by <@{ctx.author.id}>.")
    else:
        await member.timeout_for(duration, reason = reason)
        await ctx.respond(f"<@{member.id}> has been timed out for {days} days, {hours} hours, {minutes} minutes, and {seconds} seconds by <@{ctx.author.id}> for '{reason}'.")

@timeout.error
async def timeouterror(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.respond("You can't do this! You need to have moderate members permissions!")
    else:
        raise error

@client.command(name='unmute',description = "unmutes/untimeouts a member")
@commands.has_permissions(moderate_members = True)
async def unmute(ctx, member: Option(discord.Member, required = True), reason: Option(str, required = False)):
    if reason == None:
        await member.remove_timeout()
        await ctx.respond(f"<@{member.id}> has been untimed out by <@{ctx.author.id}>.")
    else:
        await member.remove_timeout(reason = reason)
        await ctx.respond(f"<@{member.id}> has been untimed out by <@{ctx.author.id}> for '{reason}'.")

@unmute.error
async def unmuteerror(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.respond("You can't do this! You need to have moderate members permissions!")
    else:
        raise error






@client.command(name='ping',description="Check if the bot is as fast as you lol")
async def ping(ctx):
    await ctx.respond(f"Pong! 🏓 \n\nLatency {client.latency * 1000} .ms")






@client.command(name='bye',description="Say bye!")
async def bye(ctx):
    await ctx.respond("Bye, Cya!")






@client.command(name='rickroll',description="Rickroll a member of the server!")
async def rickroll(ctx, member: Option(discord.Member, description='Who do you want to rickroll?', required=True)):
  if member.id == ctx.author.id:
        await ctx.respond("Rickrolling yourself is deadly.")
  elif member.id == client.user.id:
        await ctx.respond('I am NOT gonna do that.')
  else:  
        rick = discord.Embed(title="Rickroll Alert", description=f"You just got rickrolled by {ctx.author.mention}", colour=discord.Colour.random())
        rick.add_field(name="HAHA", value=f"{member.mention} Get rickrolled!")
        rick.set_thumbnail(url='https://tenor.com/view/rickroll-roll-rick-never-gonna-give-you-up-never-gonna-gif-22954713')
        await ctx.respond(embed=rick)
        await ctx.respond(
        f'{ctx.author.mention} just rickrolled {member.mention}!')
        


@client.command(name='slap',description="Slap your enemy >:D")
async def slap(ctx, member: Option(discord.Member, description="Who do you want to slap? >:)", required=True)):
  if member.id == ctx.author.id:
        await ctx.respond("BRUH! You can't slap yourself!")
  elif member.id == client.user.id:
        await ctx.respond('But I love myself')
  else:      
      slap=discord.Embed(title="Slap Alert", description=f"You just got slapped by {ctx.author.mention}", colour=discord.Colour.random())
      slap.add_field(name="AHHHH", value=f"You got slapped by {ctx.author.mention}")
      slap.set_thumbnail(url='https://tenor.com/view/will-smith-chris-rock-jada-pinkett-smith-oscars2022-smack-gif-25234614')
      await ctx.respond(embed=slap)
      await ctx.respond(
        f'AHHHHHHH {ctx.author.mention} just slapped {member.mention} !')
      





@client.command(name='help',description=' All the commands in this bot')
async def help(ctx):
    embed = discord.Embed(title='Help', description='All the commands of this bot', color=discord.Colour.random(), timestamp=datetime.utcnow())
    embed.add_field(name='Moderation Commands (/)', value='/ban, /kick, /lock, /unlock, /mute, /unmute, /announce')
    embed.add_field(name='Fun Commands (/)', value='/slap, /rickroll, /bye')
    embed.add_field(name='Info (/)', value='/ping')
    embed.add_field(name="Moderation Commands (!)", value="!reactrole")
    embed.add_field(name="Fun Commands (!)", value = "!gtn")
    embed.set_footer(text=f'Issued by {ctx.author}')  
    embed.set_author(name="Having a great day or what?", icon_url="https://pbs.twimg.com/media/E2S6GMxX0AA03Df?format=png&name=small")
    await ctx.respond(embed=embed)







# ---------------------------------------------------------------Events----------------------------------------------------------------------------------------


@client.event
async def on_ready():
    status_task.start()
    print('Connected to bot: {}'.format(client.user.name))
    print('Bot ID: {}'.format(client.user.id))

@tasks.loop()
async def status_task() -> None:
    await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name="Legend Sa maskom's server".format(len(client.guilds))))
    await asyncio.sleep(7)
    await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name="Your Commands"))
    await asyncio.sleep(7)

@client.event
async def on_member_join(member: discord.Member):
    guild = member.guild
    if guild.system_channel is not None:  # For this to work, System Messages Channel should be set in guild settings.
        await guild.system_channel.send(f"Welcome {member.mention} to {guild.name}!")

@client.event
async def on_guild_join(guild):
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            await channel.send('Yo! Thanks for adding me')
        break

@client.event
async def on_raw_reaction_add(payload):

    if payload.member.bot:
        pass

    else:
        with open('reactrole.json') as react_file:
            data = json.load(react_file)
            for x in data:
                if x['message_id'] == payload.message_id:  # checks if the found member id is equal to the id from the
                                                           # message where a reaction was added
                    if x['emoji'] == payload.emoji.name:  # checks if the found emoji is equal to the reacted emoji
                        role = discord.utils.get(client.get_guild(
                            payload.guild_id).roles, id=x['role_id'])

                    await payload.member.add_roles(role)


@client.event
async def on_raw_reaction_remove(payload):

    with open('reactrole.json') as react_file:
        data = json.load(react_file)
        for x in data:

            if x['message_id'] == payload.message_id:  # checks if the found member id is equal to the id from the
                                                        # message where a reaction was added
                if x['emoji'] == payload.emoji.name:  # checks if the found emoji is equal to the reacted emoji
                    role = discord.utils.get(client.get_guild(
                        payload.guild_id).roles, id=x['role_id'])

                
                await client.get_guild(payload.guild_id).get_member(payload.user_id).remove_roles(role)

@client.command(name="reactrole", description="Create a reaction role!")
@commands.has_permissions(administrator=True, manage_roles=True)
async def reactrole(ctx, emoji, role: Option(discord.Role), *, message):

    emb = discord.Embed(description=message)
    msg1 = await ctx.respond(embed=emb)
    await msg1.add_reaction(emoji)

    with open('reactrole.json') as json_file:
        data = json.load(json_file)

        new_react_role = {'role_name': role.name, 
        'role_id': role.id,
        'emoji': emoji,
        'message_id': msg1.id}

        data.append(new_react_role)

    with open('reactrole.json', 'w') as f:
        json.dump(data, f, indent=4)


@client.event
async def on_member_remove(ctx, member):
    await ctx.welcomechannel.respond(f'{member} has left the server.')

@client.event
async def on_ready():
    print(f"we have logged in as {client.user}")


@client.event
async def on_message(message):

    if message.author.bot != True:
        try:

            cur.execute(f"SELECT * FROM GUILD_{message.guild.id} WHERE user_id={message.author.id}")
            result = cur.fetchone()

            if result[1]==99:

                await message.channel.send(f"{message.author.mention} advanced to lvl {result[2]+1}")
                cur.execute(f"UPDATE GUILD_{message.guild.id} SET exp=0, lvl={result[2]+1} WHERE user_id={message.author.id}")
                con.commit()
            else:

                cur.execute(f"UPDATE GUILD_{message.guild.id} SET exp={result[1]+1} WHERE user_id={message.author.id}")
                con.commit()

        except sqlite3.OperationalError:

            pass




@client.slash_command(name="init", description="initialize xp")
async def init(ctx):

    cur.execute(f'''CREATE TABLE IF NOT EXISTS GUILD_{ctx.guild.id} (user_id int NOT NULL, exp int DEFAULT 0, lvl int DEFAULT 0) ''')

    for x in ctx.guild.members:
        if x.bot != True:
            cur.execute(f"INSERT INTO GUILD_{ctx.guild.id} (user_id) VALUES ({x.id})")

    con.commit()

    await ctx.respond("Leveling system initiaized")


@client.slash_command(name="xp", description="Find your level in the server!")
async def xp(ctx, user: discord.User = None):

    try:

        if user == None :
            cur.execute(f"SELECT * FROM GUILD_{ctx.guild.id} WHERE user_id={ctx.author.id}")
            result = cur.fetchone()

            await ctx.channel.send(f"{ctx.author.mention} Exp: {result[1]} Lvl: {result[2]}")

        else:
             cur.execute(f"SELECT * FROM GUILD_{ctx.guild.id} WHERE user_id={user.id}")
             result = cur.fetchone()

             if result!=None:
                 await ctx.channel.send(f"{user.mention} Exp: {result[1]} Lvl: {result[2]}")
             else:

                 await ctx.channel.send("Hmm no such user in the db")

    except sqlite3.OperationalError:

        await ctx.respond("DataBase not initialized")

keep_alive()

client.run(token)
