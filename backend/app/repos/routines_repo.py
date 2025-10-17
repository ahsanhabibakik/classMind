"""Repository for routines table operations."""
from typing import Any
from fastapi import HTTPException
from app.core.supabase_client import supabase


class RoutinesRepo:
    """Repository for managing routines in Supabase."""
    
    def __init__(self):
        self.table_name = "routines"
    
    def list_routines(self, limit: int | None = None, user_id: str | None = None) -> list[dict[str, Any]]:
        """
        List all routines, optionally limited and filtered by user.
        
        Args:
            limit: Maximum number of routines to return
            user_id: Optional user ID to filter routines
            
        Returns:
            List of routine dictionaries
            
        Raises:
            HTTPException: If database query fails
        """
        try:
            query = supabase.table(self.table_name).select("*")
            
            if user_id:
                query = query.eq("user_id", user_id)
            
            if limit:
                query = query.limit(limit)
            
            response = query.execute()
            return response.data or []
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to fetch routines: {str(e)}"
            )
    
    def get_routine(self, routine_id: int) -> dict[str, Any]:
        """
        Get a single routine by ID.
        
        Args:
            routine_id: ID of the routine to fetch
            
        Returns:
            Routine dictionary
            
        Raises:
            HTTPException: If routine not found or query fails
        """
        try:
            response = supabase.table(self.table_name)\
                .select("*")\
                .eq("id", routine_id)\
                .execute()
            
            if not response.data:
                raise HTTPException(
                    status_code=404,
                    detail=f"Routine with id {routine_id} not found"
                )
            
            return response.data[0]
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to fetch routine: {str(e)}"
            )
    
    def create_routine(self, payload: dict[str, Any]) -> dict[str, Any]:
        """
        Create a new routine.
        
        Args:
            payload: Routine data to insert
            
        Returns:
            Created routine dictionary
            
        Raises:
            HTTPException: If creation fails
        """
        try:
            response = supabase.table(self.table_name)\
                .insert(payload)\
                .execute()
            
            if not response.data:
                raise HTTPException(
                    status_code=500,
                    detail="Failed to create routine: no data returned"
                )
            
            return response.data[0]
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to create routine: {str(e)}"
            )
    
    def update_routine(self, routine_id: int, payload: dict[str, Any]) -> dict[str, Any]:
        """
        Update an existing routine.
        
        Args:
            routine_id: ID of the routine to update
            payload: Updated routine data
            
        Returns:
            Updated routine dictionary
            
        Raises:
            HTTPException: If routine not found or update fails
        """
        try:
            response = supabase.table(self.table_name)\
                .update(payload)\
                .eq("id", routine_id)\
                .execute()
            
            if not response.data:
                raise HTTPException(
                    status_code=404,
                    detail=f"Routine with id {routine_id} not found"
                )
            
            return response.data[0]
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to update routine: {str(e)}"
            )
    
    def delete_routine(self, routine_id: int, user_id: str | None = None) -> dict[str, Any]:
        """
        Delete a routine by ID.
        
        Args:
            routine_id: ID of the routine to delete
            user_id: Optional user ID to verify ownership
            
        Returns:
            Deleted routine dictionary
            
        Raises:
            HTTPException: If routine not found or deletion fails
        """
        try:
            query = supabase.table(self.table_name).delete()
            
            # Filter by ID
            query = query.eq("id", routine_id)
            
            # If user_id provided, ensure ownership
            if user_id:
                query = query.eq("user_id", user_id)
            
            response = query.execute()
            
            if not response.data:
                raise HTTPException(
                    status_code=404,
                    detail=f"Routine with id {routine_id} not found or you don't have permission to delete it"
                )
            
            return response.data[0]
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to delete routine: {str(e)}"
            )
