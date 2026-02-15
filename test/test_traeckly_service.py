import unittest

from traeckly_service import TraecklyBackendBase


class Test_Traeckly_service(unittest.TestCase):
    def test_normalize_task_name(self):
        self.assertEqual(TraecklyBackendBase._normalize_task_name('Task 1'), 'Task_1')
        self.assertEqual(TraecklyBackendBase._normalize_task_name('Task\tName'), 'Task_Name')
        self.assertEqual(TraecklyBackendBase._normalize_task_name('A/B'), 'A_B')
        self.assertEqual(TraecklyBackendBase._normalize_task_name('A-B:C.D'), 'A_B_C_D')
        self.assertEqual(TraecklyBackendBase._normalize_task_name('Task_Name'), 'Task_Name')
        self.assertEqual(TraecklyBackendBase._normalize_task_name(''), '')


if __name__ == '__main__':
    unittest.main()
