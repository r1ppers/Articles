from fastapi import HTTPException

def given_error(error_text: str, object_to_check: bool, status: int):
    if not object_to_check:
        raise HTTPException(status_code=status, detail=error_text)