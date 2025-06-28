# Django Ecommerce

A modern, responsive ecommerce web application built with Django.  
Features include user authentication, product catalog, shopping cart, wishlist, order management, and more.

## Features

- User registration, login, and profile management
- Product catalog with categories and subcategories
- Product detail pages with image gallery and size selection
- Shopping cart with add, remove, and quantity adjustment
- Wishlist functionality
- Secure checkout and order placement
- Order history for users
- Responsive Bootstrap 5 UI

## Requirements

- Python 3.8+
- Django 4.x or 5.x
- Pillow (for image uploads)
- Bootstrap 5 (via CDN)
- [Optional] django-widget-tweaks (for form rendering)

## Setup

1. **Clone the repository**
    ```bash
    git clone https://github.com/furqann76/Lumi-So-ecommerce.git
    cd django-ecommerce
    ```

2. **Create and activate a virtual environment**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4. **Apply migrations**
    ```bash
    python manage.py migrate
    ```

5. **Create a superuser (admin)**
    ```bash
    python manage.py createsuperuser
    ```

6. **Run the development server**
    ```bash
    python manage.py runserver
    ```

7. **Access the site**
    - Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

## Project Structure

```
django-ecommerce/
├── manage.py
├── store/
│   ├── admin.py
│   ├── cart.py
│   ├── context_processors.py
│   ├── forms.py
│   ├── models.py
│   ├── templates/
│   ├── urls.py
│   ├── views.py
│   └── ...
├── static/
├── media/
└── requirements.txt
```

## Customization

- Add products, categories, and images via the Django admin panel.
- Update site branding and styles in `store/templates/store/base.html` and static files.

## License

This project is licensed under the MIT License.

---

**Happy selling!**
