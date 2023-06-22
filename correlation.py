#This script passes down the settings and the source file to the corresponding method.
from easygui import *
import pandas as pd

# VARIABLES -------------
input_file = 'INPUT/synchrony_sample.csv'
# -----------------------

import gui_abstractions.gui_choosefile as gui_choosefile
# choosefile_args = ("Choose file #1 (correlation)",         # params_title
#                    "../comparesegments/inter",                     # params_initbrowser
#                    ".csv")                      # params_extensions
# file_chosen = gui_choosefile.main(choosefile_args)
file_chosen1 = gui_choosefile.main(["Choose file #1 (correlation)", # params_title
                                   "../comparesegments/inter",      # params_initbrowser
                                   ".csv"])                            # params_extensions
# print("file_chosen:", file_chosen)
file_chosen2 = gui_choosefile.main(["Choose file #2 (correlation)", # params_title
                                   "../comparesegments/inter",      # params_initbrowser
                                   ".csv"])                            # params_extensions

inter1 = pd.read_csv(file_chosen1)
inter2 = pd.read_csv(file_chosen2)

inter_frames = [inter1, inter2]
result = pd.concat(inter_frames)
print(result.head(5))

# input_file = file_chosen

method_choices = ["Pearson correlation", 
           "Time Lagged Cross Correlation (TLCC)", 
           "Dynamic Time Warping (DTW)", 
           "Instantaneous phase synchrony (IPS)"]
output = choicebox("Select method", "Window Title", method_choices)

print("The chosen method is:", output)

if output == method_choices[0]:
    import tut_pearson
    pearson_values = tut_pearson.main()
    print(pearson_values)
elif output == method_choices[1]:
    import tut_tlcc
    tlcc_values = tut_tlcc.main()
    print(tlcc_values)
elif output == method_choices[2]:
    import tut_dtw
    dtw_values = tut_dtw.main()
    print(dtw_values)
elif output == method_choices[3]:
    import tut_ips
    ips_values = tut_ips.main()
    print(ips_values)