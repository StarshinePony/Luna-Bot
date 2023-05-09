from discord import app_commands
import discord
import requests
import random
import json

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
BOT_TOKEN = "YOUR TOKEN HERE"
GUILD_ID = guild=discord.Object(id=YOUR GUILD ID HERE)

@client.event
async def on_ready():
    await tree.sync(GUILD_ID)
    print("Ready!")

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
client.run(BOT_TOKEN)
