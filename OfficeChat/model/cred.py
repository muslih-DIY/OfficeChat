

from typing import Any, Dict,List
from sqlmodel import Session,SQLModel,select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException,APIRouter,Depends
from ..depends.database import get_db_Session



class NotFound(HTTPException):
    def __init__(self, status_code: int=404, detail: Any = None, headers: Dict[str, str] | None = None) -> None:
        
        super().__init__(status_code, detail, headers)    

class RecordExist(HTTPException):
    def __init__(self, status_code: int=409, detail: Any = None, headers: Dict[str, str] | None = None) -> None:
        
        super().__init__(status_code, detail, headers)
    

def create_model(db:Session,model:SQLModel,auto_error: bool=True):
    try:
        db.add(model)
        db.commit()
        db.refresh(model)
        return model
    except IntegrityError:
        if auto_error:
            raise RecordExist(detail="Record Already exist")
        return None


def get_crud_router(
        model:SQLModel,
        operation:str="CRIUD",
        pk_name:str='id',
        pk_type:str ='int',
        route_prefix='/api',
        new_model:SQLModel=None,
        select_model:SQLModel=None,
        update_model:SQLModel=None,
        auto_error:bool=True,
        **apirouterargs
        ):
    """
    operation = CRUD
    operation = CRU

    operation = CRD

    operation = CR

    """
    modelname = model.__name__.lower()
    new_model = new_model or model
    select_model = select_model or model
    update_model = update_model or model
    router = APIRouter(
        prefix=route_prefix,
        tags=[model.__name__],
        **apirouterargs
        
    )

    if 'R' in operation:

        @router.get(f'/{modelname}s/',response_model=List[select_model])
        async def getall(
            session:Session=Depends(get_db_Session),
            # user=Depends(AuthManager.get_user_from_cookie)
            ):

            stmnt = select(model)
            result = session.exec(stmnt).all()
            
            return result
    
    if 'C' in operation:

        @router.post(f'/{modelname}/',response_model=new_model,responses={409:{"detail":"Record Already exist"}})
        async def create(
            model_instant:new_model,
            session:Session=Depends(get_db_Session),
            # user=Depends(AuthManager.user)
            ):
            
            model_dict = create_model(
                session,
                model(**model_instant.dict(exclude_none=True)),
                auto_error=auto_error)
            return model_dict
    
    if 'RI' in operation:

        @router.get(f'/{modelname}/{"{pk}"}',response_model=select_model,responses={404:{"detail":"Record not found"}})
        async def get(
            pk:pk_type,
            session:Session=Depends(get_db_Session),
            # user=Depends(AuthManager.user)
            ):
            result = session.get(model,pk)
            if not result:
                raise NotFound(detail='Record not found')

            return result
    if 'D' in operation:

        @router.delete(f'/{modelname}/{"{pk}"}',responses={404:{"detail":"Record not found"}})
        async def delete(
            pk:pk_type,
            session:Session=Depends(get_db_Session),
            # user=Depends(AuthManager.user)
            ):
            model_instance = session.get(model,pk)
            if not model_instance:
                raise NotFound(detail="Record not found")
            session.delete(model_instance)
            session.commit()
            return "OK"
    if 'DM' in operation:
        
        @router.delete(f'/{modelname}/',responses={500:{"detail":" having some issue"}})
        async def deleteall(
            pks:List,
            session:Session=Depends(get_db_Session),
            # user=Depends(AuthManager.user)
            ):

            deleted = []
            for pk in pks:
                model_instance = session.get(model,pk)
                if not model_instance:
                    raise NotFound(detail="Record not found")
                session.delete(model_instance)
                session.commit()
                deleted.append(pk)

            return {"deleted_records":deleted}

                
    if 'U' in operation:
        @router.put(f'/{modelname}/{"{pk}"}',response_model=select_model,responses={404:{"detail":"Record not found"}})
        async def update(
            pk:pk_type,
            model_instant:update_model,
            session:Session=Depends(get_db_Session),
            # user=Depends(AuthManager.user)
            ):
            current_model = session.get(model,pk)
            if not current_model:
                raise NotFound(detail="Record not found")
            
            model_dict = model_instant.dict(exclude_none=True)
            model_dict.pop(pk_name)

            for k,v in model_dict.items():
                setattr(current_model,k,v)
            setattr(current_model,k,v)                
            session.add(current_model) 
            session.commit()
            session.refresh(current_model)
            return current_model
               
    return router