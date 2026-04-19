import pandas as pd
from pathlib import Path

CSV_FILE = Path(r"C:\Users\User\Desktop\FileOrganizer\iris\iris.data")
column_names = [
    "sepal_length", 
    "sepal_width", 
    "petal_length", 
    "petal_width", 
    "species"
]

# Load the CSV 
df = pd.read_csv(CSV_FILE, header=None, names=column_names)

# print("=" * 50)
# print("DATASET OVERVIEW")
# print("=" * 50)

# # How many rows and columns?
# print(f"\nRows    : {df.shape[0]}")
# print(f"Columns : {df.shape[1]}")

# # First 5 rows
# print("\n--- First 5 Rows ---")
# print(df.head())

# # Last 5 rows
# print("\n--- Last 5 Rows ---")
# print(df.tail())

# # Column names and data types
# print("\n--- Columns & Data Types ---")
# print(df.dtypes)

# # Basic statistics
# print("\n--- Basic Statistics ---")
# print(df.describe())

# ── LEVEL 2: SELECT & FILTER ──────────────────────────
# print("\n" + "=" * 50)
# print("SELECT & FILTER")
# print("=" * 50)

# # Select a single column
# print("\n--- Petal Length Column Only ---")
# print(df["petal_length"].head())

# # Select multiple columns
# print("\n--- Petal Measurements Only ---")
# print(df[["petal_length", "petal_width"]].head())

# # Filter rows by condition
# print("\n--- Rows Where Petal Length > 5 ---")
# long_petals = df[df["petal_length"] > 5]
# print(long_petals.head())
# print(f"Count: {len(long_petals)} flowers have petal length > 5")

# # Filter by species
# print("\n--- Iris Setosa Only ---")
# setosa = df[df["species"] == "Iris-setosa"]
# print(setosa.head())
# print(f"Count: {len(setosa)} Setosa flowers")

# # Multiple conditions
# print("\n--- Long AND Narrow Petals ---")
# filtered = df[(df["petal_length"] > 5) & (df["petal_width"] < 2)]
# print(filtered.head())
# print(f"Count: {len(filtered)} flowers match")

# ── LEVEL 3: SORT ─────────────────────────────────────
# print("\n" + "=" * 50)
# print("SORT & RANK")
# print("=" * 50)

# # Sort by petal length descending
# print("\n--- Top 5 Largest Petals ---")
# print(df.sort_values("petal_length", ascending=False).head())

# # Sort by petal length ascending
# print("\n--- Top 5 Smallest Petals ---")
# print(df.sort_values("petal_length", ascending=True).head())

# # Sort by multiple columns
# print("\n--- Sorted by Species then Petal Length ---")
# print(df.sort_values(["species", "petal_length"], ascending=[True, False]).head(8))


# # ── LEVEL 4: GROUP BY ─────────────────────────────────
# print("\n" + "=" * 50)
# print("GROUP BY SPECIES")
# print("=" * 50)

# # Mean of every column per species
# print("\n--- Average Measurements Per Species ---")
# print(df.groupby("species").mean().round(2))

# # Min and max per species
# print("\n--- Min Per Species ---")
# print(df.groupby("species").min().round(2))

# print("\n--- Max Per Species ---")
# print(df.groupby("species").max().round(2))

# # Count per species
# print("\n--- Count Per Species ---")
# print(df.groupby("species").size())

# # Multiple stats at once
# print("\n--- Full Stats Per Species ---")
# print(df.groupby("species").agg(["mean", "min", "max"]).round(2))


# ── LEVEL 5: ADD COLUMNS & TRANSFORM ──────────────────
# print("\n" + "=" * 50)
# print("ADD COLUMNS & TRANSFORM")
# print("=" * 50)

# # Add a new calculated column
# df["petal_ratio"] = (df["petal_length"] / df["petal_width"]).round(2)
# print("\n--- New Column: Petal Ratio (length/width) ---")
# print(df[["petal_length", "petal_width", "petal_ratio"]].head(8))

# Add a size category based on sepal length
def size_category(length):
    if length < 5.0:
        return "Small"
    elif length < 6.5:
        return "Medium"
    else:
        return "Large"

df["sepal_size"] = df["sepal_length"].apply(size_category)
# print("\n--- New Column: Sepal Size Category ---")
# print(df[["sepal_length", "sepal_size"]].head(10))

# # Count each size category
# print("\n--- Size Category Distribution ---")
# print(df["sepal_size"].value_counts())

# # Petal ratio by species
# print("\n--- Average Petal Ratio Per Species ---")
# print(df.groupby("species")["petal_ratio"].mean().round(2))

# # Add a column flagging unusually large petals
# df["large_petal_flag"] = df["petal_length"] > 5
# print("\n--- Large Petal Flag ---")
# print(df[["petal_length", "large_petal_flag"]].tail(10))
# print(f"\nTotal large petal flowers: {df['large_petal_flag'].sum()}")


# ── LEVEL 6: CLEAN & EXPORT ───────────────────────────
print("\n" + "=" * 50)
print("CLEAN & EXPORT")
print("=" * 50)

# Check for missing values
print("\n--- Missing Values Per Column ---")
print(df.isnull().sum())

# Rename columns to cleaner names
df_clean = df.rename(columns={
    "sepal_length" : "sepal_len",
    "sepal_width"  : "sepal_wid",
    "petal_length" : "petal_len",
    "petal_width"  : "petal_wid",
})
print("\n--- Renamed Columns ---")
print(df_clean.columns.tolist())

# Drop a column we no longer need
df_clean = df_clean.drop(columns=["sepal_size"])
print("\n--- Columns After Drop ---")
print(df_clean.columns.tolist())

# Fill missing values — simulating a real scenario
# First introduce a fake missing value to practice
df_clean.loc[0, "petal_len"] = None
df_clean.loc[5, "petal_len"] = None
print("\n--- After Introducing 2 Missing Values ---")
print(df_clean["petal_len"].isnull().sum(), "missing values in petal_len")

# Fill with column mean
mean_val = df_clean["petal_len"].mean().round(2)
df_clean["petal_len"] = df_clean["petal_len"].fillna(mean_val)
print(f"Filled missing values with mean: {mean_val}")
print(df_clean["petal_len"].isnull().sum(), "missing values remaining")

# Export clean version
OUTPUT = Path(r"C:\Users\User\Desktop\FileOrganizer\iris_clean.csv")
df_clean.to_csv(OUTPUT, index=False)
print(f"\n--- Exported clean file to ---")
print(OUTPUT)