from django.core.management.base import BaseCommand
from core.models import AdLink
from core.utils import get_clicks_count
from asgiref.sync import sync_to_async


class Command(BaseCommand):
    help = "Обновление количества переходов по рекламным ссылкам"

    def handle(self, *args, **kwargs):
        import asyncio
        asyncio.run(self.update_clicks())

    async def update_clicks(self):
        ad_links = await sync_to_async(list)(AdLink.objects.all())

        for ad_link in ad_links:
            clicks = await get_clicks_count(ad_link.link)
            ad_link.clicks_count = clicks
            await sync_to_async(ad_link.save)()

        self.stdout.write(self.style.SUCCESS('Статистика успешно обновлена'))
