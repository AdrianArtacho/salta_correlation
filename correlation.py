#This script passes down the settings and the source file to the corresponding method.
from easygui import *

# VARIABLES -------------
input_file = 'INPUT/synchrony_sample.csv'
# -----------------------

import gui_abstractions.gui_choosefile as gui_choosefile
choosefile_args = ("Choose file #1 (correlation)",         # params_title
                   "../comparesegments",                     # params_initbrowser
                   ".csv")                      # params_extensions
file_chosen = gui_choosefile.main(choosefile_args)
# print("file_chosen:", file_chosen)

input_file = file_chosen

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