# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Lumi&So — a Django 5.2 ecommerce platform (fashion/lifestyle) with a modular `store` app, a `competitor` pricing app, Celery/Redis for background jobs, and a separate FastAPI microservice for an AI/RAG chatbot.

## Commands

```bash
# Environment
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Django dev server
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver              # http://127.0.0.1:8000/ (admin at /admin/)

# Tests (Django's test runner; store/tests.py and competitor/tests.py are currently stubs)
python manage.py test
python manage.py test store
python manage.py test store.tests.SomeTestClass.test_method   # single test

# Background workers (required for cart recovery emails, competitor price scraping)
sudo systemctl start redis-server
celery -A ecommerce worker --loglevel=info
celery -A ecommerce beat --loglevel=info    # scheduled tasks (uses django_celery_beat DatabaseScheduler)

# RAG chatbot microservice (separate process, FastAPI, not managed by manage.py)
uvicorn store.main:app --port 8001          # frontend fetches http://127.0.0.1:8001/ask (see base.html)

# Local LLM for AI description generation / chatbot (optional)
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3
ollama run llama3                           # exposes http://localhost:11434/api/generate
```

Secrets (`EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`) are read via `python-decouple` from a `.env` file (gitignored) — required for `runserver` to start without erroring, since `settings.py` reads them at import time.

## Architecture

**Two Django apps + one standalone FastAPI service, tied together by Celery:**

- `ecommerce/` — Django project root: `settings.py`, root `urls.py` (mounts `store.urls` at `/`, admin at `/admin/`), `celery.py` (defines the Celery app and the `send-cart-recovery-every-2-mins` beat schedule).
- `store/` — the main ecommerce app, organized as sub-packages rather than single files:
  - `models/` — split by domain: `product.py`, `category.py`, `order.py`, `customer.py`, `wishlist.py`, `abandoned_cart.py`, `theme.py`. All re-exported through `models/__init__.py`.
  - `views/` — split by feature (`auth`, `product`, `cart`, `profile`, `wishlist`, `order`, `checkout`), all re-exported (`from .x import *`) through `views/__init__.py` so `store/urls.py` can do `from . import views` and reference any view flatly.
  - `forms/` — same pattern, split by feature and re-exported via `forms/__init__.py`.
  - `cart.py` — session-based `Cart` class (not a model); cart contents live in `request.session["cart"]` as `{product_id: {quantity, size}}`.
  - `middleware.py` — `AbandonedCartMiddleware` runs on every request for authenticated users and upserts an `AbandonedCart` row from the current session cart; this is what the Celery beat task (`store.tasks.send_cart_recovery_emails`) later emails out.
  - `context_processors.py` — injects `nav_categories` (for the nav menu) and `current_theme` (the single active `SiteTheme`) into every template's context; registered in `settings.TEMPLATES`.
  - `utils.py` — `generate_product_description()` (streams a prompt to the local Ollama/LLaMA API at `localhost:11434`, used from `ProductAdmin.save_model` when an admin saves a product with no description) and `get_ai_related_products()` (TF-IDF/cosine-similarity based "related products", not an LLM call).
  - `main.py` — a **separate FastAPI app**, not wired into Django at all. Loads `LumiSo_FAQ_and_Policies.pdf`, chunks it, embeds chunks with `sentence-transformers`, indexes them with FAISS, and serves `POST /ask` (RAG: retrieve top-3 chunks, then complete via local LLaMA/Ollama). The storefront chatbot widget in `store/templates/store/base.html` calls this service directly over HTTP (`http://127.0.0.1:8001/ask`), bypassing Django entirely — it must be started separately (see Commands).
  - `tasks.py` — Celery tasks: `send_order_confirmation_email`, `send_cart_recovery_emails` (queries `AbandonedCart` rows older than 4 minutes and not yet emailed).
- `competitor/` — automated competitor price tracking, added for the admin. `CompetitorProduct` links a scraped competitor listing to a `store.Product`; `utils/scraper.py` scrapes a price by CSS selector; the Celery task `update_competitor_prices` (`competitor/tasks.py`) refreshes `latest_price` for every tracked competitor product and calls `Product.apply_competitor_price()` to auto-undercut it by 5%. Managed from Django admin via `CompetitorProductAdmin`.

**Request flow for AI features:** the Django admin's "save product" path and the storefront chatbot use two different AI backends — admin description generation goes through Django → `store/utils.py` → Ollama directly; the chatbot goes browser → FastAPI (`store/main.py`) → Ollama, with Django never in the loop for that request.

**Theming:** `SiteTheme` model plus the `activate_theme` admin action enforce "only one active theme at a time"; `current_theme` context processor exposes the active theme name to templates for conditional styling.
