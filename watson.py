from watson_developer_cloud import DiscoveryV1

discovery = DiscoveryV1(
  username="9d4dc181-a636-46c3-9e7a-48a60a9b0255",
  password="eIq0XfzlWdqI",
  version="2016-12-01"
)

environment_id = 'f8c120ac-c67a-4983-ba71-693704418700'
collection_id = '33821e0a-5fef-4675-9f98-478b6f49cbe7'

# see https://www.ibm.com/watson/developercloud/discovery/api/v1/?python#query-collection
def query(qopts={}):
    return discovery.query(environment_id, collection_id, qopts)

def add_document():
