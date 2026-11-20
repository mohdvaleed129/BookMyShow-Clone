from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User, Movie, Show, Seat, Booking
from forms import (RegistrationForm, LoginForm, ProfileForm, ChangePasswordForm, 
                     MovieForm, ShowForm, AdminLoginForm)
from config import Config
from datetime import datetime, date, timedelta
import random

main = Blueprint('main', __name__)

@main.route('/')
def index():
    search = request.args.get('search', '')
    language = request.args.get('language', '')
    genre = request.args.get('genre', '')
    sort = request.args.get('sort', '')
    
    query = Movie.query
    if search:
        query = query.filter(Movie.title.contains(search))
    if language:
        query = query.filter_by(language=language)
    if genre:
        query = query.filter(Movie.genre.contains(genre))
    if sort == 'rating_desc':
        query = query.order_by(Movie.rating.desc())
    elif sort == 'rating_asc':
        query = query.order_by(Movie.rating.asc())
    elif sort == 'date_desc':
        query = query.order_by(Movie.release_date.desc())
    elif sort == 'date_asc':
        query = query.order_by(Movie.release_date.asc())
    
    featured_movies = Movie.query.order_by(Movie.rating.desc()).limit(5).all()
    now_showing = Movie.query.filter_by(status='now_showing').order_by(Movie.rating.desc()).limit(8).all()
    coming_soon = Movie.query.filter_by(status='coming_soon').order_by(Movie.release_date.asc()).limit(8).all()
    all_movies = query.all()
    
    languages = [l[0] for l in db.session.query(Movie.language).distinct().all()]
    genres = [g[0] for g in db.session.query(Movie.genre).distinct().all()]
    
    return render_template('index.html', 
                         featured=featured_movies,
                         now_showing=now_showing,
                         coming_soon=coming_soon,
                         movies=all_movies,
                         languages=languages,
                         genres=genres,
                         search=search,
                         selected_language=language,
                         selected_genre=genre,
                         selected_sort=sort)

@main.route('/movies')
def movies():
    search = request.args.get('search', '')
    language = request.args.get('language', '')
    genre = request.args.get('genre', '')
    sort = request.args.get('sort', '')
    page = request.args.get('page', 1, type=int)
    
    query = Movie.query
    if search:
        query = query.filter(Movie.title.contains(search))
    if language:
        query = query.filter_by(language=language)
    if genre:
        query = query.filter(Movie.genre.contains(genre))
    
    if sort == 'rating_desc':
        query = query.order_by(Movie.rating.desc())
    elif sort == 'rating_asc':
        query = query.order_by(Movie.rating.asc())
    elif sort == 'date_desc':
        query = query.order_by(Movie.release_date.desc())
    elif sort == 'date_asc':
        query = query.order_by(Movie.release_date.asc())
    else:
        query = query.order_by(Movie.rating.desc())
    
    per_page = 12
    movies_paginated = query.paginate(page=page, per_page=per_page, error_out=False)
    
    languages = [l[0] for l in db.session.query(Movie.language).distinct().all()]
    genres_list = [g[0] for g in db.session.query(Movie.genre).distinct().all()]
    
    return render_template('movies.html',
                         movies=movies_paginated,
                         languages=languages,
                         genres=genres_list,
                         search=search,
                         selected_language=language,
                         selected_genre=genre,
                         selected_sort=sort)

@main.route('/movie/<int:movie_id>')
def movie_details(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    today = date.today()
    shows = Show.query.filter(
        Show.movie_id == movie_id,
        Show.show_date >= today
    ).order_by(Show.show_date, Show.show_time).all()
    
    shows_by_date = {}
    for show in shows:
        date_str = show.show_date.strftime('%Y-%m-%d')
        if date_str not in shows_by_date:
            shows_by_date[date_str] = []
        shows_by_date[date_str].append(show)
    
    return render_template('movie_details.html', movie=movie, shows_by_date=shows_by_date)

@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegistrationForm()

    print("Request Method:", request.method)

    if form.validate_on_submit():
        print("Form validated")

        user = User(
            fullname=form.fullname.data,
            email=form.email.data,
            phone=form.phone.data
        )
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        print("User created successfully")

        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('main.login'))

    if request.method == "POST":
        print("Validation failed")
        print(form.errors)

    return render_template('register.html', form=form)
@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            remember = form.remember.data == 'True'
            login_user(user, remember=remember)
            next_page = request.args.get('next')
            flash(f'Welcome back, {user.fullname}!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            flash('Invalid email or password.', 'danger')
    
    return render_template('login.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))

@main.route('/profile')
@login_required
def profile():
    total_bookings = Booking.query.filter_by(user_id=current_user.id).count()
    return render_template('profile.html', user=current_user, total_bookings=total_bookings)

@main.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = ProfileForm(obj=current_user)
    if form.validate_on_submit():
        current_user.fullname = form.fullname.data
        current_user.email = form.email.data
        current_user.phone = form.phone.data
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('main.profile'))
    return render_template('edit_profile.html', form=form)

@main.route('/profile/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if not current_user.check_password(form.current_password.data):
            flash('Current password is incorrect.', 'danger')
        else:
            current_user.set_password(form.new_password.data)
            db.session.commit()
            flash('Password changed successfully!', 'success')
            return redirect(url_for('main.profile'))
    return render_template('change_password.html', form=form)

@main.route('/show/<int:show_id>/seats')
@login_required
def seat_selection(show_id):
    show = Show.query.get_or_404(show_id)
    movie = Movie.query.get(show.movie_id)
    seats = Seat.query.filter_by(show_id=show_id).order_by(Seat.seat_number).all()
    
    vip_seats = [s for s in seats if s.category == 'VIP']
    premium_seats = [s for s in seats if s.category == 'Premium']
    regular_seats = [s for s in seats if s.category == 'Regular']
    
    def group_into_rows(seat_list, seats_per_row=10):
        rows = {}
        for seat in seat_list:
            row_letter = seat.seat_number[0]
            if row_letter not in rows:
                rows[row_letter] = []
            rows[row_letter].append(seat)
        for row in rows:
            rows[row].sort(key=lambda s: int(s.seat_number[1:]) if s.seat_number[1:].isdigit() else 0)
        return dict(sorted(rows.items()))
    
    vip_rows = group_into_rows(vip_seats)
    premium_rows = group_into_rows(premium_seats)
    regular_rows = group_into_rows(regular_seats)
    
    prices = {}
    if seats:
        for category in ['VIP', 'Premium', 'Regular']:
            cat_seat = next((s for s in seats if s.category == category), None)
            if cat_seat:
                prices[category] = cat_seat.price
    
    return render_template('seat_selection.html',
                         show=show, movie=movie,
                         vip_rows=vip_rows, premium_rows=premium_rows, regular_rows=regular_rows,
                         prices=prices)

@main.route('/api/book-seats', methods=['POST'])
@login_required
def book_seats():
    data = request.get_json()
    show_id = data.get('show_id')
    seat_ids = data.get('seat_ids', [])
    
    if not show_id or not seat_ids:
        return jsonify({'success': False, 'message': 'Invalid data'}), 400
    
    show = Show.query.get_or_404(show_id)
    movie = Movie.query.get(show.movie_id)
    
    seats = Seat.query.filter(Seat.id.in_(seat_ids)).all()
    for seat in seats:
        if seat.status != 'available':
            return jsonify({'success': False, 'message': f'Seat {seat.seat_number} is no longer available'}), 400
    
    total_amount = sum(seat.price for seat in seats)
    seat_numbers = ', '.join([s.seat_number for s in seats])
    
    booking = Booking(
        booking_id=Booking.generate_booking_id(),
        user_id=current_user.id,
        movie_id=show.movie_id,
        show_id=show_id,
        seats=seat_numbers,
        total_amount=total_amount
    )
    
    db.session.add(booking)
    db.session.flush()
    
    for seat in seats:
        seat.status = 'booked'
        seat.booking_id = booking.id
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'booking_id': booking.booking_id,
        'redirect': url_for('main.booking_confirmation', booking_id=booking.id)
    })

@main.route('/booking/confirmation/<int:booking_id>')
@login_required
def booking_confirmation(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    if booking.user_id != current_user.id and not current_user.is_admin:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('main.index'))
    movie = Movie.query.get(booking.movie_id)
    show = Show.query.get(booking.show_id)
    return render_template('booking_confirmation.html', booking=booking, movie=movie, show=show)

@main.route('/bookings')
@login_required
def booking_history():
    bookings = Booking.query.filter_by(user_id=current_user.id).order_by(Booking.booking_date.desc()).all()
    booking_details = []
    for booking in bookings:
        movie = Movie.query.get(booking.movie_id)
        show = Show.query.get(booking.show_id)
        booking_details.append({'booking': booking, 'movie': movie, 'show': show})
    return render_template('booking_history.html', bookings=booking_details)

@main.route('/booking/<int:booking_id>')
@login_required
def view_ticket(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    if booking.user_id != current_user.id and not current_user.is_admin:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('main.index'))
    movie = Movie.query.get(booking.movie_id)
    show = Show.query.get(booking.show_id)
    return render_template('view_ticket.html', booking=booking, movie=movie, show=show)

@main.route('/booking/cancel/<int:booking_id>', methods=['POST'])
@login_required
def cancel_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    if booking.user_id != current_user.id and not current_user.is_admin:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('main.booking_history'))
    
    show = Show.query.get(booking.show_id)
    show_datetime = datetime.combine(show.show_date, show.show_time)
    
    if datetime.now() > show_datetime:
        flash('Cannot cancel a booking for a show that has already started.', 'danger')
        return redirect(url_for('main.booking_history'))
    
    booking.status = 'cancelled'
    seats = Seat.query.filter_by(booking_id=booking.id).all()
    for seat in seats:
        seat.status = 'available'
        seat.booking_id = None
    
    db.session.commit()
    flash('Booking cancelled successfully. Seats have been released.', 'success')
    return redirect(url_for('main.booking_history'))

@main.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated and current_user.is_admin:
        return redirect(url_for('main.admin_dashboard'))
    
    form = AdminLoginForm()
    if form.validate_on_submit():
        if (form.username.data == Config.ADMIN_USERNAME and 
            form.password.data == Config.ADMIN_PASSWORD):
            admin = User.query.filter_by(email='admin@bookmyshow.com').first()
            if not admin:
                admin = User(
                    fullname='Admin',
                    email='admin@bookmyshow.com',
                    phone='0000000000',
                    is_admin=True
                )
                admin.set_password(Config.ADMIN_PASSWORD)
                db.session.add(admin)
                db.session.commit()
            login_user(admin)
            flash('Welcome to Admin Panel!', 'success')
            return redirect(url_for('main.admin_dashboard'))
        else:
            flash('Invalid admin credentials.', 'danger')
    
    return render_template('admin/login.html', form=form)

@main.route('/admin')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash('Access denied. Admin only.', 'danger')
        return redirect(url_for('main.index'))
    
    stats = {
        'total_users': User.query.count(),
        'total_movies': Movie.query.count(),
        'total_bookings': Booking.query.count(),
        'total_shows': Show.query.count(),
        'confirmed_bookings': Booking.query.filter_by(status='confirmed').count(),
        'cancelled_bookings': Booking.query.filter_by(status='cancelled').count(),
        'revenue': db.session.query(db.func.sum(Booking.total_amount)).filter(
            Booking.status == 'confirmed'
        ).scalar() or 0
    }
    
    recent_bookings = Booking.query.order_by(Booking.booking_date.desc()).limit(10).all()
    return render_template('admin/dashboard.html', stats=stats, recent_bookings=recent_bookings)

@main.route('/admin/movies')
@login_required
def admin_movies():
    if not current_user.is_admin:
        flash('Access denied.', 'danger')
        return redirect(url_for('main.index'))
    movies = Movie.query.order_by(Movie.created_at.desc()).all()
    return render_template('admin/movies.html', movies=movies)

@main.route('/admin/movie/add', methods=['GET', 'POST'])
@login_required
def add_movie():
    if not current_user.is_admin:
        flash('Access denied.', 'danger')
        return redirect(url_for('main.index'))
    
    form = MovieForm()
    if form.validate_on_submit():
        movie = Movie(
            title=form.title.data,
            genre=form.genre.data,
            language=form.language.data,
            duration=form.duration.data,
            rating=form.rating.data,
            description=form.description.data,
            poster=form.poster.data or 'default_poster.jpg',
            trailer=form.trailer.data or '',
            release_date=form.release_date.data,
            status=form.status.data
        )
        db.session.add(movie)
        db.session.commit()
        flash('Movie added successfully!', 'success')
        return redirect(url_for('main.admin_movies'))
    return render_template('admin/movie_form.html', form=form, title='Add Movie')

@main.route('/admin/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def edit_movie(movie_id):
    if not current_user.is_admin:
        flash('Access denied.', 'danger')
        return redirect(url_for('main.index'))
    
    movie = Movie.query.get_or_404(movie_id)
    form = MovieForm(obj=movie)
    if form.validate_on_submit():
        movie.title = form.title.data
        movie.genre = form.genre.data
        movie.language = form.language.data
        movie.duration = form.duration.data
        movie.rating = form.rating.data
        movie.description = form.description.data
        movie.poster = form.poster.data or 'default_poster.jpg'
        movie.trailer = form.trailer.data or ''
        movie.release_date = form.release_date.data
        movie.status = form.status.data
        db.session.commit()
        flash('Movie updated successfully!', 'success')
        return redirect(url_for('main.admin_movies'))
    return render_template('admin/movie_form.html', form=form, title='Edit Movie', movie=movie)

@main.route('/admin/movie/delete/<int:movie_id>', methods=['POST'])
@login_required
def delete_movie(movie_id):
    if not current_user.is_admin:
        flash('Access denied.', 'danger')
        return redirect(url_for('main.index'))
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash('Movie deleted successfully!', 'success')
    return redirect(url_for('main.admin_movies'))

@main.route('/admin/shows')
@login_required
def admin_shows():
    if not current_user.is_admin:
        flash('Access denied.', 'danger')
        return redirect(url_for('main.index'))
    shows = Show.query.order_by(Show.show_date.desc(), Show.show_time.desc()).all()
    return render_template('admin/shows.html', shows=shows)

@main.route('/admin/show/add', methods=['GET', 'POST'])
@login_required
def add_show():
    if not current_user.is_admin:
        flash('Access denied.', 'danger')
        return redirect(url_for('main.index'))
    
    form = ShowForm()
    form.movie_id.choices = [(m.id, m.title) for m in Movie.query.all()]
    
    if form.validate_on_submit():
        show = Show(
            movie_id=form.movie_id.data,
            theatre=form.theatre.data,
            show_date=form.show_date.data,
            show_time=form.show_time.data,
            screen=form.screen.data
        )
        db.session.add(show)
        db.session.flush()
        generate_seats(show.id)
        db.session.commit()
        flash('Show added successfully with seats!', 'success')
        return redirect(url_for('main.admin_shows'))
    return render_template('admin/show_form.html', form=form, title='Add Show')

@main.route('/admin/show/edit/<int:show_id>', methods=['GET', 'POST'])
@login_required
def edit_show(show_id):
    if not current_user.is_admin:
        flash('Access denied.', 'danger')
        return redirect(url_for('main.index'))
    
    show = Show.query.get_or_404(show_id)
    form = ShowForm(obj=show)
    form.movie_id.choices = [(m.id, m.title) for m in Movie.query.all()]
    
    if form.validate_on_submit():
        show.movie_id = form.movie_id.data
        show.theatre = form.theatre.data
        show.show_date = form.show_date.data
        show.show_time = form.show_time.data
        show.screen = form.screen.data
        db.session.commit()
        flash('Show updated successfully!', 'success')
        return redirect(url_for('main.admin_shows'))
    return render_template('admin/show_form.html', form=form, title='Edit Show', show=show)

@main.route('/admin/show/delete/<int:show_id>', methods=['POST'])
@login_required
def delete_show(show_id):
    if not current_user.is_admin:
        flash('Access denied.', 'danger')
        return redirect(url_for('main.index'))
    show = Show.query.get_or_404(show_id)
    db.session.delete(show)
    db.session.commit()
    flash('Show deleted successfully!', 'success')
    return redirect(url_for('main.admin_shows'))

@main.route('/admin/users')
@login_required
def admin_users():
    if not current_user.is_admin:
        flash('Access denied.', 'danger')
        return redirect(url_for('main.index'))
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin/users.html', users=users)

@main.route('/admin/user/delete/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if not current_user.is_admin:
        flash("Access denied.", "danger")
        return redirect(url_for('main.index'))

    user = User.query.get_or_404(user_id)

    if user.is_admin:
        flash("Admin account cannot be deleted.", "danger")
        return redirect(url_for('main.admin_users'))

    db.session.delete(user)
    db.session.commit()

    flash("User deleted successfully.", "success")
    return redirect(url_for('main.admin_users'))

@main.route('/admin/bookings')
@login_required
def admin_bookings():
    if not current_user.is_admin:
        flash('Access denied.', 'danger')
        return redirect(url_for('main.index'))
    bookings = Booking.query.order_by(Booking.booking_date.desc()).all()
    return render_template('admin/bookings.html', bookings=bookings)

@main.route('/admin/booking/cancel/<int:booking_id>', methods=['POST'])
@login_required
def admin_cancel_booking(booking_id):
    if not current_user.is_admin:
        flash('Access denied.', 'danger')
        return redirect(url_for('main.index'))
    
    booking = Booking.query.get_or_404(booking_id)
    if booking.status == 'cancelled':
        flash('Booking is already cancelled.', 'warning')
        return redirect(url_for('main.admin_bookings'))
    
    show = Show.query.get(booking.show_id)
    show_datetime = datetime.combine(show.show_date, show.show_time)
    
    if datetime.now() > show_datetime:
        flash('Cannot cancel a booking for a show that has already started.', 'danger')
        return redirect(url_for('main.admin_bookings'))
    
    booking.status = 'cancelled'
    seats = Seat.query.filter_by(booking_id=booking.id).all()
    for seat in seats:
        seat.status = 'available'
        seat.booking_id = None
    
    db.session.commit()
    flash('Booking cancelled successfully.', 'success')
    return redirect(url_for('main.admin_bookings'))

@main.app_errorhandler(404)
def not_found(error):
    return render_template('errors/404.html'), 404

@main.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500

def generate_seats(show_id):
    for row in ['A', 'B']:
        for num in range(1, 11):
            seat = Seat(show_id=show_id, seat_number=f'{row}{num}', category='VIP', price=50.0, status='available')
            db.session.add(seat)
    for row in ['C', 'D', 'E']:
        for num in range(1, 11):
            seat = Seat(show_id=show_id, seat_number=f'{row}{num}', category='Premium', price=35.0, status='available')
            db.session.add(seat)
    for row in ['F', 'G', 'H', 'I', 'J']:
        for num in range(1, 11):
            seat = Seat(show_id=show_id, seat_number=f'{row}{num}', category='Regular', price=20.0, status='available')
            db.session.add(seat)