from sqlalchemy import create_engine, MetaData

DB_SERVER = 'localhost:3306'
DB_DATABASE = 'Test'
DB_USERNAME = 'root'
DB_PASSWORD = 'tiger'  # Replace this with the actual password

engine = create_engine(f'mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_SERVER}/{DB_DATABASE}')

meta = MetaData()

conn = engine.connect()
