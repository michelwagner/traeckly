import traeckly_service
import unittest   # The test framework

class Test_TraecklyService(unittest.TestCase):
    def test_traeckly_service_start_task(self):
        backend = traeckly_service.TraecklyLoggingBackend()
        service = traeckly_service.TraecklyService(backend)
        service.start_task('Task-123')
        self.assertEqual(1, 1)

    def test_TraecklyLoggingBackend_format_time_difference(self):
        backend = traeckly_service.TraecklyLoggingBackend()
        s = backend._format_time_difference(0)
        self.assertEqual(s, "0:00")
        s = backend._format_time_difference(60)
        self.assertEqual(s, "0:01")
        s = backend._format_time_difference(3600)
        self.assertEqual(s, "1:00")
        s = backend._format_time_difference(29)
        self.assertEqual(s, "0:00")
        s = backend._format_time_difference(31)
        self.assertEqual(s, "0:01")
        s = backend._format_time_difference(3540)
        self.assertEqual(s, "0:59")
        s = backend._format_time_difference(36059)
        self.assertEqual(s, "10:01")


if __name__ == '__main__':
    unittest.main()
