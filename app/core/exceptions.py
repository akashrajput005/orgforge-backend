from fastapi import HTTPException


class OrgExistsException(HTTPException):
    def __init__(self, detail: str = "Organization already exists"):
        super().__init__(status_code=409, detail=detail)


class OrgNotFoundException(HTTPException):
    def __init__(self, detail: str = "Organization not found"):
        super().__init__(status_code=404, detail=detail)
