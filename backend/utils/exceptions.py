from fastapi import HTTPException

class SystemError(HTTPException):
    def __init__(self,detail:str="Internal system error"):
        super().__init__(status_code=500,detail=detail)