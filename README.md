# Alignment

To evaluate how well-aligned two lists of timepoints (a reference list and a proposed list) are, we can compute a numeric score. Here's a step-by-step approach:

Align the Lists: For each timepoint in the proposed list, find the nearest timepoint in the reference list.

Compute Errors: Calculate the absolute difference between each proposed timepoint and its closest reference timepoint.

Aggregate the Errors: Use an aggregation metric, such as the mean absolute error (MAE), root mean squared error (RMSE), or sum of absolute errors.

Penalty for Missing Matches: If the proposed list has more or fewer points than the reference, penalize for the unmatched timepoints.

---

## Usage

```shell
python ALIGNMENT.py
```

---

# Correlation

Determining the correaltion values between different segments, according to [this tutorial](https://towardsdatascience.com/four-ways-to-quantify-synchrony-between-time-series-data-b99136c4a9c9), and this [collab notebook](https://colab.research.google.com/gist/jcheong0428/c68c60fe4ee8d9e794a5423552344569/synchrony_tutorial.ipynb).

---

## Usage

1. Run main script:

    ```shell
    python CORRELATION.py
    ```

1. Select intermediate files 1 & 2 (to measure correlation from) from the [comparesegments/inter](../comparesegments/inter) folder.

1. A combined `.csv` file will be generated in the `/INPUT` folder.

1. Select method from dialog

    ![select_method.png](doc/images/corre_select_method.png)

---

## Installation

Vreate VENV and install requirements:

```shell
python3 -m venv ./.venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

### Pearson correlation

The Pearson correlation measures how two continuous signals co-vary over time and indicate the linear relationship as a number between -1 (negatively correlated) to 0 (not correlated) to 1 (perfectly correlated).

#### Caveats

1. outliers can skew the results of the correlation estimation

2. it assumes the data are homoscedastic such that the variance of your data is homogenous across the data range.

Generally, the correlation is a snapshot measure of global synchrony. Therefore it does not provide information about directionality between the two signals such as which signal leads and which follows.

The Pearson correlation is implemented in multiple packages including Numpy, Scipy, and Pandas. If you have null or missing values in your data, correlation function in Pandas will drop those rows before computing whereas you need to manually remove those data if using Numpy or Scipy’s implementations.

The following code loads are sample data (in the same folder), computes the Pearson correlation using Pandas and Scipy and plots the median filtered data.

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats

df = pd.read_csv('synchrony_sample.csv')
overall_pearson_r = df.corr().iloc[0,1]
print(f"Pandas computed Pearson r: {overall_pearson_r}")
# out: Pandas computed Pearson r: 0.2058774513561943

r, p = stats.pearsonr(df.dropna()['S1_Joy'], df.dropna()['S2_Joy'])
print(f"Scipy computed Pearson r: {r} and p-value: {p}")
# out: Scipy computed Pearson r: 0.20587745135619354 and p-value: 3.7902989479463397e-51
```

---

### Rolling window

Once again, the Overall Pearson `r` is a measure of global synchrony that reduces the relationship between two signals to a single value. Nonetheless there is a way to look at moment-to-moment, local synchrony, using Pearson correlation. One way to compute this is by measuring the Pearson correlation in a small portion of the signal, and repeat the process along a rolling window until the entire signal is covered. This can be somewhat subjective as it requires arbitrarily defining the window size you’d like to repeat the procedure. In the code below we use a window size of 120 frames (~4 seconds) and plot the moment-to-moment synchrony in the bottom figure.

Overall, the Pearson correlation is a good place to start as it provides a very simple way to compute both global and local synchrony. However, this still does not provide insights into signal dynamics such as which signal occurs first which can be measured via cross correlations.

---

## Time Lagged Cross Correlation — assessing signal dynamics

Time lagged cross correlation (TLCC) can identify directionality between two signals such as a leader-follower relationship in which the leader initiates a response which is repeated by the follower. There are couple ways to do investigate such relationship including Granger causality, used in Economics, but note that these still do not necessarily reflect true causality. Nonetheless we can still extract a sense of which signal occurs first by looking at cross correlations.

![http://robosub.eecs.wsu.edu/wiki/ee/hydrophones/start](https://miro.medium.com/v2/resize:fit:640/1*mWsGTGVdAsy6KoF3n3MyLA.gif)

As shown above, TLCC is measured by incrementally shifting one time series vector (red) and repeatedly calculating the correlation between two signals. If the peak correlation is at the center (offset=0), this indicates the two time series are most synchronized at that time. However, the peak correlation may be at a different offset if one signal leads another. The code below implements a cross correlation function using pandas functionality. It can also wrap the data so that the correlation values on the edges are still calculated by adding the data from the other side of the signal.

```python

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

```

![Peak synchrony is not at the center, suggesting a leader-follower signal dynamic.
](https://miro.medium.com/v2/resize:fit:720/format:webp/1*3mGkchTMkLvCaFgY8zOQcA.png)

In the plot above, we can infer from the negative offset that Subject 1 (S1) is leading the interaction (correlation is maximized when S2 is pulled forward by 46 frames). But once again this assesses signal dynamics at a global level, such as who is leading during the entire 3 minute period. On the other hand we might think that the interaction may be even more dynamic such that the leader follower roles vary from time to time.

---

### Windowed time lagged cross correlations (WTLCC)

To assess the more fine grained dynamics, we can compute the windowed time lagged cross correlations (WTLCC). This process repeats the time lagged cross correlation in multiple windows of the signal. Then we can analyze each window or take the sum over the windows would provide a score comparing the difference between the leader follower interaction between two individuals.

## Dynamic Time Warping — synchrony of signals varying in lengths

Dynamic time warping (DTW) is a method that computes the path between two signals that minimize the distance between the two signals. The greatest advantage of this method is that it can also deal with signals of different length. Originally devised for speech analysis (learn more in [this video](https://www.youtube.com/watch?v=_K1OsqCicBY)), DTW computes the euclidean distance at each frame across every other frames to compute the minimum path that will match the two signals. One downside is that it cannot deal with missing values so you would need to interpolate beforehand if you have missing data points.

![XantaCross](https://miro.medium.com/v2/resize:fit:640/format:webp/1*LXQSbLyr_d_IkiDjiWx5nA.jpeg)

To compute DTW, we will use the `dtw` Python package which will speed up the calculation.

![path cost](https://miro.medium.com/v2/resize:fit:640/format:webp/1*Jg6QtRHd7VCZR-YPtgvLyQ.png)

Here we can see the minimum path shown in the white convex line. In other words, earlier Subject2 data is matched with synchrony of later Subject1 data. The minimum path cost is d=.33 which can be compared with that of other signals.

## Instantaneous phase synchrony

Lastly, if you have a time series data that you believe may have oscillating properties (e.g. EEG, fMRI), you may also be able to measure instantaneous phase synchrony. This measure also measures moment-to-moment synchrony between two signals. It can be somewhat subjective because you need to filter the data to the wavelength of interest but you might have theoretical reasons for determining such bands. To calculate phase synchrony, we need to extract the phase of the signal which can be done by using the Hilbert transform which splits the signal into its phase and power ([learn more about Hilbert transform here](https://www.youtube.com/watch?v=VyLU8hlhI-I)). This allows us to assess if two signals are in phase (moving up and down together) or out of phase.

![Gonfer at English Wikipedia](https://miro.medium.com/v2/resize:fit:640/1*Bo0LsXy6kq1oWcw2RAkRCA.gif)

![Filtered time series (top), angle of each signal at each moment in time (middle row), and instantaneous phase synchrony measure (bottom)](https://miro.medium.com/v2/resize:fit:720/format:webp/1*na7RbielmedgyqvqRzfk-g.png)

The instantaneous phase synchrony measure is a great way to compute moment-to-moment synchrony between two signals without arbitrarily deciding the window size as done in rolling window correlations. If you’d like to know how instantaneous phase synchrony compares to windowed correlations, [check out my earlier blog post here](http://jinhyuncheong.com/jekyll/update/2017/12/10/Timeseries_synchrony_tutorial_and_simulations.html).

## Conclusion

Here we covered four ways to measure synchrony between time series data: Pearson correlation, time lagged cross correlations, dynamic time warping, and instantaneous phase synchrony. Deciding the synchrony metric will be based on the type of signal you have, the assumptions you have about the data, and your objective in what synchrony information you’d like from the data. Feel free to leave any questions or comments below!
