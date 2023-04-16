import logging


class TraecklyServiceInterface:
    def create_task(self, name):
        pass

    def start_task(self, id):
        pass


class TraecklyFrontendInterface:
    def __init__(self):
        pass

    def show_status(self):
        pass


class TraecklyBackendInterface:
    def __init__(self):
        pass

    def start_task(self, id):
        pass
    
    def get_task_durations(self, from_isotime, to_isotime):
        pass



class TraecklyReportInterface:
    def __init__(self):
        pass

    def create_report(self, data):
        pass



class TraecklyService(TraecklyServiceInterface):
    def __init__(self, backend):
        self._backend = backend

    def create_task(self, name):
        logging.info("{} created".format(name))

    def start_task(self, id):
        self._backend.start_task(id)
