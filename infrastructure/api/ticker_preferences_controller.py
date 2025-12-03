from fastapi import APIRouter, Depends, HTTPException, Body, Request, Cookie
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from infrastructure.repository.ticker_preferences_repository import TickerPreferencesRepository
from infrastructure.api.auth.models_pydantic import TickerPreferencesCreate, TickerPreferencesUpdate, TickerPreferencesOut
from infrastructure.api.auth.auth import get_current_user
from sqlalchemy.exc import IntegrityError
import os

router = APIRouter(prefix="/api/preferences", tags=["preferences"])
ticker_repo = TickerPreferencesRepository()
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), '../../web'))

@router.post("/add")
def create_preference(pref: TickerPreferencesCreate, current_user: dict = Depends(get_current_user)):
    try:
        # Comprobar el número de preferencias existentes para el usuario
        user_id = str(current_user["id"])
        is_premium = current_user.get("is_premium", False)
        preferences = ticker_repo.get_by_user_id(user_id)
        num_preferences = len(preferences)
        max_preferences = 50 if is_premium else 5
        if num_preferences >= max_preferences:
            raise HTTPException(
                status_code=403,
                detail=f"Límite de preferencias alcanzado: {'Premium (50)' if is_premium else 'Freemium (5)'}"
            )
        created = ticker_repo.create(
            ticker=pref.ticker,
            drop_percentage=pref.drop_percentage,
            days=pref.days,
            user_id=user_id
        )
        if created:
            return {"success": True, "message": "Preferencia guardada correctamente."}
        else:
            raise HTTPException(status_code=409, detail="Ya existe una preferencia igual para este usuario.")
    except IntegrityError as e:
        if 'unique constraint' in str(e).lower() or 'duplicate key value' in str(e).lower():
            raise HTTPException(status_code=409, detail="Ya existe una preferencia igual para este usuario.")
        raise HTTPException(status_code=500, detail=f"Error de integridad: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.put("/{pref_id}")
def update_preference(pref_id: str, pref: TickerPreferencesUpdate):
    try:
        data = pref.model_dump(exclude_unset=True)
        updated = ticker_repo.update(pref_id, **data)
        if not updated:
            return {"success": False, "message": "No se encontró la preferencia para actualizar."}
        return {"success": True, "message": "Preferencia actualizada correctamente."}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}

@router.delete("/{pref_id}")
def delete_preference(pref_id: str):
    try:
        deleted = ticker_repo.delete(pref_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="No se encontró la preferencia para eliminar.")
        return {"success": True, "message": "Preferencia eliminada correctamente."}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.get("/")
def get_preferences(current_user: dict = Depends(get_current_user)):
    try:
        preferences = ticker_repo.get_by_user_id(str(current_user["id"]))
        return [
            {
                "id": str(p.id),
                "ticker": p.ticker,
                "drop_percentage": p.drop_percentage,
                "days": p.days
            } for p in preferences
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
