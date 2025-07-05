import os
from fastapi import APIRouter, HTTPException, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.crud import user_by_id, random_user, fetch_data, del_all_users, all_users


router = APIRouter()


templates_directory = os.path.abspath("app/static/templates")
templates = Jinja2Templates(directory=templates_directory)


@router.get("/", response_class=HTMLResponse)
async def read_root():
    file_path = os.path.abspath("app/static/templates/index.html")

    with open(file_path, encoding="utf-8") as f:
        return HTMLResponse(content=f.read(), status_code=200)


@router.get("/users", summary="Вывод пользователей с пагинацией")
async def get_all_users(
    skip: int = Query(0, alias="skip"),
    limit: int = Query(10, alias="limit")
):
    return await all_users(skip, limit)


@router.post("/", summary="Добавление новых подльзователей в БД")
async def add_users(request: Request):
    data = await request.json()
    n = data.get("n", 0)
    return await fetch_data(n)


@router.delete("/", summary="Удаление всех записей из БД")
async def delete_all_users():
    await del_all_users()


@router.get("/user_id/{user_id}", summary="Получение пользователя по id", response_class=HTMLResponse)
async def get_user_page(user_id: int):
    user = await user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return templates.TemplateResponse(
        "user_details.html",
        {"request": {}, "user": user}
    )


@router.get("/random", summary="Получение случайного пользователя", response_class=HTMLResponse)
async def get_random_user():
    user = await random_user()
    if not user:
        raise HTTPException(status_code=404, detail="No users found in database")

    return templates.TemplateResponse(
        "user_details.html",
        {"request": {}, "user": user}
    )
