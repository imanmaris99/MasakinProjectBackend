from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import scoped_session, sessionmaker
import os


# Creating a SQLAlchemy db object without direct initialization
db = SQLAlchemy()
migrate = Migrate()

# Konfigurasi basis data dari variabel lingkungan
DB_TYPE = os.getenv("DB_TYPE")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

# URI koneksi PostgreSQL
# Pastikan DATABASE_URI diatur dengan benar sesuai dengan konfigurasi Anda
# DATABASE_URI = f"{DB_TYPE}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
# print(f"DATABASE_URI: {DATABASE_URI}")  # Debug print untuk memeriksa nilai DATABASE_URI

# Construct the DATABASE_URI if not explicitly set
if not os.getenv('DATABASE_URI'):
    DATABASE_URI = f"{DB_TYPE}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
else:
    DATABASE_URI = os.getenv('DATABASE_URI')

# Debugging output
# print("Constructed DATABASE_URI:", DATABASE_URI)

engine = create_engine(DATABASE_URI)
Session = scoped_session(sessionmaker(bind=engine))

def init_db(app):
    try:
        db.init_app(app)
        with app.app_context():
            db.create_all()
            print(f'Successfully connected to the database using provided URI')
    except SQLAlchemyError as e:
        print(f'Error connecting to the database: {e}')
