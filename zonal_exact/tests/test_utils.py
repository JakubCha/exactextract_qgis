from zonal_exact.utils import extract_function_name


def test_extract_function_name():
    # Test case 1: Function name without arguments
    custom_function_str = "def my_function():"
    expected_result = "my_function"
    assert extract_function_name(custom_function_str) == expected_result

    # Test case 2: Function name with arguments
    custom_function_str = "def my_function(arg1, arg2):"
    expected_result = "my_function"
    assert extract_function_name(custom_function_str) == expected_result

    # Test case 3: Function name with indentation
    custom_function_str = "    def my_function():"
    expected_result = "my_function"
    assert extract_function_name(custom_function_str) == expected_result

    # Test case 4: Function name with additional spaces
    custom_function_str = "def   my_function   (   ):"
    expected_result = "my_function"
    assert extract_function_name(custom_function_str) == expected_result

    # Test case 5: Function name with comments
    custom_function_str = "def my_function():  # This is a function"
    expected_result = "my_function"
    assert extract_function_name(custom_function_str) == expected_result
