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
		The bot should be able to create VC's in the voice channel category.
		If you are the admin of a VC, it will not let you make a new one.
		However, this breaks if you do it fast enough.. TODO FIX THIS.
		VcCreation uses a temp channels dictionary to do this.
		'''

		if vc_after := after.channel:
			if vc_after.id == self.CREATOR_CHANNEL_ID:
				if member.id not in self.temp_channels: #check if you already own a channel
					voice_channel = await member.guild.create_voice_channel(
						name=f"{member.display_name}'s VC", category=vc_after.category
					) 
					#await member.move_to(voice_channel)
					self.temp_channels[member.id] = voice_channel.id
					await voice_channel.set_permissions(member, administrator=True)
				await member.move_to(member.guild.get_channel(self.temp_channels[member.id]))

		if vc_before := before.channel:
			if vc_before.id in self.temp_channels.values() and not vc_before.members:
				keys = [k for k, v in self.temp_channels.items() if v == vc_before.id]
				await vc_before.delete()
				self.temp_channels.pop(keys)


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