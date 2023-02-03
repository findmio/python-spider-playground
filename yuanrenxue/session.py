import os

import aiohttp
from dotenv import load_dotenv

load_dotenv()

username = os.environ.get("YRX_USERNAME")
password = os.environ.get("YRX_PASSWORD")


async def get_session_id():
    async with aiohttp.ClientSession() as session:
        async with session.post('https://match.yuanrenxue.com/api/login', data={
            "username": username,
            "password": password,
        }) as response:
            cookie_str = list(filter(lambda s: 'sessionid' in s, response.headers.getall('Set-Cookie')))[0]
            session_str = list(filter(lambda s: 'sessionid' in s, cookie_str.split(';')))[0]
            return session_str.split('=')[-1]
