from fastapi import APIRouter


router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.post('/register')
def register(
        username: str,
        email: str,
        password: str,
        password2: str):
    return True
