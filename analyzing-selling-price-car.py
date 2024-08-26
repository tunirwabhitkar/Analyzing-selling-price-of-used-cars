# Importing the required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy as sp

# URL of the dataset
url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/autos/imports-85.data'

# Load the dataset from the URL
df = pd.read_csv(url, header=None)

# Defining headers for the dataset
headers = ["symboling", "normalized-losses", "make", 
           "fuel-type", "aspiration", "num-of-doors",
           "body-style", "drive-wheels", "engine-location",
           "wheel-base", "length", "width", "height", "curb-weight",
           "engine-type", "num-of-cylinders", "engine-size", 
           "fuel-system", "bore", "stroke", "compression-ratio",
           "horsepower", "peak-rpm", "city-mpg", "highway-mpg", "price"]

df.columns = headers

# Checking the first 5 entries of the dataset
print(df.head())

# Finding and removing missing values
df.replace('?', np.nan, inplace=True)
df.dropna(inplace=True)

# Convert 'price' to numeric
df['price'] = pd.to_numeric(df['price'])

# Convert mpg to L/100km
df['city-mpg'] = 235 / df['city-mpg']
df.rename(columns={'city-mpg': "city-L/100km"}, inplace=True)

# Normalize values
df['length'] = df['length'].astype(float) / df['length'].astype(float).max()
df['width'] = df['width'].astype(float) / df['width'].astype(float).max()
df['height'] = df['height'].astype(float) / df['height'].astype(float).max()

# Binning prices
bins = np.linspace(min(df['price']), max(df['price']), 4)
group_names = ['Low', 'Medium', 'High']
df['price-binned'] = pd.cut(df['price'], bins, labels=group_names, include_lowest=True)

# Plot histogram of binned prices
plt.hist(df['price-binned'])
plt.title('Price Binned Distribution')
plt.xlabel('Price Binned')
plt.ylabel('Frequency')
plt.show()

# Descriptive analysis
print(df.describe())

# Plotting
plt.figure(figsize=(10, 6))
sns.boxplot(x='drive-wheels', y='price', data=df)
plt.title('Boxplot of Price by Drive Wheels')
plt.show()

plt.figure(figsize=(10, 6))
plt.scatter(df['engine-size'], df['price'])
plt.title('Scatterplot of Engine Size vs Price')
plt.xlabel('Engine Size')
plt.ylabel('Price')
plt.grid()
plt.show()

# Grouping data
grouped_data = df[['drive-wheels', 'body-style', 'price']]
data_grouped = grouped_data.groupby(['drive-wheels', 'body-style'], as_index=False).mean()

# Pivot and heatmap
data_pivot = data_grouped.pivot(index='drive-wheels', columns='body-style')
plt.figure(figsize=(10, 6))
plt.pcolor(data_pivot, cmap='RdBu')
plt.colorbar()
plt.title('Heatmap of Drive Wheels vs Body Style')
plt.show()

# ANOVA
data_anova = df[['make', 'price']]
grouped_anova = data_anova.groupby('make')
anova_results = sp.stats.f_oneway(
    grouped_anova.get_group('honda')['price'],
    grouped_anova.get_group('subaru')['price']
)
print(anova_results)

# Regression plot
plt.figure(figsize=(10, 6))
sns.regplot(x='engine-size', y='price', data=df)
plt.ylim(0, )
plt.title('Regression Plot of Engine Size vs Price')
plt.show()
