import uvicorn
import math
from sqlalchemy import text
from fastapi import FastAPI, Depends, exceptions, Response
from sqlalchemy.orm import Session
from db import get_db, engine
# import models
from models import *
from schemas import Restaurants

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/restaurant")
def create(restaurant: Restaurants, db: Session = Depends(get_db)):
    print(restaurant)
    new_rest = Restaurant(**restaurant.model_dump())
    db.add(new_rest)
    db.commit()
    db.refresh(new_rest)
    return new_rest

@app.get("/restaurant")
def get(db: Session = Depends(get_db)):
    restaurants = db.query(Restaurant).all()
    return restaurants

@app.delete("/delete/{id}")
def delete(id:str, db: Session = Depends(get_db), status_code = 204):
    delete_result = db.query(Restaurant).filter(Restaurant.id == id)
    if not delete_result:
        raise exceptions.HTTPException(status_code=404, detail=f"Restaurant id not exists")
    
    else:
        delete_result.delete(synchronize_session=False)
        db.commit()
    
    return Response(status_code=204)

@app.put("/update/{id}")
def update(id: str, restaurant: Restaurants, db: Session = Depends(get_db)):
    update_result = db.query(Restaurant).filter(Restaurant.id == id)
    update_result.first()
    if not update_result:
        raise exceptions.HTTPException(status_code=204, detail=f"Id {id} does not exist!")
    
    else:
        update_result.update(restaurant.model_dump(), synchronize_session=False)
        db.commit()

    return update_result.first()

@app.post("/restaurants/statistics")
def statistics(latitude: float, longitude: float, radius: float, db: Session = Depends(get_db)):
    ###
    restaurants = db.execute(text("""
        SELECT * 
        FROM restaurants 
        WHERE ST_DWithin(ST_MakePoint(lng, lat)::geography, ST_MakePoint({}, {})::geography, {});
    """.format(longitude, latitude, radius))).all()

    response = {
        'count' : len(restaurants),
        'avg': None,
        'std': None
    }

    avg = {
        '0': 0,
        '1': 0,
        '2': 0,
        '3': 0,
        '4': 0,
        }
    for row in restaurants: 
        avg[str(row[1])] += 1
    
    final_avg = 0
    total_ = 0
    std_list = []
    for key in avg:
        final_avg = avg[key]*int(key)
        total_ += avg[key]
        std_list.append(avg[key])
    
    final_avg = final_avg/total_

    response['avg'] = final_avg

    mean = sum(std_list) / len(std_list)
    var = sum((l-mean)**2 for l in std_list) / len(std_list)
    st_dev = math.sqrt(var)

    response['std'] = st_dev

    return response


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)



