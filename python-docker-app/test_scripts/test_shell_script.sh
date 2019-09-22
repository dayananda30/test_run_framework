#/bin/bash

test_integer_compare_negative(){
	test 100 -lt 99 && echo "Pass" || echo "Fail"
}

test_integer_compare_positive(){
	return test 100 -lt 199 && echo "Pass" || echo "Fail"
}

test_string_compare_negative(){
	return test "String" = "STRING" && echo "Pass" || echo "Fail"
}

test_string_compare_positive(){
	return test "String" = "String" && echo "Pass" || echo "Fail"
}

result=$(test_integer_compare_negative)
echo "Test result - ${result}"
