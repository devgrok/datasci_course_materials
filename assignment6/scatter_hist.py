import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import pandas
import seaborn as sns
from geopy.distance import vincenty

sanfran = pandas.read_csv("sanfrancisco_incidents_summer_2014.csv")
# wrong sanfran["Date"] = pandas.concat([sanfran["Date"], sanfran["Time"]]).reindex_like(sanfran)
sanfran["Date"] = pandas.to_datetime(sanfran["Date"] + " " + sanfran["Time"])
# sanfran["Date"] = pandas.to_datetime(sanfran["Date"], dayfirst=False)
# sanfran["Time"] = pandas.to_datetime(sanfran["Time"], dayfirst=False)

# parse location into tuples
sanfran["Location"] = sanfran["Location"]

print(sanfran.describe())
print(sanfran[1:5])

# the random data
# x = np.random.randn(1000)
# y = np.random.randn(1000)

print("plotting")

#sns.stripplot(x="Date", y="Category", data=sanfran, jitter=True)
#sns.barplot("Date", y="Category", data=sanfran, jitter=True)

g = sns.FacetGrid(data=sanfran, row="PdDistrict", col="DayOfWeek")
g.map(sns.barplot, "Date", "Category", estimator=len).set_axis_labels("Date", "Category")

sns.plt.show()
print("Done plot")

# fig, axScatter = plt.subplots(figsize=(5.5, 5.5))
#
# # the scatter plot:
# axScatter.scatter(x="Date", y="Time", data=sanfran)
# axScatter.set_aspect(1.)
#
# # create new axes on the right and on the top of the current axes
# # The first argument of the new_vertical(new_horizontal) method is
# # the height (width) of the axes to be created in inches.
# divider = make_axes_locatable(axScatter)
# axHistx = divider.append_axes("top", 1.2, pad=0.1, sharex=axScatter)
# axHisty = divider.append_axes("right", 1.2, pad=0.1, sharey=axScatter)
#
# # make some labels invisible
# plt.setp(axHistx.get_xticklabels() + axHisty.get_yticklabels(),
#          visible=False)
#
# # now determine nice limits by hand:
# binwidth = 0.25
# xymax = np.max([np.max(np.fabs(x)), np.max(np.fabs(y))])
# lim = (int(xymax/binwidth) + 1)*binwidth
#
# bins = np.arange(-lim, lim + binwidth, binwidth)
# axHistx.hist(x, bins=bins)
# axHisty.hist(y, bins=bins, orientation='horizontal')
#
# # the xaxis of axHistx and yaxis of axHisty are shared with axScatter,
# # thus there is no need to manually adjust the xlim and ylim of these
# # axis.
#
# #axHistx.axis["bottom"].major_ticklabels.set_visible(False)
# for tl in axHistx.get_xticklabels():
#     tl.set_visible(False)
# axHistx.set_yticks([0, 50, 100])
#
# #axHisty.axis["left"].major_ticklabels.set_visible(False)
# for tl in axHisty.get_yticklabels():
#     tl.set_visible(False)
# axHisty.set_xticks([0, 50, 100])

#plt.draw()
#plt.show()