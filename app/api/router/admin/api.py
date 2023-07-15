from fastapi import FastAPI, Depends
from typing import Annotated, List

from api.router.product_router import product_list, create_product, product_by_id, update_product, delete_product
from api.schemas.product_schema import ProductSchemaReadV2
from api.schemas.admin_schema import Admin_Read_Schema
from api.router.amin_router import register, update_admin, user_list
from api.router.category_router import category_list, category_create, category_update, delete_category
from api.schemas.category_schema import CategorySchema
from api.router.colour_router import list_colours, colour_create, colour_update, delete_colour
from api.schemas.colour_schema import ColourSchema
from api.router.promocode_router import promocode_list, create_promocode, update_promocode, delete_promocode, \
    get_promocode_by_id
from api.schemas.promocode_schema import PromocodeReadSchema
from api.router.users_router import lists_users, list_users, delete_user, update_user_by_id
from api.schemas.users_schemas import User_Schema
from api.auth.admin_auth import login_for_access_token, refresh_token

app = FastAPI(title="Admin")

"""
________________________________________________________________________________________________________________________
Login

"""


@app.post("/login", tags=["login"])
async def login(auth: Annotated[dict, Depends(login_for_access_token)]):
    return auth


"""
________________________________________________________________________________________________________________________
Authenticate

"""


@app.post("/auth/token/", tags=["auth"])
async def access_token(auth: Annotated[dict, Depends(login_for_access_token)]):
    return auth


@app.post("/auth/refresh_token", tags=["auth"])
async def login_to_refresh_tocken(auth: Annotated[dict, Depends(refresh_token)]):
    return auth


"""
________________________________________________________________________________________________________________________
Admin

"""


@app.post("/api/admin/registr", response_model=List[Admin_Read_Schema], tags=["admin"])
async def create_admin(admin: Annotated[dict, Depends(register)]):
    return admin


@app.put("/api/admin/update", tags=["admin"])
async def update_admin(admin: Annotated[dict, Depends(update_admin)]):
    return admin


@app.get("/api/admin/admins-list", response_model=List[Admin_Read_Schema], tags=["admin"])
async def admin_list(admin: Annotated[dict, Depends(user_list)]):
    return admin


@app.delete("/api/admin/delete/{id}", tags=["admin"])
async def delete_admin(admin: Annotated[dict, Depends(user_list)]):
    return admin


"""
________________________________________________________________________________________________________________________
Product

"""


@app.get("/api/product/list-product",
         response_model=List[ProductSchemaReadV2], tags=["product"])
async def list_products(products: Annotated[dict, Depends(product_list)]):
    return products


@app.post("/api/product/create", response_model=ProductSchemaReadV2, tags=["product"])
async def create(products: Annotated[dict, Depends(create_product)]):
    return products


@app.get("/api/product/get/{id}/", response_model=List[ProductSchemaReadV2], tags=["product"])
async def get_by_id(product: Annotated[dict, Depends(product_by_id)]):
    return product


@app.put("/api/product/update/{id}", tags=["product"])
async def update_by_id(product: Annotated[dict, Depends(update_product)]):
    return product


@app.delete("/api/product/delete/{id}", tags=["product"])
async def delete_by_id(product: Annotated[dict, Depends(delete_product)]):
    return product


"""
________________________________________________________________________________________________________________________
Category

"""


@app.get('/api/category/list', tags=["category"])
async def category_list_(category: Annotated[dict, Depends(category_list)]):
    return category


@app.post("/api/category/create", response_model=CategorySchema, tags=["category"])
async def create_category(category: Annotated[dict, Depends(category_create)]):
    return category


@app.put("/api/category/update/{id}}", response_model=CategorySchema, tags=["category"])
async def create_update(category: Annotated[dict, Depends(category_update)]):
    return category


@app.delete("/api/category/delete/{id}", tags=["category"])
async def cagtegory_delete(category: Annotated[dict, Depends(delete_category)]):
    return category


"""
________________________________________________________________________________________________________________________
Colour

"""


@app.get("/api/colour/list", tags=["colour"])
async def colour_list(colour: Annotated[dict, Depends(list_colours)]):
    return colour


@app.post("/api/colour/create", response_model=ColourSchema, tags=["colour"])
async def create_colour(colour: Annotated[dict, Depends(colour_create)]):
    return colour


@app.put("/api/colour/update/{id}}", response_model=ColourSchema, tags=["colour"])
async def update_colour(colour: Annotated[dict, Depends(colour_update)]):
    return colour


@app.delete("/api/colour/delete/{id}", tags=["colour"])
async def colour_delete(colour: Annotated[dict, Depends(delete_colour)]):
    return colour


"""
________________________________________________________________________________________________________________________
Promocode

"""


@app.get("/api/promo-code/get-list-prom", response_model=List[PromocodeReadSchema], tags=["promocode"])
async def get_list_promocode(promocode: Annotated[dict, Depends(promocode_list)]):
    return promocode


@app.post("/api/promo-code/create", response_model=PromocodeReadSchema, tags=["promocode"])
async def promocode_create(promocode: Annotated[dict, Depends(create_promocode)]):
    return promocode


@app.put("/api/promo-code/update/{id}", response_model=PromocodeReadSchema, tags=["promocode"])
async def promocode_update(promocode: Annotated[dict, Depends(update_promocode)]):
    return promocode


@app.delete("/api/promo-code/delete/{id}", tags=["promocode"])
async def promocode_delete(promocode: Annotated[dict, Depends(delete_promocode)]):
    return promocode


@app.get("/api/promo-code/get-by/{id}", response_model=PromocodeReadSchema, tags=["promocode"])
async def promocode_by_id(promocode: Annotated[dict, Depends(get_promocode_by_id)]):
    return promocode


"""
________________________________________________________________________________________________________________________
Users

"""


@app.get("/api/users/user/{id}/", response_model=User_Schema, tags=["user"])
async def get_user_id(users: Annotated[dict, Depends(lists_users)]):
    return users


@app.get("/api/users/users-list", response_model=List[User_Schema], tags=["user"])
async def list_user(users: Annotated[dict, Depends(list_users)]):
    return users


@app.put("/api/users/update/{id}", tags=["user"])
async def update_user(users: Annotated[dict, Depends(update_user_by_id)]):
    return users


@app.delete("/api/users/delete/{id}", tags=["user"])
async def user_delete(users: Annotated[dict, Depends(delete_user)]):
    return users
