from fastapi import APIRouter, Response
from fastapi.responses import RedirectResponse

router = APIRouter()

@router.post("/api/logout")
def logout():
    response = RedirectResponse(url="/login", status_code=303)
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")
    return response

