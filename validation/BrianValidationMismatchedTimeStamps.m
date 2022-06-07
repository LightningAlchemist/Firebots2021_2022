clc 
clear

a = readtable("C:\Users\josep\OneDrive\Documents\UniversityofWashington\SeniorProject\BrianValidation\LEDValidation\arduino_5_19_22_8_01pm.csv");%Read in True State
b = readtable("C:\Users\josep\OneDrive\Documents\UniversityofWashington\SeniorProject\BrianValidation\RobotValidation\robot_5_19_22_8_01pm.csv");%Read in Estimated State

arduino = table2timetable(a);%Convert true state to timetable object
brian = table2timetable(b); %Conver estimated state to timetable object
validation = synchronize(arduino, brian); %Combine true state and estimated state into one timetable, matching rows by timeStamp
data = validation.Variables; %Extract data from validation table
totTime = height(validation); %Total time is equal to the number of rows



mseError = zeros(1,totTime); %MSE error set to rows of zeros
numWrongError = zeros(1,totTime); %MSE error set to rows of zeros
for a = 1: totTime %Iterate from 1 to totTime
    y = data(a, 1:150); %function y is the true state
    x = data(a, 152:301); %function x is the estimated state
    if isnan(data(a,1))==false %if true state is not empty update the graph
        subplot(2,2,1)
        plot(y, 'red');
        axis([0 150 -0.05 1.2])
        title('Simulated Fire True State')
    end
     if isnan(data(a, 152))== false%if estimated state is not empty update the graph
        subplot(2,2,2)
        plot(x, 'red');
        axis([0 150 -0.05 1.2]);
        title('Simulated Fire Estimated State')
        subplot(2,2,3); 
        plot(data(a,151),1, 'o'); %location data located in column 151 on data table
        axis([0 150 0 2])
        title('Robot Location')
     end
    subplot(2,2,4); 
    title('MSE Error over time');  %Graph MSE over time
    for j = 1:150 
        mseError(a) = mseError(a) + ((data(a, j) - data(a, j+151))^2);
        numWrongError(a) = numWrongError(a) + abs((data(a, j) - round(data(a, j+151))));
    end
    mseError(a) = mseError(a)/150;
    %numWrongError(a) = numWrongError(a)/150
    plot(a, mseError(a),'.');
    axis([0 a 0 0.3])
    %plot(mseError);
    %axis([0 totTime -0.1 0.3])
    hold on
    pause(0.008)
end

figure;
plot(numWrongError);



