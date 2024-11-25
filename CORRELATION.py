#This script passes down the settings and the source file to the corresponding method.
from easygui import *
import pandas as pd
import combine_names
# import gui.gui_choosefile as gui_choosefile
import gui.gui_browse_t as gui_browse

# VARIABLES -------------
input_file = 'INPUT/synchrony_sample.csv'
# -----------------------


file_chosen1 = gui_browse.main(params_title="Choose file #1 (correlation)",         # params_title
                                   params_initbrowser="../comparesegments/inter",   # params_initbrowser
                                   params_extensions=".csv")                        # params_extensions

file_chosen2 = gui_browse.main(params_title="Choose file #2 (correlation)",         # params_title
                                   params_initbrowser="../comparesegments/inter",   # params_initbrowser
                                   params_extensions=".csv")                        # params_extensions

inter1 = pd.read_csv(file_chosen1)
inter2 = pd.read_csv(file_chosen2)


print("inter1:")
inter1.columns = ['key', 'S1_Joy']
print(inter1.head(5))

print("inter2:")
inter2.columns = ['key', 'S2_Joy']
print(inter2.head(5))

## Sample file
# inter0 = pd.read_csv("INPUT/synchrony_sample.csv")
# print(inter0.head(5))


# workings
print("workings:")
# inter_frames = [inter1, inter2]
intermediate = inter1.merge(inter2, on='key', how='inner')
inter_clean = intermediate.iloc[: , 1:]
# del intermediate["key"]
# inter_clean = intermediate.iloc[0, 1]
print(inter_clean.head(5))


combined_name = combine_names.main(file_chosen1 = file_chosen1,
                   file_chosen2 = file_chosen2)


inter_newpath = combined_name + '.csv'
inter_clean.to_csv(inter_newpath, index=False)


input_file = inter_newpath
print("input file:", input_file)

method_choices = ["Pearson correlation", 
           "Time Lagged Cross Correlation (TLCC)", 
           "Dynamic Time Warping (DTW)", 
           "Instantaneous phase synchrony (IPS)"]
output = choicebox("Choose method to be used to measure the correlation between two segmentations", 
                   "Select method", 
                   method_choices)

print("The chosen method is:", output)

if output == method_choices[0]:
    import tut_pearson
    pearson_values = tut_pearson.main(filepath = input_file, 
                                      suptitle = 'Pearson correlation of segmentation data',
                                      ylabel = 'raw segmentation')
    print(pearson_values)
elif output == method_choices[1]:
    import tut_tlcc
    tlcc_values = tut_tlcc.main(filepath = input_file, 
                                      suptitle = 'TLCC correlation of segmentation data',
                                      ylabel = 'raw segmentation')
    print(tlcc_values)
elif output == method_choices[2]:
    import tut_dtw
    dtw_values = tut_dtw.main(filepath = input_file, 
                                      suptitle = 'DTW correlation of segmentation data',
                                      ylabel = 'raw segmentation')
    print(dtw_values)
elif output == method_choices[3]:
    import tut_ips
    ips_values = tut_ips.main(filepath = input_file, 
                                      suptitle = 'IPS correlation of segmentation data',
                                      ylabel = 'raw segmentation')
    print(ips_values)