#https://www.statology.org/correlation-test-in-python/#:~:text=To%20determine%20if%20the%20correlation,two%2Dtailed%20p%2Dvalue.
#

#create two arrays
x = [3, 4, 4, 5, 7, 8, 10, 12, 13, 15]
y = [2, 4, 4, 5, 4, 7, 8, 19, 14, 10]

from scipy.stats import pearsonr

#calculation correlation coefficient and p-value between x and y
results = pearsonr(x, y)

print(results)
# (0.8076177030748631, 0.004717255828132089)