# this uses the weightings used by the canadian crime index
# http://www.statcan.gc.ca/pub/85-004-x/2009001/t001-eng.htm
import numpy as np
import pandas
import seaborn as sns

descriptions = {
    "ATTEMPTED HOMICIDE": 1411
}
categories = {
    "LARCENY/THEFT": 37,
    "OTHER OFFENSES": 30,
    "NON-CRIMINAL": 9,
    "ASSAULT": 267,
    "VEHICLE THEFT": 84,
    "WARRANTS": 16,
    "DRUG/NARCOTIC": 69,
    "SUSPICIOUS OCC": 9,
    "MISSING PERSON": 30,
    "SECONDARY CODES": 9,
    "WEAPON LAWS": 267,
    "ROBBERY": 583,
    "TRESPASS": 187,
    "FRAUD": 109,
    "DRUNKENNESS": 30,
    "KIDNAPPING": 678,
    "PROSTITUTION": 30,
    "DRIVING UNDER THE INFLUENCE": 23,
    "ARSON": 267,
    "RUNAWAY": 30,
    "LIQUOR LAWS": 9,
    "DISORDERLY CONDUCT": 30,
    "FORGERY/COUNTERFEITING": 69,
    "VANDALISM": 30,
    "SUICIDE": 30,
    "FAMILY OFFENSES": 23,
    "EMBEZZLEMENT": 109,
    "STOLEN PROPERTY": 37,
    "EXTORTION": 109,
    "BURGLARY": 583,
    "LOITERING": 9,
    "GAMBLING": 69,
    "PORNOGRAPHY/OBSCENE MAT": 9,
    "BRIBERY": 69,
}

sanfran = pandas.read_csv("sanfrancisco_incidents_summer_2014.csv", parse_dates=True)
print(sanfran.describe())
sanfran["DateTime"] = pandas.to_datetime(sanfran["Date"] + " " + sanfran["Time"])
# sanfran["Date"] = pandas.to_datetime(sanfran["Date"])

sanfran["Severity"] = np.nan

for descript in descriptions:
    severity = descriptions[descript]
    mask = sanfran["Descript"].str.contains(descript) & sanfran["Severity"].isnull()
    # print("Description:%s Severity:%s count:%s" % (descript, severity, sum(mask)))
    sanfran.loc[mask, "Severity"] = severity

for cat in categories:
    severity = categories[cat]
    mask = (sanfran["Category"] == cat) & sanfran["Severity"].isnull()
    # print("Category:%s Severity:%s count:%s" % (cat, severity, sum(mask)))
    sanfran.loc[mask, "Severity"] = severity


print("Missing Severities: %s" % sum(sanfran["Severity"].isnull()))

print("Average severity %s" % sanfran["Severity"].mean())

grouped = sanfran.groupby("PdDistrict", as_index=False).agg(sum)
# [["PdDistrict", "Severity"]]
grouped = grouped.sort_values("Severity")
# print(grouped)
plot = sns.barplot(data=grouped, x="Severity", y="PdDistrict", )
plot.set_xlabel("Total Weighted Severity")
plot.set_ylabel("Police Department District")

# sns.plt.figure()
# f, ax = plt.subplots(figsize=(15, 6))


#
# Severity by date and district
#
grouped2 = sanfran.sort_values("Date").groupby(["Date", "PdDistrict"], as_index=False).agg(sum)
grouped2.pivot(index="Date", columns="PdDistrict", values="Severity").plot()

# as grouping by Date and DayOfWeek doesn't plot right...
# grouped2["DayOfWeek"] = grouped2["Date"].dt.dayofweek.map(
#     {0: "MONDAY", 1: "TUESDAY", 2: "WEDNESDAY", 3: "THURSDAY", 4: "FRIDAY", 5: "SATURDAY", 6: "SUNDAY"})
# grouped2 = grouped2.sort_values("Date")
# plot2 = sns.barplot(data=grouped2, x="Date", y="Severity", hue="DayOfWeek")
# plot2 = sns.barplot(data=grouped2, x="Date", y="Severity") #, color=sns.color_palette("Blues_d", n_colors=7))
# plot2 = sns.tsplot(data=grouped2, time="Date", value="Severity")
# plot2 = grouped2[["PdDistrict", "Date", "Severity"]].set_index('Date').plot()
# plot2.set_ylabel("Total Weighted Severity")
# plot2.set_xlabel("Date")

# grouped2 = sanfran.sort_values("Date").groupby(["Date", "PdDistrict"]).agg(sum)
# plot2 = grouped2[["Severity"]].plot()

# sns.plt.show()

# grouped3 = sanfran.sort_values("DateTime").groupby(["DateTime"]).agg(sum)
# grouped3[["Severity"]].plot.line()
# grouped3 = sanfran.sort_values("DateTime").groupby(["DateTime"]).agg(sum)
# bins = np.linspace(sanfran["DateTime"].min().value, sanfran["DateTime"].max().value, num=20)
# bins = pandas.to_datetime(bins)
# plot3 = sanfran[["DateTime", "Severity"]].hist(by="DateTime", bins=bins)
# plt.gcf().autofmt_xdate()

#
# http://stackoverflow.com/questions/16947336/binning-a-dataframe-in-pandas-in-python
#