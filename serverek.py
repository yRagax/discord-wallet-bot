from keep_alive import keep_alive
import discord
import os

client = discord.Client(intents=discord.Intents().all())


@client.event
async def on_ready():
  print('Bot is now running!')


@client.event
async def on_message(message):
  if message.author == client.user:
    return

  server1_token = 'some_token_here'
  server2_token = 'some_token_here2'

  if message.guild.id in [int(server1_token), int(server2_token)]:
    args = ' '.join(message.content.split()).split(' ')
    if args[0] in ['wallet', 'w']:
      if len(args) < 2:
        await message.channel.send('Incorrect command input')
        return

      if args[1] in ['print', 'p']:
        lines = open('wallets.txt', 'r').readlines()
        for line in lines:
          if line.split(',')[0] == '<@'+str(message.author.id)+'>':
            await message.channel.send(f"{message.author.name} has ${line.split(',')[1]}")
            break
        await message.add_reaction('👍')

      if not 'Bankier' in [role.name for role in message.author.roles]:
        return

      if args[1] in ['printall', 'pa']:
        output = []
        lines = open('wallets.txt', 'r').readlines()
        for line in lines:
          for member in message.guild.members:
            if member.id == int(line.split(',')[0][2:-1]):
              output.append((line.split(',')[1], member.name))
        if output:
          output_msg = ''
          output = sorted(output, reverse=True)
          for entry in output:
            output_msg += entry[1] + ' has $' + entry[0]
          await message.channel.send(output_msg)
        await message.add_reaction('👍')

      if args[1] in ['resetwalletfile']:
        open('wallets.txt', 'w').close()
        await message.add_reaction('👍')

      if args[1] in ['add', 'a']:
        if len(args) < 3:
          await message.channel.send('Incorrect command input')
          return
        lines = open('wallets.txt', 'r').readlines()
        for line in lines:
          if line.split(',')[0] == args[2]:
            await message.channel.send('Member already has a wallet')
            return
        f = open('wallets.txt', 'a')
        f.write(args[2]+',0\n')
        f.close()
        await message.add_reaction('👍')

      if args[1] in ['remove', 'r']:
        if len(args) < 3:
          await message.channel.send('Incorrect command input')
          return
        lines = open('wallets.txt', 'r').readlines()
        with open('wallets.txt', 'w') as f:
          for line in lines:
            if line.split(',')[0] != args[2]:
              f.write(line)
        await message.add_reaction('👍')

      if args[1] in ['give', 'g']:
        members = [arg for arg in args if arg.startswith('<@') and arg.endswith('>')]
        if len(args) < 4 or not args[len(members)+2].isdigit():
          await message.channel.send('Incorrect command input')
          return
        amount = args[len(members)+2]
        lines = open('wallets.txt', 'r').readlines()
        with open('wallets.txt', 'w') as f:
          for line in lines:
            if line.split(',')[0] in members:
              f.write( line.split(',')[0] + ',' + str(int(line.split(',')[1])+int(amount)) + '\n')
            else:
              f.write(line)
        await message.add_reaction('👍')

      if args[1] in ['take', 't']:
        members = [arg for arg in args if arg.startswith('<@') and arg.endswith('>')]
        if len(args) < 4 or not args[len(members)+2].isdigit():
          await message.channel.send('Incorrect command input')
          return
        amount = args[len(members)+2]
        lines = open('wallets.txt', 'r').readlines()
        with open('wallets.txt', 'w') as f:
          for line in lines:
            if line.split(',')[0] in members:
              f.write( line.split(',')[0] + ',' + str(int(line.split(',')[1])-int(amount)) + '\n')
            else:
              f.write(line)
        await message.add_reaction('👍')


keep_alive()
client.run(os.getenv('TOKEN'))

