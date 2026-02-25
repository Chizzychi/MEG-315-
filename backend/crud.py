from .database import SessionLocal
from .models import ProcessPoint

def save_points_to_db(process_type, points):
    session = SessionLocal()
    for p in points:
        db_point = ProcessPoint(process_type=process_type, V=p["V"], P=p["P"], T=p["T"], s=p["s"])
        session.add(db_point)
    session.commit()
    session.close()
