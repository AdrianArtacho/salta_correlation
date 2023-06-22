import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from dtw import dtw,accelerated_dtw

# VARIABLES-----------
filepath = 'INPUT/synchrony_sample.csv'
#---------------------

def main(**kwargs):
    # print(kwargs)
    for key, value in kwargs.items():
        # print("{0} = {1}".format(key, value))
        if key == 'filepath':
            filepath = value
        elif key == 'suptitle':
            suptitle_value = value
        elif key == 'ylabel':
            ylabel_value = value
   
    df = pd.read_csv(filepath)

    d1 = df['S1_Joy'].interpolate().values
    d2 = df['S2_Joy'].interpolate().values
    d, cost_matrix, acc_cost_matrix, path = accelerated_dtw(d1,d2, dist='euclidean')

    plt.imshow(acc_cost_matrix.T, origin='lower', cmap='gray', interpolation='nearest')
    plt.plot(path[0], path[1], 'w')
    plt.xlabel('Subject1')
    plt.ylabel('Subject2')
    plt.title(f'DTW Minimum Path with minimum distance: {np.round(d,2)}')
    plt.show()

if __name__ == '__main__':
#main(sys.argv)
#main()
    main()