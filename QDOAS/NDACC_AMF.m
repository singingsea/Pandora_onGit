function data = NDACC_AMF(data,code_path,lambda)
if nargin < 2 
    code_path = 'C:/Projects/Zenith_NO2/';
    lambda = 460;
end
amf_dir = [code_path '/no2_amf_lut_v1_0/'];


% print the ozone data to the sza input file
try
    input_DAY_SZA_table = table(data.Year,data.Fractionalday,data.SZA);
catch
        input_DAY_SZA_table = table(data.Year_x,data.Fractionalday,data.SZA);
end
writetable(input_DAY_SZA_table,[amf_dir 'DAY_SZA.dat'],'Delimiter','\t','WriteVariableNames',false);

% now print up to input no2 file
fid = fopen([amf_dir 'input_file_no2_amf.dat'], 'w');
fprintf(fid, '%s\n', '*Input file for NO2 AMF interpolation program');
fprintf(fid, '%s\n', '*');
fprintf(fid, '%s\n', '*Wavelength (350-550 nm) ?');
fprintf(fid, '%s\n', num2str(lambda));
fprintf(fid, '%s\n', '*Latitude (-90 (SH) to +90 (NH)) ?');
fprintf(fid, '%s\n', '43.781');
fprintf(fid, '%s\n', '*Longitude (-180 (- for W) to +180 (+ for E)) ?');
fprintf(fid, '%s\n', '-79.468');
fprintf(fid, '%s\n', '*Ground albedo flag: 1 for Koelemeijer dscd_vecbase and 2 for albedo value defined by the user');
fprintf(fid, '%s\n', '1');
fprintf(fid, '%s\n', '*Ground albedo value (if albedo flag = 1, put -99)');
fprintf(fid, '%s\n', '-99');
fprintf(fid, '%s\n', '*Name of the file with SZA values for interpolation (less than 30 characters) ?');
fprintf(fid, '%s\n', 'DAY_SZA.dat');
fprintf(fid, '%s\n', '*Interpolation results appearing on the screen: 1 -> yes, 0 -> no');
fprintf(fid, '%s\n', '0');
fclose(fid);

cd(amf_dir);
executable = [amf_dir 'no2_amf_interpolation_v1_0.exe'];
[status, result] = dos(executable, '-echo');

[tmp_year, tmp_day, tmp_sza, amf] = textread([amf_dir 'no2_amf_output.dat'], '%f%f%f%f', 'headerlines',5);

data.ndacc_amf = amf;
