import json
import os


class ServicesModel(object):
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
        self.append_service(service)

    def create_service(self, service):
        self.append_service(service)

    def append_service(self, service):
        self.data['services'].append(service)
        self.is_data_updated = True

    def get_service_index(self, service_name):
        for i, service in enumerate(self.data['services']):
            if service_name == service['service']:
                return i
            else:
                continue
        return None

    def persist_data_in_db(self):
        if self.is_data_updated:
            with open(os.path.join('static', 'db.json'), 'w') as file:
                json.dump(self.data, file, indent=4)
