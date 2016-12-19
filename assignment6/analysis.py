import pandas
from geopy.distance import vincenty


# from multiprocessing import Pool, cpu_count
# pool = Pool(cpu_count())  # use cpu processes

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


sanfran = pandas.read_csv("sanfrancisco_incidents_summer_2014.csv", parse_dates={'DateTime': ['Date', 'Time']})


# wrong sanfran["Date"] = pandas.concat([sanfran["Date"], sanfran["Time"]]).reindex_like(sanfran)
# sanfran["DateTime"] = pandas.to_datetime(sanfran["Date"] + " " + sanfran["Time"])
# sanfran["Date"] = pandas.to_datetime(sanfran["Date"], dayfirst=False)
# sanfran["Time"] = pandas.to_datetime(sanfran["Time"], dayfirst=False)


# print(sanfran.describe())
# print(sanfran[0:4])



def plot_category(data):
    import seaborn as sns
    print("plotting")
    sanfran = data.groupby("IncidntNum").first()
    sns.stripplot(x="DateTime", y="Category", data=sanfran, jitter=True)
    sns.barplot(x="DateTime", y="Category", data=sanfran, jitter=True)

    g = sns.FacetGrid(data=sanfran, row="PdDistrict", col="DayOfWeek")
    g.map(sns.barplot, "DateTime", "Category", estimator=len).set_axis_labels("Date", "Category")

    sns.plt.show()
    print("Done plot")


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


print("ready")
