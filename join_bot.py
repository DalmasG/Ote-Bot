# This example requires the 'message_content' intent.

import discord
import logging


load_dotenv() #Load the .env
token = 'your token'

handler = logging.FileHandler(filename='discord.log',
	encoding='utf-8', mode='w') #Creates a logging file, so that the console isn't cluttered

intents = discord.Intents.default()
intents.message_content = True #intent nonsense

client = discord.Client(intents=intents) #Creates a "client" to handle events that happen when the bot is logged into a server


'''Clean up the functionality.. make sure there is a "voice-owner"
by default, make the first peson who joins vc-owner. Retrieve whether
a voice-owner is in the chat and identify them.

Implement new voice-channels to be at a specific location, presumably
the bottom of the "category" of voice-channels the new vc will be in.
'''
@client.event
async def on_ready(): #When the bot logs into discord
	print(f'We have logged in as {client.user}')

@client.event
async def on_message(message): #When the bot sees a message... message is an object
	if message.author == client.user:
		return

	if message.content.startswith('$hello'):
		await message.channel.send('Hello!')

@client.event
async def on_voice_state_update(member, before, after): #When the bot detects an update to a voice channel
	#member is an instance for the person joining
	#before is the channel state before the update
	#after is the channel state after... these are objects with attributes


	if str(before.channel).endswith("'s VC"):
		await before.channel.delete()

	if str(after.channel) == "join-to-create":
		#guild is just the server. this is needed since bots can be in multiple servers.
		v_channel = await member.guild.create_voice_channel(f"{str(member)}'s VC",
			position=len(member.guild.channels)-1)
		print("Created New VC")
		print(f"Move the member {str(member)}")
		await member.move_to(v_channel)
		






client.run(token, log_handler=handler, log_level=logging.DEBUG)

