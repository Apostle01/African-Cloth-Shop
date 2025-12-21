# 🧵 African-Cloth-Shop
# https://apostle01.github.io/African-Cloth-Shop/
# https://github.com/Apostle01/African-Cloth-Shop.git

A **Django-powered e-commerce platform** for selling authentic African cloth and fashion products.  
The project supports product management, shopping cart, checkout, payments, and order management with room for future scalability.

---

## 📌 Project Overview

**African-Cloth-Shop** is designed to help small and medium fashion businesses sell African textiles online.  
It provides a clean customer experience and a powerful Django Admin backend for store owners.

---

## ✨ Features

### 🛍️ Storefront
- Product listings with images
- Category-based product filtering
- Product detail pages
- Search functionality
- Responsive Bootstrap UI (Bootstrap 4)

### 🛒 Cart & Checkout
- Add/remove products from cart
- Cart summary page
- Checkout flow
- Guest & authenticated checkout support
- Persistent cart using sessions

### 💳 Payments
- Stripe payment integration
- Secure payment handling
- Payment success confirmation
- Order creation after payment

### 📦 Orders
- Order creation and storage
- Order status tracking:
  - Processing
  - Shipped
  - Delivered
- Admin-managed order updates
- Automatic order status emails

### 📊 Admin Features
- Django Admin dashboard
- Product & category management
- Order management
- Stock quantity tracking
- Sales history (foundation in place)

### 📧 Email Notifications
- Order confirmation emails
- Shipping notification emails
- Delivery confirmation emails

---

## 🧰 Tech Stack

- **Backend:** Django 5.x
- **Frontend:** HTML, CSS, Bootstrap 4
- **Database:** SQLite (development)
- **Payments:** Stripe
- **Email:** SMTP (Gmail supported)
- **Storage:** Django Media Files

---

## 📂 Project Structure

shop/
├── cart/
├── payment/
├── products/
├── templates/
├── static/
├── media/
├── shop/
│ ├── settings.py
│ ├── urls.py
│ └── wsgi.py
├── manage.py

yaml
Copy code

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/Apostle01/African-Cloth-Shop.git
cd African-Cloth-Shop
2️⃣ Create Virtual Environment
bash
Copy code
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
3️⃣ Install Dependencies
bash
Copy code
pip install -r requirements.txt
4️⃣ Apply Migrations
bash
Copy code
python manage.py makemigrations
python manage.py migrate
5️⃣ Create Superuser
bash
Copy code
python manage.py createsuperuser
6️⃣ Run Development Server
bash
Copy code
python manage.py runserver
Visit:
👉 http://127.0.0.1:8000/

🔑 Environment Variables (Recommended)
Create a .env file for sensitive keys:

env
Copy code
SECRET_KEY=your_django_secret_key
STRIPE_PUBLIC_KEY=your_stripe_public_key
STRIPE_SECRET_KEY=your_stripe_secret_key
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
🖼️ Media Files
Product images are stored in the /media/ directory

Ensure MEDIA_URL and MEDIA_ROOT are set in settings.py

🚀 Future Enhancements
Sales analytics dashboard

Refund handling

Webhook-based payment verification

PDF invoices

Order tracking numbers

Wishlist feature

REST API (Django REST Framework)

Deployment (Railway / Render / AWS)

🤝 Contributing
Contributions are welcome!

Fork the repository

Create a feature branch

Commit your changes

Submit a pull request

📜 License
This project is licensed under the MIT License.

👤 Author
Apostle01
GitHub: https://github.com/Apostle01

⭐ If you like this project, give it a star and share it!
