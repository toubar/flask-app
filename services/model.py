import json
import os


class Services(object):
    def __init__(self):
        self.data = {}
        self.is_data_updated = False

    def load_data_from_json(self):
        with open(os.path.join('static', 'db.json')) as file:
            self.data = json.load(file)
            return self.data

    def update_service(self, service):
        service_name = service['service']
        del self.data['services'][self.get_service_index(service_name)]
        self.data['services'].append(service)
        self.is_data_updated = True

    def create_service(self, service):
        self.data['services'].append(service)

    def get_service_index(self, service_name):
        for i, service in enumerate(self.data['services']):
            if service_name == service['service']:
                return i
            else:
                continue
        return None

    # do async after response
    def persist_data_in_db(self):
        with open(os.path.join('static', 'db.json'), 'w') as file:
            json.dump(self.data, file, indent=4)
