import datetime

import numpy as np
import pandas
import seaborn as sns
from geopy.distance import vincenty
from matplotlib import colors
from matplotlib.lines import Line2D


def print_nominals(data):
    # print("\n\ncategories(Category):")
    # print(data["Descript"].unique())

    # uses IncidntNum as every row has it populated
    categories = data.groupby("Category")["IncidntNum"].count().sort_values(0, ascending=False)
    print("")
    print(categories)

    descriptions = data.groupby("Descript")["IncidntNum"].count().sort_values(0, ascending=False)
    print("")
    print(descriptions)

    districts = data.groupby("PdDistrict")["IncidntNum"].count().sort_values(0, ascending=False)
    print("")
    print(districts)

    resolutions = data.groupby("Resolution")["IncidntNum"].count().sort_values(0, ascending=False)
    print("")
    print(resolutions)

    print("\n\n")
    print("number of records: %s" % data["IncidntNum"].size)
    print("number of incidntNum: %s" % data["IncidntNum"].unique().size)
    print("number of PdId: %s" % data["PdId"].unique().size)


def calculate_distances(data):
    # type: (pandas.DataFrame) -> None

    # parse location into tuples
    # print(sanfran["Location"][0])
    # print(sanfran["Location"].str.extract("\\(([^,]*), ([^)]*)\\)", expand=True)[1:5])
    sanfran = data.sort_values(["PdDistrict", "DateTime"], )
    tuples = [tuple(x) for x in sanfran["Location"].str.extract("\\(([^,]*), ([^)]*)\\)", expand=True).values]
    sanfran["Location"] = pandas.Series(tuples)
    print(sanfran["Location"][0])

    sanfran["LocationP1"] = sanfran["Location"].shift(1)
    # distances = vincenty(sanfran["Location"], sanfran["Location"].shift(1)).miles
    vincenty(sanfran["Location"][0], sanfran["Location"][1]).miles
    # print(distances)


print("Reading data...")
sanfran = pandas.read_csv("sanfrancisco_incidents_summer_2014.csv", parse_dates={'DateTime': ['Date', 'Time']})


# wrong sanfran["Date"] = pandas.concat([sanfran["Date"], sanfran["Time"]]).reindex_like(sanfran)
# sanfran["DateTime"] = pandas.to_datetime(sanfran["Date"] + " " + sanfran["Time"])
# sanfran["Date"] = pandas.to_datetime(sanfran["Date"], dayfirst=False)
# sanfran["Time"] = pandas.to_datetime(sanfran["Time"], dayfirst=False)


# print(sanfran.describe())
# print(sanfran[0:4])



def plot_category(data):
    print("plotting categories")
    sanfran = data.groupby("IncidntNum").first()

    plot1 = sns.stripplot(x="DateTime", y="Category", data=sanfran, jitter=True)
    plot1.set_xlim(datetime.datetime(2014, 6, 1), datetime.datetime(2014, 9, 1))

    # sns.barplot(x="DateTime", y="Category", data=sanfran, jitter=True)

    # g = sns.FacetGrid(data=sanfran, row="PdDistrict", col="DayOfWeek")
    # g.map(sns.barplot, "DateTime", "Category", estimator=len).set_axis_labels("Date", "Category")
    # sns.tsplot(sanfran, time="DateTime", value="")

    sns.plt.show()
    print("Done plot")


def plot_districts(data):
    print("plotting districts")
    filteredData = data.groupby("IncidntNum").first()

    plot1 = sns.stripplot(x="DateTime", y="PdDistrict", data=filteredData, jitter=True)
    plot1.set_xlim(datetime.datetime(2014, 6, 1), datetime.datetime(2014, 9, 1))

    # plot2 = sns.swarmplot(x="DateTime", y="PdDistrict", data=filteredData)
    # f, axes = plt.subplots(figsize=(7, 7))
    plot2 = sns.violinplot(x="DateTime", y="PdDistrict", data=filteredData)
    plot2.set_xlim(datetime.datetime(2014, 6, 1), datetime.datetime(2014, 9, 1))

    print("Done plot(s)")


def print_categories(data):
    print("homicides/murder")
    print(sanfran[sanfran["Descript"].str.contains("HOMICIDE")][["Descript", "Category"]]
          .groupby(["Descript", "Category"]).aggregate(len))

    print("gun crimes")
    print(sanfran[sanfran["Descript"].str.contains("GUN")][["Descript", "Category"]]
          .groupby(["Descript", "Category"]).aggregate(len))

    print("sex crimes")
    print(sanfran[sanfran["Descript"].str.contains("SEX")][["Descript", "Category"]]
          .groupby(["Descript", "Category"]).aggregate(len))


# plot_category(sanfran)

print("Munging data...")

sanfran['HourOfDay'] = [r.hour for r in sanfran["DateTime"]]
sanfran['Date'] = sanfran["DateTime"].dt.date

print("Creating resolution fields...")
sanfran['Arrested or Booked'] = sanfran["Resolution"].str.contains("ARREST") | sanfran["Resolution"].str.contains(
    "BOOKED") | sanfran["Resolution"].str.contains("JUVENILE BOOKED")
# sanfran['Booked'] = sanfran["Resolution"].str.contains("BOOKED") | sanfran["Resolution"].str.contains("JUVENILE BOOKED")
sanfran['No Resolution'] = sanfran["Resolution"].str.contains("NONE")
sanfran['Other Resolution'] = ~(sanfran['No Resolution'] | sanfran['Arrested or Booked'])

print("Indexing categories")
districtMap = {}
for idx, dist in enumerate(sanfran["PdDistrict"].unique()):
    districtMap[dist] = float(idx) / 10.0

catMap = dict()
for idx, cat in enumerate(sanfran["Category"].unique()):
    catMap[cat] = Line2D.markers.keys()[idx]

sanfran["DistrictNum"] = sanfran["PdDistrict"].map(districtMap)
sanfran["CategoryMarker"] = sanfran["Category"].map(catMap)


# i'm sure these can be re-written using some builtin function wrappers
# @numba.jit()
def bitwise_or_reduce(x):
    return x.any()


# @numba.jit
def agg_first(x=None):
    return x.iloc[0]


# @numba.jit
def bin_t(x):
    return datetime.datetime(x.year, x.month, x.day, x.hour, 0, 0)


def do_filter():
    global filteredData

    func_map = dict.fromkeys(sanfran.columns.values, agg_first)
    del func_map["IncidntNum"]
    func_map["Arrested or Booked"] = func_map["No Resolution"] = func_map["Other Resolution"] = bitwise_or_reduce

    print("Filtering data... (grouping)")
    grouped = sanfran.groupby("IncidntNum", as_index=False)
    print("Filtering data... (aggregating)")
    filteredData = grouped.agg(func_map)

    print("Updating filtered data...")
    # filteredData['No Resolution'] = ~filteredData['Arrested or Booked'] & ~filteredData['Other Resolution'] & filteredData['No Resolution']
    filteredData['No Resolution'] = pandas.eval(
        "~filteredData['Arrested or Booked'] & ~filteredData['Other Resolution'] & filteredData['No Resolution']")


do_filter()

print("Binning...")
bins = pandas.to_datetime(np.linspace(sanfran["DateTime"].min().value, sanfran["DateTime"].max().value, num=20))

print("ready")

colors.ListedColormap