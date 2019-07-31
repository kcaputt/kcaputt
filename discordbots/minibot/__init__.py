from discord.ext import commands
import asyncio
import os

extensions = [
  "discordbots.minibot.tea"
]
async def setup():
  try:
    bot = commands.Bot(command_prefix="mini")
    for extension in extensions:
      try:
        bot.load_extension(extension)
      except Exception as e:
        print("Failed to load "+str(extension)+"... \n>>> Full traceback is "+str(e))
    await bot.start(os.environ["MINIBOT_TOKEN"])
  except Exception as e:
    print("Running MiniBot failed... \n>>> Full traceback is "+str(e))
  

loop = asyncio.get_event_loop()

loop.create_task(setup())
