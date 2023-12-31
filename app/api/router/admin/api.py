from fastapi import FastAPI, Depends
from typing import Annotated, List

from api.router.product_router import product_list, create_product, product_by_id, update_product, delete_product
from api.schemas.product_schema import ProductSchemaReadV2
from api.schemas.admin_schema import Admin_Read_Schema
from api.router.amin_router import register, update_admin, admin_list, delete_admin, admin_by_ID
from api.router.category_router import category_list, category_create, category_update, delete_category, category_by_id
from api.schemas.category_schema import CategorySchema
from api.router.colour_router import list_colours, colour_create, colour_update, delete_colour, colour_by_id
from api.schemas.colour_schema import ColourSchema
from api.router.promocode_router import promocode_list, create_promocode, update_promocode, delete_promocode, \
    get_promocode_by_id
from api.schemas.promocode_schema import PromocodeReadSchema
from api.router.users_router import lists_users, list_users, delete_user, update_user_by_id, me
from api.schemas.users_schemas import UserSchema, UserSchemaRead, CreateUserSchema
from api.auth.admin_auth import login_for_access_token, refresh_token
from api.router.charecter_router import create_char_mobile, update_char_mobile, get_char_mobile, get_all_mobile_char, \
    dlete_mobile_char, create_character_comp, get_character_comp, update_character_comp, delete_comp_char, \
    get_all_comp_char
from api.schemas.charecter_schema import MobileCharSchemaRead, MobileCharSchemaReadV2, CompCharSchemaRead, \
    CompCharSchemaReadV2

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


@app.put("/api/admin/update/{id}", tags=["admin"])
async def update_admin(admin: Annotated[dict, Depends(update_admin)]):
    return admin


@app.get("/api/admin/admins-list", response_model=List[Admin_Read_Schema], tags=["admin"])
async def admin_list(admin: Annotated[dict, Depends(admin_list)]):
    return admin


@app.get("/api/admin/{id}", response_model=Admin_Read_Schema, tags=["admin"])
async def admin_by_id(admin: Annotated[dict, Depends(admin_by_ID)]):
    return admin

@app.delete("/api/admin/delete/{id}", tags=["admin"])
async def delete_admin(admin: Annotated[dict, Depends(delete_admin)]):
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


@app.get("/api/category/get-by/{id}", tags=["category"])
async def cagtegory_by_id(category: Annotated[dict, Depends(category_by_id)]):
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


@app.get("/api/colour/get-by/{id}", tags=["colour"])
async def colour_get_by(colour: Annotated[dict, Depends(colour_by_id)]):
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


@app.get("/api/users/user/{id}/", response_model=UserSchemaRead, tags=["user"])
async def get_user_id(users: Annotated[dict, Depends(lists_users)]):
    return users


@app.get("/api/users/users-list", response_model=List[UserSchemaRead], tags=["user"])
async def list_user(users: Annotated[dict, Depends(list_users)]):
    return users


@app.put("/api/users/update/{id}",response_model=List[CreateUserSchema], tags=["user"])
async def update_user(users: Annotated[dict, Depends(update_user_by_id)]):
    return users


@app.delete("/api/users/delete/{id}", tags=["user"])
async def user_delete(users: Annotated[dict, Depends(delete_user)]):
    return users


@app.get("/api/users/me")
async def user_me(users: Annotated[dict, Depends(me)]):
    return users

"""
________________________________________________________________________________________________________________________
Charecter mobile 

"""

@app.post("/app/char-mobile/create",response_model=MobileCharSchemaRead, tags=["Mobile-Char"])
async def create_char_mobile(char_mobile: Annotated[dict, Depends(create_char_mobile)]):
    return char_mobile

@app.put("/app/char-mobile/update/{char_id}",response_model=MobileCharSchemaRead, tags=["Mobile-Char"])
async def update_char_mobile(char_mobile: Annotated[dict, Depends(update_char_mobile)]):
    return char_mobile


@app.get("/app/char-mobile/{id}",response_model=MobileCharSchemaRead, tags=["Mobile-Char"])
async def get_char_mobile(char_mobile: Annotated[dict, Depends(get_char_mobile)]):
    return char_mobile


@app.get("/app/mobile-char/all", response_model=List[MobileCharSchemaReadV2], tags=["Mobile-Char"])
async def list_char_mobile(char_mobile: Annotated[dict, Depends(get_all_mobile_char)]):
    return char_mobile


@app.delete("/app/mobile-char/delete/{id}", tags=["Mobile-Char"])
async def delete_char_mobile(char_mobile: Annotated[dict, Depends(dlete_mobile_char)]):
    return char_mobile


"""
________________________________________________________________________________________________________________________
Charecter comp 

"""

@app.post('/app/char-comp/create', response_model=CompCharSchemaRead, tags=["Comp-Char"])
async def create_char_comp(char_comp: Annotated[dict, Depends(create_character_comp)]):
    return char_comp


@app.get('/app/char-comp/{id}', response_model=CompCharSchemaRead, tags=["Comp-Char"])
async def get_char_comp(char_comp: Annotated[dict, Depends(get_character_comp)]):
    return char_comp


@app.put('/app/char-comp/update/{char_id}', response_model=CompCharSchemaRead, tags=["Comp-Char"])
async def update_char_comp(char_comp: Annotated[dict, Depends(update_character_comp)]):
    return char_comp


@app.delete("/app/comp-char/delete/{id}", tags=["Comp-Char"])
async def delete_char_comp(char_comp: Annotated[dict, Depends(delete_comp_char)]):
    return char_comp


@app.get("/app/comp-char/all", response_model=List[CompCharSchemaReadV2], tags=["Comp-Char"])
async def list_char_comp(char_comp: Annotated[dict, Depends(get_all_comp_char)]):
    return char_comp
