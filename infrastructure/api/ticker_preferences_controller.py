from fastapi import APIRouter, HTTPException, Depends
from infrastructure.repository.ticker_preferences_repository import TickerPreferencesRepository
from infrastructure.api.auth.models_pydantic import TickerPreferencesCreate, TickerPreferencesUpdate, TickerPreferencesOut
from infrastructure.api.auth.auth import get_current_user
from sqlalchemy.exc import IntegrityError

router = APIRouter(prefix="/preferences", tags=["preferences"])
ticker_repo = TickerPreferencesRepository()

@router.post("/add")
def create_preference(pref: TickerPreferencesCreate, current_user: dict = Depends(get_current_user)):
    try:
        created = ticker_repo.create(
            ticker=pref.ticker,
            drop_percentage=pref.drop_percentage,
            days=pref.days,
            user_id=str(current_user["id"])
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
