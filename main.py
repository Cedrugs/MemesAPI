from aiohttp import web, request as req, ClientSession
from random import choice, randint
from dadjokes import dadjoke
import os

routes = web.RouteTableDef()

subreddit = ['memes', 'dankmemes', 'funny']
updates = ['hot', 'new']


def list_or_reddit():
    number = randint(0, 5)
    if number >= 3:
        return True
    return False


async def getmeme():
    async with req("GET", f"https://www.reddit.com/r/{choice(subreddit)}/{choice(updates)}.json?limit=50") as resp:
        data = await resp.json()
        memes = [x for x in data['data']['children'] if x['data']['is_video'] is not True]
        randomizer = randint(0, 20)
        try:
            url = memes[randomizer]['data']['url_overridden_by_dest']
        except KeyError:
            url = memes[randomizer]['data']['url']
        title = memes[randomizer]['data']['title']
        score = memes[randomizer]['data']['score']
        submission = memes[randomizer]['data']['subreddit_name_prefixed']
        author = memes[randomizer]['data']['author']
        returning = {'image': f'{url}', 'title': f'{title}', 'score': f'{score}', 'subreddit': f'{submission}',
                     'author': f'{author}'}
        return returning


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
    if response is None:
        return web.json_response(data={"error": "there's a error while getting memes from reddit."})
    else:
        return web.json_response(data=response, status=200)


@routes.get('/subreddit')
async def handle(request):
    response = {"error": "You must input a subreddit"}
    return web.json_response(data=response)


@routes.get('/subreddit/{subreddit}')
async def handle(request):
    selected = request.match_info.get('subreddit', '')
    try:
        response = await custom_subreddit(selected)
        if response is None:
            error = {"error": f"{selected} sub is not available!", "status": 404}
            return web.json_response(data=error, status=404)
        return web.json_response(data=response, status=200)
    except KeyError:
        key_error = {"error": f"There's a problem while trying to connect to {selected}. Pleasse try again later."}
        return web.json_response(data=key_error, status=403)


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
    final = {'setup': f'{setup}', 'punchline': f'{punchline}'}
    return web.json_response(data=final, status=200)


@routes.get('/')
@routes.get('/home')
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


port = int(os.environ.get("PORT", "8080"))
web.run_app(initialize(), port=port)
