from pydantic import BaseModel, constr, conint


class GroupBase(BaseModel):
    group_name: str
    city: str

    class Config:
        orm_mode = True


class NodeBase(BaseModel):
    node: str
    group_id: int


class Node(NodeBase):
    node: str

    class Config:
        orm_mode = True


class ReadGroup(GroupBase):
    group_name: str
    id: int
    city: str
    nodes: list[Node] =[]

    class Config:
        orm_mode = True

