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
			
			

class ActivityChecks(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(name="setup")
	async def setup(self, ctx):
		"""Setup your server for the bot"""

	@commands.command(name="check")
	async def check(self, ctx):
		"""Start an activity check"""
		await sendembed(ctx, "Loading activity check", "This may take a while... I will react to your message with ✅ when I start...")
		activeRole = discord.utils.get(ctx.guild.members, name='Active')
		closedRole = discord.utils.get(ctx.guild.members, name='Activity Check Closed')
		activityCheckChannel = getCheckChannel(ctx);
		if activeRole == None or closedRole == None or activityCheckChannel == None:
			await sendembed(ctx, "Your server is incorrectly setup", "Please run the "+ctx.prefix+"setup command to setup your server again", 0xaa0000)
			return

def setup(bot):
	bot.add_cog(ActivityChecks(bot))
	
if __name__ == "__main__":
	print("Please run this cog as a discord bot")
