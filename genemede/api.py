import json

class JSONValidator:
    """allows a user to specify a template for a JSON file and then use that template to validate the structure of a JSON file"""
    def __init__(self, template):
        self.template = template

    def validate(self, json_data):
        # Validate the JSON data against the template
        return json_data == self.template

# Create a JSONValidator instance with a template
validator = JSONValidator({
    "name": str,
    "age": int,
    "email": str
})

# Validate some JSON data
json_data = {
    "name": "John Doe",
    "age": 30,
    "email": "john.doe@example.com"
}

if validator.validate(json_data):
    print("JSON data is valid")
else:
    print("JSON data is invalid")






class JsonAPI:
    """
    Write a python API to interface with different json files enforcing a template to be defined by the user. The API should have functions for reading, writing, updating, and searching entries by any of the template keys
    Example usage:
    template = {
    'name': '',
    'age': 0,
    'city': ''
    }

    api = JsonAPI(template)
    api.write_json('example.json', {'name': 'John', 'age': 30, 'city': 'New York'})
    api.update_json('example.json', 'age', 31)
    print(api.read_json('example.json'))
    print(api.search_json('example.json', 'age'))
    print(api.search_json('example.json', 'country'))"""
    def __init__(self, template):
        self.template = template
    
    def read_json(self, file_path):
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
            return data

    def write_json(self, file_path, data):
        with open(file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)

    def update_json(self, file_path, key, value):
        data = self.read_json(file_path)
        data[key] = value
        self.write_json(file_path, data)

    def search_json(self, file_path, key):
        data = self.read_json(file_path)
        if key in data:
            return data[key]
        else:
            return None

### Write a python API to interface with different json files. The json files act like databases of  entities defined by a template which is user defined
import json

class JSONAPI:
    def init(self, template):
        self.template = template
        self.entities = {}

    def add_entity(self, entity):
        if not all(key in entity for key in self.template):
            raise ValueError("Entity does not match template")

        self.entities[entity["id"]] = entity

    def get_entity(self, entity_id):
        if entity_id not in self.entities:
            raise ValueError("Entity not found")
        return self.entities[entity_id]

    def update_entity(self, entity_id, updates):
        if entity_id not in self.entities:
            raise ValueError("Entity not found")
        self.entities[entity_id].update(updates)

    def delete_entity(self, entity_id):
        if entity_id not in self.entities:
            raise ValueError("Entity not found")
        del self.entities[entity_id]

    def save(self, filepath):
        with open(filepath, "w") as f:
            json.dump(self.entities, f)

    def load(self, filepath):
        with open(filepath, "r") as f:
            self.entities = json.load(f)

"""
Example usage
template = ["id", "name", "age", "gender"]

api = JSONAPI(template)

api.add_entity({"id": 1, "name": "John", "age": 35, "gender": "male"})
api.add_entity({"id": 2, "name": "Jane", "age": 30, "gender": "female"})

api.get_entity(1) # {"id": 1, "name": "John", "age": 35, "gender": "male"}
api.update_entity(2, {"age": 31})
api.get_entity(2) # {"id": 2, "name": "Jane", "age": 31, "gender": "female"}
api.delete_entity(1)
api.get_entity(1) # raises ValueError

api.save("entities.json")
api.load("entities.json")
api.get_entity(2) # {"id": 2, "name": "Jane", "age": 31, "gender": "female"}
"""
