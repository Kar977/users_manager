from fastapi import APIRouter

from employees.schemas import (
    CreateUser,
    SetUserPasswordEmail,
    DeleteUserAccount,
    ModifyUser,
    NewMember,
    ModifyClientType,
)
from employees.services.users import user_manager_obj

router = APIRouter()


@router.post("/user", status_code=201)
async def create_user(user_request: CreateUser):
    return await user_manager_obj.create_user(
        email=user_request.email,
        name=user_request.name,
        family_name=user_request.family_name,
        username=user_request.username,
    )


@router.get("/users", status_code=200)
async def get_all_users():
    return await user_manager_obj.list_users()


@router.get("/user/by_email", status_code=200)
async def get_user_by_email(email: str):
    return await user_manager_obj.get_user_id_by_email(email)


@router.post("/user/password_change", status_code=201)
async def send_password_email_ticket(user_request: SetUserPasswordEmail):
    return await user_manager_obj.send_email_with_password_change(
        email=user_request.user_email
    )


@router.delete("/user", status_code=204)
async def delete_user(user_request: DeleteUserAccount):
    return await user_manager_obj.delete_user(email=user_request.email)


@router.put("/user", status_code=200)
async def modify_user(user_request: ModifyUser):
    return await user_manager_obj.modify_user(
        user_id=user_request.user_id,
        blocked=user_request.blocked,
        email_verified=user_request.email_verified,
        email=user_request.email,
        phone_number=user_request.phone_number,
        phone_verified=user_request.phone_verified,
        user_metadata=user_request.user_metadata,
        app_metadata=user_request.app_metadata,
        given_name=user_request.given_name,
        family_name=user_request.family_name,
        name=user_request.name,
        nickname=user_request.nickname,
        picture=user_request.picture,
        verify_email=user_request.verify_email,
        verify_phone_number=user_request.verify_phone_number,
        password=user_request.password,
        connection=user_request.connection,
        client_id=user_request.client_id,
        username=user_request.username,
    )


@router.post("/send_invitation", status_code=200)
async def send_invitation(user_request: NewMember):
    return await user_manager_obj.invite_user_to_organization(user_request.email)


@router.patch("/change_client_type", status_code=200)
async def change_client_type(user_request: ModifyClientType):
    return await organization_manager_obj.change_client_type(
        user_request.client_id, user_request.app_type
    )
