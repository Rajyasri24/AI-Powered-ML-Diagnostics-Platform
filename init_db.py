from backend.app.db.database import engine
from backend.app.db.models import Base

Base.metadata.create_all(bind=engine)