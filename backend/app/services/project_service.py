from backend.app.db.models import Project
from backend.app.db.database import SessionLocal

def save_project(user_id, model, result):
    db = SessionLocal()
    p = Project(user_id=user_id, model=model, result=result)
    db.add(p)
    db.commit()
    db.close()

def get_projects(user_id):
    db = SessionLocal()
    data = db.query(Project).filter(Project.user_id == user_id).all()
    db.close()
    return data