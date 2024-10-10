# Import Library
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as ticker
import geopandas as gpd
import matplotlib.colors as mcolors

# ==============================
# Introduction
# ==============================

# Title
st.title('Proyek Analisis Data: E-commerce Public Dataset')

# Pertanyaan Bisnis
st.header('Pertanyaan Bisnis')

st.write("""
1. **Kota mana yang mengeluarkan uang terbanyak pada platform e-commerce tersebut?**
""")

st.write("""
2. **Kategori produk apa yang paling diminati di masing-masing state?**
""")

st.write("""
3. **Secara keseluruhan, kategori produk apa yang paling banyak dibeli pada platform e-commerce tersebut?**
""")

# Import Dataset
city_payment_sum_sorted = pd.read_csv('/data/processed/city_payment_sum_sorted.csv')
df_highest = pd.read_csv('/data/processed/df_highest.csv')
geojson_file = '/data/brazil-states.geojson'
gdf = gpd.read_file(geojson_file)
product_category_counts = pd.read_csv('/data/processed/product_category_counts.csv')

# ==============================
# Pertanyaan Bisnis 1
# ==============================

# Pertanyaan Bisnis 1
st.header('Top 20 Kota dengan pengeluaran terbanyak')

# Set the aesthetic style of the plots
sns.set_style("whitegrid")

# Create a figure and a set of subplots for Streamlit
fig, ax = plt.subplots(figsize=(12, 8))

# Create a horizontal barplot by swapping x and y
barplot = sns.barplot(
    x='payment_value',  
    y='customer_city', 
    data=city_payment_sum_sorted.head(20),  # Display top 20 cities
    ax=ax
)

# Add a title and labels
barplot.set_title('Top 20 Cities by Total Payment Value', fontsize=16)
barplot.set_xlabel('Total Payment Value', fontsize=12)
barplot.set_ylabel('City', fontsize=14)

# Set the x-axis to use a regular number format
barplot.xaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))

# Display the plot in Streamlit
st.pyplot(fig)

# ==============================
# Pertanyaan Bisnis 2 - Bagian 1
# ==============================

# Pertanyaan Bisnis 2
st.header('Kategori Produk Paling Diminati untuk Tiap State')

# Merge GeoDataFrame with df_highest based on 'sigla' and 'customer_state'
gdf = gdf.merge(df_highest, left_on='sigla', right_on='customer_state', how='left')

# Create a color map for the product categories
unique_categories = gdf['product_category_name_english'].unique()
colors = plt.cm.get_cmap('tab20', len(unique_categories))  
category_color_map = {category: colors(i) for i, category in enumerate(unique_categories)}

# Assign colors to the states based on their category
gdf['color'] = gdf['product_category_name_english'].map(category_color_map)

# Create a plot
fig, ax = plt.subplots(figsize=(30, 20))
gdf.plot(ax=ax, color=gdf['color'], edgecolor='black')

# Calculate centroids of the polygons
gdf['centroid'] = gdf.geometry.centroid

# Add labels to the centroids showing the product_category_name_english
for x, y, label in zip(gdf.centroid.x, gdf.centroid.y, gdf['product_category_name_english']):
    ax.text(x, y, label, fontsize=10, ha='center', color='black')

# Add title and labels
plt.title('Kategori Produk Paling Diminati untuk Tiap State', fontsize=16)
plt.xlabel('Longitude')
plt.ylabel('Latitude')

# Add a legend
handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=category_color_map[category], markersize=10) 
           for category in unique_categories]
ax.legend(handles, unique_categories, title="Product Category", loc='upper left', bbox_to_anchor=(1, 1))

# Display the plot in Streamlit
st.pyplot(fig)

# ==============================
# Pertanyaan Bisnis 2 - Bagian 2
# ==============================

# Get unique customer states for the dropdown selection
customer_states = df_highest['customer_state'].unique()
selected_state = st.selectbox('Select a Customer State:', customer_states)

# Filter data based on selected customer state
filtered_data = df_highest[df_highest['customer_state'] == selected_state]

# Display the most bought category and its count
if not filtered_data.empty:
    most_bought_category = filtered_data.loc[filtered_data['row_count'].idxmax()]
    st.subheader(f'Most Bought Category in {selected_state}')
    st.write(f"Category: {most_bought_category['product_category_name_english']}")
    st.write(f"Row Count: {most_bought_category['row_count']}")
    
else:
    st.write("No data available for the selected state.")

# ==============================
# Pertanyaan Bisnis 3
# ==============================

# Set the title of the Streamlit app
st.header('Kategori Paling Banyak Dibeli pada Platform')

# Set the aesthetic style of the plots
sns.set_style("whitegrid")

# Create a figure and a set of subplots for Streamlit
fig, ax = plt.subplots(figsize=(12, 8))

# Create a horizontal barplot by swapping x and y
barplot = sns.barplot(
    x='product_category_name_english',  
    y='count', 
    data=product_category_counts.head(10),  # Display top 10 categories
    ax=ax
)

# Add a title and labels
barplot.set_title('Top 10 Most Bought Categories in E-commerce', fontsize=16)
barplot.set_xlabel('Product Category', fontsize=12)
barplot.set_ylabel('Count', fontsize=14)
plt.xticks(rotation=45, ha='right')

# Display the plot in Streamlit
st.pyplot(fig)

