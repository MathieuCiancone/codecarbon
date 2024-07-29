from typing import List

from container import ServerContainer
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status

from carbonserver.api.schemas import User, UserAutoCreate
from carbonserver.api.services.signup_service import SignUpService
from carbonserver.api.services.user_service import UserService

USERS_ROUTER_TAGS = ["Users"]

router = APIRouter()


@router.post(
    "/users/signup",
    tags=USERS_ROUTER_TAGS,
    status_code=status.HTTP_201_CREATED,
    response_model=User,
)
@inject
def sign_up(
    user: UserAutoCreate,
    signup_service: SignUpService = Depends(Provide[ServerContainer.sign_up_service]),
) -> User:
    return signup_service.sign_up(user)


@router.get(
    "/users/{user_id}",
    tags=USERS_ROUTER_TAGS,
    status_code=status.HTTP_200_OK,
    response_model=User,
)
@inject
def get_user_by_id(
    user_id: str,
    user_service: UserService = Depends(Provide[ServerContainer.user_service]),
) -> User:
    return user_service.get_user_by_id(user_id)
