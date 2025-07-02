# Lumi&So

Lumi&So is a modern, scalable Django-based ecommerce platform designed for fashion and lifestyle brands. It features a clean, responsive UI, robust product catalog, advanced filtering, user authentication, wishlist, cart, order management, AI-powered tools, and email notifications (including cart recovery). The project is organized for maintainability and growth, using a modular directory structure.

---

## Features

- **User Authentication:** Register, login, logout, profile management, and profile editing.
- **Product Catalog:** Categories, subcategories, product detail pages, and image galleries.
- **Advanced Filtering:** Filter products by availability, price range, and sort by newest or price.
- **Shopping Cart:** Add, remove, and update product quantities; persistent cart per user/session.
- **Wishlist:** Save favorite products for later.
- **Order Management:** Secure checkout, order history, and order success pages.
- **Cart Recovery Emails:** Automated emails to remind users about abandoned carts.
- **AI Tools:** Product description generation and chatbot support.
- **Responsive Design:** Built with Bootstrap 5 for mobile and desktop.
- **Scalable Codebase:** Modular structure for models, views, and forms.
- **Admin Panel:** Manage products, categories, orders, and users via Django admin.

---

## AI Tools

Lumi&So integrates AI-powered features to enhance both admin and customer experience:

- **AI Product Description Generator:**  
  In the Django admin, generate engaging product descriptions with a single click using integrated AI (LLaMA or OpenAI backend).
- **Chatbot Support:(RAG)**  
  A chatbot widget is available on the storefront, answering customer queries using AI.
- **How it works:**  
  - The backend exposes endpoints (e.g., `/generate-description/`, `/ask/`) that interact with your AI service.
  - You can run your own AI microservice (Flask/FastAPI) or connect to OpenAI, LLaMA, or similar APIs.

---

## Directory Structure

```
lumiandso/
├── manage.py
├── store/
│   ├── admin.py
│   ├── apps.py
│   ├── cart.py
│   ├── context_processors.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── category.py
│   │   ├── product.py
│   │   ├── order.py
│   │   ├── customer.py
│   │   └── wishlist.py
│   ├── views/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── cart.py
│   │   ├── checkout.py
│   │   ├── product.py
│   │   ├── profile.py
│   │   ├── wishlist.py
│   │   └── order.py
│   ├── forms/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── checkout.py
│   │   ├── profile.py
│   │   └── product.py
│   ├── templates/
│   │   └── store/
│   │       ├── base.html
│   │       ├── home.html
│   │       ├── product_detail.html
│   │       ├── subcategory_products.html
│   │       ├── cart.html
│   │       ├── wishlist.html
│   │       ├── profile.html
│   │       ├── edit_profile.html
│   │       ├── register.html
│   │       ├── login.html
│   │       ├── order_success.html
│   │       ├── emails/
│   │       │   └── cart_recovery.html
│   │       └── partials/
│   │           └── breadcrumb.html
│   ├── static/
│   │   └── store/
│   │       ├── style.css
│   │       └── ...
│   ├── urls.py
│   └── ...
├── static/
├── media/
├── requirements.txt
└── README.md
```

---

## Setup Instructions

```bash
# 1. Clone the Repository
git clone https://github.com/furqann76/Lumi-So-ecommerce.git
cd Lumi-So-ecommerce

# 2. Create and Activate a Virtual Environment
python3 -m venv venv
source venv/bin/activate

# 3. Install Dependencies
pip install -r requirements.txt

# 4. Apply Migrations
python manage.py migrate

# 5. Create a Superuser
python manage.py createsuperuser

# 6. Run the Development Server
python manage.py runserver

# 7(optional). If you want to use llama for AI description generator
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3
ollama run llama3
```

- Access the site at [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- Access the admin panel at [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## Running Background Services

Lumi&So uses Celery and Redis for background tasks (e.g., sending cart recovery emails, AI requests):

```bash
# Start Redis server (if not already running)
sudo systemctl start redis-server

# Start Celery worker (in your project directory)
celery -A ecommerce worker --loglevel=info

# (Optional) Start Celery beat for scheduled tasks
celery -A ecommerce beat --loglevel=info

```

---

## Customization

- **Branding:** Update `base.html` and static files (like `static/store/style.css`) for your brand’s look and feel.
- **Products & Categories:** Use the Django admin panel to add/edit products, categories, and subcategories.
- **Context Processors:** Use `context_processors.py` to inject global data (like categories and cart) into all templates.
- **Cart Recovery Emails:** Customize the email template at `store/templates/store/emails/cart_recovery.html`.
- **AI Endpoints:** Adjust `/generate-description/` and `/ask/` endpoints to connect to your preferred AI backend.
- **Modular Code:** Add new features by creating new modules in `models/`, `views/`, and `forms/`.

---

## Contributing

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -am 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a pull request.

---

## License

This project is licensed under the MIT License.

---

**Lumi&So — Modern Ecommerce, Beautifully Crafted with Django and AI**