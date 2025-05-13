import matplotlib.pyplot as plt
import numpy as np
from queue import Queue

#def plot_stuff():

def plots(param_list_1):

    # For Param List 1
    last_idx = len(param_list_1) - 1
    r = param_list_1[last_idx].plot_idx + 1
    fig, axs = plt.subplots(r, 1, figsize=(10, 10))

    extracted_values = []
    mean_value = []

    for i, param in enumerate(param_list_1):
        extracted_values.append(param.values)
        mean_value.append(np.nanmean(param.values))
        #print(extracted_values)
        if param.plot_idx < r:
            
            if (param.label == "BW" or param.label == "Serv PCI"):
                u = np.unique(param.values)
                if len(u) >= 0:
                    axs[param.plot_idx].set_yticks(u)
                axs[param.plot_idx].plot(param.values, color= 'green',label= {param.label})
            else:
                axs[param.plot_idx].plot(param.values, label= f"{param.label} Avg:{mean_value[i]:.3f} {param.unit}")
                #print(param.values)
            axs[param.plot_idx].grid(True, which='major', linestyle='-', color='black', alpha=0.2)
                
            axs[param.plot_idx].set_ylabel(param.name)
            axs[param.plot_idx].legend(loc= 'best')

        else:
            print(param.label + " has a missing plot. Add proper index")
            
    plt.suptitle("")
    plt.tight_layout()
    plt.show()

    return fig


def plot_w_options(param_list2):
    ok = False
    fig, ax = plt.subplots(figsize=(10, 8))
    avg = []

    user_in = input("Enter the LTE layer parameter (PHY, MAC, RLC or PDCP) or enter 'q' to quit: ")
    if user_in == "q":
        return

    for i, val in enumerate(param_list2):
        avg.append(np.nanmean(val.values))
        if (val.name == user_in.upper()):
            ax.plot(val.values, label= f"{val.label} Avg:{avg[i]:.2f} {val.unit}")
            ax.grid(True, which='major', linestyle='-', color='black', alpha=0.2)
            ax.set_ylabel(val.name)
            ax.legend(loc= 'best')  
            ok = True

    # entering wrong value
    if not ok:
        print("Wrong input! Enter the correct parameter!")
        return
            
    #plt.suptitle(val.name + "Layer Throughput Results - Nokia PTT ROHC OFF")
    plt.suptitle("PDCP Layer Throughput Results - Nokia PTT ROHC ON 25.03.2024")
    plt.tight_layout()
    plt.show()

    return fig   
