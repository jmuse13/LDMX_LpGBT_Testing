import os
import time
import h5py
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.cm import get_cmap
import mplhep as hep
hep.style.use(hep.style.ATLAS)

in_directory = input("What should I call the output directory?: ")

hf = h5py.File(in_directory+'/trial.h5','w')

rr = hf.create_group('reg')
vv = hf.create_group('value')
tt = hf.create_group('time')
ff = hf.create_group('frequencies')

in_time = input("How long should I run? (in seconds): ")
in_time = float(in_time)

tstart = time.time()
current_time = time.time()-tstart

iteration = 0
while current_time < in_time:

    reg = []
    values = []
    times = [time.time()-tstart]
    frequencies = []

    os.system('/home/HGCAL_dev/enginetesterdev/adcstuff/zcu_multitool.py --status &> temp.txt')

    file1 = open('temp.txt','r')
    lines = file1.readlines()
    file1.close()

    for i in range(len(lines)):
        if(i>1 and i<12):
            split = lines[i].split(':')
            split2 = split[1].split('M')
            frequencies.append(float(split2[0]))

    os.system('rm temp.txt')

    os.system('/home/HGCAL_dev/enginetesterdev/adcstuff/lpgbt_status.py --dump &> temp.txt')

    file1 = open('temp.txt','r')
    lines = file1.readlines()
    file1.close()

    for i in range(len(lines)):
        splitted = lines[i].split(',')
        values.append(int(splitted[2].strip('\n'),16))
        reg.append(int(splitted[1],16))

    os.system('rm temp.txt')

    rr.create_dataset(str(iteration),data=np.asarray(reg,dtype=np.float32))
    vv.create_dataset(str(iteration),data=np.asarray(values,dtype=np.float32))
    tt.create_dataset(str(iteration),data=np.asarray(times,dtype=np.float32))
    ff.create_dataset(str(iteration),data=np.asarray(frequencies,dtype=np.float32))

    current_time = time.time()-tstart

    iteration += 1
hf.close()

registers = ['LOCKMODE','CLKG_CONFIG_I_FLL','CLKG_CONFIG_I_CDR','CLKG_CONFIG_P_FF_CDR','CLKG_CONFIG_P_CDR',
             'CLKG_lfLossOfLockCount','CLKG_BIASGEN_CONFIG','CLKG_vcoCapSelect','CLKG_dataMuxCfg',
             'CLKG_vcoDAC','CLKG_connectCDR','CLKG_disDataCounterRef','CLKG_enableCDR','CLKG_overrideVc',
             'CLKG_refClkSel','CLKG_vcoRailMode','CLKG_ENABLE_CDR_R','CLKG_smLocked','CLKG_lfInstLock',
             'CLKG_lfLocked','CLKG_CONFIG_FF_CAP','CLKG_lfState','CLKG_smState','FEC','DLDPFecCounterEnable']
description = ['Lock Mode','CDR FLL I [uA]','CDR Integral I [uA]','CDR Prop. Feedforward I [uA]',
                'CDR Phase Detector Prop. I [uA]','Lock Filter Loss of Lock',
                'Bias DAC for Charge Pumps [uA]','VCO Capacitor Bank','MUX Loopback','VCO DAC Current [uA]',
                'CDR Loop Connect to VCO','Data/4 Ripple Counter Enabled','Enable CDR','VCO Control V Override',
                'Reference Clock Select','VCO Rail Mode','CDR resistor enabled','ljCDR State Machine Locked',
                'Lock Filter Instant Lock','Lock Filter Locked','CDR Feedfoward Filter Cap',
                'ljCDR’s Lock Filter State Machine Status','ljCDR’s State Machine Status','FEC Counter','FEC Enabled']
if(len(registers)!=len(description)):
    print('not the same size')


f = h5py.File(in_directory+'/trial.h5','r')

reg = f['reg']
frequencies = f['frequencies']
time = f['time']
value = f['value']

flat_reg = []
flat_frequencies = []
flat_time = []
flat_value = []

flat_quantities = []

for i in range(len(reg['0'])):
    flat_reg.append([])
    flat_value.append([])
for i in range(len(frequencies['0'])):
    flat_frequencies.append([])
for i in range(len(registers)):
    flat_quantities.append([])
    
for i in range(len(time)):
    if(i>20):
        break
    flat_time.append(time[str(i)][0])
    t_449 = '0b'
    t_fec = '0b'
    for j in range(len(reg[str(i)])):
        flat_reg[j].append(reg[str(i)][j])
        flat_value[j].append(value[str(i)][j])
        if(reg[str(i)][j]==336):
            temp_ = '0b'
            t_val = format(int(value[str(i)][j]),'08b')
            for k, ele in enumerate(t_val):
                if(k==6):
                    temp_ += ele
            flat_quantities[0].append(int(temp_,2))
        if(reg[str(i)][j]==445):
            temp_ = '0b'
            temp1_ = '0b'
            t_val = format(int(value[str(i)][j]),'08b')
            for k, ele in enumerate(t_val):
                if(k<4):
                    temp_ += ele
                else:
                    temp1_ += ele
            flat_quantities[1].append(int(temp_,2))
            flat_quantities[2].append(int(temp1_,2))
        if(reg[str(i)][j]==446):
            temp_ = '0b'
            temp1_ = '0b'
            t_val = format(int(value[str(i)][j]),'08b')
            for k, ele in enumerate(t_val):
                if(k<4):
                    temp_ += ele
                else:
                    temp1_ += ele
            flat_quantities[3].append(int(temp_,2))
            flat_quantities[4].append(int(temp1_,2))
        if(reg[str(i)][j]==447):
            flat_quantities[5].append(int(value[str(i)][j]))
        if(reg[str(i)][j]==448):
            temp_ = '0b'
            t_val = format(int(value[str(i)][j]),'08b')
            for k, ele in enumerate(t_val):
                if(k>3):
                    temp_ += ele
            flat_quantities[6].append(int(temp_,2))
        if(reg[str(i)][j]==449):
            t_val = format(int(value[str(i)][j]),'08b')
            for k, ele in enumerate(t_val):
                t_449 += ele
        if(reg[str(i)][j]==450):
            temp_ = '0b'
            temp1_ = '0b'
            t_val = format(int(value[str(i)][j]),'08b')
            for k, ele in enumerate(t_val):
                if(k==0):
                    if(t_449!='0b'):
                        t_449 += ele
                    else:
                        print('weirdness with 449')
                if(k==1 or k==2):
                    temp_ += ele
                if(k>3):
                    temp1_ += ele
            flat_quantities[7].append(int(t_449,2))
            flat_quantities[8].append(int(temp_,2))
            flat_quantities[9].append(int(temp1_,2))
            t_449='0b'
        if(reg[str(i)][j]==451):
            temp_ = '0b'
            temp1_ = '0b'
            temp2_ = '0b'
            temp3_ = '0b'
            temp4_ = '0b'
            t_val = format(int(value[str(i)][j]),'08b')
            for k, ele in enumerate(t_val):
                if(k==0):
                    temp_ += ele
                if(k==2):
                    temp1_ += ele
                if(k==3):
                    temp2_ += ele
                if(k==6):
                    temp3_ += ele
                if(k==7):
                    temp3_ += ele
            flat_quantities[10].append(int(temp_,2))
            flat_quantities[11].append(int(temp1_,2))
            flat_quantities[12].append(int(temp2_,2))
            flat_quantities[13].append(int(temp3_,2))
            flat_quantities[14].append(int(temp3_,2))
        if(reg[str(i)][j]==452):
            temp_ = '0b'
            temp1_ = '0b'
            temp2_ = '0b'
            temp3_ = '0b'
            temp4_ = '0b'
            temp5_ = '0b'
            t_val = format(int(value[str(i)][j]),'08b')
            for k, ele in enumerate(t_val):
                if(k==0):
                    temp_ += ele
                if(k==1):
                    temp1_ += ele
                if(k==2):
                    temp2_ += ele
                if(k==3):
                    temp3_ += ele
                if(k==4):
                    temp4_ += ele
                if(k>4):
                    temp5_ += ele
            flat_quantities[15].append(int(temp_,2))
            flat_quantities[16].append(int(temp1_,2))
            flat_quantities[17].append(int(temp2_,2))
            flat_quantities[18].append(int(temp3_,2))
            flat_quantities[19].append(int(temp4_,2))
            flat_quantities[20].append(int(temp5_,2))
        if(reg[str(i)][j]==453):
            temp_ = '0b'
            temp1_ = '0b'
            t_val = format(int(value[str(i)][j]),'06b')
            for k, ele in enumerate(t_val):
                if(k==0 or k==1):
                    temp_ += ele
                if(k>1):
                    temp1_ += ele
            flat_quantities[21].append(int(temp_,2))
            flat_quantities[22].append(int(temp1_,2))
        if(reg[str(i)][j]==454):
            t_val = format(int(value[str(i)][j]),'08b')
            for k, ele in enumerate(t_val):
                t_fec += ele
        if(reg[str(i)][j]==455):
            t_val = format(int(value[str(i)][j]),'08b')
            for k, ele in enumerate(t_val):
                t_fec += ele
        if(reg[str(i)][j]==456):
            t_val = format(int(value[str(i)][j]),'08b')
            for k, ele in enumerate(t_val):
                t_fec += ele
        if(reg[str(i)][j]==457):
            t_val = format(int(value[str(i)][j]),'08b')
            for k, ele in enumerate(t_val):
                t_fec += ele
            flat_quantities[23].append(int(t_fec,2))
        if(reg[str(i)][j]==322):
            temp_ = '0b'
            t_val = format(int(value[str(i)][j]),'08b')
            for k, ele in enumerate(t_val):
                if(k==3):
                    temp_ += ele
            flat_quantities[24].append(int(temp_,2))
            
for i in range(len(time)):
    for j in range(len(frequencies[str(i)])):
        flat_frequencies[j].append(frequencies[str(i)][j])

for i in range(len(flat_quantities)):
    fig,ax = plt.subplots(figsize=(8, 8))
    ax.scatter(flat_time,flat_quantities[i],label=str(registers[i]))
    ax.set_xlabel('Time [s]')
    ax.set_ylabel(str(description[i]))
    ax.legend(frameon=False)
    plt.savefig(in_directory+'/register_'+str(registers[i])+'.pdf')
    plt.close()

labels = ['100 MHz','Ref','TX','TX40','RX0','RX1','RX2','RX0-DV','RX1-DV','RX2-DV']
fig,ax = plt.subplots(figsize=(8, 8))
for i in range(len(flat_frequencies)):
    ax.scatter(time,flat_frequencies[i],label=labels[i])
ax.set_xlabel('Time [s]')
ax.set_ylabel('Clock Frequency [MHz]')
ax.legend(frameon=False)
plt.savefig(in_directory+'/frequencies.pdf')
plt.close()
