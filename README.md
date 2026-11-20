# 🎬 BookMyShow – Movie Ticket Booking System

A movie ticket booking web application built using Python and Flask. Users can browse movies, explore showtimes, select seats, book tickets, and manage their bookings through a personal account. The application also includes an admin panel for managing movies, shows, users, and bookings.

---

## ✨ Features

### 🎥 Movie Browsing
- Browse featured movies and currently showing movies
- Explore upcoming movies
- View movie details, descriptions, ratings, genres, and trailers
- Search movies by title
- Filter movies by language and genre
- Sort movies by ratings and release date
- Paginated movie listings

### 👤 User Authentication
- User registration and login
- Password hashing
- Session-based authentication
- Remember me functionality
- User logout
- Protected routes

### 🎟️ Ticket Booking
- Browse available movie shows
- Select show dates and timings
- Interactive seat selection
- VIP, Premium, and Regular seat categories
- Category-based seat pricing
- Booking confirmation
- Unique booking ID generation
- View booked tickets
- Booking history
- Booking cancellation

### ⚙️ User Profile
- View user profile
- Edit personal information
- Change password
- View total bookings

### 🛠️ Admin Dashboard
- Admin login
- Dashboard overview
- Add, edit, and delete movies
- Manage movie details and status
- Add, edit, and delete shows
- Manage users
- View all bookings
- Cancel bookings
- Manage seat availability through booking operations

---

## 🛠️ Tech Stack

### Backend
- Python
- Flask 3.0.3
- Flask-SQLAlchemy
- Flask-Login
- Flask-WTF
- WTForms

### Database
- SQLite
- SQLAlchemy ORM

### Frontend
- HTML5
- CSS3
- JavaScript
- Jinja2 Templates

### Security & Validation
- Werkzeug Password Hashing
- Flask-Login Authentication
- Flask-WTF Form Validation
- CSRF Protection

---

## 📁 Project Structure

```text
.
├── app.py
├── config.py
├── models.py
├── routes.py
├── forms.py
├── seed_data.py
├── requirements.txt
├── templates/
│   ├── index.html
│   ├── movies.html
│   ├── movie_details.html
│   ├── login.html
│   ├── register.html
│   ├── profile.html
│   ├── edit_profile.html
│   ├── change_password.html
│   ├── seat_selection.html
│   ├── booking_confirmation.html
│   ├── booking_history.html
│   ├── view_ticket.html
│   ├── admin/
│   └── errors/
└── instance/
    └── database.db
