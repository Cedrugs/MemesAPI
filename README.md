# Foobar

MemesAPI is a open API to return a Memes from reddit in a dict object.

## Requesting randomly generated memes

`GET` Method to get the memes

```python
from aiohttp import ClientSession
from asyncio import run
from json import loads

url = "http://localhost:8080/getmeme"

async def getmeme():
    async with ClientSession() as session:
        async with session.get(url) as resp:
            print(loads(await resp.read()))

run(getmeme())
```
`GET` Method to get the post

`subreddit` Change aww into a custom subreddit

## Requesting a post from subreddit

```python
from aiohttp import ClientSession
from asyncio import run
from json import loads

url = "http://localhost:8080/subreddit/aww"

async def getmeme():
    async with ClientSession() as session:
        async with session.get(url) as resp:
            print(loads(await resp.read()))

run(getmeme())
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
