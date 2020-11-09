# MemesAPI

MemesAPI is a open API to return a Memes from reddit in a dict object.

## Requesting randomly generated memes

`GET` Method to get the memes

```python
from aiohttp import ClientSession
from asyncio import run

url = "https://dumboapi.herokuapp.com/getmeme"

async def getmeme():
    async with ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
    print(print)

run(getmeme())
```
`GET` Method to get the post

## Requesting a post from subreddit
`subreddit` you can change the subreddit to custom subreddit.
```python
from aiohttp import ClientSession
from asyncio import run

url = "https://dumboapi.herokuapp.com/subreddit/aww"

async def getmeme():
    async with ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
    print(data)

run(getmeme())
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
