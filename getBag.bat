@ECHO OFF
set /p id="Local user name: "
echo Input remote pc password: firebot1234
pscp joseph@10.16.9.18:catkin_ws/estimator_state.csv /Users/%id%/Desktop/state.csv
echo coppied to /Users/%id%/Desktop/state.csv
cmd /k
