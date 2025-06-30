# Lumi&So

Lumi&So is a modern, scalable Django-based ecommerce platform designed for fashion and lifestyle brands. It features a clean, responsive UI, robust product catalog, advanced filtering, user authentication, wishlist, cart, and order management. The project is organized for maintainability and growth, using a modular directory structure.

---

## Features

- **User Authentication:** Register, login, logout, profile management, and profile editing.
- **Product Catalog:** Categories, subcategories, product detail pages, and image galleries.
- **Advanced Filtering:** Filter products by availability, price range, and sort by newest or price.
- **Shopping Cart:** Add, remove, and update product quantities; persistent cart per user/session.
- **Wishlist:** Save favorite products for later.
- **Order Management:** Secure checkout, order history, and order success pages.
- **Responsive Design:** Built with Bootstrap 5 for mobile and desktop.
- **Scalable Codebase:** Modular structure for models, views, and forms.
- **Admin Panel:** Manage products, categories, orders, and users via Django admin.

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
│   │       └── partials/
│   │           └── breadcrumb.html
│   ├── static/
│   ├── urls.py
│   └── ...
├── static/
├── media/
├── requirements.txt
└── README.md
```

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/furqann76/Lumi-So-ecommerce.git
cd Lumi-So-ecommerce
```

### 2. Create and Activate a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply Migrations

```bash
python manage.py migrate
```

### 5. Create a Superuser

```bash
python manage.py createsuperuser
```

### 6. Run the Development Server

```bash
python manage.py runserver
```

### 7. Access the Site

- Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

---

## Customization

- **Branding:** Update `base.html` and static files for your brand’s look and feel.
- **Products & Categories:** Use the Django admin panel to add/edit products, categories, and subcategories.
- **Context Processors:** Use `context_processors.py` to inject global data (like categories and cart) into all templates.
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

**Lumi&So — Modern Ecommerce, Beautifully Crafted with Django**
