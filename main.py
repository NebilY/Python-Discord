import discord
from discord.ext import commands
import requests

bot_token = 'Secret_token'

# Define your intents
intents = discord.Intents.default()
intents.typing = True
intents.message_content = True

# Create a bot instance
bot = commands.Bot(command_prefix='!', intents=intents)

# Define the API endpoint and headers
base_url = "https://api.football-data.org/v4/teams/66"
headers = {"X-Auth-Token": "seceret_token"}

# Function to get and print team details
def get_team_details():
    url = f"{base_url}"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()

        # Construct and return a formatted team details message
        team_details_message = (
            f"**Team Name:** {data['name']}\n"
            f"**Short Name:** {data['shortName']}\n"
            f"**Tla:** {data['tla']}\n"
            f"**Crest:** {data['crest']}\n"
            f"**Address:** {data['address']}\n"
            f"**Website:** {data['website']}\n"
            f"**Founded:** {data['founded']}\n"
            f"**Club Colors:** {data['clubColors']}\n"
            f"**Venue:** {data['venue']}\n\n"
            "**Running Competitions:**\n"
        )

        for competition in data["runningCompetitions"]:
            team_details_message += (
                f"**Competition Name:** {competition['name']}\n"
                f"**Competition Code:** {competition['code']}\n"
                f"**Competition Type:** {competition['type']}\n"
                #f"**Competition Emblem:** {competition['emblem']}\n\n"
            )

        coach = data["coach"]
        team_details_message += (
            "**Coach:**\n"
            f"**Name:** {coach['name']}\n"
            f"**Date of Birth:** {coach['dateOfBirth']}\n"
            f"**Nationality:** {coach['nationality']}\n"
        )

        #contract = coach["contract"]
        #team_details_message += (
            #f"**Contract Start:** {contract['start']}\n"
            #f"**Contract Until:** {contract['until']}\n\n"
            #"**Squad:**\n"
        #)

        for player in data["squad"]:
            team_details_message += (
                f"**Name:** {player['name']}\n"
                #f"**Position:** {player['position']}\n"
                #f"**Date of Birth:** {player['dateOfBirth']}\n"
                #f"**Nationality:** {player['nationality']}\n\n"
            )

        return team_details_message
    else:
        return f"API request failed with status code {response.status_code}"

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    print('------')

    # Send a structured introduction message when the bot is live
    introduction = (
        f"Hello, I'm your Manchester United bot!\n"
        "I have a list of commands to provide information about Manchester United.\n"
        "You can ask me about general info, players, or matches.\n"
        "To get started, type `!bot_help` to see the available commands."
    )

    for guild in bot.guilds:
        for channel in guild.text_channels:
            await channel.send(introduction)

@bot.command()
async def hello(ctx):
    user = ctx.author
    await ctx.send(f"Hello, {user.mention}!")

@bot.command()
async def bot_help(ctx):
    help_message = (
        "Here are the available commands:\n"
        "`!general` - General information about Manchester United.\n"
        "`!players` - Information about players in the team.\n"
        "`!matches` - Information about recent matches played.\n"
        "You can use these commands to explore more about Manchester United."
    )
    await ctx.send(help_message)

@bot.command()
async def general(ctx):
    # Call the get_team_details function to get and send team details
    team_details = get_team_details()

    chunk_size = 2000
    chunks = [team_details[i:i + chunk_size]for i in range(0,len(team_details),chunk_size )]

    for chunk in chunks:
        await ctx.send(chunk)

@bot.command()
async def players(ctx):
    # Provide player information here
    await ctx.send("Information about players in the team goes here.")

@bot.command()
async def matches(ctx):
    # Provide match information here
    await ctx.send("Information about matches goes here")
bot.run(bot_token)
