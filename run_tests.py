# run_tests.py
"""
Test runner script for MindMate chatbot.
Runs all tests and generates a report.

Usage:
    python run_tests.py              # Run all tests
    python run_tests.py --unit       # Run only unit tests
    python run_tests.py --integration # Run only integration tests
    python run_tests.py --coverage   # Run with coverage report
"""

import sys
import subprocess
from pathlib import Path


def run_tests(test_type="all", coverage=False):
    """Run tests based on specified type."""
    
    print("=" * 70)
    print("MINDMATE TEST SUITE")
    print("=" * 70)
    print()
    
    # Base pytest command
    cmd = ["pytest", "-v"]
    
    # Add coverage if requested
    if coverage:
        cmd.extend(["--cov=.", "--cov-report=html", "--cov-report=term"])
    
    # Add test markers
    if test_type == "unit":
        cmd.extend(["-m", "unit"])
        print("Running UNIT tests only...")
    elif test_type == "integration":
        cmd.extend(["-m", "integration"])
        print("Running INTEGRATION tests only...")
    else:
        print("Running ALL tests...")
    
    print()
    
    # Run tests
    try:
        result = subprocess.run(cmd, check=False)
        return result.returncode
    except FileNotFoundError:
        print("ERROR: pytest not found. Install it with:")
        print("  pip install pytest pytest-cov")
        return 1


def main():
    """Main entry point."""
    args = sys.argv[1:]
    
    test_type = "all"
    coverage = False
    
    if "--unit" in args:
        test_type = "unit"
    elif "--integration" in args:
        test_type = "integration"
    
    if "--coverage" in args:
        coverage = True
    
    if "--help" in args or "-h" in args:
        print(__doc__)
        return 0
    
    return_code = run_tests(test_type, coverage)
    
    print()
    print("=" * 70)
    if return_code == 0:
        print("✓ ALL TESTS PASSED")
    else:
        print("✗ SOME TESTS FAILED")
    print("=" * 70)
    
    if coverage:
        print()
        print("Coverage report generated in htmlcov/index.html")
    
    return return_code


if __name__ == "__main__":
    sys.exit(main())
