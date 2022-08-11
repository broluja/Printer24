from fastapi import APIRouter, Depends

from framework.middleware.authentication import SuperUser
from framework.exceptions.exceptions import ServerException
from src.repository.organisation_repository import organisation_repository
from src.repository.user_repository import user_repository


router = APIRouter(
    prefix='/organisations',
    tags=['organisations'],
    responses={404: {"description": "Not found"}}
)


@router.post('')
def create(name: str):
    """ Registering organisation. """
    if organisation_repository.get_by_name(name):
        return ServerException(message='This company already registered.', status_code=400)
    try:
        organisation_repository.create({'name': name})
    except Exception as e:
        print(e)
        return ServerException(message='Company creation failed.', status_code=500)


@router.put('')
def update(name: str, new_name: str, email: str, admin: SuperUser = Depends()):
    """ Updating organisation. """
    user = user_repository.get_by_email(email)
    organisation = organisation_repository.get_by_name(name)

    if user == admin.user:
        try:
            organisation_repository.update(organisation, fields={'organisation': new_name})
        except:
            raise ServerException(message="Failed.", status_code=400)
        return 'Your Organisation updated.'
    raise ServerException(message="No superuser status.", status_code=400)
