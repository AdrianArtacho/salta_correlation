#This script passes down the settings and the source file to the corresponding method.
from easygui import *

input_file = 'INPUT/synchrony_sample.csv'

method_choices = ["Pearson correlation", 
           "Time Lagged Cross Correlation (TLCC)", 
           "Dynamic Time Warping (DTW)", 
           "Instantaneous phase synchrony (IPS)"]
output = choicebox("Select method", "Window Title", method_choices)

print("The chosen method is:", output)

if output == method_choices[0]:
    import tut_pearson
    print(method_choices[0])