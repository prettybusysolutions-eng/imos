from fastapi import APIRouter
from imos.services.query_service import QueryService
from imos.services.entity_linker import EntityLinker

router = APIRouter()

@router.get('/summary')
def graph_summary():
    return QueryService().summary()

@router.get('/blockers')
def blockers():
    return {'items': QueryService().blockers()}

@router.get('/entities/{entity_type}')
def entities(entity_type: str):
    return {'items': QueryService().entities_by_type(entity_type)}

@router.post('/link')
def link_entities():
    return EntityLinker().link_same_name()

