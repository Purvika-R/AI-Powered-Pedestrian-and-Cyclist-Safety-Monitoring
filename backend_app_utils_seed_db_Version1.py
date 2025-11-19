from ..db import engine
from ..models import models
from ..auth import get_password_hash
from ..config import settings

def seed():
    models.Base.metadata.create_all(bind=engine)
    from sqlalchemy.orm import Session
    from ..db import SessionLocal
    db = SessionLocal()
    u = db.query(models.User).filter(models.User.username == settings.ADMIN_USERNAME).first()
    if not u:
        user = models.User(username=settings.ADMIN_USERNAME, password_hash=get_password_hash(settings.ADMIN_PASSWORD), is_admin=True)
        db.add(user)
        db.commit()
    db.close()
    print("Seeded DB with admin user")

if __name__ == "__main__":
    seed()