function [p,stats] = estimate_RCD(data)
addpath('C:\Users\ZhaoX\Documents\MATLAB\matlab\quantreg');
% AMF filter
%TF = data.ndacc_amf <= 5;
TF = (data.ndacc_amf >= 2) & (data.ndacc_amf <= 10);
data = data(TF,:);

x = data.ndacc_amf;
y = data.dSCD;

[p,stats]=quantreg(x,y,0.05,1);
figure;hold all;
plot(x,y,'b.',x,polyval(p,x),x,stats.yfitci,'k:');
legend('data','1st order 10th percentile fit','95% confidence interval','location','best'); 
disp(['estimated RCD = ' num2str(abs(p(2))) ' [DU]']);
