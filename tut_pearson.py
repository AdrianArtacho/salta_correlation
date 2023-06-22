import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

#####SETTINGS
plot_pearson = False
plot_rolling_window = True
r_window_size = 120
filepath = 'INPUT/synchrony_sample.csv' # dummy
suptitle_value = "Smiling data and rolling window correlation"
ylabel_value = 'Smiling Evidence'
#######

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

    # df = pd.read_csv('INPUT/synchrony_sample.csv')
    df = pd.read_csv(filepath)
    overall_pearson_r = df.corr().iloc[0,1]
    print(f"Pandas computed Pearson r: {overall_pearson_r}")
    # out: Pandas computed Pearson r: 0.2058774513561943

    r, p = stats.pearsonr(df.dropna()['S1_Joy'], df.dropna()['S2_Joy'])
    print(f"Scipy computed Pearson r: {r} and p-value: {p}")
    # out: Scipy computed Pearson r: 0.20587745135619354 and p-value: 3.7902989479463397e-51

    if plot_pearson:
        # Compute rolling window synchrony
        f,ax=plt.subplots(figsize=(7,3))
        df.rolling(window=30,center=True).median().plot(ax=ax)
        ax.set(xlabel='Time',ylabel='Pearson r')
        ax.set(title=f"Overall Pearson r = {np.round(overall_pearson_r,2)}")

    if plot_rolling_window:
        # Set window size to compute moving window synchrony.
        # r_window_size = 120
        # Interpolate missing data.
        df_interpolated = df.interpolate()
        # Compute rolling window synchrony
        rolling_r = df_interpolated['S1_Joy'].rolling(window=r_window_size, center=True).corr(df_interpolated['S2_Joy'])
        f,ax=plt.subplots(2,1,figsize=(14,6),sharex=True)
        df.rolling(window=30,center=True).median().plot(ax=ax[0])
        ax[0].set(xlabel='Frame',ylabel=ylabel_value)
        rolling_r.plot(ax=ax[1])
        ax[1].set(xlabel='Frame',ylabel='Pearson r')
        plt.suptitle(suptitle_value)

    plt.show()
    return(overall_pearson_r,r, p) 

if __name__ == '__main__':
#main(sys.argv)
#main()
    main()
