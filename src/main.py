from fastapi import APIRouter, HTTPException, status, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from connection.typesense_connection import client
from models.search_parameters import SearchParameters
from typing import Any

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

@app.post("/api/v1/search")
async def search(params: SearchParameters) -> dict[str, Any]:
    search_parameters = {
    'q'         : params.q,
    'query_by'  : 'item_desc,item_number_str',
    # 'filter_by' : 'store_unit:>9600',
    'sort_by'   : 'store_unit:desc',
    'include_fields':'store_unit,item_desc,item_number,rating',
    'facet_by': "store_unit,rating",
    'prioritize_exact_match':False,
    'prioritize_num_matching_fields':False
    # 'group_by':"store_unit"
    }

    search_params = params.model_dump(exclude_none=True)
    resp = search_documents(collection_name="inv", search_parameters=search_params)
    return resp

@app.post("/api/v1/english_words")
async def english_words(params: SearchParameters) -> dict[str, Any]:
    search_parameters = {
    'q'         : params.q,
    'query_by'  : 'item_desc',
    # 'filter_by' : 'store_unit:>9600',
    'sort_by'   : 'store_unit:desc',
    'include_fields':'store_unit,item_desc,item_number,rating',
    'facet_by': "store_unit,rating",
    # 'group_by':"store_unit"
    }

    search_parameters = params.model_dump(exclude_none=True)

    resp = search_documents(collection_name="english_words", search_parameters=search_parameters) 
    return resp