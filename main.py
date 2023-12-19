import discord
from discord.ext import commands
import random
import asyncio

intents = discord.Intents.default()
intents.message_content = True
intents.typing = False
intents.presences = False
bot = commands.Bot(command_prefix='$', intents=intents)

#==================List of custom status messages===============#
custom_statuses = [
    "Coding Dreams 🌌",
    "Searching for WiFi in a Forest 🌲📶",
    "Conquering the Digital Realm 🚀",
    "Calculating the Meaning of Life (and Pi) 🤔🥧",
    "Befriending Aliens on Discord 👽",
    "Inventing a Bot Language 🤖💬",
    "Training Pixel Penguins for World Domination 🐧🌍",
    "Hunting Bugs in the Matrix 🐜🕸️",
    "Mastering the Art of Emoji-fu 🥋",
    "Breaking the Discord Sound Barrier 🔊✨"
]

#===================Command categories======================#
categories = {
    'Fun': 'Commands for fun and entertainment',
    'Moderation': 'Commands for moderation and server management',
    'Utility': 'Utility commands',
    'Misc': 'Miscellaneous commands',
}
#==========================================================#

async def update_custom_status():
    while True:
        custom_status = random.choice(custom_statuses)
        await bot.change_presence(activity=discord.Game(custom_status))
        await asyncio.sleep(60 * 1)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    bot.loop.create_task(update_custom_status())

# Ping command
@bot.command(name='ping', category='Utility', help='Check the bot\'s latency and response time.')
async def ping(ctx):
    start_time = discord.utils.utcnow()
    message = await ctx.send('Pinging...')
    end_time = discord.utils.utcnow()
    bot_response_time = (end_time - start_time).total_seconds() * 1000
    api_latency = round(bot.latency * 1000)
    server_latency = round((end_time - ctx.message.created_at).total_seconds() * 1000)
    embed = discord.Embed(
        title='Bot Latency',
        description=(
            f'**Bot Ping:** {bot_response_time:.2f}ms\n 💯'
            f'**API Ping:** {api_latency}ms\n 💥'
            f'**Server Ping:** {server_latency}ms 💫'
        ),
        color=discord.Color.blue()
    )
    await message.edit(content=None, embed=embed)

#Userinfo
@bot.command(name='userinfo', category='Utility', help='Shows user\'s info')
async def userinfo(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(
        title=f'{member.display_name}',
        color=discord.Color.green()
    )

    embed.set_thumbnail(url=member.avatar.url)
    embed.add_field(name='User ID', value=member.id, inline=False)
    embed.add_field(name='Created At', value=member.created_at.strftime('%Y-%m-%d %H:%M:%S'), inline=False)
    embed.add_field(name='Joined At', value=member.joined_at.strftime('%Y-%m-%d %H:%M:%S'), inline=False)
    embed.add_field(name='Roles', value=', '.join(role.name for role in member.roles), inline=False)

    await ctx.send(embed=embed)

# Serverinfo command
@bot.command(name='serverinfo', category='Utility', help='Shows server\'s info')
async def serverinfo(ctx):
    embed = discord.Embed(
        title=f'{ctx.guild.name}',
        color=discord.Color.gold()
    )

    embed.set_thumbnail(url=ctx.guild.icon.url)
    embed.add_field(name='Server ID', value=ctx.guild.id, inline=False)
    embed.add_field(name='Owner', value=ctx.guild.owner, inline=False)
    embed.add_field(name='Members', value=ctx.guild.member_count, inline=False)
    embed.add_field(name='Created At', value=ctx.guild.created_at.strftime('%Y-%m-%d %H:%M:%S'), inline=False)
    embed.add_field(name='Text Channels', value=len(ctx.guild.text_channels), inline=False)
    embed.add_field(name='Voice Channels', value=len(ctx.guild.voice_channels), inline=False)
    embed.add_field(name='Emojis', value=', '.join(str(emoji) for emoji in ctx.guild.emojis[:10]), inline=False)
    embed.add_field(name='Roles', value=', '.join(role.name for role in ctx.guild.roles[:10]), inline=False)

    await ctx.send(embed=embed)

# Kicks
@bot.command(name='kick', category='Moderation', help='Kicks the targeted member')
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'**{member.display_name}** has been kicked 💢')

# Ban
@bot.command(name='ban', category='Moderation', help='Bans the targeted member')
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'**{member.display_name}** has been banned 💢')

# Add Role
@bot.command(name='addrole', category='Moderation', help='add role to the targeted member')
@commands.has_permissions(manage_roles=True)
async def add_role(ctx, member: discord.Member, role: discord.Role):
    await member.add_roles(role)
    await ctx.send(f'Added **{role.name}** to **{member.display_name}** 👍')

# Remove Role
@bot.command(name='removerole', category='Moderation', help='remove role of the targeted member')
@commands.has_permissions(manage_roles=True)
async def remove_role(ctx, member: discord.Member, role: discord.Role):
    await member.remove_roles(role)
    await ctx.send(f'Removed **{role.name}** from **{member.display_name}** 👊')

#nick 
@bot.command(name='nick', category='Misc', help='Change the nickname of the targeted member')
@commands.has_permissions(manage_nicknames=True)
async def nick(ctx, member: discord.Member, *, new_nick=None):
    if new_nick is None:
        await ctx.send("Please provide a new nickname 🦾")
        return

    try:
        await member.edit(nick=new_nick)
        await ctx.send(f"**{member.mention}'s Nickname Has Been Changed to `{new_nick}` 🤖**")
    except discord.Forbidden:
        await ctx.send("I don't have permission to change that user's nickname 🤖")

#lock channel
@bot.command(name='lock', category='Moderation', help='Lock the channel')
@commands.has_permissions(manage_channels=True)
async def lock(ctx):
    overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = False
    await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    await ctx.send(f"✅ **This channel has been locked.**")

#unlock channel
@bot.command(name='unlock', category='Moderation', help='unlock the channel')
@commands.has_permissions(manage_channels=True)
async def unlock(ctx):
    overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = True
    await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    await ctx.send("✅ **This channel has been unlocked.**")

#hide channel
@bot.command(name='hide', category='Moderation', help='Hide the channel')
@commands.has_permissions(manage_channels=True)
async def hide(ctx):
    overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
    overwrite.view_channel = False
    await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    await ctx.send(f"✅ **This channel has been hidden.**")

#unhide channel
@bot.command(name='unhide', category='Moderation', help='Unhide the channel')
@commands.has_permissions(manage_channels=True)
async def unhide(ctx):
    overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
    overwrite.view_channel = True
    await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    await ctx.send("✅ **This channel has been unhidden.**")

#Staff Role
@bot.command(name='staff', category='Moderation', help='Add staff role to the targeted member')
@commands.has_permissions(manage_roles=True)
async def staff(ctx, member: discord.Member):
    staff_role_id = 1119689115579973872  #<----- staff role ID
    
    staff_role = ctx.guild.get_role(staff_role_id)
    
    if staff_role:
        await member.add_roles(staff_role)
        await ctx.send(f"✅ ** Successfully Given `{staff_role.name}` Role To {member.mention} **")
    else:
        await ctx.send("Cant Role Id jo dala hye check karle")

#remove staff role
@bot.command(name='rstaff', category='Moderation', help='Remove staffrole of the targeted user')
@commands.has_permissions(administrator=True)
async def rstaff(ctx, member: discord.Member):
    staff_role_id = 1119689115579973872  #<---- staff role ID
    
    staff_role = ctx.guild.get_role(staff_role_id)
    
    if staff_role:
        if staff_role in member.roles:
            await member.remove_roles(staff_role)
            await ctx.send(f"✅ **Successfully Removed `{staff_role.name}` Role From {member.mention}**")
        else:
            await ctx.send(f"{member.mention} doesn't have the `{staff_role.name}` role.")
    else:
        await ctx.send("**Invalid Staff Role ID. Please configure it properly.**")

#dm command 
@bot.command(name='Dm', category='Misc', help='Dms the targeted userid')
@commands.has_permissions(administrator=True)
async def dm(ctx, user_id_or_mention, *, message):
    # Check if the user ID is valid
    try:
        user_id = int(user_id_or_mention.strip("<@!>"))
        user = await bot.fetch_user(user_id)
    except ValueError:
        user = ctx.message.mentions[0] if ctx.message.mentions else None

    if user is not None:
        if user.id == 1086567184920227900:
            await ctx.send("❌ You cannot DM your father.")
        else:
            try:
                await user.send(message)
                await ctx.send(f"✅ Message sent to {user.mention}")
            except discord.Forbidden:
                await ctx.send("❌ Unable to send a message to this user.")
    else:
        await ctx.send("❌ User not found. Make sure you provide a valid user ID or mention.")

# Steal emoji
@bot.command(name='steal', category='Misc', help='Steal\'s the replied emoji')
@commands.has_permissions(manage_emojis=True)
async def steal(ctx, emoji: discord.Emoji, *, name=None):
    async with ctx.typing():
        emoji_image = await emoji.url.read()
        emoji = await ctx.guild.create_custom_emoji(name=name or emoji.name, image=emoji_image)

    await ctx.send(f'Emoji {emoji} has been added.')

# Purge command
@bot.command(name='purge', category='Misc', help='Purge the previous chats')
@commands.has_permissions(manage_messages=True)
async def purge(ctx, limit: int):
    deleted_messages = await ctx.channel.purge(limit=limit + 1)
    await ctx.send(f'Purged {len(deleted_messages) - 1} messages.')

# Purge command for bot messages
@bot.command(name='bpurge', category='Misc', help='Purge the previous bot messages')
@commands.has_permissions(manage_messages=True)
async def bpurge(ctx, limit: int):
    def is_bot_message(message):
        return message.author.bot

    deleted_messages = await ctx.channel.purge(limit=limit + 1, check=is_bot_message)
    await ctx.send(f'Purged {len(deleted_messages) - 1} bot messages.')

#Rule
@bot.command(name='rule', help='Display server rules')
async def rule(ctx):
    with open('rules.txt', 'r', encoding='utf-8') as file:
        rules = file.read()
    embed = discord.Embed(
        title='Rules & Guideness',
        description=rules,
        color=discord.Color.green()
    )
    message = await ctx.send(embed=embed)
    emojis = ['✅']
    for emoji in emojis:
        await message.add_reaction(emoji)


#===========================================================#

class MyHelpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def send_bot_help(self, mapping, ctx):
        embed = discord.Embed(
            title="Command Help",
            color=discord.Color.blue(),
            description="Please choose a category:"
        )

        # Display server icon
        embed.set_thumbnail(url=ctx.guild.icon.url)

        # Generate a list of categories
        categories = sorted(set(cog.qualified_name for cog in self.bot.cogs.values()))
        for category in categories:
            cog = self.bot.get_cog(category)
            if cog:
                commands_list = []
                for command in cog.get_commands():
                    commands_list.append(f'`{command.name}` - {command.short_doc or "No description"}')
                category_description = '\n'.join(commands_list)
                embed.add_field(name=f"**{category}**", value=category_description, inline=False)

        message = await ctx.send(embed=embed)
        reactions = ['⬅️', '➡️']

        for reaction in reactions:
            await message.add_reaction(reaction)

        def check(reaction, user):
            return user == ctx.author and reaction.message.id == message.id and str(reaction.emoji) in reactions

        current_page = 0

        while True:
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)

                if str(reaction.emoji) == '⬅️':
                    current_page = max(0, current_page - 1)
                elif str(reaction.emoji) == '➡️':
                    current_page = min(len(categories) - 1, current_page + 1)

                new_embed = discord.Embed(
                    title=f"Command Help - Category: {categories[current_page]}",
                    color=discord.Color.blue()
                )
                cog_name = categories[current_page]
                cog = self.bot.get_cog(cog_name)
                if cog:
                    commands_list = []
                    for command in cog.get_commands():
                        commands_list.append(f'`{command.name}` - {command.short_doc or "No description"}')
                    new_embed.description = '\n'.join(commands_list)

                # Display server icon
                new_embed.set_thumbnail(url=ctx.guild.icon.url)

                await message.edit(embed=new_embed)
                await message.remove_reaction(reaction, user)

            except asyncio.TimeoutError:
                break

# Remove the default help command
bot.remove_command('help')

# Add the cog to the bot
help_cog = MyHelpCommand(bot)
bot.add_cog(help_cog)

# Custom $help command
@bot.command(name='help', help='Display a list of commands and their descriptions.')
async def help(ctx):
    # Trigger the simplified help system
    await help_cog.send_bot_help(None, ctx)

#===========================================================#

# Run the bot with the token
bot.run('MTE4NTk1NDM5NDgzNjA1MDAyMQ.GxbXBx.ZMm0f9C_l8Q-XMSYfvmScQrjqAtZUx6Amj9efg')