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
            "interval": "day",
        }

        try:
            async with session.get(f"{VK_API_BASE_URL}/utils.getLinkStats",
                                   params=params) as response:
                data = await response.json()
                print(data)

                stats = data.get("response", {}).get("stats", [])

                if not stats:
                    return 0  # Если stats пустой, возвращаем 0

                return stats[-1].get("views", 0)
        except aiohttp.ClientError as e:
            print(f"Ошибка при запросе к VK API: {e}")
            return 0
        except Exception as e:
            print(f"Неожиданная ошибка: {e}")
            return 0
