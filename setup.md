# Local Setup

Steps to run Lumi&So locally: the Django site, Celery (cart-recovery emails + competitor pricing), and the FastAPI RAG chatbot. Skip the sections marked *(optional)* if you only need the storefront/admin.

## Prerequisites

- Python 3.12 (project was developed and tested against it; newer versions may hit ML-dependency wheel issues)
- Redis — *(optional, only for Celery)*
- [Ollama](https://ollama.com) with the `llama3` model pulled — *(optional, only for AI description generation and the chatbot)*

## 1. Virtual environment

```bash
python3.12 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

`requirements.txt` includes the heavy ML stack (torch, sentence-transformers, faiss-cpu) needed for the chatbot service — installing it fully can take several minutes.

## 2. Environment variables

Create a `.env` file in the project root (gitignored). `settings.py` reads these via `python-decouple` and **fails to start without them**:

```
EMAIL_HOST_USER=your-gmail-address@gmail.com
EMAIL_HOST_PASSWORD=your-gmail-app-password
```

For local dev where you don't need real emails to send, any placeholder values work — the server will boot fine and email-sending tasks will just fail silently.

## 3. Database

```bash
python manage.py migrate
python manage.py createsuperuser
```

Uses SQLite (`db.sqlite3`) by default, no extra setup needed.

## 4. Static files directory

`STATICFILES_DIRS` points at a top-level `static/` folder that isn't in version control:

```bash
mkdir -p static
```

## 5. Run the Django site

```bash
python manage.py runserver 127.0.0.1:8000
```

- Storefront: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

## 6. Celery worker + beat *(optional — cart-recovery emails, competitor pricing)*

Requires Redis running (`redis-server`, default `redis://localhost:6379/0`):

```bash
celery -A ecommerce worker --loglevel=info
celery -A ecommerce beat --loglevel=info   # separate terminal; runs the scheduled tasks
```

Registered tasks: `store.tasks.send_order_confirmation_email`, `store.tasks.send_cart_recovery_emails` (runs every 2 minutes via beat), `competitor.tasks.update_competitor_prices`.

## 7. AI features *(optional)*

Both AI features call a local Ollama instance at `http://localhost:11434`:

```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3
ollama serve      # or `ollama run llama3`; leave running
```

- **Admin product-description generation** — works automatically once Ollama is running: saving a `Product` in the admin with no description triggers `store/utils.py:generate_product_description`.
- **Storefront chatbot** (RAG over `LumiSo_FAQ_and_Policies.pdf`) — a separate FastAPI service, not started by `manage.py`:

  ```bash
  uvicorn store.main:app --port 8001
  ```

  The chat widget in `store/templates/store/base.html` calls `http://127.0.0.1:8001/ask` directly from the browser.

## Notes / known gaps

- `django-celery-beat` and `beautifulsoup4` are required (`INSTALLED_APPS` / `competitor/utils/scraper.py`) and are pinned in `requirements.txt`, but weren't in earlier versions of this file — if you're on an older lockfile and hit `ModuleNotFoundError`, `pip install django-celery-beat beautifulsoup4`.
- The competitor-pricing scraper (`competitor/utils/scraper.py`) expects a `.price` CSS selector on the competitor's page — update `competitor/tasks.py` if a tracked site uses a different one.
