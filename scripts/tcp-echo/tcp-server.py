from aiohttp import web

routes = web.RouteTableDef()

@routes.get('/tcp')
async def handle(request):
    text = 'Get'
    return web.Response(text=text)

@routes.post('/tcp')
async def handle(request):
    text = 'Post'
    return web.Response(text=text)



if __name__ == "__main__":
    # app.secret_key = 'super secret key'
    # app.config['SESSION_TYPE'] = 'filesystem'
    # app.run(port=5000,host='0.0
    app = web.Application()
    app.add_routes(routes)
    web.run_app(app, path='0.0.0.0', port=8080)
