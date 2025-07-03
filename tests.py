from functions.run_python import run_python_file

# Test cases for the run_python_file function
print("\n--- Test 1: Run main.py ---")
print(run_python_file("calculator", "main.py"))

print("\n--- Test 2: Run tests.py ---")
print(run_python_file("calculator", "tests.py"))

print("\n--- Test 3: Run ../main.py (should error) ---")
print(run_python_file("calculator", "../main.py"))

print("\n--- Test 4: Run nonexistent.py ---")
print(run_python_file("calculator", "nonexistent.py"))
