from fastapi import APIRouter, Depends
from email_validator import validate_email, EmailNotValidError
from typing import List

from framework.exceptions.exceptions import ServerException
from framework.middleware.authentication import Authenticated, SuperUser
from framework.security.security import get_password_hash, create_access_token
from src.repository.user_repository import user_repository
from src.services.user_service import UserService
from src.utils import generate_code, send_email
from email_templates.templates import RESET_PASSWORD_TEMPLATE

router = APIRouter(
    prefix='/users',
    tags=['users'],
    responses={404: {'description': 'Not found'}}
)


@router.post('/superuser')
def create_superuser(first_name: str, last_name: str, email: str, password: str, password2: str, company: str, ):
    """ Endpoint for superuser creation. Only owners has access. """
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
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'hashed_password': get_password_hash(password),
            'is_superuser': True,
            'company': company,
            'has_color': True,
            'limit': 1000
        })
    except Exception as e:
        print(e)
        return ServerException(message='User creation failed.', status_code=500)


@router.post('/register')
def register(first_name: str, last_name: str, email: str, admin: SuperUser = Depends()):
    """ Superuser`s endpoint for registering his workers. Individual registration, email used as a password. """
    try:
        valid = validate_email(email)
        email = valid.email
        if user_repository.get_by_email(email):
            return ServerException(message='User with this email already exists.', status_code=400)
    except EmailNotValidError as e:
        return ServerException(message=str(e), status_code=400)
    try:
        user_repository.create({
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'hashed_password': get_password_hash(email),
            'is_superuser': False,
            'company': admin.user.company
        })
    except Exception as e:
        print(e)
        return ServerException(message='User creation failed.', status_code=500)


@router.post('/bulk_register')
def bulk_register(iterable: List[str], admin: SuperUser = Depends()):
    """ Superuser`s endpoint for group registration. Using iterable with emails. Email used as password"""
    for email in iterable:
        full_name = email.split('@')[0]
        first_name, last_name = full_name.split('.')
        try:
            user_repository.create({
                'first_name': first_name.capitalize(),
                'last_name': last_name.capitalize(),
                'email': email,
                'hashed_password': get_password_hash(email),
                'is_superuser': False,
                'company': admin.user.company
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


@router.get("/reset_password")
def reset_password(email: str, authenticated: Authenticated = Depends()):
    """ Individual user endpoint for adjusting his own password. """
    user = user_repository.get_by_email(email)
    if user == authenticated.user:
        code = generate_code(5)
        try:
            user_repository.update(user, fields={'code': code})
            send_email(user.email, code=code, subject='Reset Password Code', template=RESET_PASSWORD_TEMPLATE)
        except:
            raise ServerException(message="Failed.", status_code=400)
        return 'Instructions are sent to your email.'
    raise ServerException(message="Be sure to use email you provided on registration.", status_code=400)


@router.get('/reset_password_complete')
def reset_password_complete(code: int, new_password: str, password_confirm):
    """ Completing password reset. """
    try:
        user = user_repository.get_by_code(code)
    except:
        raise ServerException(message="Wrong code.", status_code=400)
    if new_password != password_confirm:
        return ServerException(message='Your passwords do not match. Try again', status_code=400)
    password = get_password_hash(new_password)
    try:
        user_repository.update(user, fields={'hashed_password': password, 'code': None})
        return 'Account updated.'
    except Exception as e:
        print(e)
        return ServerException(message='Failed.')
