import pytest
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def run_all_tests():
    """Run all test suites"""
    print("=" * 80)
    print("LAZADA WEB E-COMMERCE PLATFORM - TEST EXECUTION")
    print("=" * 80)
    print()

    # Configure pytest arguments
    pytest_args = [
        "-v",  # Verbose output
        "-s",  # Show print statements
        "--tb=short",  # Short traceback format
        f"--html=src/reports/test_report.html",  # HTML report
        "--self-contained-html",  # Self-contained HTML report
        "src/tests/",  # Test directory
    ]

    # Run tests
    exit_code = pytest.main(pytest_args)

    print()
    print("=" * 80)
    print("TEST EXECUTION COMPLETED")
    print("=" * 80)

    return exit_code


def run_specific_module(module_name):
    """Run tests for a specific module"""
    module_mapping = {
        "auth": "src/tests/auth/",
        "cart": "src/tests/cart/",
        "search": "src/tests/search/",
        "review": "src/tests/review/",
        "security": "src/tests/security/",
    }

    if module_name.lower() not in module_mapping:
        print(f"Error: Module '{module_name}' not found.")
        print(f"Available modules: {', '.join(module_mapping.keys())}")
        return 1

    test_path = module_mapping[module_name.lower()]

    print("=" * 80)
    print(f"RUNNING {module_name.upper()} MODULE TESTS")
    print("=" * 80)
    print()

    pytest_args = [
        "-v",
        "-s",
        "--tb=short",
        f"--html=src/reports/{module_name}_report.html",
        "--self-contained-html",
        test_path,
    ]

    exit_code = pytest.main(pytest_args)

    print()
    print("=" * 80)
    print(f"{module_name.upper()} MODULE TESTS COMPLETED")
    print("=" * 80)

    return exit_code


def run_specific_test(test_path):
    """Run a specific test file or test case"""
    print("=" * 80)
    print(f"RUNNING SPECIFIC TEST: {test_path}")
    print("=" * 80)
    print()

    pytest_args = [
        "-v",
        "-s",
        "--tb=short",
        test_path,
    ]

    exit_code = pytest.main(pytest_args)

    print()
    print("=" * 80)
    print("TEST EXECUTION COMPLETED")
    print("=" * 80)

    return exit_code


def show_menu():
    """Display test execution menu"""
    print("\n" + "=" * 80)
    print("LAZADA TEST AUTOMATION - MAIN MENU")
    print("=" * 80)
    print("\n[1] Run All Tests")
    print("[2] Run Authentication Module Tests (Login, Register)")
    print("[3] Run Cart Management Module Tests (Add, Update)")
    print("[4] Run Search Module Tests (Search, Filter, Sort)")
    print("[5] Run Review Module Tests (Submit, Filter Reviews)")
    print("[6] Run Security Module Tests (SQL Injection, DoS)")
    print("[7] Run Specific Test File")
    print("[0] Exit")
    print("\n" + "=" * 80)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Command-line argument provided
        arg = sys.argv[1].lower()

        if arg == "all":
            sys.exit(run_all_tests())
        elif arg in ["auth", "cart", "search", "review", "security"]:
            sys.exit(run_specific_module(arg))
        elif arg.endswith(".py") or "::" in arg:
            sys.exit(run_specific_test(arg))
        else:
            print(f"Unknown argument: {arg}")
            print("\nUsage:")
            print("  python run.py all                    - Run all tests")
            print("  python run.py auth                   - Run auth module tests")
            print("  python run.py cart                   - Run cart module tests")
            print("  python run.py search                 - Run search module tests")
            print("  python run.py review                 - Run review module tests")
            print("  python run.py security               - Run security module tests")
            print("  python run.py <test_file.py>         - Run specific test file")
            sys.exit(1)
    else:
        # Interactive menu
        while True:
            show_menu()
            choice = input("\nEnter your choice: ").strip()

            if choice == "1":
                run_all_tests()
            elif choice == "2":
                run_specific_module("auth")
            elif choice == "3":
                run_specific_module("cart")
            elif choice == "4":
                run_specific_module("search")
            elif choice == "5":
                run_specific_module("review")
            elif choice == "6":
                run_specific_module("security")
            elif choice == "7":
                test_path = input(
                    "\nEnter test file path (e.g., src/tests/auth/test_user_login.py): "
                ).strip()
                if test_path:
                    run_specific_test(test_path)
            elif choice == "0":
                print("\nExiting test automation. Goodbye!")
                break
            else:
                print("\nInvalid choice. Please try again.")

            input("\nPress Enter to continue...")
