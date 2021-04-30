from aiohttp import web

async def handle(request):
    text = 'Get'
    return web.Response(text=text)

app = web.Application()
app.add_routes([web.get('/', handle)])

if __name__ == '__main__':
    web.run_app(app)
