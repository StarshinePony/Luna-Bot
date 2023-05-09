from discord.ext import commands
from discord import app_commands
import discord
import requests
import random
import json

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
MODROLE = <MODROLE HERE>
BOT_TOKEN = "YOUR TOKEN HERE"
GUILD_ID = guild=discord.Object(id=YOUR GUILD ID HERE)
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("Bot is ready!")
  
@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=GUILD_ID))
    print("Ready!")


@bot.hybrid_command()
@commands.has_role(MODROLE)
async def echo(ctx, channel: discord.TextChannel, *, message):
    await channel.send(message)

@bot.hybrid_command()
async def luna(ctx):
    await ctx.send("HAIL LUNA")

@bot.command(name='prefix')
@commands.has_role(MODROLE)
async def change_prefix(ctx, new_prefix: str):
    bot.command_prefix = new_prefix
    await ctx.send(f'Prefix has been changed to `{new_prefix}`')

@bot.command()
async def pick(ctx, search_term: str):
    client_id = 'ID HERE'
    client_secret = 'SECRET HERE'

    token_url = 'https://www.deviantart.com/oauth2/token'
    payload = {'grant_type': 'client_credentials', 'client_id': client_id, 'client_secret': client_secret}
    response = requests.post(token_url, data=payload)

    if response.status_code == 200:
        access_token = json.loads(response.content.decode('utf-8'))['access_token']
        url = f'https://www.deviantart.com/api/v1/oauth2/browse/tags/?tag={search_term}&access_token={access_token}'
        headers = {'Authorization': f'Bearer {access_token}', 'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        print(url)

        if response.status_code == 200:
            data = json.loads(response.content.decode('utf-8'))
            if data['has_more']:
                image_url = random.choice(data['results'])['content']['src']
                await ctx.send(f'More than one image found for "{search_term}"')
                await ctx.send(image_url)
                print(image_url)
                
            elif len(data['results']) == 0:
                await ctx.send(f'No images found for "{search_term}"')
            else:
                image_url = data['results'][0]['content']['src']
                await ctx.send(image_url)
        else:
            await ctx.send(f'Could not search for images on DeviantArt')
    else:
        await ctx.send(f'Could not authenticate with DeviantArt API')
                
@tree.command(name = "pick", description = "Get a pick from DeviantArt!", guild=discord.Object(id=123456789)) #Add the guild ids in which the slash command will appear. If it should be in all, remove the argument, but note that it will take some time (up to an hour) to register the command if it's for all guilds.
async def pick(interaction, search_term: str):
    client_id = 'ID here'
    client_secret = 'SECRET here'

    token_url = 'https://www.deviantart.com/oauth2/token'
    payload = {'grant_type': 'client_credentials', 'client_id': client_id, 'client_secret': client_secret}
    response = requests.post(token_url, data=payload)

    if response.status_code == 200:
        access_token = json.loads(response.content.decode('utf-8'))['access_token']
        url = f'https://www.deviantart.com/api/v1/oauth2/browse/tags/?tag={search_term}&access_token={access_token}'
        headers = {'Authorization': f'Bearer {access_token}', 'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        print(url)

        if response.status_code == 200:
            data = json.loads(response.content.decode('utf-8'))
            if data['has_more']:
                image_url = random.choice(data['results'])['content']['src']
                await interaction.response.send_message(image_url)
                print(image_url)
                
            elif len(data['results']) == 0:
                await interaction.response.send_message(f'No images found for "{search_term}"')
            else:
                image_url = data['results'][0]['content']['src']
                await interaction.response.send_message(image_url)
        else:
            await interaction.response.send_message(f'Could not search for images on DeviantArt')
    else:
        await interaction.response.send_message(f'Could not authenticate with DeviantArt API')
#For Slash cmds use client.run, for ! cmds use bot.run
#bot.run(BOT_TOKEN) 
client.run(BOT_TOKEN)
