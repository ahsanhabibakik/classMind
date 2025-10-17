"""Routines API endpoints."""
from typing import Dict
from fastapi import APIRouter, Query, Depends
from pydantic import BaseModel, Field
from app.repos.routines_repo import RoutinesRepo
from app.core.auth import get_current_user, get_current_user_optional

router = APIRouter()
repo = RoutinesRepo()


# Pydantic models
class RoutineBase(BaseModel):
    """Base routine model with common fields."""
    title: str = Field(..., min_length=1, max_length=255, description="Routine title")
    time: str | None = Field(None, description="Time for the routine (e.g., '09:00 AM')")
    section_id: int | None = Field(None, description="Optional section ID")


class RoutineCreate(RoutineBase):
    """Model for creating a new routine."""
    pass


class RoutineUpdate(BaseModel):
    """Model for updating a routine (all fields optional)."""
    title: str | None = Field(None, min_length=1, max_length=255)
    time: str | None = None
    section_id: int | None = None


class RoutineResponse(RoutineBase):
    """Response model for a routine."""
    id: int
    created_at: str | None = None
    
    class Config:
        from_attributes = True


# API endpoints
@router.get("/", response_model=list[RoutineResponse])
def list_routines(
    limit: int | None = Query(
        default=None,
        ge=1,
        le=100,
        description="Maximum number of routines to return"
    ),
    user: Dict[str, str] | None = Depends(get_current_user_optional)
):
    """
    Get all routines.
    
    Optionally limit the number of results.
    If authenticated, returns only user's routines.
    """
    user_id = user["user_id"] if user else None
    return repo.list_routines(limit, user_id=user_id)


@router.get("/{routine_id}", response_model=RoutineResponse)
def get_routine(routine_id: int):
    """
    Get a specific routine by ID.
    
    Returns 404 if routine not found.
    """
    return repo.get_routine(routine_id)


@router.post("/", response_model=RoutineResponse, status_code=201)
def create_routine(
    routine: RoutineCreate,
    user: Dict[str, str] = Depends(get_current_user)
):
    """
    Create a new routine.
    
    Requires authentication.
    Returns the created routine with its ID.
    """
    routine_data = routine.model_dump(exclude_unset=True)
    routine_data["user_id"] = user["user_id"]  # Associate with authenticated user
    return repo.create_routine(routine_data)


@router.patch("/{routine_id}", response_model=RoutineResponse)
def update_routine(routine_id: int, routine: RoutineUpdate):
    """
    Update an existing routine.
    
    Only provided fields will be updated.
    Returns 404 if routine not found.
    """
    update_data = routine.model_dump(exclude_unset=True)
    if not update_data:
        return repo.get_routine(routine_id)  # No updates, just return current
    return repo.update_routine(routine_id, update_data)


@router.delete("/{routine_id}", response_model=RoutineResponse)
def delete_routine(
    routine_id: int,
    user: Dict[str, str] = Depends(get_current_user)
):
    """
    Delete a routine by ID.
    
    Requires authentication.
    Users can only delete their own routines.
    Returns the deleted routine.
    Returns 404 if routine not found or not owned by user.
    """
    return repo.delete_routine(routine_id, user_id=user["user_id"])
