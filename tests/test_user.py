from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)

users = [
# Существующие пользователи
    {
        'id': 1,
        'name': 'Ivan Ivanov',
        'email': 'i.i.ivanov@mail.com',
    },
    {
        'id': 2,
        'name': 'Petr Petrov',
        'email': 'p.p.petrov@mail.com',
    },
# Несуществующий пользователь
    {
        'id': 3,
        'name': 'Test User',
        'email': 'i.do.not@exist.com',
    }
]



def test_get_existed_user():
    '''Получение существующего пользователя'''
    response = client.get("/api/v1/user", params={'email': users[0]['email']})
    assert response.status_code == 200
    assert response.json() == users[0]

def test_get_unexisted_user():
    '''Получение несуществующего пользователя'''
    response = client.get("/api/v1/user", params={'email': users[2]['email']})
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}

def test_create_user_with_valid_email():
    '''Создание пользователя с уникальной почтой'''
    response = client.post("/api/v1/user", json={
        'name': users[2]['name'],
        'email': users[2]['email']
    })
    assert response.status_code == 201
    user_id = response.json()
    assert isinstance(user_id, int)
   
    get_response = client.get("/api/v1/user", params={'email': users[2]['email']})
    assert get_response.status_code == 200
    assert get_response.json()['name'] == users[2]['name']
    assert get_response.json()['email'] == users[2]['email']

def test_create_user_with_invalid_email():
    '''Создание пользователя с почтой, которую использует другой пользователь'''
    response = client.post("/api/v1/user", json={
        'name': 'Duplicate User',
        'email': users[1]['email']
    })
    assert response.status_code == 409
    assert response.json() == {"detail": "User with this email already exists"}

def test_delete_user():
    '''Удаление пользователя'''
    delete_response = client.delete("/api/v1/user", params={'email': users[1]['email']})
    assert delete_response.status_code == 204
    assert delete_response.text == ''
    
    get_response = client.get("/api/v1/user", params={'email': users[1]['email']})
    assert get_response.status_code == 404
    assert get_response.json() == {"detail": "User not found"}
