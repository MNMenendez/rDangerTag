for x in {1..6}; 
do make TESTCASE=test_00,test_0$x SIM_ARGS=--wave=test_0$x.ghw;
done
