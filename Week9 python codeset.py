 
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from scipy import stats
%matplotlib inline
conn = sqlite3.connect('D:/Erik/cunyweek9.sqlite')
cur = conn.cursor()

#Takes the data from the SQLite database and generates a set of points
def read_table(tablename):
    table = str(tablename)
    cur.execute('SELECT * FROM %s' %table)
    points = []
    for row in cur:
        points.append(row)
        points.sort()
    return points

#Takes a list of points(as a tuple or list), a title for the plot, and degree of the
#model and generates a scatterplot and a regression line for the data.
def plot_reg(ax, points, title, degree=1):
    x = []
    y = []
    for point in points:
        x.append(point[0])
        y.append(point[1])
    fit = np.polyfit(x, y, degree)
    yp = np.polyval(fit, x)
    ax.scatter(x, y) #Scatter plot of the data
    ax.plot(x,yp) #Plots the regression line
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title(title)

#Generates and output of the descriptive statistics for the data set    
def des_stats(points,title):
    n, min_max, mean, var, skew, kurt = stats.describe(points) #scipy function for descriptive stats
    print title
    print 'Number of elements: %d' % n
    min_val = min_max[0][1]
    max_val = min_max[1][1]
    print 'Minimum: %f Maximum: %f' % (min_val, max_val)
    print 'Mean: %f' % mean[1]
    print 'Variance: %f' % var[1]
    print 'Skew : %f' % skew[1]
    print 'Kurtosis: %f' % kurt[1]
    print ''

#Generates the Ordininary Least Squares regression and prints the summary stats.
def least_squares(points,title):
    x = []
    y = []
    for point in points:
        x.append(point[0])
        y.append(point[1])
    ols_model = sm.OLS(y, x) #OLS must be capatialized here.
    ols_fit = ols_model.fit()
    print title
    print ols_fit.summary()
    print ' '
    
#Finally we call the function for each table in the database and assign each to it's own list.  
points1 = read_table('I')
points2 = read_table('II')
points3 = read_table('III')
points4 = read_table('IV')

#Plotting the 4 data sets with regression lines.
#fig allows you to put multiple plots in one resizable figure
fig, ((ax1, ax2),(ax3,ax4)) = plt.subplots(nrows=2, ncols=2)
plot_reg(ax1, points1, 'Data Set I')
plot_reg(ax2, points2, 'Data Set II')
plot_reg(ax3, points3, 'Data Set III')
plot_reg(ax4, points4, 'Data Set IV')
plt.tight_layout()

#running the linear regression on the four data sets.
least_squares(points1,'Data Set I')
least_squares(points2,'Data Set II')
least_squares(points3,'Data Set III')

#descriptive statistics for the four data sets.
#using scipy to do descriptive stats on the data set
des_stats(points1, 'Data Set I')
des_stats(points2, 'Data Set II')
des_stats(points3, 'Data Set III')
des_stats(points4, 'Data Set IV')
least_squares(points4,'Data Set IV')

#evaluate the Data Set III again with the outlier removed.
#Removing the outlier and sorting the data.
points5 = [(10,7.46), (8,6.77), (9, 7.11), (11, 7.81), (14, 8.84), (6, 6.08), (4, 5.39),
           (12, 8.15), (7, 6.42), (5, 5.73)]
points5.sort()

#Generating the plot.
fig, ax = plt.subplots()
plot_reg(ax, points5, 'Data III with Outlier Removed')
plt.tight_layout()

#Generating the regression statistics.
least_squares(points5, 'Data III with Outlier Removed')

#Generating the descriptive statistics.
des_stats(points5, 'Data III with Outlier Removed')

# fitting various polynomial functions to Data Set II.
#Trying four different polynomial regressions.
fig, ((ax1, ax2),(ax3,ax4)) = plt.subplots(nrows=2, ncols=2)
plot_reg(ax1, points2, 'Data Set II - Linear', 1)
plot_reg(ax2, points2, 'Data Set II - Quadratic', 2)
plot_reg(ax3, points2, 'Data Set II - Cubic', 3)
plot_reg(ax4, points2, 'Data Set II - Quartic', 4)
plt.tight_layout()


