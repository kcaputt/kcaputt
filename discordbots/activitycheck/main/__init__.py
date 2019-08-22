from discord.ext import commands
import discord
import os
import asyncio
import time

shuttingDown = False
activityCheckChannels = []

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

def owner_or_has_perms(**perms):
	async def predicate(ctx):
		return commands.has_permissions.predicate(ctx) or commands.is_owner.predicate(ctx)
	return commands.check(predicate)

class ActivityChecks(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	@commands.Cog.listener()
	async def on_member_join(self, member):
		closedRole = discord.utils.get(ctx.guild.roles, name='activity check closed')
		if closedRole == None:
			pass # Server isn't set up correctly

	async def cog_command_error(self, ctx, error):
		if isinstance(error, commands.MissingPermissions):
			await sendEmbed(ctx, "Oops, we got an error", "**You don't seem to have enough permissions to run that command**\n\nAnd here is the error in person to tell you what it thinks...\n`"+str(error)+"`\n*(There- wasn't that just delightful)*")
		elif isinstance(error, commands.BotMissingPermissions):
			await sendEmbed(ctx, "Oops, we got an error", "**I don't seem to have enough permissions to run that command**\n\nAnd here is the error in person to tell you what it thinks...\n`"+str(error)+"`\n*(There- wasn't that just delightful)*")
		elif isinstance(error, commands.NoPrivateMessage):
			await sendEmbed(ctx, "Oops, we got an error", "**You can't run this one in DMs**\n\nAnd here is the error in person to tell you what it thinks...\n`"+str(error)+"`\n*(There- wasn't that just delightful)*")
	
	@commands.command(name="setup")
	@commands.guild_only()
	@owner_or_has_perms(manage_roles=True, manage_channels=True)
	@commands.bot_has_permissions(manage_roles=True, manage_channels=True)
	async def setup(self, ctx):
		"""Setup your server for the bot"""
		updated = []
		activeRole = discord.utils.get(ctx.guild.roles, name='active')
		closedRole = discord.utils.get(ctx.guild.roles, name='activity check closed')
		activityCheckChannel = getCheckChannel(ctx)
		if activeRole.position >= ctx.guild.me.top_role.position or closedRole.position >= ctx.guild.me.top_role.position:
			await sendEmbed(ctx, "I couldn't setup permissions", "It appears that you have `active` and/or `activity check closed` roles that I can't.. quite.. reach....... *puff puff*. Please move them down for me. Kthxbye", 0xaa0000)
			return
		if activeRole == None:
			updated.append("Active role updated")
			activeRole = await ctx.guild.create_role("active", reason="Setup command for the activity checks run by "+str(ctx.author))
		if closedRole == None:
			updated.append("Closed role updated")
			closedRole = await ctx.guild.create_role("activity check closed", reason="Setup command for the activity checks run by "+str(ctx.author))
		if activityCheckChannel == None:
			updated.append("Check channel updated")
			overwrites = {
				ctx.guild.default_role: discord.PermissionOverwrite(read_messages=True, send_messages=True, add_reactions=False),
				activeRole: discord.PermissionOverwrite(read_messages=True, send_messages=False),
				closedRole: discord.PermissionOverwrite(read_messages=True, send_messages=False),
				ctx.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True, add_reactions=True)
			}
			channel = await ctx.guild.create_text_channel('activity-check', overwrites=overwrites, topic="[activity] Autogenerated channel for activity checks", reason="Setup command for the activity checks run by "+str(ctx.author))
		description = str(len(updated))+" things had to be updated\n\nHere they are:\n"
		if len(updated) == 0:
			description = "Nothing had to be updated\n"
		for item in updated:
			description = description + "○ " + item + "\n"
		description = description + "\n\n**What can I do to ensure that things remain correctly setup?**\n○ You *can* change the channel name and topic but ensure that the topic always starts with `[activity]`\n○ You *can* change role permissions or move roles but ensure that I am always above the `active` and `activity check closed` role\n○You *should not* deny me permissions on the activity check channel"
		for member in ctx.guild.members:
				await member.add_roles(closedRole, reason="Setup command for the activity checks run by "+str(ctx.author))
		await sendEmbed(ctx, "Server setup finished!", description, 0x6cb83a)
		
			
			
			
		
	@commands.command(name="check")
	@commands.has_permissions(manage_roles=True)
	@commands.bot_has_permissions(manage_roles=True)
	async def check(self, ctx):
		"""Start an activity check"""
		checkStopped = False
		activeRole = discord.utils.get(ctx.guild.roles, name='active')
		closedRole = discord.utils.get(ctx.guild.roles, name='activity check closed')
		activityCheckChannel = getCheckChannel(ctx)
		if activeRole == None or closedRole == None or activityCheckChannel == None:
			await sendEmbed(ctx, "Your server is incorrectly setup", "Please run the "+ctx.prefix+"setup command to setup your server again", 0xaa0000)
			return
		elif activeRole.position >= ctx.guild.me.top_role.position or closedRole.position >= ctx.guild.me.top_role.position:
			await sendEmbed(ctx, "Your server is incorrectly setup", "It appears that you have `active` and/or `activity check closed` roles that I can't.. quite.. reach....... *puff puff*. Please move them down for me. Kthxbye", 0xaa0000)
			return
		elif not (activityCheckChannel.permissions_for(ctx.guild.me).send_messages and activityCheckChannel.permissions_for(ctx.guild.me).add_reactions and activityCheckChannel.permissions_for(ctx.guild.me).read_messages):
			await sendEmbed(ctx, "Your server is incorrectly setup", "I... might not be allowed to do that. I don't really want to do anything that I don't have authorization for... Please can you make sure that I have `send messages`, `add reactions` and `read messages` permissions in "+activityCheckChannel.mention+" please.", 0xaa0000)
			return
		elif activityCheckChannel in activityCheckChannels:
			await sendEmbed(ctx, "Your server is already running a check in this channel", "Wait till the current check is over or stop it by saying `stop` in the check channel if you started it before starting a new one", 0xaa0000)
			return
		activityCheckChannels.append(activityCheckChannel)
		myResponseMessage = await sendEmbed(ctx, "Loading activity check", "This may take a while... This embed will turn green when I start... Once the check has started you can send `stop` to the channel to stop the check early. A bot admin can also stop/mass-stop the check early, for example if maintenance is needed on the bot.")
		for member in ctx.guild.members:
			await member.remove_roles(activeRole, closedRole, reason="Activity Check Starting...")
		await changeEmbedColor(myResponseMessage, 0x6cb83a)
		await sendEmbed(activityCheckChannel, "Activity Check", "Type `me`. Nothing More. Nothing Less. All messages are due within 1 day of this being sent. I will react with ✅ if it worked.", message="@everyone")
		timeout = time.time() + 60*60*24
		while time.time() <= timeout and not checkStopped:
			msg = None
			try:
				msg = await self.bot.wait_for("message", check=lambda msg : msg.channel == activityCheckChannel, timeout=5)
			except asyncio.TimeoutError:
				pass
			if msg != None and msg.content.lower() == "me":
				await msg.author.add_roles(activeRole, reason="Proven activity in the activity check, well done!")
				await msg.add_reaction('✅')
			elif msg != None and msg.content.lower() == "stop" and (msg.author == ctx.author or self.bot.is_owner(msg.author)):
				activityCheckChannels.remove(activityCheckChannel)
				await sendEmbed(msg.channel, "Activity Check Over", "This activity check has been ended early by "+str(msg.author), 0xaa0000)
				checkStopped = True
			elif msg != None and msg.content.lower() != "me" and msg.author != self.bot.user:
				await msg.delete()
		activityCheckChannels.remove(activityCheckChannel)
		if not shuttingDown:
			for member in ctx.guild.members:
				await member.add_roles(closedRole, reason="Activity Check Over, Well Done @active")
			await sendEmbed(activityCheckChannel, "Activity check complete", "well done @active")

def setup(bot):
	bot.add_cog(ActivityChecks(bot))
	
if __name__ == "__main__":
	print("Please run this cog as a discord bot")
