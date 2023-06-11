from pydantic import BaseModel
import typing

class User(BaseModel):
    id:int 
    name:str

class Users(BaseModel):
    __root__:typing.List[User]


d = Users.parse_obj([{'id':1, 'name':'A'}, {'id':2, 'name':'B'}])
for user in d:
    print(user.id)