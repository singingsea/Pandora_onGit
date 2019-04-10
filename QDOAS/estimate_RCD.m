function [p,stats] = estimate_RCD(data)
addpath('C:\Users\ZhaoX\Documents\MATLAB\matlab\quantreg');
if nargin < 1
    %load('C:\Projects\Zenith_NO2\plots\ndacc_ZS_PanPS_DS_VCDs.mat');% CF > 1.1
    load('C:\Projects\Zenith_NO2\plots\ndacc_ZS_PanPS_DS_VCDs_unfintered.mat');% unfiltered
end
% AMF filter
%TF = data.ndacc_amf <= 5;
TF = (data.ndacc_amf >= 2) & (data.ndacc_amf <= 10);
data = data(TF,:);

% add more ZS NO2 filters
% add SZA filter
TF_SZA = (data.SZA >75);
data(TF_SZA,:) = [];

% add CI filter
TF_ci = (data.CI <1.2) | (data.CI >1.7);
data(TF_ci,:) = [];
% add ZS RMS filter
TF_ZS_rms = data.NO2_VisRMS >0.005;
data(TF_ZS_rms,:) = [];
% add ZS NO2 err filter
TF_ZS_NO2err = data.NO2_VisSlErrno2 >1e15;
data(TF_ZS_NO2err,:) = [];


x = data.ndacc_amf;
y = data.dSCD;

[p,stats]=quantreg(x,y,0.05,1);
figure;hold all;
plot(x,y,'b.',x,polyval(p,x),x,stats.yfitci,'k:');
legend('data','1st order 10th percentile fit','95% confidence interval','location','best'); 
disp(['estimated RCD = ' num2str(abs(p(2))) ' [DU]']);
textbp(['estimated RCD = ' num2str(abs(p(2))) ' [DU]']);
xlabel('NDACC AMF');
ylabel('NO_2 dSCDs [DU]');
