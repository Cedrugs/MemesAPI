from aiohttp import web, request as req, ClientSession
from random import choice, randint
from dadjokes import dadjoke
import json
import os

routes = web.RouteTableDef()

subreddit = ['memes', 'dankmemes', 'funny']

HEADERS = {
    'User-Agent' : "Dumbo"
}

def list_or_reddit():
    number = randint(0, 5)
    if number >= 3:
        return True
    return False

async def getmeme():
    async with req("GET", f"https://www.reddit.com/r/{choice(subreddit)}/new.json?limit=50", headers=HEADERS) as resp:
        data = await resp.json()
        randomizer = randint(0, 49)
        link_data = data['data']['children'][randomizer]['data']['url_overridden_by_dest']
        title_data = data['data']['children'][randomizer]['data']['title']
        score_data = data['data']['children'][randomizer]['data']['score']
        submission = data['data']['children'][randomizer]['data']['subreddit_name_prefixed']
        meme_data = {'image': f'{link_data}', 'title': f'{title_data}', 'score': f'{score_data}', 'subreddit': f'{submission}'}
        return meme_data

async def custom_subreddit(chosen_subreddit):
    async with req("GET", f"https://www.reddit.com/r/{chosen_subreddit}/new.json?limit=100", headers=HEADERS) as resp:
        data = await resp.json()
        try:
            subreddit_url = data['data']['children'][2]['data']['url_overridden_by_dest']
            subreddit_title = data['data']['children'][2]['data']['title']
            subreddit_score = data['data']['children'][2]['data']['score']
            submission_name = data['data']['children'][2]['data']['subreddit_name_prefixed']
            subreddit_data = {'image': f'{subreddit_url}', 'title': f'{subreddit_title}', 'score': f'{subreddit_score}', 'subreddit': f'{submission_name}'}
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
    try:
        response = await custom_subreddit(selected)
        if response is None:
            error = {"error": f"{selected} sub is not available!", "status": 404}
            return web.Response(text=json.dumps(error), status=404)
        return web.Response(text=json.dumps(response), status=200)
    except KeyError:
        key_error = {"error": f"There's a problem while trying to connect to {selected}. Pleasse try again later."}
        return web.Response(text=json.dumps(key_error), status=403)

@routes.get('/dadjoke')
async def handle(request):
    if list_or_reddit():
        async with ClientSession() as session:
            async with session.get("https://www.reddit.com/r/dadjokes/new.json?limit=50") as resp:
                data = await resp.json()
            randomizer = randint(0, 49)
            setup = data['data']['children'][randomizer]['data']['title']
            punchline = data['data']['children'][randomizer]['data']['selftext']
    else:
        randomizer = randint(0, 10)
        setup = dadjoke[randomizer]['setup']
        punchline = dadjoke[randomizer]['punchline']
    return web.Response(text=json.dumps({'setup': f'{setup}', 'punchline': f'{punchline}'}), status=200)

@routes.get('/')
async def handle(request):
    return web.Response(text="""Welcome to Dumbo Memes API! 
You can view a dadjokes, randomly generated meme, random subreddit memes!
[GET] /dadjoke
[GET] /subreddit/{subreddit}
[GET] /getmeme
    """)


async def initialize():
    app = web.Application()
    app.add_routes(routes)
    return app


port=int(os.environ.get("PORT", "8080"))
web.run_app(initialize(), port=port)
