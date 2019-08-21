from discord.ext import commands
import asyncio
import os

extensions = [
  "discordbots.activitycheck.main",
	"discordbots.activitycheck.spy" # spying on the chromebook777 productions server and reporting back to the website. It's nothing bad- promise.
]
async def setup():
  try:
    bot = commands.Bot(command_prefix="&")
    for extension in extensions:
      try:
        bot.load_extension(extension)
      except Exception as e:
        print("Failed to load "+str(extension)+"... \n>>> Full traceback is "+str(e))
    await bot.start(os.environ["ACTIVITY_CHECK_TOKEN"])
  except Exception as e:
    print("Running ActivityCheck failed... \n>>> Full traceback is "+str(e))
  

loop = asyncio.get_event_loop()

loop.create_task(setup())
