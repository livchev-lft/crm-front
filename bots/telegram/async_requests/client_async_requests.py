import aiohttp

base_url = 'http://127.0.0.1:8000/'

async def client_check(client_id: int)->dict:
    async with aiohttp.ClientSession() as session:
        url = f"{base_url}client/check_client?client_id={client_id}"
        async with session.get(url) as response:
            if response.status == 200:
                return await response.json()
            else:
                return {}

async def reg_client_request(client_data: dict)->bool:
    async with aiohttp.ClientSession() as session:
        url = f"{base_url}client/register_client"
        async with session.post(url, json=client_data) as response:
            if response.status == 201:
                return True
            else:
                return False

async def check_cars(client_id: int)->list[dict]:
    async with aiohttp.ClientSession() as session:
        url = f"{base_url}client/mycars/{client_id}"
        async with session.get(url) as response:
            if response.status == 200:
                return await response.json()
            else:
                return []

async def add_car_request(data: dict)->bool:
    async with aiohttp.ClientSession() as session:
        url = f"{base_url}client/addcar"
        async with session.post(url, json=data) as response:
            if response.status == 200:
                return True
            else:
                return False

async def delete_car_request(car_id: int)->bool:
    async with aiohttp.ClientSession() as session:
        url = f"{base_url}client/delete_car/{car_id}"
        async with session.delete(url) as response:
            if response.status == 204:
                return True
            else:
                return False

async def post_app_request(data: dict)->dict | None:
    async with aiohttp.ClientSession() as session:
        url = f"{base_url}client/addapp"
        async with session.post(url, json=data) as response:
            if response.status == 200:
                return await response.json()
            else:
                return None

async def replace_phone_request(client_id: int, phone: str)->bool:
    async with aiohttp.ClientSession() as session:
        url = f"{base_url}client/replace_phone"
        params = {"client_id": client_id, "phone": phone}
        async with session.patch(url, params=params) as response:
            if response.status == 200:
                return True
            else:
                return False

async def check_apps(client_id: int)->dict:
    async with aiohttp.ClientSession() as session:
        url = f"{base_url}client/get_apps?client_id={client_id}"
        async with session.get(url) as response:
            if response.status == 200:
                return await response.json()
            else:
                return {}

async def check_car_app(car_id: int)->bool:
    async with aiohttp.ClientSession() as session:
        url = f"{base_url}client/check_car_app?car_id={car_id}"
        async with session.get(url) as response:
            if response.status == 200:
                return True
            else:
                return False

async def check_client_car(car_id: int)->dict:
    async with aiohttp.ClientSession() as session:
        url = f"{base_url}client/check_client_car?car_id={car_id}"
        async with session.get(url) as response:
            if response.status == 200:
                return await response.json()
            else:
                return {}