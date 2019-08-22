from discord.ext import commands
import discord
import os
import asyncio

async def sendEmbed(ctx, title, text=None, color=0x7289da, message=""):
	embed = discord.Embed(title = title, description = text, color = color)
	embed.set_footer(text = "Made By Minion3665")
	return await ctx.send(message, embed = embed)

async def changeEmbedColor(message, color=0x7289da):
	newEmbed = None
	try:
		newEmbed = message.embeds[0].copy()
	except:
		pass
	newEmbed.color = color
	await message.edit(embed = newEmbed)

def getCheckChannel(ctx):
	for channel in ctx.guild.channels:
		if isinstance(channel, discord.TextChannel) and channel.topic != None and channel.topic.startswith("[activity]"):
			return channel
	return None
			
			

class ActivityChecks(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(name="setup")
	async def setup(self, ctx):
		"""Setup your server for the bot"""

	@commands.command(name="check")
	async def check(self, ctx):
		"""Start an activity check"""
		activeRole = discord.utils.get(ctx.guild.roles, name='active')
		closedRole = discord.utils.get(ctx.guild.roles, name='activity check closed')
		activityCheckChannel = getCheckChannel(ctx)
		if activeRole == None or closedRole == None or activityCheckChannel == None:
			await sendEmbed(ctx, "Your server is incorrectly setup", "Please run the "+ctx.prefix+"setup command to setup your server again", 0xaa0000)
			return
		myResponseMessage = await sendEmbed(ctx, "Loading activity check", "This may take a while... This embed will turn green when I start... Once the check has started you can send `stop` to the channel to stop the check early. A bot admin can also stop/mass-stop the check early, for example if maintenance is needed on the bot.")
		for member in ctx.guild.members:
			await member.remove_roles(activeRole, closedRole, reason="Activity Check Starting...")
		await sendEmbed(activityCheckChannel, "Activity Check", "Type `me`. Nothing More. Nothing Less. All messages are due within 1 day of this being sent. I will react with ✅ if it worked.", message="@everyone")
		changeEmbedColor(myResponseMessage, 0x6cb83a)

def setup(bot):
	bot.add_cog(ActivityChecks(bot))
	
if __name__ == "__main__":
	print("Please run this cog as a discord bot")
