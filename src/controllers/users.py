from fastapi import APIRouter, Depends
from email_validator import validate_email, EmailNotValidError

from framework.exceptions.exceptions import ServerException
from framework.security.security import get_password_hash, create_access_token
from src.repository.user_repository import user_repository
from src.services.user_service import UserService

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.post('/register')
def register(username: str, email: str, password: str, password2: str, superuser: bool, company: str):
    if password != password2:
        return ServerException(message='Your passwords do not match. Try again', status_code=400)

    try:
        valid = validate_email(email)
        email = valid.email
        if user_repository.get_by_email(email):
            return ServerException(message='User with this email already exists.', status_code=400)
    except EmailNotValidError as e:
        return ServerException(message=str(e), status_code=400)

    try:
        user_repository.create({
            'username': username,
            'email': email,
            'hashed_password': get_password_hash(password),
            'is_superuser': superuser,
            'company': company
        })
    except Exception as e:
        print(e)
        return ServerException(message='User creation failed.', status_code=500)


@router.get('/login')
def login(email: str, password: str, service: UserService = Depends()):
    user = user_repository.get_by_email(email)
    if not user:
        return ServerException(message="User with this email does not exist.", status_code=401)

    service.email = email
    service.password = password
    authenticated = service.authenticate()
    if authenticated is None:
        raise ServerException(message="Check your credentials", status_code=401)

    return create_access_token(authenticated.id.__str__(), authenticated.email)
