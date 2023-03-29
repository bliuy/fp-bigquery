import unittest
import typing
import functions.helper_functions as fn
from unittest import mock

class TestFunctions(unittest.TestCase):
    
    def test_invalid_load_query(self):
        
        # Arrange
        empty_fp: str = ""
        invalid_fp: str = "foo"
        
        # Act - Assert
        with self.assertRaises(ValueError):
            fn.load_query(empty_fp)
        
        with self.assertRaises(OSError):
            fn.load_query(invalid_fp)
            
    def test_valid_load_query(self):
        
        # Arrange
        fp: str = "src/queries/bq-1.txt"
        
        # Act
        result = fn.load_query(fp)
        
        # Assert
        self.assertGreater(len(result._query_string), 0)

        
class TestBigQueryQuery(unittest.TestCase):
    
    def setUp(self) -> None:
        self.valid_instance = fn.BigQueryQuery("foobar")
    
    def test_failed_construction(self):
        
        # Arrange
        query_str = ""
        
        # Act + Assert
        with self.assertRaises(ValueError):
            result = fn.BigQueryQuery(
                query_str=query_str
            )
            
    def test_invalid_job_config(self):
        
        # Arrange
        job = self.valid_instance
        
        # Act + Assert
        with self.assertRaises(AttributeError):
            job.add_job_config(foo="bar")

                
    def test_missing_job_config(self):
        # Arrange
        job = self.valid_instance
        mocked_client = mock.MagicMock()
        
        # Act + Arrange
        with self.assertRaises(ValueError):
            job.run_query(mocked_client)
    
            
    def test_failed_job_response(self):
        
        # Arrange
        mocked_client = mock.MagicMock()
        job_results = mock.MagicMock()
        job_results.error_result = {} # Represents that there are errors being returned
        mocked_client.query.return_value = job_results
        job = self.valid_instance
        job.add_job_config(destination=mock.MagicMock())
        
        # Act
        result = job.run_query(mocked_client)
        
        # Assert
        self.assertFalse(result)
        
    def test_sucessful_job_response(self):
        
        # Arrange
        mocked_client = mock.MagicMock()
        job_results = mock.MagicMock()
        job_results.error_result = None
        job_results.result.return_value = []
        mocked_client.query.return_value = job_results
        job = self.valid_instance
        job.add_job_config(destination="foo.bar.baz")
        
        # Act
        result = job.run_query(mocked_client)
        
        # Assert
        self.assertTrue(result)
        
        
        
    
    
        
if __name__ == "__main__":
    
    test_cases: typing.List = [
        TestFunctions,
        TestBigQueryQuery
    ]
    
    test_suites = [
        unittest.TestLoader().loadTestsFromTestCase(test) for test in test_cases
    ]

    all_tests = unittest.TestSuite(test_suites)

    runner = unittest.TextTestRunner()
    runner.run(all_tests)