# 👕 FashionStore - Clothing E-Commerce Platform
 
[![React](https://img.shields.io/badge/React-18.2.0-61DAFB?logo=react)](https://reactjs.org/)
[![Django](https://img.shields.io/badge/Django-4.2-092E20?logo=django)](https://www.djangoproject.com/)
[![Tailwind](https://img.shields.io/badge/Tailwind-3.3.2-06B6D4?logo=tailwindcss)](https://tailwindcss.com/)
[![Stripe](https://img.shields.io/badge/Stripe-5.5-008CDD?logo=stripe)](https://stripe.com/)
[![Cloudinary](https://img.shields.io/badge/Cloudinary-1.32-3448C5?logo=cloudinary)](https://cloudinary.com/)
 
## 📌 About
 
**FashionStore** is a full-stack e-commerce platform for men's and women's clothing, built with a **React** frontend (Vite, Tailwind CSS, Redux Toolkit) and a **Django REST Framework** backend (JWT, Stripe, Cloudinary, transactional emails).
 
---
 
## ✨ Key Features
 
- **Authentication** — Email confirmation, JWT login, profile management, wishlist
- **Product Catalog** — Advanced filtering, search, pagination, featured items, Cloudinary images
- **Cart & Orders** — Multi-step checkout, order history, confirmation emails
- **Payments** — Stripe integration (test/production), Stripe webhooks
- **Admin Panel** — Full product, category, variant, and order management via Django Admin
---
 
## 🏗️ Architecture
 
```text
React Frontend (Vite + Tailwind) — Port 5173
        |
   HTTP / REST API
        |
Django REST Framework — Port 8000
  [Accounts] [Products] [Cart] [Orders] [Payments]
        |
      SQLite
```
 
---
 
## 🛠️ Tech Stack
 
| Layer | Technologies |
|-------|-------------|
| Frontend | React 18, Redux Toolkit, React Router, Tailwind CSS, Axios, Stripe.js, Framer Motion |
| Backend | Django 4.2, DRF 3.14, Simple JWT, Stripe 5.5, Cloudinary 1.32 |
| Database | SQLite |
 
---
 
## 🚀 Getting Started
 
### Prerequisites
- Python 3.10+, Node.js 18+
- Accounts: [Stripe](https://stripe.com), [Cloudinary](https://cloudinary.com), Gmail
### 1. Clone the repo
```bash
git clone https://github.com/Mouad-El-Aouiz/clothing-ecommerce.git
cd clothing-ecommerce
```
 
### 2. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```
 
Create a `.env` file in `backend/`:
```bash
SECRET_KEY=your_secret_key
DEBUG=True
STRIPE_PUBLIC_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
CLOUDINARY_CLOUD_NAME=your_cloud
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```
 
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
 
### 3. Frontend Setup
```bash
cd frontend
npm install
cp .env.example .env  # Add VITE_STRIPE_PUBLIC_KEY
npm run dev
```
 
### 4. Access
 
| Service | URL | Credentials |
|---------|-----|-------------|
| Frontend | http://localhost:5173 | — |
| API | http://localhost:8000/api | — |
| Admin | http://localhost:8000/admin | admin / admin123 |
 
---
 
## 💳 Stripe Test Card
 
Use `4242 4242 4242 4242` with any future expiry and CVC `123`.
 
---
 
## 🔮 Future Improvements
 
- Dark mode, PWA, multilingual support (EN/FR/AR)
- Product ratings, promo codes, AI recommendations
- Customer support chatbot, newsletter
---
 
## 📞 Contact
 
**Mouad El Aouiz** — Full Stack Developer
- 📧 mouadelaouiz@gmail.com
- 🔗 [LinkedIn](https://linkedin.com/in/mouad-el-aouiz-310811343/)
- 🐙 [GitHub](https://github.com/Mouad-El-Aouiz)
---
 
Built with ❤️ by Mouad El Aouiz — ⭐ Star this repo if you found it useful!
 
