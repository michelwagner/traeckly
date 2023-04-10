import traeckly_service
import unittest   # The test framework

class Test_TestIncrementDecrement(unittest.TestCase):
    def test_increment(self):
        self.assertEqual(traeckly_service.increment(3), 4)

    def test_decrement(self):
        self.assertEqual(traeckly_service.increment(13), 14)


if __name__ == '__main__':
    unittest.main()
