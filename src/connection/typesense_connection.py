import typesense

client: typesense.Client = typesense.Client({
    'nodes':[{
    'host': 'localhost',  # For Typesense Cloud use xxx.a1.typesense.net
    'port': '8108',       # For Typesense Cloud use 443
    'protocol': 'http'    # For Typesense Cloud use https
    }
        
    ],
  'api_key': 'kwDoyhZWzili8NdRebNuBUebVhyWlxiU',
  'connection_timeout_seconds': 2
})

