from functions.write_file import write_file

# Test cases for the write_file function
print("\n--- Test 1: Overwrite calculator/lorem.txt ---")
print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))

print("\n--- Test 2: Write to calculator/pkg/morelorem.txt ---")
print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))

print("\n--- Test 3: Attempt to write outside permitted directory ---")
print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))