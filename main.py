from fastapi import FastAPI
from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    email: str | None = None
    city: str | None = None

    class Config:
        json_schema_extra = {
            "example": {
                "name" : "Alex",
                "email" : "alex@email.ru",
                "city" : "Russia"
            }
        }
class UserUpdate(BaseModel):
    name: str
    email: str | None = None
    city: str | None = None

    class Config:
        json_schema_extra = {
            "example": {
                "name" : "Alex",
                "email" : "alex@email.ru",
                "city" : "Russia"
            }
        }

app = FastAPI()

data_base = []

# @app.get("/")
# def root():
#     return {"message": "API работает"}

@app.post("/create_user")
def create_user(user: UserCreate):
    name = user.name

    for item in data_base:
        if item['name'] == name:
            return {'status': 'error', 'status code': '400', 'message': 'User already exists'}

    new_user = {
        'name': name,
        'email': user.email,
        'city': user.city,
    }

    new_user['status'] = set_status(new_user)
    data_base.append(new_user)
    return {'status': 'success', 'message': 'User created successfully'}

@app.post("/update_user")
def update_user(user: UserUpdate):
    name = user.name
    for item in data_base:
        if item['name'] == name:
            if user.email:
                item['email'] = user.email
            if user.city:
                item['city'] = user.city
            item['status'] = set_status(item)
            return {'status': 'success', 'message': 'User updated successfully'}
    return {'status': 'error', 'code': '400', 'message': 'User does not exist'}

@app.get("/users")
def get_users():
    return data_base

def set_status(user: dict):
    if user['name'] and user['email'] and user['city']:
        return 'complete'
    elif user['name'] and (user['email'] is None or user['city'] is None):
        return 'in_progress'
    else:
        return 'draft'