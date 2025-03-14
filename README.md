# Ecommerce-Website

This is an e-commerce platform built with Django and Django Rest Framework (DRF) for managing products, users, orders, cart, sales, and wishlists. The project includes JWT token-based authentication for secure access to API endpoints, and it also provides API documentation via Swagger and ReDoc.

Table of Contents:
Installation
Project Structure
Usage
API Endpoints
Authentication
Permissions
Swagger and ReDoc Documentation
Running Tests
License
Live Demo

Live Demo:
https://geguchadzeadmin.pythonanywhere.com/swagger/
https://ecommerce-colab.vercel.app/

Installation:
Prerequisites
Python 3.x
Django 4.x or higher
Django Rest Framework
Django Rest Framework Simple JWT
PostgreSQL (or any other database you prefer)

Steps to Install
Clone the repository:
git clone https://github.com/anageguchadze/Ecommerce-Website.git
cd Ecommerce-Website

Create a virtual environment and activate it:
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

Install dependencies:
pip install -r requirements.txt

Set up the database:
Ensure you have PostgreSQL (or any other DB) set up and configured in your settings.py.

Migrate the database:
python manage.py migrate

Create a superuser (admin):
python manage.py createsuperuser

Run the server:
python manage.py runserver

Project Structure:

ecommerce_project/
├── auth_app/                # Custom authentication app
│   ├── migrations/
│   ├── models.py            # Custom User model
│   ├── views.py
│   └── serializers.py       # User serializers
├── cart_app/                # Cart and Order management
│   ├── migrations/
│   ├── models.py            # Cart and Order models
│   ├── views.py
│   └── serializers.py       # Cart and Order serializers
├── product_app/             # Product and category management
│   ├── migrations/
│   ├── models.py            # Product, Category, Subcategory models
│   ├── views.py
│   └── serializers.py       # Product serializers
├── sales_app/               # Sales and discount management
│   ├── migrations/
│   ├── models.py            # Sale models
│   ├── views.py
│   └── serializers.py       # Sale serializers
├── wishlist_app/            # Wishlist management
│   ├── migrations/
│   ├── models.py            # Wishlist models
│   ├── views.py
│   └── serializers.py       # Wishlist serializers
├── ecommerce_project/       # Main project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py                # Django management script
└── requirements.txt         # List of required packages

Usage
This project provides API endpoints for the following functionalities:
User Authentication: Registration, Login, and Token Management.
Product Management: Categories, Subcategories, Product Listings, and Ratings.
Cart Management: Adding, removing, and updating items in the cart.
Order Processing: Create and track orders.
Sales and Discounts: Apply discounts and manage sales campaigns.
Wishlist: Manage user wishlists.

API Endpoints
User Endpoints
Register User:
POST /auth/register/
Fields: email, name, password
Login User:
POST /auth/login/
Fields: email, password
Logout User:
POST /auth/logout/
User Details:
GET /auth/user/
Product Endpoints
List Products:
GET /products/
Product Detail:
GET /products/<id>/
Product Ratings:
POST /products/<id>/ratings/
Cart Endpoints
List Cart Items:
GET /cart/
Add Item to Cart:
POST /cart/add/
Fields: product_id, quantity
Remove Item from Cart:
DELETE /cart/remove/<id>/
Order Endpoints
Create Order:
POST /orders/create/
Fields: recipientName, recipientPhoneNumber, address, total, etc.
Order Details:
GET /orders/<id>/
Wishlist Endpoints
List Wishlist Items:
GET /wishlist/
Add Item to Wishlist:
POST /wishlist/add/
Remove Item from Wishlist:
DELETE /wishlist/remove/<id>/

Authentication
This project uses JWT (JSON Web Token) authentication via the Django Rest Framework Simple JWT package.

Getting a Token
Use the /auth/login/ endpoint to log in and get a JWT token.
The response will contain the access and refresh tokens.
Using the Token
Include the access token in the Authorization header as Bearer <your-token> for accessing protected API endpoints.

Example:
Authorization: Bearer <your-access-token>
Refreshing the Token
Use the /auth/token/refresh/ endpoint to refresh the JWT access token.
Settings Overview
JWT Access Token Lifetime: 1 day
JWT Refresh Token Lifetime: 1 day
CORS: Allowed for all origins (CORS_ALLOW_ALL_ORIGINS = True)
Blacklist Tokens: JWT tokens are blacklisted after they are rotated.
Permissions
IsAuthenticated: Applied to user-specific views, such as profile, cart, and orders. Only authenticated users can access these endpoints.
IsAdminUser: Applied to admin-specific views (e.g., product management) where only staff members are allowed access.
IsOwner: Applied to views where the user needs to own the resource (e.g., a cart or order).
Swagger and ReDoc Documentation
This project includes auto-generated API documentation using Swagger and ReDoc via the drf-yasg package.

Swagger UI:
Visit: http://127.0.0.1:8000/swagger/
Provides an interactive interface to explore and test the API.
ReDoc:
Visit: http://127.0.0.1:8000/redoc/
Provides a more comprehensive, static API documentation view.
These endpoints provide detailed information about all available API endpoints and allow you to test them directly.


License
This project is licensed under the MIT License.

