from app import create_app
from models import db, Movie, Show, Seat
from routes import generate_seats
from datetime import date, timedelta, datetime
import random

app = create_app()

THEATRES = [
    "PVR Cinemas - Phoenix Marketcity",
    "INOX - Metro Mall",
    "Cinepolis - World Square",
    "PVR - Orion Mall",
    "INOX - Garuda Mall"
]

TIME_SLOTS = [
    "10:00",
    "13:30",
    "17:00",
    "20:30"
]


def seed_database():

    with app.app_context():

        print("======================================")
        print("BookMyShow Database Seeder")
        print("======================================")

        # Get movies that already exist
        movies = Movie.query.filter_by(status="now_showing").all()

        if not movies:
            print("ERROR: No now-showing movies found.")
            print("Please add movies before running this script.")
            return

        print(f"Found {len(movies)} now-showing movies.")

        total_shows_created = 0
        total_seats_created = 0

        # ==========================================
        # CREATE SHOWS AND SEATS
        # ==========================================

        for movie in movies:

            print(f"\nProcessing: {movie.title}")

            for day_offset in range(7):

                show_date = date.today() + timedelta(days=day_offset)

                # Select two theatres for each day
                selected_theatres = random.sample(THEATRES, 2)

                for theatre in selected_theatres:

                    for time_slot in TIME_SLOTS:

                        show_time = datetime.strptime(
                            time_slot,
                            "%H:%M"
                        ).time()

                        # Check whether this exact show already exists
                        existing_show = Show.query.filter_by(
                            movie_id=movie.id,
                            theatre=theatre,
                            show_date=show_date,
                            show_time=show_time
                        ).first()

                        if existing_show:

                            show = existing_show

                            print(
                                f"  Existing show: "
                                f"{show_date} | "
                                f"{time_slot} | "
                                f"{theatre}"
                            )

                        else:

                            # Create new show
                            show = Show(
                                movie_id=movie.id,
                                theatre=theatre,
                                show_date=show_date,
                                show_time=show_time,
                                screen=f"Screen {random.randint(1, 4)}"
                            )

                            db.session.add(show)

                            # Generate show ID
                            db.session.flush()

                            total_shows_created += 1

                            print(
                                f"  Created show: "
                                f"{show_date} | "
                                f"{time_slot} | "
                                f"{theatre}"
                            )

                        # ==========================================
                        # CREATE SEATS IF THEY DON'T EXIST
                        # ==========================================

                        existing_seats = Seat.query.filter_by(
                            show_id=show.id
                        ).count()

                        if existing_seats == 0:

                            generate_seats(show.id)

                            total_seats_created += 100

                            print(
                                f"    Created 100 seats "
                                f"for Show ID {show.id}"
                            )

                        else:

                            print(
                                f"    Seats already exist "
                                f"({existing_seats} seats)"
                            )

        # Save changes
        db.session.commit()

        print("\n======================================")
        print("DATABASE REPAIR COMPLETED")
        print("======================================")
        print(f"Shows created : {total_shows_created}")
        print(f"Seats created : {total_seats_created}")
        print("======================================")


if __name__ == "__main__":
    seed_database()