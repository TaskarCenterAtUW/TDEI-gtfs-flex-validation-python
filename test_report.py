import unittest
import HtmlTestRunner

# Define your test cases
from tests.unit_tests.test_gtfs_flex_serializer import TestGTFSFlexUpload, TestGTFSFlexUploadData, TestRequest, \
    TestMeta, TestResponse
from tests.unit_tests.test_gtfs_flex_validation import TestSuccessGTFSFlexValidation, TestFailureGTFSFlexValidation
from tests.unit_tests.test_gtfx_flex_validator import TestGTFSFlexValidator
from tests.unit_tests.test_file_upload_msg import TestFileUploadMsg
from tests.unit_tests.test_main import TestApp

if __name__ == '__main__':
    # Create a test suite
    test_suite = unittest.TestSuite()
    # Add your test cases to the test suite
    test_suite.addTest(unittest.makeSuite(TestGTFSFlexUpload))
    test_suite.addTest(unittest.makeSuite(TestGTFSFlexUploadData))
    test_suite.addTest(unittest.makeSuite(TestRequest))
    test_suite.addTest(unittest.makeSuite(TestMeta))
    test_suite.addTest(unittest.makeSuite(TestResponse))
    test_suite.addTest(unittest.makeSuite(TestSuccessGTFSFlexValidation))
    test_suite.addTest(unittest.makeSuite(TestFailureGTFSFlexValidation))
    test_suite.addTest(unittest.makeSuite(TestGTFSFlexValidator))
    test_suite.addTest(unittest.makeSuite(TestApp))
    test_suite.addTest(unittest.makeSuite(TestFileUploadMsg))

    # Define the output file for the HTML report
    output_file = 'test_report.html'

    # Open the output file in write mode
    with open(output_file, 'w') as f:
        # Create an HTMLTestRunner instance with the output file and customize the template
        runner = HtmlTestRunner.HTMLTestRunner(stream=f, report_title='Test Report', combine_reports=True)

        # Run the test suite with the HTMLTestRunner
        runner.run(test_suite)
