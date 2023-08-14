from fastapi import FastAPI, Depends
from typing import Annotated, List

from sqlalchemy.orm import Session, joinedload
from starlette import status
from starlette.responses import JSONResponse

from api.router.product_router import search_product, get_all_products
from api.schemas.product_schema import ProductSchemaSearch, ProductImageSchema, ProductSchemaReadV2
from api.router.users_router import user, register, user_update, me
from api.schemas.users_schemas import UserSchema, CreateUserSchema
from api.router.order_router import create_order, order_list_by_user_id
from api.schemas.order_schema import OrderSchemaRead
from api.auth.admin_auth import login_for_access_token
from api.db.session import get_db
from api.models.product_model import CategoryModel, ColourModel, ProductModel, ProductImage, ColourProduct, Promocode
from api.router.category_router import category_list, category_by_product
from api.router.colour_router import list_colours
from api.schemas.category_schema import CategorySchema
from api.schemas.colour_schema import ProductColourSchema
from api.schemas.promocode_schema import PromocodeReadSchema

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


@app.get('/api/category/by-{id}', response_model=List[ProductSchemaSearch], tags=["Category"])
async def category_by_id(category: Annotated[dict, Depends(category_by_product)]):
    return category


@app.get('/api/colour/list', tags=["Colour"])
async def list_colours(db: Session = Depends(get_db)):
    query = db.query(ColourModel).all()
    return query


@app.get('/api/product/{id}', response_model=List[ProductSchemaReadV2], tags=["Product"])
async def product_by_id(id: int,
                        db: Session = Depends(get_db),

                        ):
    query = (
        db.query(ProductModel)
        .join(ProductImage, ProductModel.id == ProductImage.product_id)
        .join(CategoryModel, ProductModel.category_id == CategoryModel.id)
        .join(ColourProduct, ProductModel.id == ColourProduct.product_id)
        .join(Promocode, ProductModel.promocode_id == Promocode.id)
        .options(joinedload(ProductModel.images))
        .filter(ProductModel.id == id)
        .first()
    )

    if query is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=f"Product {id} not found"
        )

    images = [
        ProductImageSchema(file_name=image.file_name, file_path=image.file_path)
        for image in query.images
    ]

    query_to_category = db.query(CategoryModel).filter(CategoryModel.id == query.category_id).first()

    colour_data = db.query(ColourProduct).filter(ColourProduct.product_id == query.id).all()

    product_data = ProductSchemaReadV2(
        id=query.id,
        title=query.title,
        description=query.description,
        category=[CategorySchema(id=query.category_id, title=query_to_category.title)],
        images=images,
        owner=query.owner,
        created_at=query.created_at,
        count=query.count,
        procent_sale=query.procent_sale,
        promocode=[PromocodeReadSchema(id=query.promocode_rel.id,
                                       name=query.promocode_rel.name,
                                       procent=query.promocode_rel.procent,
                                       category=[query.promocode_rel.category_rel])],
        colour=[ProductColourSchema(id=colour.id, product_id=colour.product_id, colour_id=colour.colour_id)
                for colour in colour_data],
        price=query.price,
        visible=query.visible

    )

    return [product_data]
