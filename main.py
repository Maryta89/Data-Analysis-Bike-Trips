import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# -------------------- Style Settings --------------------
sns.set_theme(style="whitegrid", palette="Set2")
plt.rcParams["figure.dpi"] = 120
plt.rcParams["axes.titlesize"] = 11
plt.rcParams["axes.labelsize"] = 9

# -------------------- Load and Clean Data --------------------
file_path = "DataSet.csv"
df = pd.read_csv(file_path)

# Convert to datetime
df["Departure"] = pd.to_datetime(df["Departure"], errors="coerce")
df["Return"] = pd.to_datetime(df["Return"], errors="coerce")

# Remove invalid / missing data
df.dropna(subset=["Departure", "Return", "Covered distance (m)"], inplace=True)
df = df[(df["Covered distance (m)"] > 0) & (df["Duration (sec.)"] > 0)]
df = df[df["Duration (sec.)"] < 36000]  # remove extreme outliers

# Add helpful columns
df["Duration (min)"] = df["Duration (sec.)"] / 60
df["Date"] = df["Departure"].dt.date

# -------------------- Key Stats --------------------
print("Total trips:", len(df))
print("Average duration (min):", round(df["Duration (min)"].mean(), 2))
print("Average distance (m):", round(df["Covered distance (m)"].mean(), 2))

# -------------------- Prepare data for plots --------------------
top_departure = df["Departure station name"].value_counts().head(10)
top_return = df["Return station name"].value_counts().head(10)
daily_trips = df["Date"].value_counts().sort_index()

# -------------------- Dashboard Layout --------------------
fig, axes = plt.subplots(3, 2, figsize=(14, 12))
fig.suptitle("🚴‍♀️ Bike Trips Data Analysis Dashboard", fontsize=16, fontweight="bold", color="#333")

# Trip Duration Distribution
sns.histplot(df["Duration (min)"], bins=50, kde=True, color="#60A5FA", ax=axes[0,0])
axes[0,0].set_title("Trip Duration Distribution (minutes)")
axes[0,0].set_xlabel("Duration (min)")
axes[0,0].set_ylabel("Trips")

# Covered Distance Distribution
sns.histplot(df["Covered distance (m)"], bins=50, kde=True, color="#34D399", ax=axes[0,1])
axes[0,1].set_title("Covered Distance Distribution (meters)")
axes[0,1].set_xlabel("Distance (m)")
axes[0,1].set_ylabel("Trips")

# Top 10 Departure Stations
sns.barplot(x=top_departure.values, y=top_departure.index, palette="Set3", ax=axes[1,0])
axes[1,0].set_title("Top 10 Departure Stations")
axes[1,0].set_xlabel("Number of Departures")
axes[1,0].set_ylabel("Station Name")

# Top 10 Return Stations
sns.barplot(x=top_return.values, y=top_return.index, palette="Paired", ax=axes[1,1])
axes[1,1].set_title("Top 10 Return Stations")
axes[1,1].set_xlabel("Number of Returns")
axes[1,1].set_ylabel("Station Name")

# Trips per Day (Line Chart)
sns.lineplot(x=daily_trips.index, y=daily_trips.values, color="#F59E0B", linewidth=2.5, ax=axes[2,0])
axes[2,0].set_title("Trips per Day")
axes[2,0].set_xlabel("Date")
axes[2,0].set_ylabel("Number of Trips")
axes[2,0].tick_params(axis='x', rotation=45)

# Hide the last empty subplot
axes[2,1].axis("off")

plt.tight_layout(rect=[0, 0, 1, 0.96])

# Save dashboard image
output_path = os.path.join(os.getcwd(), "bike_data_dashboard.png")
plt.savefig(output_path, dpi=300)
plt.close()

print("✅ Dashboard created and saved successfully at:", output_path)
