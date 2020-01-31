import json
import os


class ServicesModel(object):
    def __init__(self):
        self.data = {}
        # this flag is set to true after PUT operations, otherwise data is loaded from memory
        self.is_data_updated = False

    def sync_data_with_db(self):
        if self.data == {} or self.is_data_updated:
            self.data = self.load_data_from_db()
            self.is_data_updated = False

    def load_data_from_db(self):
        try:
            with open(os.path.join('static', 'db.json')) as file:
                self.data = json.load(file)
                return self.data
        except (FileNotFoundError, OSError) as e:
            print(e)

    def update_service(self, service):
        # get service name from request JSON
        service_name = service['service']
        # delete the service entry from memory
        del self.data['services'][self.get_service_index(service_name)]
        self.append_service(service)

    def create_service(self, service):
        self.append_service(service)

    def append_service(self, service):
        # append service to dict
        self.data['services'].append(service)
        self.is_data_updated = True

    def get_service_index(self, service_name):
        # gets the index of the to-be-updated service, so that it gets deleted
        for i, service in enumerate(self.data['services']):
            if service_name == service['service']:
                return i
            else:
                continue
        return None

    def persist_data_in_db(self):
        # if data has been updated, write dict to JSON file
        if self.is_data_updated:
            try:
                with open(os.path.join('static', 'db.json'), 'w') as file:
                    json.dump(self.data, file, indent=2)
            except (FileNotFoundError, OSError) as e:
                print(e)

