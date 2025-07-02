from django.core.management.base import BaseCommand
from competitor.models import CompetitorProduct
from competitor.utils.scraper import scrape_price_from_url


class Command(BaseCommand):
    help = "Scrapes competitor prices and updates your product prices"

    def handle(self, *args, **kwargs):
        for comp in CompetitorProduct.objects.all():
            # 👇 Customize CSS selector for each website
            selector = ".price"  # You must inspect element on competitor site to get correct class
            price = scrape_price_from_url(comp.competitor_url, selector)

            if price:
                comp.latest_price = price
                comp.save()

                # Adjust your own product price
                comp.your_product.apply_competitor_price(price)

                self.stdout.write(f"✅ Updated {comp.name} to Rs {price}")
            else:
                self.stdout.write(f"❌ Failed to get price for {comp.name}")
