import json
import os
from typing import Dict, List
from tinydb import TinyDB, Query

class Database():
    def __init__(self, file_name: str, collection: str) -> None:
        self.dbname = file_name
        self.db = TinyDB(file_name)
        self.collection = collection

        # core_collections = ['configs', 'blocks']
        # for c in core_collections:
        #     self.db.table(c)

    # def restore_database(self) -> None:
    #     # Deve restaurar somente se objeto nao existir no db!
    #     # Precisa melhorar esse método!

    #     cur_dir = os.path.dirname(__file__)
    #     blocks_directory = os.path.join(cur_dir, '..', 'blocks')
    #     blocks_directory = os.path.abspath(blocks_directory)

    #     if (not self.db.table('blocks').all()):
    #         raw_data = []
    #         for filename in os.listdir(blocks_directory):
    #             if filename.endswith(".json"):
    #                 file_path = os.path.join(blocks_directory, filename)
    #                 with open(file_path, 'r') as json_file:
    #                     data = json.load(json_file)
    #                 raw_data.append(data)

    #         collection = self.db.table('blocks')
    #         collection.insert_multiple(raw_data)

    def get_all(self) -> List:
        q = Query()
        table = self.db.table(self.collection)

        return table.all()

    def get_one(self, field: str, value: str) -> Dict:
        q = Query()
        table = self.db.table(self.collection)
        data = table.search(q[field] == value)

        return data[0] if data else None

    def insert_one(self, data: Dict):
        collection = self.db.table(self.collection)
        _id = collection.insert(data)

        return _id