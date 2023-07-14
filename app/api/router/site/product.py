from fastapi import FastAPI, Depends
from typing import Annotated, List

from api.router.product_router import search_product, get_all_products
from api.schemas.product_schema import ProductSchemaSearch
from api.router.users_router import user, register, user_update
from api.schemas.users_schemas import User_Schema
from api.router.order_router import create_order, order_list_by_user_id
from api.schemas.order_schema import OrderSchemaRead

app = FastAPI(title="Site")


@app.get('/api/search_product/', tags=["search"], response_model=List[ProductSchemaSearch])
async def delete_by_id(product: Annotated[dict, Depends(search_product)]):
    return product


@app.get('/api/site/get-all-products', tags=["Site"], response_model=List[ProductSchemaSearch])
async def delete_by_id(product: Annotated[dict, Depends(get_all_products)]):
    return product


@app.get("/api/user/get-user", response_model=User_Schema, tags=["User"])
async def get_user(users: Annotated[dict, Depends(user)]):
    return users


@app.post("/api/user/register", response_model=List[User_Schema], tags=["User"])
async def registration(users: Annotated[dict, Depends(register)]):
    return users


@app.put("/api/user/update", tags=["User"])
async def update_user(users: Annotated[dict, Depends(user_update)]):
    return users


@app.post('/api/order/create', response_model=OrderSchemaRead, tags=["Order"])
async def update_user(order: Annotated[dict, Depends(create_order)]):
    return order


@app.get('/api/orders-list', response_model=List[OrderSchemaRead], tags=["Order"])
async def oder_by_user_id(order: Annotated[dict, Depends(order_list_by_user_id)]):
    return order
