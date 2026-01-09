import unittest
from unittest.mock import patch, MagicMock
import AutoDUCKS

class TestAutoDUCKS(unittest.TestCase):

    def test_initializationSettings(self):
        # Mock the readConfig function
        mock_readConfig = MagicMock(return_value={'filepath': 'test.csv'})
        with patch('AutoDUCKS.readConfig', mock_readConfig):
            result = AutoDUCKS.initializationSettings('y')
            self.assertEqual(result['numberoftimes'], 10)
            self.assertEqual(result['count'], 100)
            self.assertEqual(result['filename'], 'test_file')
            self.assertEqual(result['filepath'], 'test.csv')

if __name__ == '__main__':
    unittest.main()

    def test_executeProgram(self): 
        mock_getNumberFromScreen = MagicMock(return_value=42)
