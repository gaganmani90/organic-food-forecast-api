#!/usr/bin/env python3
"""
Test runner script for the organic food web scraper project.
Runs all unit and integration tests.
"""
import sys
import os
import subprocess
import unittest

# Add project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def run_all_tests():
    """Discover and run all tests in the tests directory"""
    # Set PYTHONPATH to include backend directory
    env = os.environ.copy()
    env['PYTHONPATH'] = os.path.join(project_root, 'backend')
    
    # Discover and run tests
    loader = unittest.TestLoader()
    suite = loader.discover(
        start_dir='tests',
        pattern='test_*.py',
        top_level_dir=project_root
    )
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors) - len(result.skipped)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    print("="*70)
    
    if result.failures:
        print("\nFAILURES:")
        for test, traceback in result.failures:
            print(f"\n{test}")
            print(traceback)
    
    if result.errors:
        print("\nERRORS:")
        for test, traceback in result.errors:
            print(f"\n{test}")
            print(traceback)
    
    if result.skipped:
        print("\nSKIPPED:")
        for test, reason in result.skipped:
            print(f"  {test}: {reason}")
    
    # Return exit code
    return 0 if result.wasSuccessful() else 1

if __name__ == "__main__":
    exit_code = run_all_tests()
    sys.exit(exit_code)
