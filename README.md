# 🧵 African-Cloth-Shop
# https://apostle01.github.io/African-Cloth-Shop/
# https://github.com/Apostle01/African-Cloth-Shop.git

A **Django-powered e-commerce platform** for selling authentic African cloth and fashion products.  
The project supports product management, shopping cart, checkout, payments, and order management with room for future scalability.

# Repository: African Cloth Shop on GitHub

---

## Project Overview

**African-Cloth-Shop** is an e-commerce website designed for customers who want to browse and purchase African cloth products online.

The website allows customers to browse products, search for items, add products to a shopping cart and proceed through checkout. Customers can also create accounts, view their orders and leave reviews on products.

The project also includes a Django administration area where authorised staff can manage products, categories, stock, orders and customer reviews.

The main aim of the project was to build a practical online shop that is easy to use while providing the basic features needed to manage an e-commerce business.

### User Experience (UX)

The design of the website was planned around two main groups of users:

Customers

Customers should be able to:

Browse products easily
Find products using categories and search
View product information and prices
Add products to their shopping cart
Change quantities or remove products
Complete the checkout process
Make payments securely
View orders
Leave product reviews
Store Administrators

Administrators should be able to:

Add and edit products
Manage product categories
Update stock levels
Manage customer orders
Update order statuses
View customer reviews
Manage other store information through Django Admin

## User Stories

The following user stories were used to help guide the design and development of the website.

Customer
As a customer, I want to browse African cloth products so that I can find something I want to buy.
As a customer, I want to search for products so that I can find products quickly.
As a customer, I want to view product details so that I can make an informed purchase.
As a customer, I want to add products to my cart so that I can purchase them.
As a customer, I want to change product quantities so that I can order the amount I need.
As a customer, I want to remove products from my cart if I change my mind.
As a customer, I want to pay securely so that I can complete my order safely.
As a customer, I want to view my previous orders so that I can keep track of my purchases.
As a customer, I want to leave reviews so that I can share my experience with other customers.

Administrator
As an administrator, I want to add and edit products so that the catalogue remains up to date.
As an administrator, I want to manage stock so that customers cannot order unavailable products.
As an administrator, I want to manage orders so that purchases can be processed.
As an administrator, I want to view reviews so that customer feedback can be monitored.

### Design Process

The website design was developed before and during implementation. The following design work was used to plan the appearance, structure and responsiveness of the website.

1. Wireframes

Wireframes were created to plan the main pages before finalising the interface.

The main pages considered were:

Home page
Product listing page (with Categories)
Product detail page
Shopping cart
Checkout
Login
Registration
Order history
Product review section
Admin interface

### 2. Colour Scheme
The colour scheme was selected to complement the African textile theme while keeping text and controls easy to read.

### Typography
- I kept fonts simple and readable across devices.

- Element	Font	Purpose
- Main headings	Playfair Display	Page titles, brand identity
- Body text	Open Sans	Product descriptions, general content
- Buttons	Open Sans (semi-bold)	Call-to-action clarity

### Storefront
- Product listings with images
- Category-based product filtering
- Product detail pages
- Search functionality
- Responsive Bootstrap UI (Bootstrap 4)

### Cart & Checkout
- Add/remove products from cart
- Cart summary page
- Checkout flow
- Guest & authenticated checkout support
- Persistent cart using sessions

### Payments
- Stripe payment integration
- Secure payment handling
- Payment success confirmation
- Order creation after payment

### Orders
- Order creation and storage
- Order status tracking:
  - Processing
  - Shipped
  - Delivered
- Admin-managed order updates
- Automatic order status emails

### Admin Features
- Django Admin dashboard
- Product & category management
- Order management
- Stock quantity tracking
- Sales history (foundation in place)

### Email Notifications
- Order confirmation emails
- Shipping notification emails
- Delivery confirmation emails

---

## Tech Stack

- Backend: Django 5.x
- Frontend: HTML, CSS, Bootstrap 4
- Database: SQLite (development)
- Payments: Stripe
- Email: SMTP (Gmail supported)
- Storage: Django Media Files

---

##  Project Structure

shop/
├── cart/
├── media
├── payment/
├── products/
├── reviews
├── shop/
│ ├── settings.py
│ ├── urls.py
│ └── wsgi.py
├── staticfiles
├── static/
├── templates/
├── venv
├── .env
├── .gitignore
├── .hintrc
├── db.sqlite3
├── manage.py
├── README.md
├── requirements.txt

# Responsive Design
I tested the site at different screen sizes to make sure it works on desktops, tablets, and phones.

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
