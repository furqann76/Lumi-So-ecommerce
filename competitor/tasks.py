from celery import shared_task
from competitor.models import CompetitorProduct
from competitor.utils.scraper import scrape_price_from_url


@shared_task
def update_competitor_prices():
    for comp in CompetitorProduct.objects.all():
        selector = ".price"  # Update as per competitor site
        price = scrape_price_from_url(comp.competitor_url, selector)

        if price:
            comp.latest_price = price
            comp.save()
            comp.your_product.apply_competitor_price(price)
            print(f"✅ Updated {comp.name} to Rs {price}")
        else:
            print(f"❌ Failed to get price for {comp.name}")
