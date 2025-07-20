import aiohttp

base_url = 'http://127.0.0.1:8000/'

async def get_app_for_admin(app_id: int):
    async with aiohttp.ClientSession() as session:
        url = f"{base_url}admin/get_app/{app_id}"
        async with session.get(url) as response:
            if response.status == 200:
                return await response.json()
            else:
                return None

async def get_all_apps():
    async with aiohttp.ClientSession() as session:
        url = f"{base_url}admin/get_all_apps"
        async with session.get(url) as response:
            if response.status == 200:
                return await response.json()
            else:
                return None