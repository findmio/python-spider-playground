import asyncio
from functools import reduce
from bs4 import BeautifulSoup
import aiohttp


async def get_movie_names(page: int):
    url = f'https://ssr1.scrape.center/page/{page}'

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html = await response.text()
            soup = BeautifulSoup(html, 'lxml')
            names = list(map(lambda el: el.get_text(), soup.find_all(class_='m-b-sm')))
            return names


async def main():
    movie_list = await asyncio.gather(*map(get_movie_names, range(1, 11)))
    return reduce(lambda a, b: a + b, movie_list)


if __name__ == '__main__':
    movies = asyncio.run(main())
    print(movies)
