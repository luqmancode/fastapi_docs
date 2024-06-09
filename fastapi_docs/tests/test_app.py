from httpx import AsyncClient
import pytest
from fastapi_docs import app
from fastapi import Depends
from typing import Annotated

# async def async_client():
#     async with AsyncClient(app=app, base_url="http://test") as async_client:
#         yield async_client

@pytest.mark.anyio
async def test_read_main():
    async with AsyncClient(app=app, base_url="http://luqman.com") as async_client:
        response = await async_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}

@pytest.mark.anyio
async def test_enum():
    async with AsyncClient(app=app, base_url="http://luqman.com") as async_client:
        response = await async_client.get('/enums/resnet')
    assert response.status_code == 200
    assert response.json() == "This is resnet"

@pytest.mark.anyio
async def test_read_item():
    async with AsyncClient(app=app, base_url="http://luqman.com") as async_client:
        response = await async_client.get('/items/foo?query=Mohamed&q=fixedquery')
    assert response.status_code == 200
    assert response.json() == {'item_id': 'foo', 'query': 'Mohamed'}