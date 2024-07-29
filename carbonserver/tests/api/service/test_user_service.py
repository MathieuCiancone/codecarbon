from unittest import mock
from uuid import UUID

from carbonserver.api.infra.repositories.repository_users import (
    SqlAlchemyRepository as UserSqlRepository,
)
from carbonserver.api.schemas import User, UserAuthenticate, UserAutoCreate, UserCreate
from carbonserver.api.services.user_service import UserService

API_KEY = "9INn3JsdhCGzLAuOUC6rAw"

ORG_ID = UUID("f52fe339-164d-4c2b-a8c0-f562dfce066d")

USER_ID = UUID("f52fe339-164d-4c2b-a8c0-f562dfce066d")
USER_ID_2 = UUID("e52fe339-164d-4c2b-a8c0-f562dfce066d")

USER_1 = User(
    id=USER_ID,
    name="Gontran Bonheur",
    email="xyz@email.com",
    api_key=API_KEY,
    organizations=["DataForGood"],
    is_active=True,
)

USER_2 = User(
    id=USER_ID_2,
    name="Jonnhy Monnay",
    email="1234+1@email.fr",
    api_key=API_KEY,
    organizations=["DataForGood"],
    is_active=True,
)

USER_AUTHENTICATE = UserAuthenticate(email="xyz@email.com", password="pwd")


def test_user_service_creates_correct_user_on_sign_up_from_auth_server():
    user_mock_repository: UserSqlRepository = mock.Mock(spec=UserSqlRepository)
    expected_id = USER_ID_2
    user_service: UserService = UserService(user_mock_repository)
    user_mock_repository.create_user.return_value = USER_2
    user_to_create: UserAutoCreate = UserAutoCreate(
        name="Gontran Bonheur", email="xyz@email.com", id=USER_ID_2
    )

    actual_db_user = user_service.create_user(user_to_create)

    user_mock_repository.create_user.assert_called_with(user_to_create)
    assert actual_db_user.id == expected_id


def test_user_service_retrieves_correct_user_by_id():
    user_mock_repository: UserSqlRepository = mock.Mock(spec=UserSqlRepository)
    expected_user: User = USER_1
    user_service: UserService = UserService(user_mock_repository)
    user_mock_repository.get_user_by_id.return_value = USER_1

    actual_saved_user = user_service.get_user_by_id(USER_ID)

    assert actual_saved_user.id == expected_user.id
    assert actual_saved_user.name == expected_user.name

