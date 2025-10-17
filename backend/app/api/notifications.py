from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_all_notifications():
    return {"data": []}

@router.post("/")
def create_notification():
    return {"message": "Notification created"}

@router.delete("/{notification_id}")
def delete_notification(notification_id: int):
    return {"message": f"Notification {notification_id} deleted"}
