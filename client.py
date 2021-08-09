import logging
import json
from typing import Dict


class DataProvider:    
    def __init__(self, logger=logging.Logger):
        self.logger = logger
        
    def get_jsonFromFile(self, fileName: str) -> Dict:
        f = open(fileName, 'r')
        jsonData = json.loads(f.read())
        f.close()
        return jsonData
