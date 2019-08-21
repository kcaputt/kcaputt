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
		if channel.isinstance(discord.TextChannel) and channel.topic.startswith("[activity]"):
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
		await ctx.sendembed("Loading activity check", "This may take a while... I will react to your message with ✅ when I start")
				activeRole = discord.utils.get(ctx.guild.members, name='Active')
        closedRole = discord.utils.get(ctx.guild.members, name='Activity Check Closed')
				activityCheckChannel = getCheckChannel();
				if activeRole == None or closedRole == None or activityCheckChannel == None:
					await ctx.sendembed("Your server is incorrectly setup", "Please run the "+bot.prefix+"setup command to setup your server again", 0xaa0000)
        x = message.server.members
        for member in x:
            await client.remove_roles(member, role, role2)
        channel = discord.utils.get(message.server.channels, name='activity-check')
        await client.add_reaction(message, '✅')
        print("starting a check")
        await client.send_message(channel, "@everyone Activity check. Type `me`. Nothing More. Nothing Less. All messages are due within 1 day of this being sent. I will react with ✅ if it worked and nothing if it did not.")
        timeout = time.time() + 60*60*24
        while True:
            msg = await client.wait_for_message(channel=channel, timeout=5)
            if msg == None:
                pass
            elif msg.content.lower() != "me":
                if msg.author == client.user:
                    pass
                else:
                    await client.delete_message(msg)
            else:
                await client.add_roles(msg.author, role)
                await client.add_reaction(msg, '✅')
            if time.time() > timeout:
                break
        for member in x:
            await client.add_roles(member, role2)
        await client.send_message(channel, "Activity check complete. well done `@active`")

def setup(bot):
	bot.add_cog(ActivityChecks(bot))
	
if __name__ == "__main__":
	print("Please run this cog as a discord bot")
