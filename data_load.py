from sqlalchemy import Column, Float, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from modules.models import Firm, User


DATABASE_URI = "sqlite:///instance/app.db"
engine = create_engine(DATABASE_URI)

def clean_db():
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # # Drop and recreate all tables
        base = declarative_base()
        base.metadata.drop_all(engine)
        base.metadata.create_all(engine)
        session.commit()
    except Exception as e:
        print(e)
        session.rollback()
    session.close()

def populate_db():
    # Create a session
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # # Drop and recreate all tables
        base = declarative_base()
        base.metadata.drop_all(engine)
        session.commit()
    except Exception as e:
        print(e)
        session.rollback()
    session.close()

    session = Session()
    try:
        base = declarative_base()
        base.metadata.create_all(engine)
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


        user4 = User(
            email="josephn@slalom.com",
            role="Trader",
            password="password",
            first_name="Joseph",
            last_name="Nielsen",
        )
        user4.firm = firm2

        user5 = User(
            email="matthew.sommers@slalom.com",
            role="Trader",
            password="password",
            first_name="Matthew",
            last_name="Sommers",
        )
        user5.firm = firm2

        session.add_all(
            [firm1, firm2, user1, user2, user3, user4, user5]
        )

        # Commit the session to write data to the database
        session.commit()
        print("Database populated with mock data.")

    except Exception as e:
        print(e)
        session.rollback()
    session.close()

        
    print("Load data complete.")

