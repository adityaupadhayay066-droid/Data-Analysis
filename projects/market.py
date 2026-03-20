import pandas as pd
import matplotlib.pyplot as plt 

# Read  csv file
df = pd.read_csv("ADANIPORTS.csv")
df.columns = df.columns.str.strip() # Remove extra spaces form the Columns name form start and end 
print("Hape of csv file ",df.shape)
print("Data info : ",df.info()) # missing values
print("Number of duplicate column present",df.columns)
print("------Find Null value ---------")
df.dropna(inplace = True)
print("---------------------")
print("Number of duplicate row present : ",df.duplicated().sum())  # find duplicate rows in the csv 
# convert Date column to realtime datetime
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date")
print(df["Date"].head())
print(df.columns.tolist())
'''this convert into datetime because csv don't understand dtype int,float Date column only raad ash text, 
pd.to_datetime convert into real time datetime so Pandas can sort and Understand'''

# plotting start from here 
plt.figure(figsize=(10,5))  # figure control size of graph figsize(width,height)
plt.plot(df["Date"], df["Close"],linewidth=1,color = "red")
plt.title("ADANIPORTS closing price over time")
plt.xlabel("Date")
plt.ylabel("Closing prices(₹)")
plt.xticks(rotation=45)  # it rotate 
plt.tight_layout()
plt.savefig("Closing_price.png")  # save the plotting in png format 

# plotting  trading Volume
plt.figure(figsize =(10,5))
plt.plot(df["Date"], df["Volume"],)
plt.title("VOLUME TRADING OVER")
plt.xlabel("Date")
plt.ylabel("Volume")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("Trading_volume.png")
# plotting High vs low 
plt.figure(figsize=(10,5)) 
plt.plot(df["Date"],df["Low"], label ="LOW", linewidth =2, color ="red")
plt.plot(df["Date"], df["High"],label = "HIGH",linewidth =2,color="green")
plt.title("HIGH VS LOW DATA")
plt.xlabel("Date")
plt.legend()
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout() # Automatically adjusts spacing between plot elements so that they do not overlap.
plt.savefig("High_vs_Low.png")

# find moving average 20 and 50 days
df["MA_20"] = df["Close"].rolling(window=20).mean()
df["MA_50"] = df["Close"].rolling(window=50).mean()
plt.figure(figsize=(10,5))
plt.plot(df["Date"],df["Close"], label ="Close")
plt.plot(df["Date"],df["MA_20"], label ="Moving average of 20 days")
plt.plot(df["Date"],df["MA_50"], label ="Moving average of 50 days")
plt.title("Moving average at Close time")
plt.legend()
plt.xticks(rotation = 45)
plt.tight_layout() 
plt.savefig("Moving_averages.png")
plt.show() 