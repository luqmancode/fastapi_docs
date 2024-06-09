
from fastapi import FastAPI, Query, Depends, Cookie, Header, Response, status, Form, File, UploadFile, HTTPException
from typing import Union, Annotated, Any
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, RedirectResponse
from req_model import ModelName, ItemModel


app = FastAPI()
# code for multiple model file

items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}


@app.get('/')
async def read_root():
    return {"Hello": "World"}

@app.get('/enums/{model}')
async def read_model(model: ModelName):
    if model == ModelName.alexnet:
        return "This is Alexnet Model"
    elif model == ModelName.resnet:
        return "This is resnet"
    return "This is other DL model"

@app.get('/items/{item_id}')
async def read_item(item_id: str, query: Union[str, None] = None, q: Annotated[str | None, Query(min_length=3, max_length=50, pattern="^fixedquery$")] = None):
    items = {"foo": "The Foo Wrestlers"}
    if item_id not in items:
        raise HTTPException(status_code=404, detail='Item not found')
    return {"item_id": item_id, "query": query}

@app.put('/items/{item_id}', status_code=status.HTTP_201_CREATED)
async def put_contents(item_id: int, item: ItemModel, query_optional: str | None = None):
    result = {"name": item.name, "price": item.price, "has_offer": item.has_offer, "item_id": item_id}
    if query_optional:
        result.update({"query_params": query_optional})
    return result 
# // http://127.0.0.1:8000/items/100?query_optional=yes
# {
#   "name": "Bread",
#   "price": 100,
#   "has_offer": true,
#   "item_id": 100,
#   "query_params": "yes"
# }

@app.get('/files/{file_path:path}')
async def get_files(file_path: str):
    return {"file path": file_path}
    # http://127.0.0.1:8000/files/hi/hello/bye

print(111, ModelName.alexnet, '|', ModelName.alexnet.name)
print(222, ModelName.alexnet.value)
print(333, ModelName)
print(444, ModelName.alexnet == ModelName.alexnet.value)
print(555, ModelName.alexnet is ModelName.alexnet.value)

# Query Parameters
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}, {"item_name": "Doo"}, {"item_name": "Sar"},]

@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 2):
    return fake_items_db[skip : skip + limit]
    # http://127.0.0.1:8000/items/?limit=4 // [{"item_name":"Foo"},{"item_name":"Bar"},{"item_name":"Baz"},{"item_name":"Doo"}]

@app.get("/users/{user_id}/items/{item_id}")
async def multiple_path_query_params(
    user_id: int, item_id: str, q: str | None = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item
# http://127.0.0.1:8000/users/50/items/100?q=query&short=false
# {
#   "item_id": "100",
#   "owner_id": 50,
#   "q": "query",
#   "description": "This is an amazing item that has a long description"
# }

@app.post("/items/", status_code=201)
async def request_body(item: ItemModel) -> ItemModel:
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict
# http://127.0.0.1:8000/items/
# {
#   "name": "Pen",
#   "description": "Held in your finger",
#   "price": 10,
#   "tax": 2,
#   "has_offer": true,
#   "price_with_tax": 12
# }

@app.put("/items/{item_id}")
async def request_body_with_path_parameters(item_id: int, item: ItemModel):
    return {"item_id": item_id, **item.dict()}


@app.get("/items_id/")
async def query_params_string_validation(
    q: Annotated[
        Union[str, None],
        Query(
            title="Query string",
            description="Query string for the items to search in the database that have a good match",
            min_length=3,
            max_length=50,
            pattern="^fixedquery$",
            deprecated=True
        ),
    ] = None,
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    print(q, 2222222)
    if q:
        results.update({"q": q})
    return results
# http://127.0.0.1:8000/items_id/?q=qqquery
# {
#   "items": [
#     {
#       "item_id": "Foo"
#     },
#     {
#       "item_id": "Bar"
#     }
#   ],
#   "q": "qqquery"
# }
# but on input
# http://127.0.0.1:8000/items_id/?q=qqq
# {
#   "items": [
#     {
#       "item_id": "Foo"
#     },
#     {
#       "item_id": "Bar"
#     }
#   ],
#   "q": "qqq"
# }

@app.get("/get_cookie/")
async def get_cookie(ads_id: Annotated[str | None, Cookie()] = None):
    return {"ads_id": ads_id}

# http://127.0.0.1:8000/get_cookie/
# {
#   "ads_id": null
# }
# It doesnot take the value of ads_id and its not fetching

# headers
@app.get("/headers/")
async def read_headers(user_agent: Annotated[str | None, Header()] = None):
    return {"User-Agent": user_agent}
# {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"}

@app.get("/all_items/")
async def read_all_items() -> list[ItemModel]:
    return [
        ItemModel(name="Portal Gun", price=42.0),
        ItemModel(name="Plumbus", price=32.0),
    ]
# Response Model:
@app.get("/resp_all_items/", response_model = list[ItemModel])
async def resp_all_items() -> Any:
    return [
        ItemModel(name="Portal Gun", price=42.0),
        ItemModel(name="Plumbus", price=32.0),
    ]
# [
#   {
#     "name": "Portal Gun",
#     "description": null,
#     "price": 42,
#     "tax": null,
#     "has_offer": null
#   },
#   {
#     "name": "Plumbus",
#     "description": null,
#     "price": 32,
#     "tax": null,
#     "has_offer": null
#   }
# ]

@app.get("/portal")
async def get_portal(teleport: bool = False) -> Response:
    if teleport:
        return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    return JSONResponse(content={"message": "Here's your interdimensional portal."})

# http://127.0.0.1:8000/portal?teleport=false
# {
#   "message": "Here's your interdimensional portal."
# }
# http://127.0.0.1:8000/portal?teleport=true
	
# Failed to fetch.
# Possible Reasons:

# CORS
# Network Failure
# URL scheme must be "http" or "https" for CORS request.

@app.get("/get_teleport")
async def g_teleport() -> RedirectResponse:
    return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")



@app.get("/exclude_unset/{item_id}", response_model=ItemModel, response_model_exclude_unset=True)
async def exclude_unset_item(item_id: str):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found", 
                            headers={"X-Error": "There goes my error"})
    return items[item_id]
# On False:
# {
#   "name": "Baz",
#   "description": null,
#   "price": 50.2,
#   "tax": 10.5,
#   "has_offer": null,
#   "tags": []
# }
# On True:
# {
#   "name": "Baz",
#   "description": null,
#   "price": 50.2,
#   "tax": 10.5,
#   "tags": []
# }

# Form Data
@app.post("/login/")
async def login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    return {"username": username, "password": password}

# Request Files
@app.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file), "file": file[:1000]}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}

@app.get("/res_items/{item_id}", response_model=ItemModel)
async def read_item(item_id: str):
    return items[item_id]

@app.put("/res_items/{item_id}", response_model=ItemModel)
async def update_item(item_id: str, item: ItemModel):
    update_item_encoded = jsonable_encoder(item)
    items[item_id] = update_item_encoded
    return update_item_encoded

@app.patch("/res_items/{item_id}", response_model=ItemModel)
async def update_item(item_id: str, item: ItemModel):
    stored_item_data = items[item_id]
    stored_item_model = ItemModel(**stored_item_data)
    print(111, item.dict())
    update_data = item.dict(exclude_unset=True)
    print(222, update_data)
    updated_item = stored_item_model.copy(update=update_data)
    items[item_id] = jsonable_encoder(updated_item)
    return updated_item


async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}


@app.get("/users/")
async def read_users(commons: Annotated[dict, Depends(common_parameters)]):
    return commons

# To run : uvicorn main:app --reload
# http://127.0.0.1:8000/items/342?query=fame
# {"item_id":342,"query":"fame"}