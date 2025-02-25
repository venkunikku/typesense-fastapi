from fastapi import APIRouter, HTTPException, status, FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from connection.typesense_connection import client
from models.search_parameters import SearchParameters, MultiSearch
from typing import Any, List

app = FastAPI()

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

def search_documents(collection_name: str, search_parameters: dict):
    return client.collections[collection_name].documents.search(search_parameters)

def multi_search_collections(search_request, common_search_params):
    return client.multi_search.perform(search_request, common_search_params)

@app.post("/api/v1/search")
async def search(params: SearchParameters) -> dict[str, Any]:
    search_params = params.model_dump(exclude_none=True)
    resp = search_documents(collection_name="inv", search_parameters=search_params)
    return resp

@app.post("/api/v1/english_words")
async def english_words(params: SearchParameters) -> dict[str, Any]:
    search_parameters = params.model_dump(exclude_none=True)

    resp = search_documents(collection_name="english_words", search_parameters=search_parameters) 
    return resp

@app.post("/api/v1/multi_search")
async def multi_search(params: MultiSearch, query_by:str = None) -> dict[str, Any]:
    search_parameters = params.model_dump(exclude_none=True)
    print(search_parameters)
    common_search_params = None
    if query_by:
        common_search_params =  {
                'query_by': query_by,
                }

    resp = multi_search_collections(search_parameters, common_search_params) 
    return resp


@app.get("/api/v1/geosearch")
async def geo_search_store(q: str = Query(description="Query"), 
                     query_by: str = Query(description="Query by field"), 
                     sort_by: str = Query(description="Sorting field eg location(41.748489, -88.186111):asc"), 
                     filter_by: str = Query(description="Filter field eg location:(41.748489, -88.186111, 50 mi)")):
    
    if q is None or query_by is None or sort_by is None or filter_by is None:
        raise HTTPException(
            status_code=400,
            detail="All fields are required"
        ) 

    search_parameters = {
        'q'         : q,
        'query_by'  : query_by,
        'filter_by' : filter_by,
        'sort_by'   : sort_by,
        'per_page': 40
        }
    return client.collections['store'].documents.search(search_parameters)