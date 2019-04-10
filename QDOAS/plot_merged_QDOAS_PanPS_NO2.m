function data = plot_merged_QDOAS_PanPS_NO2()
addpath('C:\Users\ZhaoX\Documents\MATLAB\matlab');
%filename = 'C:\Projects\Zenith_NO2\plots\QDOAS_PanPS_ref2016.csv';
%data = importfile(filename);
%filename = 'C:\Projects\Zenith_NO2\plots\QDOAS_PanPS_ref2016_v3_Sky_imager_OMI.csv';
%filename = 'C:\Projects\Zenith_NO2\plot_lev3_corrected\QDOAS_PanPS_ref2016_v4_Sky_imager_OMI.csv';
filename = 'C:\Projects\Zenith_NO2\plot_lev3_corrected\QDOAS_PanPS_ref2016_v5_Sky_imager_OMI_f2_onlysmallpix.csv';
data = importfile(filename);

DU = 2.6870e+16;
data.VCD = data.NO2_VCD;% this is PanPS DS NO2, without any correction
data.dSCD = data.NO2_VisSlColno2./DU;%
data.CI = data.Fluxes450./data.Fluxes500;

% CI filter
%TF = data.CI > 1.1;
%data = data(TF,:);

% SZA groups
TF1 = (data.SZA > 20) & (data.SZA <= 30);
TF2 = (data.SZA > 30) & (data.SZA <= 40);
TF3 = (data.SZA > 40) & (data.SZA <= 50);
TF4 = (data.SZA > 50) & (data.SZA <= 60);
TF5 = (data.SZA > 60) & (data.SZA <= 70);
TF6 = (data.SZA > 70) & (data.SZA <= 80);
TF7 = (data.SZA > 80) & (data.SZA <= 90);


%% fig 1
figure; hold all;
dscatter(data.dSCD,data.VCD);
xlabel('ZS dSCD [DU]');
ylabel('DS VCD [DU]');
grid on;

%% fig 2
figure; hold all;
y = data.dSCD(TF1,:); x = data.VCD(TF1,:);
scatter(x,y,'filled');
%plot_simple_linear_fit(x,y);
plot_simple_nl_fit(x,y);

y = data.dSCD(TF2,:); x = data.VCD(TF2,:);
scatter(x,y,'filled');
%plot_simple_linear_fit(x,y);
plot_simple_nl_fit(x,y);

y = data.dSCD(TF3,:); x = data.VCD(TF3,:);
scatter(x,y,'filled');
%plot_simple_linear_fit(x,y);
plot_simple_nl_fit(x,y);

y = data.dSCD(TF4,:); x = data.VCD(TF4,:);
scatter(x,y,'filled');
%plot_simple_linear_fit(x,y);
plot_simple_nl_fit(x,y);

y = data.dSCD(TF5,:); x = data.VCD(TF5,:);
scatter(x,y,'filled');
%plot_simple_linear_fit(x,y);
plot_simple_nl_fit(x,y);

y = data.dSCD(TF6,:); x = data.VCD(TF6,:);
scatter(x,y,'filled');
%plot_simple_linear_fit(x,y);
plot_simple_nl_fit(x,y);

y = data.dSCD(TF7,:); x = data.VCD(TF7,:);
scatter(x,y,'filled');
%plot_simple_linear_fit(x,y);
plot_simple_nl_fit(x,y);

ylabel('ZS dSCD [DU]');
xlabel('DS VCD [DU]');
grid on;
xlim([-1 7]);
ylim([-1 7]);
legend('SZA 20-30','linear fit','SZA 30-40','linear fit','SZA 40-50','linear fit',...
    'SZA 50-60','linear fit','SZA 60-70','linear fit','SZA 70-80','linear fit','SZA 80-90','linear fit');

%% fig 3
figure; hold all;
dscatter(data.SZA,data.CI);
ylabel('CI [450nm/500nm]');
xlabel('SZA');

%% fig 4
figure; hold all;
dscatter(data.SZA,data.dSCD);
ylabel('ZS dSCDs [DU]');
xlabel('SZA');


%% 
function plot_simple_linear_fit(x,y)
mdl = fitlm(x,y,'y~1+x1');
intercept = mdl.Coefficients.Estimate(1);
slop = mdl.Coefficients.Estimate(2);
new_x = [-10;10];
new_y = predict(mdl,new_x);
plot(new_x,new_y);

%% 
function plot_simple_nl_fit(x,y)
modelfun = 'y ~ b1*x';
beta0 = [0];
mdl = fitnlm(x,y,modelfun,beta0);

new_x = [-10;10];
new_y = predict(mdl,new_x);
plot(new_x,new_y);

%%
function QDOASPanPSref2016v5SkyimagerOMIclosest = importfile(filename, startRow, endRow)
%IMPORTFILE Import numeric data from a text file as a matrix.
%   QDOASPANPSREF2016V5SKYIMAGEROMICLOSEST = IMPORTFILE(FILENAME) Reads
%   data from text file FILENAME for the default selection.
%
%   QDOASPANPSREF2016V5SKYIMAGEROMICLOSEST = IMPORTFILE(FILENAME, STARTROW,
%   ENDROW) Reads data from rows STARTROW through ENDROW of text file
%   FILENAME.
%
% Example:
%   QDOASPanPSref2016v5SkyimagerOMIclosest = importfile('QDOAS_PanPS_ref2016_v5_Sky_imager_OMI_closest.csv', 2, 10566);
%
%    See also TEXTSCAN.

% Auto-generated by MATLAB on 2018/04/05 14:33:41

%% Initialize variables.
delimiter = ',';
if nargin<=2
    startRow = 2;
    endRow = inf;
end

%% Format for each line of text:
%   column1: datetimes (%{yyyy-MM-dd HH:mm:ss}D)
%	column2: double (%f)
%   column3: double (%f)
%	column4: double (%f)
%   column5: double (%f)
%	column6: double (%f)
%   column7: double (%f)
%	column8: double (%f)
%   column9: double (%f)
%	column10: double (%f)
%   column11: double (%f)
%	column12: double (%f)
%   column13: double (%f)
%	column14: double (%f)
%   column15: double (%f)
%	column16: double (%f)
%   column17: double (%f)
%	column18: double (%f)
%   column19: double (%f)
%	column20: double (%f)
%   column21: double (%f)
%	column22: double (%f)
%   column23: double (%f)
%	column24: double (%f)
%   column25: double (%f)
%	column26: double (%f)
%   column27: double (%f)
%	column28: double (%f)
%   column29: double (%f)
%	column30: double (%f)
%   column31: double (%f)
%	column32: double (%f)
%   column33: double (%f)
%	column34: double (%f)
%   column35: double (%f)
%	column36: double (%f)
%   column37: double (%f)
%	column38: double (%f)
%   column39: double (%f)
%	column40: double (%f)
%   column41: double (%f)
%	column42: double (%f)
%   column43: text (%q)
%	column44: text (%q)
%   column45: double (%f)
%	column46: double (%f)
%   column47: double (%f)
%	column48: double (%f)
%   column49: text (%q)
%	column50: text (%q)
%   column51: categorical (%C)
%	column52: text (%q)
%   column53: double (%f)
%	column54: double (%f)
%   column55: double (%f)
%	column56: double (%f)
%   column57: double (%f)
%	column58: double (%f)
%   column59: double (%f)
%	column60: double (%f)
%   column61: double (%f)
%	column62: double (%f)
%   column63: double (%f)
%	column64: double (%f)
%   column65: double (%f)
%	column66: double (%f)
%   column67: double (%f)
%	column68: double (%f)
%   column69: double (%f)
%	column70: double (%f)
%   column71: double (%f)
%	column72: double (%f)
%   column73: double (%f)
%	column74: double (%f)
%   column75: double (%f)
%	column76: text (%q)
%   column77: double (%f)
%	column78: double (%f)
%   column79: text (%q)
%	column80: double (%f)
%   column81: double (%f)
%	column82: double (%f)
%   column83: double (%f)
%	column84: double (%f)
%   column85: text (%q)
%	column86: text (%q)
%   column87: text (%q)
%	column88: text (%q)
%   column89: text (%q)
%	column90: text (%q)
%   column91: text (%q)
%	column92: text (%q)
%   column93: text (%q)
%	column94: text (%q)
%   column95: text (%q)
%	column96: text (%q)
%   column97: text (%q)
%	column98: text (%q)
%   column99: text (%q)
%	column100: text (%q)
%   column101: text (%q)
%	column102: text (%q)
%   column103: double (%f)
%	column104: double (%f)
%   column105: double (%f)
%	column106: double (%f)
%   column107: double (%f)
%	column108: double (%f)
%   column109: double (%f)
%	column110: double (%f)
%   column111: double (%f)
%	column112: double (%f)
%   column113: double (%f)
%	column114: double (%f)
%   column115: double (%f)
%	column116: double (%f)
%   column117: double (%f)
%	column118: double (%f)
%   column119: double (%f)
%	column120: double (%f)
%   column121: double (%f)
%	column122: double (%f)
%   column123: double (%f)
%	column124: double (%f)
%   column125: double (%f)
% For more information, see the TEXTSCAN documentation.
formatSpec = '%{yyyy-MM-dd HH:mm:ss}D%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%q%q%f%f%f%f%q%q%C%q%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%q%f%f%q%f%f%f%f%f%q%q%q%q%q%q%q%q%q%q%q%q%q%q%q%q%q%q%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%[^\n\r]';

%% Open the text file.
fileID = fopen(filename,'r');

%% Read columns of data according to the format.
% This call is based on the structure of the file used to generate this
% code. If an error occurs for a different file, try regenerating the code
% from the Import Tool.
dataArray = textscan(fileID, formatSpec, endRow(1)-startRow(1)+1, 'Delimiter', delimiter, 'TextType', 'string', 'EmptyValue', NaN, 'HeaderLines', startRow(1)-1, 'ReturnOnError', false, 'EndOfLine', '\r\n');
for block=2:length(startRow)
    frewind(fileID);
    dataArrayBlock = textscan(fileID, formatSpec, endRow(block)-startRow(block)+1, 'Delimiter', delimiter, 'TextType', 'string', 'EmptyValue', NaN, 'HeaderLines', startRow(block)-1, 'ReturnOnError', false, 'EndOfLine', '\r\n');
    for col=1:length(dataArray)
        dataArray{col} = [dataArray{col};dataArrayBlock{col}];
    end
end

%% Close the text file.
fclose(fileID);

%% Post processing for unimportable data.
% No unimportable data rules were applied during the import, so no post
% processing code is included. To generate code which works for
% unimportable data, select unimportable cells in a file and regenerate the
% script.

%% Create output variable
QDOASPanPSref2016v5SkyimagerOMIclosest = table(dataArray{1:end-1}, 'VariableNames', {'DateDDMMYYYY_Timehhmmss','SpecNo','Year_x','Fractionalday','Fractionaltime','SZA','SolarAzimuthAngle','Elevviewingangle','Azimviewingangle','NO2_VisRMS','NO2_VisRefZm','NO2_VisSlColo3','NO2_VisSlErro3','NO2_VisSlColno2','NO2_VisSlErrno2','NO2_VisSlColo4','NO2_VisSlErro4','NO2_VisSlColh2o','NO2_VisSlErrh2o','NO2_VisSlColring','NO2_VisSlErrring','O3_VisRMS','O3_VisRefZm','O3_VisSlColo3','O3_VisSlErro3','O3_VisSlColno2','O3_VisSlErrno2','O3_VisSlColo4','O3_VisSlErro4','O3_VisSlColh2o','O3_VisSlErrh2o','O3_VisSlColring','O3_VisSlErrring','Fluxes330','Fluxes340','Fluxes350','Fluxes380','Fluxes440','Fluxes450','Fluxes500','Fluxes550','Unnamed42','UTC','LTC','O3_VCD','NO2_VCD','VCD_corrected','SO2_VCD','HCHO_VCD','time','Column1Twolettercodeofmeasurementroutine','Column2UTdateandtimeforbeginningofmeasurementyyyymmddThhmmssZIS','Column5Totaldurationofmeasurementsetinseconds','Column6Solarzenithangleatthecentertimeofthemeasurementindegree','Column7Solarazimuthatthecentertimeofthemeasurementindegree0nort','Column10Pointingzenithangleindegreeabsoluteorrelativeseenextcol','Column11Zenithpointingmodezenithangleis0absolute1relativetosun2','Column12Pointingazimuthindegreeincreasesclockwiseabsolute0north','Column13Azimuthpointingmodelikezenithanglemodebutalsofixedscatt','Column14Fittingwindowindexuniquenumberforeachfittingwindow','Column15Startingwavelengthoffittingwindownm','Column16Endingwavelengthoffittingwindownm','Column17Orderofsmoothingpolynomialusedinspectralfitting','Column18Orderofoffsetpolynomialusedinspectralfitting1nooffset','Column19Orderofwavelengthchangepolynomialusedinspectralfitting1','Column20Sumover2iwithibeingafittingconfigurationindex0Ringspect','Column21Fittingresultindex12noerror2error','Column23rmsofunweightedspectralfittingresidualsnegativevaluefit','Column24Normalizedrmsofweightedspectralfittingresidualsnegative','Column27OzoneslantcolumnamountDobsonUnits9e99notfittedorfitting','Column28UncertaintyofozoneslantcolumnamountDobsonUnitsnegativev','Column29Geometricalozoneairmassfactor','Column30NitrogendioxideslantcolumnamountDobsonUnits9e99notfitte','Column31UncertaintyofnitrogendioxideslantcolumnamountDobsonUnit','Column32Geometricalnitrogendioxideairmassfactor','Column33SulfurdioxideslantcolumnamountDobsonUnits9e99notfittedo','Column34UncertaintyofsulfurdioxideslantcolumnamountDobsonUnitsn','Column35Geometricalsulfurdioxideairmassfactor','Column36FormaldehydeslantcolumnamountDobsonUnits9e99notfittedor','Column37UncertaintyofformaldehydeslantcolumnamountDobsonUnitsne','Column38Geometricalformaldehydeairmassfactor','Column61Positionoffilterwheel10filterwheelnotused19arevalidposi','Column62Positionoffilterwheel20filterwheelnotused19arevalidposi','Column64Integrationtimems','sName','sName1','dLatitude','dLongitude','dtUTC','iSunStrength','iPctOpq','iPctThin','bSunny','iBoxCount','iSubHorzCount','iSubProcZenCount','iMaskCount','iUnknownCount','iSkyCount','iOpaqueCount','iThinCount','mean_type','Year_y','Month','Day','Hour','Minute','Second','Latitude','Longitude','Fov75Area','VZA','ColumnAmountNO2','ColumnAmountNO2Std','VcdQualityFlags','ColumnAmountNO2Strat','ColumnAmountNO2StratStd','ColumnAmountNO2Trop','ColumnAmountNO2TropStd','CloudFraction','CloudFractionStd','CloudPressure','CloudPressureStd','number_of_pix','distance'});

% For code requiring serial dates (datenum) instead of datetime, uncomment
% the following line(s) below to return the imported dates as datenum(s).

% QDOASPanPSref2016v5SkyimagerOMIclosest.DateDDMMYYYY_Timehhmmss=datenum(QDOASPanPSref2016v5SkyimagerOMIclosest.DateDDMMYYYY_Timehhmmss);


