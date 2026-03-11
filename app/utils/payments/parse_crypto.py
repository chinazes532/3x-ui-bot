import aiohttp


async def get_course_crypto(asset_pay):
    url = f'https://api.coingecko.com/api/v3/simple/price?ids={asset_pay}&vs_currencies=rub'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            return data[asset_pay]['rub']