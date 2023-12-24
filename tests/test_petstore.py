import allure
import pytest

# https://github.com/sadboy2001/api_testing/blob/main/api_testing/requests_example.py
# https://ithub.bulgakov.app/study/7298/sections/76847
# https://www.geeksforgeeks.org/http-request-methods-python-requests
# https://allurereport.org/docs/how-it-works
# python -m pytest -n 8 --alluredir allure-results

# Pet
@allure.epic("Petstore")  # Many weeks
@allure.feature("Pet")  # 8 weeks
@allure.story("Add a new pet to the store")  # 1 week
@pytest.mark.parametrize(
    "pet",
    [
        {
            "id": 0,
            "category": {"id": 0, "name": "string"},
            "name": "doggie",
            "photoUrls": ["string"],
            "tags": [{"id": 0, "name": "string"}],
            "status": "available",
        },
        {},
    ],
)
def test_add_a_new_pet_to_the_store(api, pet):
    rsp = api.post("pet", json=pet)
    with allure.step("Checking the response code"):
        assert rsp.status_code in [
            200,
            405,
        ], f"The response code {rsp.status_code} does not match"
    with allure.step("Deserializing the response from json to the dictionary"):
        data = rsp.json()
        if "id" in data:
            assert data["id"] > 0, f"The pet {pet.id} was not added to the store"
        else:
            assert (
                data["code"] == rsp.status_code
            ), f"The pet {pet.id} was not added to the store"


@allure.epic("Petstore")
@allure.feature("Pet")
@allure.story("Update an existing pet")
@pytest.mark.parametrize(
    "pet",
    [
        {
            "id": 0,
            "category": {"id": 0, "name": "string"},
            "name": "doggie",
            "photoUrls": ["string"],
            "tags": [{"id": 0, "name": "string"}],
            "status": "available",
        },
        {},
    ],
)
def test_update_an_existing_pet(api, pet):
    rsp = api.put("pet", json=pet)
    with allure.step("Checking the response code"):
        assert rsp.status_code in [
            200,
            404,
            405,
        ], f"The response code {rsp.status_code} does not match"
    with allure.step("Deserializing the response from json to the dictionary"):
        data = rsp.json()
        if "id" in data:
            assert data["id"] > 0, f"The pet {pet.id} was not updated"
        else:
            assert data["code"] == rsp.status_code, f"The pet {pet.id} was not updated"


@allure.epic("Petstore")
@allure.feature("Pet")
@allure.story("Find pet by ID")
@pytest.mark.parametrize("pet_id", [1, 2])  # code is 1
def test_find_pet_by_id(api, pet_id):
    rsp = api.get(f"pet/{pet_id}")
    with allure.step("Checking the response code"):
        assert rsp.status_code in [
            200,
            400,
            404,
        ], f"The response code {rsp.status_code} does not match for pet {pet_id}"
    with allure.step("Deserializing the response from json to the dictionary"):
        data = rsp.json()
        if "code" in data:
            assert data["type"] == "error", f"Pet {pet_id} is missing"
        else:
            assert "id" in data, f"Pet {pet_id} is missing"


@allure.epic("Petstore")
@allure.feature("Pet")
@allure.story("Finds Pets by status")
@pytest.mark.parametrize("status", ["available", "pending", "sold"])  # random zero len
def test_finds_pets_by_status(api, status):
    rsp = api.get(f"pet/findByStatus?status={status}")
    with allure.step("Checking the response code"):
        assert rsp.status_code in [
            200,
            400,
            405,
        ], f"The response code {rsp.status_code} does not match for status {status}"
    with allure.step("Deserializing the response from json to the dictionary"):
        data = rsp.json()
        if "code" in data:
            assert data["code"] == rsp.status_code, f"Pets was not exists"
        else:
            assert (
                type(data) == list
            ), f"The pets does not correspond to the status {status}"


@allure.epic("Petstore")
@allure.feature("Pet")
@allure.story("Deletes a pet")
@pytest.mark.parametrize("pet_id", [1, 2])
def test_deletes_a_pet(api, pet_id):
    rsp = api.delete(f"pet/{pet_id}")
    with allure.step("Checking the response code"):
        assert rsp.status_code in [
            200,
            404,
            400,
        ], f"The response code {rsp.status_code} does not match for pet {pet_id}"
    with allure.step("Deserializing the response from json to the dictionary"):
        if "Content-Type" in rsp.headers:
            if rsp.headers["Content-Type"] == "application/json":
                data = rsp.json()
                if "code" in data:
                    assert (
                        data["code"] == rsp.status_code
                    ), f"Pet {pet_id} has not been deleted"


# store
@allure.epic("Petstore")
@allure.feature("Store")
@allure.story("Place an order for a pet")
@pytest.mark.parametrize(
    "pet",
    [
        {
            "id": 0,
            "petId": 0,
            "quantity": 0,
            "shipDate": "2023-12-11T17:00:08.169Z",
            "status": "placed",
            "complete": True,
        },
        {"id": -10},
    ],
)
def test_place_an_order_for_a_pet(api, pet):
    rsp = api.post("store/order", json=pet)
    with allure.step("Checking the response code"):
        assert rsp.status_code in [
            200,
            400,
            404,
            405,
        ], f"The response code {rsp.status_code} does not match for pet {pet['id']}"
    with allure.step("Deserializing the response from json to the dictionary"):
        data = rsp.json()
        if "code" in data:
            assert (
                data["code"] == rsp.status_code
            ), f"Order ID {pet['id']} has not been placed"
        else:
            assert "id" in data, f"Order ID {pet['id']} has not been placed"


@allure.epic("Petstore")
@allure.feature("Store")
@allure.story("Find purchase order by ID")
@pytest.mark.parametrize("order_id", [1, 2])  # random 404
def test_find_order_by_id(api, order_id):
    rsp = api.get(f"store/order/{order_id}")
    with allure.step("Checking the response code"):
        assert rsp.status_code in [
            200,
            400,
            404,
        ], f"The response code {rsp.status_code} does not match for pet {order_id}"
    with allure.step("Deserializing the response from json to the dictionary"):
        data = rsp.json()
        if "code" in data:
            assert data["type"] == "error", f"Order {order_id} is missing"
        else:
            assert "id" in data, f"Order {order_id} is missing"


@allure.epic("Petstore")
@allure.feature("Store")
@allure.story("Delete purchase order by ID")
@pytest.mark.parametrize("order_id", [1, 2, -3])
def test_deletes_a_order_by_id(api, order_id):
    rsp = api.delete(f"store/order/{order_id}")
    with allure.step("Checking the response code"):
        assert rsp.status_code in [
            200,
            404,
            400,
        ], f"The response code {rsp.status_code} does not match for order {order_id}"
    with allure.step("Deserializing the response from json to the dictionary"):
        data = rsp.json()
        if "code" in data:
            assert (
                data["code"] == rsp.status_code
            ), f"Order {order_id} has not been deleted"


@allure.epic("Petstore")
@allure.feature("Store")
@allure.story("Returns pet inventories by status")
def test_pet_inventories(api):
    rsp = api.get("store/inventory")
    with allure.step("Checking the response code"):
        assert rsp.status_code in [
            200,
            404,
        ], f"The response code {rsp.status_code} does not match for order"
    with allure.step("Deserializing the response from json to the dictionary"):
        data = rsp.json()
        if "code" in data:
            assert data["code"] == rsp.status_code, "Inventories is missing"


@allure.epic("Petstore")
@allure.feature("Store")
@allure.story("Returns pet inventories by status and api_key")
@pytest.mark.parametrize("key", ["1", "2", "-3"])
def test_pet_inventories_by_key(api, key):
    rsp = api.get("store/inventory/", headers={"api_key": key})
    with allure.step("Checking the response code"):
        assert rsp.status_code in [
            200,
            404,
        ], f"The response code {rsp.status_code} does not match for order"
    with allure.step("Deserializing the response from json to the dictionary"):
        data = rsp.json()
        if "code" in data:
            assert data["code"] == rsp.status_code, "Inventories is missing"


# User
@allure.epic("Petstore")
@allure.feature("User")
@allure.story("Get user by user name")
@pytest.mark.parametrize("name", ["a", "b"])
def test_get_user_by_user_name(api, name):
    rsp = api.get(f"user/{name}")
    with allure.step("Checking the response code"):
        assert rsp.status_code in [
            200,
            400,
            404,
        ], f"The response code {rsp.status_code} does not match for pet {name}"
    with allure.step("Deserializing the response from json to the dictionary"):
        data = rsp.json()
        if "code" in data:
            assert data["type"] == "error", f"User {name} is missing"
        else:
            assert data["id"] == name, f"User {name} is missing"


@allure.epic("Petstore")
@allure.feature("User")
@allure.story("Updated user")
@pytest.mark.parametrize(
    "user",
    [
        {
            "name": "a",
            "value": {
                "id": 0,
                "username": "string",
                "firstName": "string",
                "lastName": "string",
                "email": "string",
                "password": "string",
                "phone": "string",
                "userStatus": 0,
            },
        },
        {
            "name": "b",
            "value": {
                "id": 1,
                "username": "name",
                "firstName": "firstName",
                "lastName": "lastName",
                "email": "email@email.email",
                "password": "password",
                "phone": "55555",
                "userStatus": 5,
            },
        },
    ],
)
def test_update_user(api, user):
    rsp = api.put(f"user/{user['name']}", json=user["value"])
    with allure.step("Checking the response code"):
        assert rsp.status_code in [
            200,
            400,
            404,
        ], f"The response code {rsp.status_code} does not match"
    with allure.step("Deserializing the response from json to the dictionary"):
        data = rsp.json()
        if "code" in data:
            assert (
                data["code"] == rsp.status_code
            ), f"The user {user['name']} was not updated"


@allure.epic("Petstore")
@allure.feature("User")
@allure.story("Delete user")
@pytest.mark.parametrize("name", ["a", "b"])
def test_deletes_user_by_name(api, name):
    rsp = api.delete(f"user/{name}")
    with allure.step("Checking the response code"):
        assert rsp.status_code in [
            200,
            404,
            400,
        ], f"The response code {rsp.status_code} does not match for user {name}"
    with allure.step("Deserializing the response from json to the dictionary"):
        if "Content-Type" in rsp.headers:
            if rsp.headers["Content-Type"] == "application/json":
                data = rsp.json()
                if "code" in data:
                    assert (
                        data["code"] == rsp.status_code
                    ), f"User {name} has not been deleted"


@allure.epic("Petstore")
@allure.feature("User")
@allure.story("Logs out current logged in user session")
def test_logs_out_user(api):
    rsp = api.get("user/logout")
    with allure.step("Checking the response code"):
        assert rsp.status_code in [
            200,
            404,
            400,
        ], f"The response code {rsp.status_code} does not match for user"
    with allure.step("Deserializing the response from json to the dictionary"):
        data = rsp.json()
        if "code" in data:
            assert data["code"] == rsp.status_code, f"User has not been logged out"


@allure.epic("Petstore")
@allure.feature("User")
@allure.story("Create user")
@pytest.mark.parametrize(
    "user",
    [
        {
            "id": 0,
            "username": "string",
            "firstName": "string",
            "lastName": "string",
            "email": "string",
            "password": "string",
            "phone": "string",
            "userStatus": 0,
        },
        {
            "id": 1,
            "username": "username",
            "firstName": "firstName",
            "lastName": "lastName",
            "email": "email",
            "password": "password",
            "phone": "55555",
            "userStatus": 7,
        },
    ],
)
def test_create_user(api, user):
    rsp = api.post("user", json=user)
    with allure.step("Checking the response code"):
        assert rsp.status_code in [
            200,
            404,
            400,
        ], f"The response code {rsp.status_code} does not match for user"
    with allure.step("Deserializing the response from json to the dictionary"):
        data = rsp.json()
        if "code" in data:
            assert data["code"] == rsp.status_code, f"User has not been created"


# Bonus
@allure.epic("Petstore")
@allure.feature("Store")
@allure.story("Try get head")
def test_head_of_order(api):
    rsp = api.head("store/order")
    with allure.step("Checking the response code"):
        assert rsp.status_code in [
            200,
            404,
            400,
            405,
        ], f"The response code {rsp.status_code} does not match for user"


@allure.epic("Petstore")
@allure.feature("Store")
@allure.story("Patch order")
@pytest.mark.parametrize(
    "pet",
    [
        {
            "id": 0,
            "petId": 0,
            "quantity": 0,
            "shipDate": "2023-12-11T17:00:08.169Z",
            "status": "placed",
            "complete": True,
        },
        {"id": -10},
    ],
)
def test_patch_an_order_for_a_pet(api, pet):
    rsp = api.patch("store/order", json=pet)
    with allure.step("Checking the response code"):
        assert rsp.status_code in [
            200,
            400,
            404,
            405,
        ], f"The response code {rsp.status_code} does not match for pet {pet['id']}"
    with allure.step("Deserializing the response from json to the dictionary"):
        data = rsp.json()
        if "code" in data:
            assert (
                data["code"] == rsp.status_code
            ), f"Order ID {pet['id']} has not been patched"
        else:
            assert "id" in data, f"Order ID {pet['id']} has not been patched"
