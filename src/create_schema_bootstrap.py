from connection.typesense_connection import client
import pprint
import json

schema = {
  'name': 'inv',
  'fields': [
    {
      'name'  :  'inventory_id',
      'type'  :  'int32'
    },
    {
      'name'  :  'store_unit',
      'type'  :  'int32',
       'facet' :  True,
       'sort': True
    },
    {
      'name'  :  'rating',
      'type'  :  'float',
       'facet' :  True,
       'sort': True,
       'range_index': True,
       'optional': True
    },
    {
      'name'  :  'item_number',
      'type'  :  'int32',
      'facet' :  True
    },
    {
      'name'  :  'item_number_str',
      'type'  :  'string',
      'weight': 2
    },
    {
      'name'  :  'item_desc',
      'type'  :  'string',
      'weight': 1
    }
  ],
  'default_sorting_field': 'store_unit',
  'token_separators': ["+", "-", "@", ".", " ", "(", ")", "-"]
}


popular_word_schema = {

    'name': 'english_words',
  'fields': [
    {
      'name'  :  'word',
      'type'  :  'string'
    },
    {
      'name'  :  'popularity',
      'type'  :  'int32'
    },
  ]
}

def creat_collection(schema:dict):
    res = client.collections.create(schema)
    return res

def get_collections(collection_name: str = "inv"):
    return client.collections[collection_name].retrieve()


def get_all_collections():
    return client.collections.retrieve()

def delete_a_collection(collection_name: str):
    return client.collections[collection_name].delete()

def update_collection(collection_name: str, update_schema: dict | None ):
    client.collections[collection_name].update(update_schema)

def index_documents(collection_name:str, documents: dict):
    return client.collections[collection_name].documents.import_(documents, {'action': 'create'})

def delete_document_by_query(collection_name: str, query: dict = {'filter_by': 'num_employees:>100'} ):
    return client.collections[collection_name].documents.delete(query)

def get_document_by_id(collection_name:str, id: str):
    return client.collections[collection_name].documents[id].retrieve()

def search_documents(collection_name: str, search_parameters: dict):
    return client.collections[collection_name].documents.search(search_parameters)


def load_inv_data():
    # Loading data
    j_records = []
    with open(r"inventory_to_load.jsonl", "r") as f:
        for each in f:
            if each.strip():
                data = json.loads(each.rstrip())
                j_records.append(data)
    print(f"Total records to load: {len(j_records)}")
    i = 0
    batch_size = 5000
    for records in range(0, len(j_records), batch_size):
        print(len(j_records[i:records]))
        print(i, records)
        resp = index_documents(collection_name="inv", documents=j_records[i: i+batch_size])
        i = records
        # print(i)


def load_data_generic(collection_name: str, 
                      file_path: str = r"english_words.jsonl"):
    # Loading data
    j_records = []
    with open(file_path, "r") as f:
        for each in f:
            if each.strip():
                data = json.loads(each.rstrip())
                j_records.append(data)
    print(f"Total records to load: {len(j_records)}")
    i = 0
    batch_size = 5000
    for records in range(0, len(j_records), batch_size):
        print(len(j_records[i:records]))
        print(i, records)
        resp = index_documents(collection_name=collection_name, documents=j_records[i: i+batch_size])
        i = records
        # print(i)

def bootstrap_english(collection_name:str = "english_words"):
    try:
        resp = delete_a_collection(collection_name=collection_name)
    except:
        pass
    creat_collection(schema=popular_word_schema)
    load_data_generic(collection_name)


def bootstrap_inventory_data(collection_name:str = 'inv'):
    try:
        resp = delete_a_collection(collection_name=collection_name)
    except:
        pass
    creat_collection(schema=schema)
    load_inv_data()


if __name__ == '__main__':

    bootstrap_inventory_data()
    bootstrap_english()

   