from traeckly_service import TraecklyBackendInterface
import logging
import time


class TraecklyLoggingBackend(TraecklyBackendInterface):
    def __init__(self):
        self._start_time = 0
        self._active_task = None
        logging.basicConfig(format='%(asctime)s %(message)s',
            datefmt='%d.%m.%Y %H:%M:%S',
            filename='traeckly.log', encoding='utf-8', level=logging.DEBUG)

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
