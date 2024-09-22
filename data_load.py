from sqlalchemy import Column, Float, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from modules.models import Firm, User


DATABASE_URI = "sqlite:///instance/app.db"
engine = create_engine(DATABASE_URI)


def populate_db():
    # Create a session
    Session = sessionmaker(bind=engine)
    session = Session()

    # # Drop and recreate all tables
    base = declarative_base()
    base.metadata.drop_all(engine)
    base.metadata.create_all(engine)

    try:
        firm1 = Firm()
        firm1.firm_name = "Alpha Capital"
        firm2 = Firm()
        firm2.firm_name= "Beta Capital"


        user1 = User(
            email="john.doe@alpha.com",
            role="Admin",
            password="password",
            first_name="John",
            last_name="Doe",
        )
        user1.firm = firm1
        user2 = User(
            email="jane.smith@alpha.com",
            role="Trader",
            password="password",
            first_name="Jane",
            last_name="Smith",
        )
        user2.firm = firm1
        user3 = User(
            email="alice.jones@beta.com",
            role="Trader",
            password="password",
            first_name="Alice",
            last_name="Jones",
        )
        user3.firm = firm2

        # Add all objects to the session
        session.add_all(
            [firm1, firm2]
        )

        # Commit the session to write data to the database
        session.commit()
        print("Database populated with mock data.")

    except Exception as e:
        print(e)
        session.rollback()

    session.close()
    print("Load data complete.")



if __name__ == "__main__":
    populate_db()
