import aiohttp
from django.conf import settings

VK_API_TOKEN = settings.VK_API_TOKEN
VK_API_BASE_URL = "https://api.vk.com/method"


async def get_clicks_count(link):
    """
    Получение количества переходов через VK API.
    """
    async with aiohttp.ClientSession() as session:
        short_key = link.split("/")[-1]

        params = {
            "access_token": VK_API_TOKEN,
            "v": "5.131",
            "key": short_key,
        }

        async with session.get(f"{VK_API_BASE_URL}/utils.getLinkStats",
                               params=params) as response:
            data = await response.json()

            if "response" in data:
                return data["response"]["stats"][-1]["views"]
            else:
                return 0
