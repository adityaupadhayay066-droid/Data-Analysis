import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
df = pd.read_csv("Zomato data .csv")
df.columns = df.columns.str.strip()
print(df.columns)
print(df.head(),"\n")
print(df.tail ())

# Removing extra values 
def Remove(value):
    value = str(value).split("/")[0]
    return float(value)
df["rate"] = df["rate"].apply(Remove)
plt.figure(figsize=(10,5))
sns.countplot(x ="listed_in(type)", data=df, palette="cubehelix")
plt.title("Restraunt Rating",fontweight="bold",size=20)
plt.xlabel("Restraunt Type", fontweight="bold",size=16)
plt.ylabel("Count",fontweight="bold",size=16)
plt.savefig("Restraunt_Rating.png")
plt.xticks(rotation=45)


plt.figure(figsize=(10,5))
sns.scatterplot(x="rate", y="votes", data=df)
plt.title("Rate vs Votes", fontweight="bold", size=16)
plt.savefig("Restraunt_Rating.png")
plt.show()
