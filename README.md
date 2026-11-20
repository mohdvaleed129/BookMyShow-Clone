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
## **🚀 Getting Started**

### **1. Clone the Repository**
    git clone https://github.com/mohdvaleed129//BookMyShow-Clone.git
    cd BookMyShow-Clone

### **2. Create a Virtual Environment**
    python -m venv venv

### **3. Activate the Virtual Environment**

**Windows:**
    venv\Scripts\activate

**Linux / macOS:**
    source venv/bin/activate

### **4. Install Dependencies**
    pip install -r requirements.txt

### **5. Configure Environment Variables**

Create a `.env` file or configure the required environment variables:

    SECRET_KEY=your-secure-secret-key
    DATABASE_URL=sqlite:///database.db

> Never commit your `.env` file or expose secret keys publicly.

### **6. Run the Application**
    python app.py

The application will start at:

    http://localhost:5000

---

## **🗄️ Database**

The application uses SQLite with Flask-SQLAlchemy.

Database tables include:

- Users
- Movies
- Shows
- Seats
- Bookings

The database tables are initialized automatically when the application starts.

---

## **🌱 Sample Data**

To populate the database with sample movies, shows, and seats, run:

    python seed_data.py

The seed script inserts sample data only when the database does not already contain movies.

---

## **🔐 Admin Panel**

The application includes an admin panel for managing the movie booking system.

Admin functionalities include:

- Dashboard overview
- Movie management
- Show management
- User management
- Booking management

Admin access is restricted to authenticated users with admin privileges.

---

## **📌 Booking Workflow**

1. Browse available movies.
2. Select a movie.
3. Choose a show.
4. Log in or register.
5. Select available seats.
6. Confirm the booking.
7. Receive booking confirmation.
8. View or manage tickets through booking history.

---

## **⚠️ Security Notice**

Before deploying this application publicly:

- Change the default secret key.
- Change the default admin credentials.
- Store credentials in environment variables.
- Do not upload `.env` files.
- Do not expose database credentials.
- Use production settings instead of Flask debug mode.
- Configure a production-ready server before deployment.

---

## **👨‍💻 Author**

Developed as a Python Flask web application project.

---

## **📄 License**

This project is intended for educational and development purposes.
