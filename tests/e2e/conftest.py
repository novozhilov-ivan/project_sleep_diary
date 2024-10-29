import pytest

from fastapi import FastAPI
from punq import Container, Scope
from sqlalchemy import Engine, create_engine, text
from starlette.testclient import TestClient

from src.application.api.main import create_app
from src.infra.database import Database
from src.infra.orm import ORMUser, metadata
from src.infra.repository import (
    INotesRepository,
)
from src.project.containers import get_container
from src.project.settings import Settings
from src.service_layer import Diary


def init_dummy_container() -> Container:
    return get_container()


@pytest.fixture(scope="session")
def settings() -> Settings:
    return Settings()


@pytest.fixture(scope="session", autouse=True)
def engine(settings: Settings) -> Engine:
    test_db_name = settings.test_postgres_db

    assert "test_" in test_db_name, "Защита от выполнения create/drop с основной БД"

    engine_for_create_db: Engine = create_engine(
        str(settings.POSTGRES_DB_URL),
        echo=False,
        isolation_level="AUTOCOMMIT",  # ???
    )

    connection_for_create_test_db = engine_for_create_db.connect()

    is_test_db_exists = connection_for_create_test_db.execute(
        text(f"SELECT 1 FROM pg_database " f"WHERE datname = '{test_db_name}';"),
    )

    if not is_test_db_exists.one_or_none():
        connection_for_create_test_db.execute(
            text(f"CREATE DATABASE {test_db_name};"),
        )
    if engine_for_create_db:
        engine_for_create_db.dispose()
    connection_for_create_test_db.close()

    return create_engine(settings.test_postgres_url)


@pytest.fixture
def database(settings: Settings, engine: Engine) -> Database:
    metadata.drop_all(engine)
    metadata.create_all(engine)

    return Database(settings.test_postgres_url)


@pytest.fixture(autouse=True)
def container(database: Database) -> Container:
    container = init_dummy_container()

    container.register(
        Database,
        instance=database,
        scope=Scope.singleton,
    )
    return container


@pytest.fixture
def user(container: Container) -> ORMUser:
    user = ORMUser(
        username="test_user",
        password=b"test_password",
    )
    database: Database = container.resolve(Database)

    with database.get_session() as session:
        session.add(user)
        session.commit()
        session.refresh(user)
    return user


@pytest.fixture
def repository(container: Container) -> INotesRepository:
    return container.resolve(INotesRepository)


@pytest.fixture
def diary(container: Container) -> Diary:
    return container.resolve(Diary)


@pytest.fixture
def app(container: Container) -> FastAPI:  # noqa: U100
    app = create_app()
    app.dependency_overrides[get_container] = init_dummy_container
    return app


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    return TestClient(app)
