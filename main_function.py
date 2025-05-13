# import serial
import tkinter as tk
from tkinter import filedialog
import os 
import pathlib
from pathlib import Path
import re
from plot import plots, plot_w_options
from typing import NamedTuple
from queue import Queue
import numpy as np
from dataclasses import dataclass, field
from typing import List

def clear():
        os.system('cls')

clear()
#print(Path.cwd())

# give path of the file to read
def convert_list_to_float(value):
    try:
        for i in range(len(value)):
                value[i] = float(value[i])
                #print(value[i]) 
    except ValueError:
        print("oops! no match found")

def convert_list_to_int_or_float(value):
    try:
        for i in range(len(value)):
                if '.' in value[i]:
                        value[i] = float(value[i])

                else:
                        value[i] = int(value[i])
                #print(type(value[0]))
        #print("String conversion successful!") 
    except ValueError:
        print("oops! no match found")

# Handling throughput data rates
def convert_list_to_kbps(value):
        try:
              for i in range(len(value)):
                        if 'K' not in value[i]:
                                value[i] = int(value[i])
                                value[i] = value[i] / 125   # convert to byte/sec(Bps) to Kbits/sec(Kbps)
                        else:
                                value[i] = value[i].replace('K', '')
                                value[i] = int(value[i])
                                #value[i] = value[i] * 1000
        except  ValueError:
                print("oops! no match found")
# filter pci values as per user's wishes 
def filter_values(value, seq): 
      f = filter()
      return
#filepath = "C:\\Users\\Admin450c\\Surya\\2024_07_11_10_23_36-qlog.txt"


       
timeS = r'\[\d{4}\-\d{2}\-\d{2}\s*\d{2}\:\d{2}\:\d{2}\]\s*\s*'

pattern_1 = r'MEAS\s*:\s*CINR\((.*?),(.*?)\)\s*RSRP\((.*?),(.*?)\)\s*RSSI\((.*?),(.*?)\)\s*RSRQ\((.*?),(.*?)\)\s*N RPT\((.*?),(.*?)\)\s*450C\((.*?),(.*?)\)'
pattern_2 = r'CHAN\s*:\s*'
pattern_3 = r'TP\s*:\s*PHY\((.*?):(.*?)\)\s*MAC\((.*?):(.*?)/(.*?)\)\s*RLC\((.*?):(.*?)\)\s*PDCP\((.*?):(.*?)\)'

@dataclass
class Parameter:
      plot_idx: int
      name: str
      label: str
      unit: str
      values: List = field(default_factory=list)

Chan_BW = Parameter(0, 'BW', 'BW', 'MHz', [])
PCI = Parameter(1, 'PCI', 'Serv PCI', '', [])
CINR_MAIN = Parameter(2, 'CINR', 'CINR Main', 'dB', [])
CINR_DIV = Parameter(2, 'CINR', 'CINR DIV', 'dB', [])
RSRP_MAIN = Parameter(3, 'RSRP', 'RSRP Main', 'dBm', [])
RSRP_DIV = Parameter(3, 'RSRP', 'RSRP DIV', 'dBm', [])
RSSI_MAIN = Parameter(4, 'RSSI', 'RSSI Main', 'dBm', [])
RSSI_DIV = Parameter(4, 'RSSI', 'RSSI DIV', 'dBm', [])
RSRQ_MAIN = Parameter(5, 'RSRQ', 'RSRQ Main', 'dB', [])
RSRQ_DIV = Parameter(5, 'RSRQ', 'RSRQ DIV', 'dB', [])

class Parameter2(NamedTuple):
      id: int
      name: str
      label: str
      unit: str
      values: list
PHY_DL = Parameter2(0, 'PHY', 'PHY DL', 'kbps', [])
PHY_UL = Parameter2(0, 'PHY', 'PHY UL', 'kbps', [])
MAC_DL = Parameter2(1, 'MAC', 'MAC DL', 'kbps', [])
MAC_UL = Parameter2(1, 'MAC', 'MAC UL', 'kbps', [])
RLC_DL = Parameter2(2, 'RLC', 'RLC DL', 'kbps', [])
RLC_UL = Parameter2(2, 'RLC', 'RLC UL', 'kbps', [])
PDCP_DL = Parameter2(3, 'PDCP', 'PDCP DL', 'kbps', [])
PDCP_UL = Parameter2(3, 'PDCP', 'PDCP UL', 'kbps', [])

meas_list = [Chan_BW, PCI, CINR_MAIN, CINR_DIV, RSRP_MAIN, RSRP_DIV,
             RSSI_MAIN, RSSI_DIV, RSRQ_MAIN, RSRQ_DIV]

tp_list = [PHY_DL, PHY_UL, MAC_DL, MAC_UL, 
             RLC_DL, RLC_UL, PDCP_DL, PDCP_UL]


select_pci = []
filtered_list = []
filter_list_vals = []

def main1():

        
        input_file = tk.filedialog.askopenfilename(title="Select a Log File")
        filepath = input_file
        if not input_file:
               print("No file is selected. Exiting...")
               exit()

        timestamp_present =  False
        lines_to_write = []
        
        
        with open(input_file, 'r', errors='ignore') as infile:
                line = infile.readlines()
                for l in line:
                        if re.match(timeS, l):
                                timestamp_present =  True
                                remove_ts = re.sub(timeS, '', l)
                                lines_to_write.append(remove_ts.strip() + '\n')
                                
                        else:
                                lines_to_write.append(l.strip() + '\n')
                
                
        if timestamp_present:
                print('File with timestamps is detected...')
                output_file = tk.filedialog.asksaveasfilename(title="Save a new file without timestamps", defaultextension=".txt")
                print('Timestamps found and removed...Creating a new file wo timestamps')
                with open(output_file, 'w') as outfile:
                        if not outfile:
                                print('No file is selected. Exiting...')
                                exit()
                        for l in lines_to_write:
                                outfile.write(l)
                            
                filepath = output_file 
        
        with open(filepath, 'r', errors='ignore') as fp:
                line = fp.readlines()
                
                for l in line:
                        
                        text = re.match(pattern_1, l) 
                        text_2 = re.match(pattern_2, l)
                        text_3 = re.match(pattern_3, l)
                        #print(text)
                        if text_2:
                                char_sep = l.split()
                                #print(char_sep)
                                keyword_1 = 'MHz'
                                keyword_2 = 'PCI'
                                found_mhz = '0MHz'
                                found_pci = 'PCI=-1'
                                for j in range(len(char_sep)):
                                        if (keyword_1 in char_sep[2] or 
                                            keyword_2 in char_sep[5]):
                                              found_mhz = char_sep[2]
                                              found_pci = char_sep[5]
                                              
                                        else:
                                             found_mhz = next((x for x in char_sep if keyword_1 in x), '0MHz')
                                             found_pci = next((x for x in char_sep if keyword_2 in x), 'PCI=-1')
                                        
                                        bw_str = found_mhz.split(keyword_1)[0]
                                        pci_str = found_pci.split('=')[1]
                                
                                meas_list[0].values.append(bw_str)
                                meas_list[1].values.append(pci_str)
                                #print(meas_list[3])
                                
                        if text: 
                                for i in range(len(meas_list)-2):
                                    meas_list[i+2].values.append(re.search(pattern_1, l).
                                                               group(i + 1))
                                
                        if text_3:
                              for i in range(len(tp_list)):
                                    tp_list[i].values.append(re.search(pattern_3, l).
                                                             group(i+1))
                                    

                for j in range(len(meas_list)):
                      convert_list_to_int_or_float(meas_list[j].values)

                for j in range(len(tp_list)):
                        #print("trying to convert datarates")
                        convert_list_to_kbps(tp_list[j].values)
                      
                #print("LOOK HERE!")
                #print(meas_list[0].values)
                #print(tp_list[6].values)
        
        user_in = input("Would you like to select a PCI? enter 'Y' or 'N' or 'q' to quit:")
        if user_in == 'q':
                return
        elif user_in.upper() == 'Y':
                u = np.unique(meas_list[1].values)  #for PCI values
                ask_user = int(input(f"Enter the PCI from the list {u} :"))
                for j, param in enumerate(meas_list[0].values):
                        select_pci.append([param.values[j] for param in meas_list])
                #print(select_pci)
                filtered_list = [row for row in select_pci if ask_user in row]
                filter_list_vals = [list(l) for l in zip(*filtered_list)]
                #print(filter_list_vals)
                for i in range(len(meas_list)):
                       meas_list[i].values = filter_list_vals[i]
                fig = plots(meas_list)
        elif user_in.upper() == 'N':
                fig = plots(meas_list) 
        else:
                print("Something went wrong!")
        
        #print(meas_list[3].values)
        fig2 = plot_w_options(tp_list)
        
        #print("Extraction of data is completed!")

if __name__ == '__main__':
    
    main1()