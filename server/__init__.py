from aiohttp import web
import asyncio
import os

routes = web.RouteTableDef()

@routes.get('')
async def hello(request):
    return web.Response(text="Hello, world")

app = web.Application()
app.add_routes(routes)

async def setup():
    asyncio.get_event_loop().create_task(web._run_app(app, path="localhost", port=os.environ["PORT"]))
    
loop = asyncio.get_event_loop()

loop.create_task(setup())
