from aiohttp import web, request, ClientSession
from random import choice, randint
import json

routes = web.RouteTableDef()

subreddit = ['memes', 'dankmemes', 'funny']

HEADERS = {
    'User-Agent' : "Dumbo"
}
async def getmeme():
    async with request("GET", f"https://www.reddit.com/r/{choice(subreddit)}/new.json?limit=100", headers=HEADERS) as resp:
        data = await resp.json()
        link_data = data['data']['children'][2]['data']['url_overridden_by_dest']
        title_data = data['data']['children'][2]['data']['title']
        score_data = data['data']['children'][2]['data']['score']
        submission = data['data']['children'][2]['data']['subreddit_name_prefixed']
        meme_data = {'image': f'{link_data}', 'title': f'{title_data}', 'score': f'{score_data}', 'subreddit': f'{submission}'}
        return meme_data

async def custom_subreddit(chosen_subreddit):
    print(chosen_subreddit)
    async with request("GET", f"https://www.reddit.com/r/{chosen_subreddit}/new.json?limit=100", headers=HEADERS) as resp:
        data = await resp.json()
        try:
            subreddit_url = data['data']['children'][2]['data']['url_overridden_by_dest']
            subreddit_title = data['data']['children'][2]['data']['title']
            subreddit_title = data['data']['children'][2]['data']['score']
            submission_name = data['data']['children'][2]['data']['subreddit_name_prefixed']
            subreddit_data = {'image': f'{subreddit_url}', 'title': f'{subreddit_title}', 'score': f'{subreddit_title}', 'subreddit': f'{submission_name}'}
        except IndexError:
            subreddit_data = None
        return subreddit_data

@routes.get('/getmeme')
async def handle(request):
    response = await getmeme()
    return web.Response(text=json.dumps(response))

@routes.get('/subreddit/{subreddit}')
async def handle(request):
    selected = request.match_info.get('subreddit', '')
    response = await custom_subreddit(selected)
    if response is None:
        error = {"error": f"{selected} sub is not available!", "status": 404}
        return web.Response(text=json.dumps(error), status=404)
    return web.Response(text=json.dumps(response), status=200)

@routes.get('/dadjoke')
async def handle(request):
    async with ClientSession() as session:
        async with session.get("https://www.reddit.com/r/dadjokes/new.json?limit=100") as resp:
            data = await resp.json()
        dadjoke_data = data['data']['children'][randint(0, 5)]['data']['selftext']
    return web.Response(text=json.dumps({'jokes': f'{dadjoke_data}'}), status=200)


async def initialize():
    app = web.Application()
    app.add_routes(routes)
    return app

web.run_app(initialize())
