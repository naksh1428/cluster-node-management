from sqlalchemy.orm import session
from sqlalchemy.exc import IntegrityError
from fastapi import FastAPI, status, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, SessionLocal
from app.schemas import GroupBase, NodeBase, ReadGroup
import app.models as models

models.Base.metadata.create_all(bind=engine)
app = FastAPI(
    title="Cluster-Node-Management",
    redoc_url=None,
    version="0.0.1",
)
origins = [
    "http://localhost:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/v1/healthchecker")
async def root():
    return {'message': 'The API is Live!!'}


@app.post("/v1/group/", status_code=status.HTTP_201_CREATED)
async def create_group(group: GroupBase, db: session = Depends(get_db)):
    """ Create new group """
    try:

        db_group = models.Group(**group.model_dump())
        db.add(db_group)
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A Group already exist.",
        ) from e
    except Exception as e:
        db.rollback()
        # Handle other types of database errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the Group.",
        ) from e


@app.get("/v1/groups/", status_code=status.HTTP_200_OK)
async def get_all_groups(db: session = Depends(get_db)):
    """ Get list of all groups """
    return db.query(models.Group).all()


@app.get("/v1/group/{Group_Id}", response_model=ReadGroup, status_code=status.HTTP_200_OK)
async def get_group(group_id: int, db: session = Depends(get_db)):
    """ Get specific group """
    group = db.query(models.Group).filter(models.Group.id == group_id).first()
    if group is None:
        raise HTTPException(status_code=404, detail=f'Group {group_id} not Found')
    return group


@app.delete("/v1/group/{Group_Id}", status_code=status.HTTP_200_OK)
async def delete_group(group_id: int, db: session = Depends(get_db)):
    """ Delete the group """
    try:
        group = db.query(models.Group).filter(models.Group.id == group_id).first()
        if group is None:
            raise HTTPException(status_code=404, detail=f'Group {group_id} not Found')
        for node in group.nodes:
            update_node_group = db.get(models.Nodes, node.group_id)
            update_node_group.group_id = None
            db.add(update_node_group)
            db.commit()
        db.delete(group)
        db.commit()

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while deleting the group.",
        ) from e


@app.post("/v1/node/", status_code=status.HTTP_201_CREATED)
async def create_node(node: NodeBase, db: session = Depends(get_db)):
    """create new node"""
    try:
        # existing_node = db.query(models.Nodes).filter(models.Nodes.node == node.node,
        #                                               models.Nodes.group_id == node.group_id).first()
        # if existing_node:
        #     raise HTTPException(status_code=400, detail='Node already Exist')
        db_node = models.Nodes(**node.model_dump())
        db.add(db_node)
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=" Node already exists.",
        ) from e

    except Exception as e:
        db.rollback()
        # Handle other types of database errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating Node.",
        ) from e


@app.get("/v1/nodes/", status_code=status.HTTP_200_OK)
async def get_all_nodes(db: session = Depends(get_db)):
    """ get list of all nodes"""
    return db.query(models.Nodes).all()

