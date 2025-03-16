import json

class API():    
    def getNetwork(self, origin):
        fake = {
            'edges' : [
                {
                    'start': {
                        'lat': 47.53613,
                        'lng': -18.91368
                    },
                    'end': {
                        'lat': -81.5158,
                        'lng': 27.6648
                    }
                }
            ]
        }
        return json.dumps(fake)