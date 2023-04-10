import logging
import time

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


class TraecklyLoggingBackend(TraecklyBackendInterface):
    def __init__(self):
        self._start_time = 0
        self._active_task = None

    def start_task(self, id):
        if (self._active_task != None):
            self._show_delta_time()

        self._start_time = time.time()
        self._active_task = id
        self._log("{} started".format(id))

    def _show_delta_time(self):
        delta_time = time.time() - self._start_time
        s = self._format_time_difference(delta_time)
        self._log("{} duration {}".format(self._active_task, s))
    
    def _format_time_difference(self, delta_time):
        hours = int(delta_time) // 3600
        minutes = round((delta_time - (hours * 3600.0)) / 60.0)
        return "{}:{:02d}".format(hours, minutes)

    def _log(self, message):
        logging.info(message)


class TraecklyService(TraecklyServiceInterface):
    def __init__(self, backend):
        self._backend = backend

    def create_task(self, name):
        logging.info("{} created".format(name))

    def start_task(self, id):
        self._backend.start_task(id)


if __name__ == "__main__":
    print("Traeckly")
    logging.basicConfig(format='%(asctime)s %(message)s',
        datefmt='%d.%m.%Y %H:%M:%S',
        filename='example.log', encoding='utf-8', level=logging.DEBUG)
    
    backend = TraecklyLoggingBackend()
    service = TraecklyService(backend)
    service.start_task('Task-123')
    service.start_task('Break')
    service.start_task('Task-123')

