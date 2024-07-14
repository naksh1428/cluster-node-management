import random

""" Random data generation"""
group_nm = ['broadband', 'e-sim', 'IPV4', 'IPV6']
city = ['Italy', 'Malmo', 'cophengen', 'eindhoven', 'rotterdam']


def test_root(test_client):
    response = test_client.get("/v1/healthchecker/")
    assert response.status_code == 200
    assert response.json() == {'message': 'The API is Live!!'}


def test_create_group(test_client):
    data = {'group_name': random.choice(group_nm), 'city': random.choice(city)}
    response = test_client.post("/v1/group/", params=data)
    assert response.status_code == 201


def test_get_group(test_client):
    """check for existing record """
    response = test_client.get("/v1/group/", params={'group_id': 5})
    assert response.status_code == 200
    response_json = response.json()
    assert response_json['id'] == 5
    """check for missing record"""
    response = test_client.get("/v1/group/", params={'group_id': 100})
    assert response.status_code == 404
    assert response.json() == {'details': 'Group not Found'}


def test_delete_group(test_client):
    response = test_client.delete("/v1/group/", params={'group_id': 1})
    assert response.status_code == 200