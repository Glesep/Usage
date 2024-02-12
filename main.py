from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()


db = []                                                                                                                 # 임시 DATABASE

# Model 만들기
class City(BaseModel):                          
    name: str
    timezone: str

# 전체 도시들의 정보
@app.get("/cities")                                                                                                     # Method = GET
def get_cities():
    results = []                                                                                                        # 결과를 저장하는 리스트
    for city in db:                                                                                                     # 임시 DB 안에서 반복
        strs = f"http://worldtimeapi.org/api/timezone/{city['timezone']}"                                               # 랑크 저장
        r = requests.get(strs)                                                                                          # 저장된 링크 안에서 GET request를 받고 그 결과를 변수 r에 저장함 
        cur_time = r.json()['datetime']                                                                                 # r의 json파일에서 datetime이라는 key에 들어있는 값을 변수 cur_time에 저장함
        results.append({'name': city['name'], 'timezone': city['timezone'], 'current_time': cur_time})                  # city 딕셔너리를 받아 result 리스트 안에 저장 (리스트 요소 하나가 city 딕셔너리 전체가 되는 것)
    return results

# 도시 하나의 정보
@app.get("/cities/{city_id}")
async def get_city(city_id: int):                                                                                       # city_id를 경로 매개변수로 받음
    city = db[city_id - 1]                                                                                              # index = city_id -1
    strs = f"http://worldtimeapi.org/api/timezone/{city['timezone']}"
    r = requests.get(strs)
    cur_time = r.json()['datetime']
    return {'name': city['name'], 'timezone': city['timezone'], 'current_time': cur_time}
   
# 도시 정보 추가
@app.post("/cities")                                                      
async def create_city(city: City):                                                                                      # City 모델을 매개변수로 받음
    db.append(city.model_dump())                                                                                        # db 리스트에 City 모델(딕셔너리 타입) 추가
    return db[-1]                                                                                                       # db 리스트의 마지막 요소 반환

# 도시 정보 삭제
@app.delete("/cities/{city_id}")                                                                                        
async def delete_city(city_id: int):
    db.pop(city_id - 1)                                                                                                 # index에 해당하는 db 요소 삭제
    return {}