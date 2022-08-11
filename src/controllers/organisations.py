from fastapi import APIRouter

from src.repository.organisation_repository import organisation_repository
from framework.exceptions.exceptions import ServerException


router = APIRouter(
    prefix='/organisations',
    tags=['organisations'],
    responses={404: {"description": "Not found"}},
)


@router.post('')
def create(name: str):
    """ Registering organisation """
    if organisation_repository.get_by_name(name):
        return ServerException(message='This company already registered.', status_code=400)
    try:
        organisation_repository.create({
            'organisation': name
        })
    except Exception as e:
        print(e)
        return ServerException(message='Company creation failed.', status_code=500)


@router.put('')
def update(name: str):
    return True
