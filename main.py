import pandas as pd

df = pd.read_csv("data_old/Market_Sizes.csv")
df = df.dropna()
df = df.drop(
    columns=[
        "Industry",
        "Data_Type",
        "Edition",
        "Currency_Conversion",
        "Current_Constant",
        "Unit",
        "Year_date",
        "Year_minus_2016",
        "Year_minus_2022",
    ]
)

df = df.rename(columns={"RSP": "RSP_USD_Mnl"})
df.loc[(df["RSP_USD_Mnl"] < df["Volume"]), "RSP_USD_Mnl"] = df["RSP_USD_Mnl"] * 1000
df.to_csv("data_new/Market_Sizes.csv", index=False)

df2 = pd.read_csv("data_old/Channel_Volume.csv")
df2.dropna()
df2["Volume"] = [float(str(i).replace(",", ".")) for i in df2["Volume"]]
df2.loc[df["Unit"] == "million litres", "Volume"] = df2["Volume"] * 100
df2 = df.drop(
    columns=["Category", "Unit", "Industry", "Edition", "Data_Type", "Year_date"]
)
df2 = df2.rename(columns={"Volume": "Volume_Kl", "Year_text": "Year"})

df2.to_csv("data_new/Channel_Volume.csv", index=False)


df3 = pd.read_csv("data_old/Company_Share_GBO_unit.csv", sep=";")
df3 = df3.dropna()
df3["Volume"] = [float(str(i).replace(",", ".")) for i in df3["Volume"]]
df3 = df3.drop(
    columns=["Unit", "Industry", "Data_Type", "Year_minus_2016", "Year_date"]
)
df3 = df3.rename(columns={"Year_text": "Year", "Volume": "Volume_Kl"})
df3["Volume_Kl"] = [float(str(i).replace(",", ".")) for i in df3["Volume_Kl"]]
df3 = df3.astype(
    {
        "Location": "int",
        "Subcategory_ID": "int",
        "Hierarchy_Level": "int",
        "Year": "int",
    }
).round({"Location": 1, "Subcategory_ID": 1, "Hierarchy_Level": 1, "Year": 1})
df3.to_csv("data_new/Company_Share_GBO_unit.csv", index=False)

df4 = pd.read_csv("data_old/Locations.csv", delimiter=";")
df4 = df.dropna(axis=1)
df4.to_csv("data_new/Locations.csv", index=False)

df5 = pd.read_csv("data_new/Company_Share_GBO_unit.csv")
df6 = pd.read_csv("data_new/Subcategories.csv")
df6 = df6.merge(df5, left_on="id", right_on="Subcategory_ID")
df6 = df6[["id", "Category", "Name", "Subcategory_ID", "Hierarchy_Level"]]
df6.drop_duplicates(subset=["Subcategory_ID"], inplace=True)
df6.to_csv("data_new/Subcategories2.csv")
