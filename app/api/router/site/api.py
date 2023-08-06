from fastapi import FastAPI, Depends
from typing import Annotated, List

from sqlalchemy.orm import Session

from api.router.product_router import search_product, get_all_products
from api.schemas.product_schema import ProductSchemaSearch
from api.router.users_router import user, register, user_update, me
from api.schemas.users_schemas import UserSchema, CreateUserSchema
from api.router.order_router import create_order, order_list_by_user_id
from api.schemas.order_schema import OrderSchemaRead
from api.auth.admin_auth import login_for_access_token
from api.db.session import get_db
from api.models.product_model import CategoryModel
from api.router.category_router import category_list

app = FastAPI(title="Site")


@app.get("/api/users/me")
async def user_me(users: Annotated[dict, Depends(me)]):
    return users


"""
________________________________________________________________________________________________________________________
Login

"""


@app.get('/api/category/list', tags=["Category"])
async def category_by_id(
                         db: Session = Depends(get_db),
                         ):
    query = db.query(CategoryModel).all()
    return query


@app.post("/site/login", tags=["login"])
async def login(auth: Annotated[dict, Depends(login_for_access_token)]):
    return auth


@app.get('/api/search_product/', tags=["search"], response_model=List[ProductSchemaSearch])
async def delete_by_id(product: Annotated[dict, Depends(search_product)]):
    return product


@app.get('/api/site/get-all-products', tags=["Site"], response_model=List[ProductSchemaSearch])
async def delete_by_id(product: Annotated[dict, Depends(get_all_products)]):
    return product


@app.get("/api/user/get-user", response_model=UserSchema, tags=["User"])
async def get_user(users: Annotated[dict, Depends(user)]):
    return users


@app.post("/api/user/register", response_model=List[CreateUserSchema], tags=["User"])
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

