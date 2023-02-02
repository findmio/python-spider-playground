import asyncio
from base64 import b64encode
from functools import reduce

from session import get_session_id
import aiohttp

session_id = None


async def get_page_sum(page: int):
    url = f'https://match.yuanrenxue.com/api/match/12?page={page}&m={b64encode(f"yuanrenxue{page}".encode()).decode()}'
    headers = {
        "user-agent": "yuanrenxue.project",
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(
                url=url,
                headers=headers,
                cookies={
                    "sessionid": session_id
                }
        ) as response:
            result = await response.json()
            return reduce(lambda a, b: a + b['value'], result['data'], 0)


async def main():
    global session_id
    session_id = await get_session_id()
    datas = await asyncio.gather(*map(get_page_sum, range(1, 6)))
    return reduce(lambda a, b: a + b, datas)


if __name__ == '__main__':
    num_sum = asyncio.run(main())
    print(num_sum)
