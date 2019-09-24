#/bin/bash
test_script_name="test_integer_compare.sh"
test_integer_compare_negative(){
	test 100 -lt 99 && echo "Pass" || echo "Fail"
}

test_integer_compare_positive(){
	test 100 -lt 199 && echo "Pass" || echo "Fail"
}

main(){
	pass=0
	fail=0
	pass_str="Pass"
	
	echo "============================= test session starts =============================="
	#Running Test - 1
	test1_result=$(test_integer_compare_negative)
	if [ "${test1_result}" = "${pass_str}" ]; then
	  echo "${test_script_name}:test_integer_compare_negative - ${test1_result}"
	  pass=$(( $pass + 1 ))
	else
	  echo "${test_script_name}:test_integer_compare_negative - ${test1_result}"
	  fail=$(( $fail+ 1 ))
	fi

	#Running Test - 2
	test2_result=$(test_integer_compare_positive)
	if [ "${test2_result}" = "${pass_str}" ]; then
	  echo "${test_script_name}:test_integer_compare_positive - ${test2_result}"
	  pass=$(( $pass + 1 ))
	else
	  echo "${test_script_name}:test_integer_compare_positive - ${test2_result}"
	  fail=$(( $fail+ 1 ))
	fi

	echo "============================== ${pass} pass, ${fail} fail =============================="
}
main
