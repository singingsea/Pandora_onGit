function calculate_zs_VCDs(data,p)
data.SCD = data.dSCD + abs(p(2));

data.ndacc_vcd = data.SCD./data.ndacc_amf;

figure;hold all;
dscatter(data.ndacc_vcd,data.NO2_VCD);