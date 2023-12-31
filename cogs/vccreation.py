import os

from discord.ext.commands import Bot, Cog
from discord import Member
from discord import VoiceState, VoiceChannel


class VcCreation(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.CREATOR_CHANNEL_ID = int(os.getenv('CREATOR_CHANNEL_ID'))
        self.temp_channels = set()

    @Cog.listener()
    async def on_voice_state_update(self, member: Member, before: VoiceState, after: VoiceState):
        if vc_before := before.channel:
            if vc_before.id in self.temp_channels and not vc_before.members:
                await vc_before.delete()
                self.temp_channels.remove(vc_before)
                
        if vc_after := after.channel:
            if vc_after.id == self.CREATOR_CHANNEL_ID:
                voice_channel = await member.guild.create_voice_channel(
                    name=f"{member.name}'s VC",
                )
                await member.move_to(voice_channel)
                self.temp_channels.add(voice_channel.id)
            await voice_channel.set_permissions(member, administrator=True)
 
 
                
async def setup(bot):
    await bot.add_cog(VcCreation(bot))