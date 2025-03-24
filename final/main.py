from contextlib import asynccontextmanager
from typing import Annotated
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastui import FastUI, AnyComponent, prebuilt_html, components as c
from fastui.components.display import DisplayMode, DisplayLookup
from fastui.events import GoToEvent, BackEvent
from fastui.forms import fastui_form
from database.db import engine
from sqlmodel import Session, select

from schemas import UserForm, DeleteUserForm
from database.models import User
c.Link.model_rebuild()

@asynccontextmanager
async def lifespan(app: FastAPI):
    users = []
    with Session(engine) as session:
        for user in users:
            db_user = session.get(User, user.id)
            if db_user is not None:
                continue
            session.add(user)
        session.commit()
    yield


app = FastAPI(lifespan=lifespan)



@app.get('/api/user/add/', response_model=FastUI, response_model_exclude_none=True)
def add_user():
    return [
        c.Page( 
            components=[
                c.Heading(text='Add User', level=2),
                c.Paragraph(text='Add a user to the system'),
                c.ModelForm(model=UserForm,
                    submit_url='/api/user/add/'
                ),
            ]
        )
    ]   

@app.post('/api/user/add/')
async def add_user(form: Annotated[UserForm, fastui_form(UserForm)]) -> list[AnyComponent]:
    with Session(engine) as session:
        user = User(**form.model_dump())
        session.add(user)
        session.commit()

    return [c.FireEvent(event=GoToEvent(url='/'))]


@app.get("/api/", response_model=FastUI, response_model_exclude_none=True)
def users_table() -> list[AnyComponent]:
    with Session(engine) as session:
        users = session.exec(select(User)).all()

    return [
        c.Page(components=[
            c.Heading(text='Users', level=2),
            c.Table(
                data=users,
                data_model=User,
                columns=[
                    DisplayLookup(field='name', on_click=GoToEvent(url='/user/{id}/')),
                    DisplayLookup(field='dob', mode=DisplayMode.date),
                ],
            ),
            c.Div(components=[
                c.Link(
                    components=[c.Button(text='Add User')],
                    on_click=GoToEvent(url='/user/add/'),
                ),
            ])
        ]
        ),
    ]
@app.get("/api/user/{user_id}/", response_model=FastUI, response_model_exclude_none=True)
def user_profile(user_id: int) -> list[AnyComponent]:
    with Session(engine) as session:
        user = session.get(User, user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        
    return [
        c.Page(
            components=[
                c.Heading(text=user.name, level=2),
                c.Link(components=[c.Text(text='Back')], on_click=BackEvent()),
                c.Details(data=user),
                c.Div(components=[
                    c.Heading(text="Delete User?", level=4),
                    c.ModelForm(model=DeleteUserForm,
                        submit_url=f'/api/user/{user_id}/delete/',
                        class_name="text-left"
                    )
                ], class_name="card p-4 col-4")
            ]
        ),
    ]

@app.post('/api/user/{user_id}/delete/')
async def delete_user(
    user_id: int, 
    form: Annotated[DeleteUserForm, fastui_form(DeleteUserForm)]
) -> list[AnyComponent]:
    with Session(engine) as session:
        user = session.get(User, user_id)
        if user is not None:
            session.delete(user)
            session.commit()

    return [c.FireEvent(event=GoToEvent(url='/'))]


@app.get('/{path:path}')
async def html_landing() -> HTMLResponse:
    return HTMLResponse(prebuilt_html(title='FastUI Demo'))