from discord.ext import commands
import discord
import os
import asyncio

async def sendembed(ctx, title, text=None, color=0x7289da):
	embed = discord.Embed(title = title, description = text, color = color)
	embed.set_footer(text = "Made By Minion3665")
	await ctx.send(embed = embed)

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
		print("Server: "+str(ctx.guild.name)+", Active role: "+str(activeRole)+", Closed role: "+str(closedRole)+", Activity check channel "+str(activityCheckChannel))
		if activeRole == None or closedRole == None or activityCheckChannel == None:
			await sendembed(ctx, "Your server is incorrectly setup", "Please run the "+ctx.prefix+"setup command to setup your server again", 0xaa0000)
			return
		await sendembed(ctx, "Loading activity check", "This may take a while... I will react to your message with ✅ when I start... Once the check has started you can send `stop` to the channel to stop the check early. A bot admin can also stop/mass-stop the check early, for example if maintenance is needed on the bot.")

def setup(bot):
	bot.add_cog(ActivityChecks(bot))
	
if __name__ == "__main__":
	print("Please run this cog as a discord bot")
