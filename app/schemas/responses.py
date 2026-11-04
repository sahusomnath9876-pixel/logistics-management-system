from pydantic import BaseModel, ConfigDict


class UserResponse(BaseModel):
    user_id : int
    mobile_no : str

    model_config = ConfigDict(from_attributes=True)