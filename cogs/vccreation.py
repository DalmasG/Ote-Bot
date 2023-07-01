import os

from discord.ext.commands import Bot, Cog, command, Context, has_permissions, check, CheckFailure, CommandError
from discord import Member
from discord import VoiceState, VoiceChannel


class VcCreation(Cog):
	def __init__(self, bot: Bot):
		self.bot = bot
		self.CREATOR_CHANNEL_ID = int(os.getenv('CREATOR_CHANNEL_ID'))
		self.temp_channels = {}

	@Cog.listener()
	async def on_voice_state_update(self, member: Member, before: VoiceState, after: VoiceState):
		'''
		Implements Join-To-Create Functionality.
		Creating a VC will make you its administrator.
		You cannot create a new VC if you are an admin.
		Admins are stored via the temp_channels dictionary.
		You will be transported back to your VC if you try
		to make a new one.
		'''

		if vc_after := after.channel:
			if vc_after.id == self.CREATOR_CHANNEL_ID: #if you clicked join-to-create
				if member.id not in self.temp_channels: #check if you already own a channel
					voice_channel = await member.guild.create_voice_channel(
						name=f"{member.display_name}'s VC", category=vc_after.category
					) 
					#await member.move_to(voice_channel)
					self.temp_channels[member.id] = voice_channel.id
					await voice_channel.set_permissions(member, administrator=True)
				await member.move_to(member.guild.get_channel(self.temp_channels[member.id]))

		if vc_before := before.channel: #If you left a channel
			if vc_before.id in self.temp_channels.values() and not vc_before.members:
				#If this channel is in the temp_channels dict and has no members.
				keys = [k for k, v in self.temp_channels.items() if v == vc_before.id]
				await vc_before.delete()
				self.temp_channels.pop(keys[0]) #Pop doesn't do slices, index the first


	#Created a testing command for the purposes of debugging
	@command(aliases=['t'])
	async def test(self, ctx: Context):
		print("Context From: ", ctx.channel)
		print("Server Voice Channels: ", ctx.author.guild.voice_channels)
		print("Server Text Channels: ", ctx.author.guild.text_channels)
		print(ctx.channel.permissions_for(ctx.author).administrator)
		print(ctx.channel.category_id)
		print(ctx.guild.categories)
		print(ctx.author.nick) #Useless
		print(ctx.author.name) #Discord Code Name
		print(ctx.author.display_name) #Server Nickname
		print(ctx.author.global_name) #Actual Display Name

 
				
async def setup(bot):
	await bot.add_cog(VcCreation(bot))