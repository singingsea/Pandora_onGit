function data = calculate_zs_VCDs(data,p)
use_corrected_NO2 = true;

if nargin < 1
    [p,stats] = estimate_RCD();
    %load('C:\Projects\Zenith_NO2\plots\ndacc_ZS_PanPS_DS_VCDs.mat');% CF > 1.1
    %load('C:\Projects\Zenith_NO2\plots\ndacc_ZS_PanPS_DS_VCDs_unfintered.mat');% unfiltered
    % just load ZS/DS NO2 data and sky imager data
    %load('C:\Projects\Zenith_NO2\matlab.mat');
    load('C:\Projects\Zenith_NO2\matlab_ZSDS_skyimager_OMI_DS_corrected.mat');
end
%data.SCD = data.dSCD + abs(p(2));
data.SCD = data.dSCD + abs(p(2))*1;% calculate slant column of ZS measurement

data.ndacc_vcd = data.SCD./data.ndacc_amf;% calculate vertical column of ZS measurement

if use_corrected_NO2
    data.VCD = data.VCD_corrected;% replace NO2 VCD used in analysis by corrected values
else
    data.VCD = data.NO2_VCD;
end

% CI filter
TF = data.CI > 1.1;
data = data(TF,:);

% DS data filter
TF_SZA = (data.SZA > 80) | (data.SZA < 20);
data(TF_SZA,:) = [];
TF = (data.NO2_VCD <= 0) | (data.NO2_VCD >= 3);
data(TF,:) = [];

% SZA groups
TF1 = (data.SZA > 20) & (data.SZA <= 30);
TF2 = (data.SZA > 30) & (data.SZA <= 40);
TF3 = (data.SZA > 40) & (data.SZA <= 50);
TF4 = (data.SZA > 50) & (data.SZA <= 60);
TF5 = (data.SZA > 60) & (data.SZA <= 70);
TF6 = (data.SZA > 70) & (data.SZA <= 80);
TF7 = (data.SZA > 80) & (data.SZA <= 90);



%% fig 1
figure;hold all;
dscatter(data.ndacc_vcd,data.VCD);
xlim([-0.5 2.5]);
ylim([-0.5 2.5]);
plot([-10 10],[-10 10],'k');
plot_simple_linear_fit(data.ndacc_vcd,data.VCD);
plot_simple_nl_fit(data.ndacc_vcd,data.VCD);
xlabel('ZS NDACC VCD [DU]');
ylabel('DS VCD [DU]');
legend('data density','1-on-1','y = a*x+b', 'y = a*x');
R = corr(data.VCD,data.ndacc_vcd);
text(0,2,['R = ' num2str(R)]);
grid on;

%% fig 2
figure; hold all;
try
    y = data.ndacc_vcd(TF1,:); x = data.VCD(TF1,:);
    scatter(x,y,'filled');
    plot_simple_linear_fit(x,y);
    %plot_simple_nl_fit(x,y);
catch
end
y = data.ndacc_vcd(TF2,:); x = data.VCD(TF2,:);
scatter(x,y,'filled');
plot_simple_linear_fit(x,y);
%plot_simple_nl_fit(x,y);

y = data.ndacc_vcd(TF3,:); x = data.VCD(TF3,:);
scatter(x,y,'filled');
plot_simple_linear_fit(x,y);
%plot_simple_nl_fit(x,y);

y = data.ndacc_vcd(TF4,:); x = data.VCD(TF4,:);
scatter(x,y,'filled');
plot_simple_linear_fit(x,y);
%plot_simple_nl_fit(x,y);

y = data.ndacc_vcd(TF5,:); x = data.VCD(TF5,:);
scatter(x,y,'filled');
plot_simple_linear_fit(x,y);
%plot_simple_nl_fit(x,y);

try
    y = data.ndacc_vcd(TF6,:); x = data.VCD(TF6,:);
    scatter(x,y,'filled');
    plot_simple_linear_fit(x,y);
    %plot_simple_nl_fit(x,y);
catch
end
try
    y = data.ndacc_vcd(TF7,:); x = data.VCD(TF7,:);
    scatter(x,y,'filled');
    plot_simple_linear_fit(x,y);
    %plot_simple_nl_fit(x,y);
catch
end

plot([-10 10],[-10 10],'k');
ylabel('ZS NDACC VCD [DU]');
xlabel('DS VCD [DU]');
grid on;
xlim([-1 3]);
ylim([-1 3]);
legend('SZA 20-30','linear fit','SZA 30-40','linear fit','SZA 40-50','linear fit',...
    'SZA 50-60','linear fit','SZA 60-70','linear fit','SZA 70-80','linear fit','SZA 80-90','linear fit');

%% fig 3
figure; hold all;
plot(data.DateDDMMYYYY_Timehhmmss,data.VCD,'.');
plot(data.DateDDMMYYYY_Timehhmmss,data.ndacc_vcd,'.');
xlabel('time');
ylabel('NO_2 VCD [DU]');
legend('DS','ZS');
R = corr(data.VCD,data.ndacc_vcd);
text(min(data.DateDDMMYYYY_Timehhmmss) + 1,max(data.VCD)/2,['R = ' num2str(R)]);

%% fig 4
figure; hold all;
histogram(data.VCD,'BinWidth',0.05);
histogram(data.ndacc_vcd,'BinWidth',0.05);
xlabel('NO_2 VCD [DU]');
ylabel('f');
legend('DS','ZS');
R = corr(data.VCD,data.ndacc_vcd);
text(max(data.VCD)/2,0,['R = ' num2str(R)]);


%% 
function plot_simple_nl_fit(x,y)
modelfun = 'y ~ b1*x';
beta0 = [0];
mdl = fitnlm(x,y,modelfun,beta0);

new_x = [-10;10];
new_y = predict(mdl,new_x);
plot(new_x,new_y);


%% 
function plot_simple_linear_fit(x,y)
mdl = fitlm(x,y,'y~1+x1');
intercept = mdl.Coefficients.Estimate(1);
slop = mdl.Coefficients.Estimate(2);
new_x = [-10;10];
new_y = predict(mdl,new_x);
plot(new_x,new_y);