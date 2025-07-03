from functions.get_file_content import get_file_content

# Test cases for the get_file_content function

print("\n--- Test: Read main.py ---")
print(get_file_content("calculator", "main.py"))

print("\n--- Test: Read pkg/calculator.py ---")
print(get_file_content("calculator", "pkg/calculator.py"))

print("\n--- Test: Read /bin/cat (outside permitted directory) ---")
print(get_file_content("calculator", "/bin/cat"))