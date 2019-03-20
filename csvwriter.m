%% Prepare data
clc
clear
M = load('230m.mat');
row = M.val(1,:)';
time=((333/1000)+1)*7;
col = 0:max(time)/length(row):time-3.70e-04;
col=col';
data=[col row];
n = numel(col);
row=row(1:1728,1);
row=row+76;
serialzeros=zeros(size(row));
for i=1:length(row)
    if row(i)<-150
        row(i)=-150;
    end   
end
serialvec=[0:7.2/1728:7.2-7.2/1728]';
%% Plot
figure
hold on
j=1;
while j<=10
    for i = 1:1000
        plot(col(1:i),row(1:i))
        xlim([0 3])
        ylim([-500 500])
        pause(.00000000000000000001)
    end
hold off;
j=j+1;
end
%% Write CSV
    csvwrite('ecg.csv', row); 
    csvwrite('timevec.csv', col);
    csvwrite('serialvec.csv',serialvec);
    csvwrite('serialzeros.csv',serialzeros);