import typesense

client: typesense.Client = typesense.Client({
    'nodes':[{
    'host': 'localhost',  
    'port': '8108',       
    'protocol': 'http'
    }
        
    ],
  'api_key': 'kwDoyhZWzili8NdRebNuBUebVhyWlxiU',
  'connection_timeout_seconds': 2
})

