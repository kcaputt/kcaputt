from discord.ext import commands
import discord
import os
import asyncio

async def sendembed(ctx, title, text=None, color=0x7289da):
	embed = discord.Embed(title = title, description = text, color = color)
	embed.set_footer(text = "Made By Minion3665")
	await ctx.send(embed = embed)

class Tea(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	@bot.event
	async def on_message(message):
		if message.lower().startswith("hi dad im") or message.lower().startswith("hi dad i'm"):
			name = arg
			for arg in args:
				name = name + " " + arg
			await sendembed(ctx, "Hi "+name+", I'm DAD!")
	@commands.command(name="hi dad i'm")
	async def dadjoke(self, ctx):
		"""Tell me a dad joke 
		(form: hi dad i'm {all arguments} - do not use a prefix)"""

def setup(bot):
	bot.add_cog(Tea(bot))
	
if __name__ == "__main__":
	print("Please run this cog as a discord bot")
