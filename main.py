import discord

client = discord.Client(intents=discord.Intents().all())


@client.event
async def on_ready():
  print('Bot is now running!')


@client.event
async def on_message(message):
  if message.author == client.user:
    return
  if message.content == 'test':
    await message.channel.send('test')

your_bot_access_token = 'some_access_token'
client.run(int(your_bot_access_token))
