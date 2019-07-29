import asyncio

# import whatever we want to run
import server
#import discordbots

loop = asyncio.get_event_loop()

loop.create_task(server.setup())
loop.run_forever()
