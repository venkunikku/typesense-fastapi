from pydantic import BaseModel, Field
from typing import Optional

class SearchParameters(BaseModel):
    q: str = Field(..., description="Search query string")
    query_by: str = Field(
        ...,
        description="Comma-separated list of fields to search in",
        # regex="^[a-zA-Z_,]+$"  # Only allow letters, underscores, and commas
    )
    sort_by: Optional[str] = Field(
        None,
        description="Field to sort by, with optional :asc/:desc suffix"
    )
    include_fields: Optional[str] = Field(
        None,
        description="Comma-separated list of fields to include in response"
    )
    query_by_weights: Optional[str] = Field(
        None,
        description="Comma-separated list of weights corresponding to query_by fields"
    )
    limit: Optional[int] = Field(
        10,
        ge=1,
        le=250,
        description="Maximum number of results to return"
    )
    query_by_weights: Optional[str] = Field(
        None,
        description="Comma separated query"
    )

    prioritize_exact_match: Optional[bool] = Field(
        True,
        description="prioritizes documents whose field value matches exactly with the query"
    )


    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "q": "IL",
                    "query_by": "store_name,city,state",
                    "sort_by": "store_unit:desc",
                    "limit": 5,
                    "prioritize_exact_match":False,
                    "query_by_weights":"4,1"
                }
            ]
        }
    }

class SearchParametersWithCollection(SearchParameters):
    collection: str = Field(..., description="Collection name (Required for /multi_search)")

class MultiSearch(BaseModel):
    searches: list[SearchParametersWithCollection]