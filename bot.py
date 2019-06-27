import discord
from discord.ext import commands
import asyncio

client = commands.Bot(command_prefix=".", status=discord.Status.idle, activity=discord.Game(name='Booting Up...'))
client.remove_command('help')


# Global Variables
global rolelist, word, space
rolelist = []
word = None
space = True

@client.event
async def on_ready():
    print("Bot is running")
    await client.change_presence(activity=discord.Game(name="Do .help for the full list of the commands"))


@client.command()
@commands.has_permissions(administrator=True)
async def help(ctx):
    embed = discord.Embed(
        title="Character Limiter",
        description="List of commands possible with the Character Limiter",
        colour=discord.Colour.green()
    )

    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/135157512012955649/546223482409844736/Utility.png")
    embed.add_field(name=".limit (number)", value="Set the character limit", inline=False)
    embed.add_field(name=".son or .soff", value="Count spaces as a character (toggle)", inline=True)
    embed.add_field(name=".rlimit", value="Resets the limit to normal incase you made a boo boo", inline=True)
    embed.add_field(name=".exempt (@role)", value="Does not sanction roles mentioned in the command", inline=True)
    embed.add_field(name=".rexempt", value="Resets exemption list", inline=True)
    embed.add_field(name=".exemptlist", value="Shows a list of all exemptions. Numbers are role ID's", inline=True)

    await ctx.channel.send(embed=embed)


# Reset Exemption List
@client.command()
@commands.has_permissions(administrator=True)
async def rexempt(ctx):
    global rolelist
    rolelist = []
    await ctx.channel.send("Successfully reset the exemption list!")


# List Exemptions
@client.command()
@commands.has_permissions(administrator=True)
async def exemptlist(ctx):
    global rolelist
    if len(rolelist) >= 1:
        await ctx.message.delete()
        await ctx.channel.send(rolelist)

    else:
        await ctx.message.delete()
        await ctx.channel.send("There are no roles in the exemptions list. Do .exempt to add roles.")


# Reset Limit Command
@client.command()
@commands.has_permissions(administrator=True)
async def rlimit(ctx):
    global word
    word = None
    await ctx.message.delete()
    await ctx.channel.send("Successfully reset the limit")


# Do not consider spaces as a character command
@client.command()
@commands.has_permissions(administrator=True)
async def soff(ctx):
    global space
    space = False
    await ctx.message.delete()
    await ctx.channel.send("Set spaces to off")


# Consider spaces as a character command
@client.command()
@commands.has_permissions(administrator=True)
async def son(ctx):
    global space
    space = True
    await ctx.message.delete()
    await ctx.channel.send("Set spaces to on")


# Limitation Command
@client.command()
@commands.has_permissions(administrator=True)
async def limit(ctx, *limitation):
    # Initialize empty array
    limit = []

    try:

        # Split limitation content into a list
        limitation = [str(d) for d in str(limitation)]

        # Check for a digit within the list
        for i in range(len(limitation)):
            t = str.isdigit(limitation[i])

            if t == True:
                limit.append(limitation[i])

        # Join list together into a string
        limitation = "".join(map(str, limit))

        # Convert String into integer
        limitation = int(limitation)

        # Restriction for minimum 2 char
        if isinstance(limitation, int):
            if limitation < 2:
                await ctx.channel.send("You can't put a limit lower than 2 characters")
                return

            else:
                global word
                word = limitation
                await ctx.channel.send("Set the limit to" + " " + str(word))

    # Incase people type random stuff
    except ValueError:
        await asyncio.sleep(0.9)
        await ctx.message.delete()
        return


# Exemption Command
@client.command()
@commands.has_permissions(administrator=True)
async def exempt(ctx, *role):
    global rolelist
    role = str(role)

    role = role.replace("'", "").replace("(", "").replace(")", "").replace(",", "").replace("<", "").replace(">","").replace("@", "").replace("&", "")
    role = role.split()
    x = 0
    for i in range(len(role)):
        t = str.isdigit(role[i])

        if t == False:
            await ctx.channel.send("Failed. Make sure you are mentioning the role")
            return

        elif t == True:
            x += 1
            if x == len(role):
                await ctx.message.delete()
                await ctx.channel.send("Successfully added roles to exemption list.")
                break

    for i in range(len(role)):
        rolelist.append(int(role[i]))

    print(rolelist)


# On message event

@client.event
async def on_message(message):
    # Check if message is command
    await client.process_commands(message)

    # Ignores Bots
    isbot = message.author.bot

    if isbot:
        return

    message2 = message.content

    # Our Input

    x = message2

    global space
    if space == True:
        x = [str(d) for d in str(x)]

    elif space == None:
        return

    elif space == False:
        # Split On space
        x = x.split(" ")

        # Convert back to string without spaces
        x = "".join(map(str, x))

        # Split each letter into an Index
        x = [str(d) for d in str(x)]

    # Word Limit
    global word
    if word == None:
        return

    else:
        limit = word

    # length of message
    lon = len(x)

    # If length of message is as long or less than limit
    if lon == limit or lon < limit:
        print("Word Passed")
        del x[:]


    # If length of message is longer than limit
    elif lon > limit:
        global rolelist
        if len(rolelist) == 1 or len(rolelist) > 1:

            allroles = [role.id for role in message.author.roles]
            for i in rolelist:
                if i in allroles:
                    return


            await message.delete()
            sen = await message.channel.send("**HEY!** You passed the character limit")
            del x[:]
            await asyncio.sleep(0.9)
            await sen.delete()


        else:
            await message.delete()
            sen = await message.channel.send("**HEY!** You passed the character limit")
            del x[:]
            await asyncio.sleep(0.9)
            await sen.delete()



    # If somehow if and elif is bypassed, return
    else:
        return






#EXECUTING BOT TOKEN


client.run("token")
