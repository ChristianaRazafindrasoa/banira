import json
from search import search

class API():    
    def getNetwork(self):
        graph = search('paris',3, 25)
        return json.dumps(graph)
