import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# VARIABLES--------
filepath = 'INPUT/synchrony_sample.csv' #dummy
#------------------

def crosscorr(datax, datay, lag=0, wrap=False):
    """ Lag-N cross correlation. 
    Shifted data filled with NaNs 
    
    Parameters
    ----------
    lag : int, default 0
    datax, datay : pandas.Series objects of equal length

    Returns
    ----------
    crosscorr : float
    """
    if wrap:
        shiftedy = datay.shift(lag)
        shiftedy.iloc[:lag] = datay.iloc[-lag:].values
        return datax.corr(shiftedy)
    else: 
        return datax.corr(datay.shift(lag))

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

    d1 = df['S1_Joy']
    d2 = df['S2_Joy']
    seconds = 5
    fps = 30
    rs = [crosscorr(d1,d2, lag) for lag in range(-int(seconds*fps),int(seconds*fps+1))]
    offset = np.floor(len(rs)/2)-np.argmax(rs)
    f,ax=plt.subplots(figsize=(14,3))
    ax.plot(rs)
    ax.axvline(np.ceil(len(rs)/2),color='k',linestyle='--',label='Center')
    ax.axvline(np.argmax(rs),color='r',linestyle='--',label='Peak synchrony')
    ax.set(title=f'Offset = {offset} frames\nS1 leads <> S2 leads',ylim=[.1,.31],xlim=[0,301], xlabel='Offset',ylabel='Pearson r')
    ax.set_xticks([0, 50, 100, 151, 201, 251, 301])
    ax.set_xticklabels([-150, -100, -50, 0, 50, 100, 150]);
    plt.legend()

    #####


    # Windowed time lagged cross correlation
    seconds = 5
    fps = 30
    no_splits = 20
    samples_per_split = df.shape[0]/no_splits
    rss=[]
    for t in range(0, no_splits):
        d1 = df['S1_Joy'].loc[(t)*samples_per_split:(t+1)*samples_per_split]
        d2 = df['S2_Joy'].loc[(t)*samples_per_split:(t+1)*samples_per_split]
        rs = [crosscorr(d1,d2, lag) for lag in range(-int(seconds*fps),int(seconds*fps+1))]
        rss.append(rs)
    rss = pd.DataFrame(rss)
    f,ax = plt.subplots(figsize=(10,5))
    sns.heatmap(rss,cmap='RdBu_r',ax=ax)
    ax.set(title=f'Windowed Time Lagged Cross Correlation',xlim=[0,301], xlabel='Offset',ylabel='Window epochs')
    ax.set_xticks([0, 50, 100, 151, 201, 251, 301])
    ax.set_xticklabels([-150, -100, -50, 0, 50, 100, 150]);

    # Rolling window time lagged cross correlation
    seconds = 5
    fps = 30
    window_size = 300 #samples
    t_start = 0
    t_end = t_start + window_size
    step_size = 30
    rss=[]
    while t_end < 5400:
        d1 = df['S1_Joy'].iloc[t_start:t_end]
        d2 = df['S2_Joy'].iloc[t_start:t_end]
        rs = [crosscorr(d1,d2, lag, wrap=False) for lag in range(-int(seconds*fps),int(seconds*fps+1))]
        rss.append(rs)
        t_start = t_start + step_size
        t_end = t_end + step_size
    rss = pd.DataFrame(rss)

    f,ax = plt.subplots(figsize=(10,10))
    sns.heatmap(rss,cmap='RdBu_r',ax=ax)
    ax.set(title=f'Rolling Windowed Time Lagged Cross Correlation',xlim=[0,301], xlabel='Offset',ylabel='Epochs')
    ax.set_xticks([0, 50, 100, 151, 201, 251, 301])
    ax.set_xticklabels([-150, -100, -50, 0, 50, 100, 150])

    plt.show()
    return()

if __name__ == '__main__':
#main(sys.argv)
#main()
    main()