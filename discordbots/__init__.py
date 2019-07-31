import asyncio

# import whatever we want to run
import minibot

loop = asyncio.get_event_loop()

loop.create_task(minibot.setup())
