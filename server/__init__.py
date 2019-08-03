from aiohttp import web
import asyncio
import aiohttp_jinja2
import os

## Define middlewares
def create_error_middleware(overrides):
    @web.middleware
    async def error_middleware(request, handler):
        try:
            response = await handler(request)
            override = overrides.get(response.status)
            if override:
                return await override(request)
            return response
        except web.HTTPException as ex:
            override = overrides.get(ex.status)
            if override:
                return await override(request)
            raise
    return error_middleware

## Define routes
routes = web.RouteTableDef()

@routes.get('')
async def hello(request):
    return web.Response(text="Hello, world")


@routes.get('/uptime_test')
async def uptimetest(request):
    return web.Response(text="I'm Up!!!")

## Define handle functions
async def handle_404(request):
    return aiohttp_jinja2.render_template('server/public/404.html', request, {})
async def handle_500(request):
    return aiohttp_jinja2.render_template('server/public/500.html', request, {})

app = web.Application()

app.add_routes(routes)
error_middleware = create_error_middleware({
    404: handle_404,
    500: handle_500
})
app.middlewares.append(error_middleware)

async def setup():
    asyncio.get_event_loop().create_task(web._run_app(app, path="localhost", port=os.environ["PORT"]))
    
loop = asyncio.get_event_loop()

loop.create_task(setup())
