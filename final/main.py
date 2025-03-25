from contextlib import asynccontextmanager
from typing import Annotated
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastui import FastUI, prebuilt_html, components as c
from fastui.components import AnyComponent
from fastui.components.display import DisplayMode, DisplayLookup
from fastui.events import GoToEvent, BackEvent
from fastui.forms import fastui_form
from database.db import engine, create_db_and_tables
from sqlmodel import Session, select
from passlib.context import CryptContext
from fastapi.security import HTTPBasic
from schemas import TaskForm, DeleteTaskForm
from database.models import Task

c.Link.model_rebuild()


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBasic()


@app.get('/api/task/add/', response_model=FastUI, response_model_exclude_none=True)
def add_task():
    return [
        c.Page(
            components=[
                c.Heading(text='Добавление Задачи', level=2),
                c.Button(text='Назад', on_click=BackEvent()),
                c.Paragraph(text='Добавление Задачи в систему'),
                c.ModelForm(model=TaskForm,
                            submit_url='/api/task/add/'
                            ),
            ]
        )
    ]


@app.post('/api/task/add/')
async def add_task(form: Annotated[TaskForm, fastui_form(TaskForm)]) -> list[AnyComponent]:
    with Session(engine) as session:
        task = Task(**form.model_dump())
        session.add(task)
        session.commit()

    return [c.FireEvent(event=GoToEvent(url='/'))]


@app.get("/api/", response_model=FastUI, response_model_exclude_none=True)
def tasks_table() -> list[AnyComponent]:
    with Session(engine) as session:
        tasks = session.exec(select(Task)).all()

    return [
        c.Page(components=[
            c.Heading(text='Задачи', level=2),
            c.Table(
                data=tasks,
                data_model=Task,
                columns=[DisplayLookup(field='dob', title='Дата', mode=DisplayMode.date),
                         DisplayLookup(field='name', title='Название', on_click=GoToEvent(url='/task/{id}/')),
                         DisplayLookup(field='task', title='Задача'),
                         DisplayLookup(field='date_create', title='Дата изготовления', mode=DisplayMode.date),
                         DisplayLookup(field='who_cook', title='Кто приготовил'),
                         DisplayLookup(field='who_comp', title='Кто выполнил'),
                         DisplayLookup(field='result', title='Результат')
                         ],
            ),
            c.Div(components=[
                c.Link(
                    components=[c.Button(text='Добавить Задачу')],
                    on_click=GoToEvent(url='/task/add/'),
                ),
            ])
        ]
        ),
    ]


@app.get("/api/task/{task_id}/", response_model=FastUI, response_model_exclude_none=True)
def task_profile(task_id: int) -> list[AnyComponent]:
    with Session(engine) as session:
        task = session.get(Task, task_id)
        if task is None:
            raise HTTPException(status_code=404, detail="Задача не найдена")

    return [
        c.Page(
            components=[
                c.Heading(text=task.name, level=2),
                c.Button(text='Назад', on_click=BackEvent()),
                c.Details(data=task),
                c.Div(components=[
                    c.Heading(text="Удалить задачу?", level=4),
                    c.ModelForm(model=DeleteTaskForm,
                                submit_url=f'/api/task/{task_id}/delete/',
                                class_name="text-left"
                                )
                ], class_name="card p-4 col-4")
            ]
        ),
    ]


@app.post('/api/task/{task_id}/delete/')
async def delete_task(
        task_id: int) -> list[AnyComponent]:
    with Session(engine) as session:
        task = session.get(Task, task_id)
        if task is not None:
            session.delete(task)
            session.commit()

    return [c.FireEvent(event=GoToEvent(url='/'))]


@app.get('/{path:path}')
async def html_landing():
    return HTMLResponse(prebuilt_html(title='Диплом'))