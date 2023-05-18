import asyncio
import os
from functools import reduce
import execjs

from session import get_session_id
import aiohttp

session_id = None
lib_path = os.path.join(os.path.dirname(__file__), '1.js')


async def get_page_sum(page: int):
    m = execjs.compile(open(lib_path).read()).call('get_m')
    url = f'https://match.yuanrenxue.com/api/match/1?page={page}&m={m}'
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
    print(num_sum / 50)
