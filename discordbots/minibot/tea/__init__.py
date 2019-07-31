from discord.ext import commands
import discord
import os
import asyncio

async def sendembed(ctx, title, text=None, color=0x7289da):
	embed = discord.Embed(title = title, description = text, color = color)
	embed.set_footer("Made By Minion3665")
	await ctx.send(embed = embed)

class Tea(commands.Cog)
	def __init__(self, bot):
		self.bot = bot
		
	@commands.command(name="dad i'm"):
	async def dadjoke(self, ctx, arg, *args):
		"""Tell me a dad joke 
		(form: {prefix}dad i'm {all arguments})"""
		name = arg
		for arg in args:
			name = name + " " + arg
		await sendembed(ctx, "Hey dad...", "Hi "++", I'm DAD!")

def setup(bot):
	bot.add_cog()
	
if __name__ == "__main__":
	print("Please run this cog as a discord bot")
