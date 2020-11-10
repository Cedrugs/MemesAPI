# MemesAPI

MemesAPI is a asynchronous python API to return a Memes from reddit returning a dictionary of url, author, upvote, and comments


## Requesting randomly generated memes

`GET` Method to get the memes

```python
from aiohttp import request
from asyncio import run

url = "https://dumboapi.herokuapp.com/getmeme"

async def getmeme():
    async with request("GET", url) as resp:
       data = await resp.json()
    print(print)

run(getmeme())
```

## Requesting a post from subreddit
`GET` Method to get the post
`subreddit` you can change the subreddit (aww) to custom subreddit such as DankMemes and etc.
```python
from aiohttp import ClientSession
from asyncio import run

url = "https://dumboapi.herokuapp.com/subreddit/aww"

async def getsubreddit():
    async with request("GET", url) as resp:
       data = await resp.json()
    print(print)
run(getmeme())
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
Created by the author of Dumbo discord bot (Cedrugs) or known as Cedric#4630 on discord.
[MIT](https://choosealicense.com/licenses/mit/)
