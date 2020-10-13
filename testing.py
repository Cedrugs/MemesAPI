from aiohttp import ClientSession
from asyncio import run
from json import loads

BASE = "http://localhost:8080/getmeme"

async def getmeme():
    async with ClientSession() as session:
        async with session.get(BASE) as resp:
            print(loads(await resp.read()))

run(getmeme())
