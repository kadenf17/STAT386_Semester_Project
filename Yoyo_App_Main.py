import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('yoyo_cleaned_data.csv')
df = df.sort_values(by='name')

brand_counts = df['brand'].value_counts()
sorted_brands = brand_counts.index.tolist()


st.title("Kaden Franklin's Yoyo Data Application")
st.image("Images/Cover_Yoyo.jpg")

st.write('''I’ve spent the last 14 years as a dedicated yoyo enthusiast. I learned to throw as a little kid, and I have kept up with the hobby through the years. Currently, I’m serving as the president of the Yo-Yo Club at BYU. My passion extends beyond personal enjoyment; it’s about sharing the thrill with others and contributing to the community.

I have been performing for larger crowds for a couple of years now, and it’s always so fun to see the look on people’s faces when I do crazy tricks! After shows, I usually have a lot of people come up and want to learn how to yoyo. I have a big collection of yoyos, and I always get questions like: What’s your best yoyo? Why are there so many different models? What’s the best yoyo to start out with?
         
To answer some of these questions, I initiated a data analysis project centered on yoyos. I collected information on over 500 yoyos and looked at different specs including price, material, weight, bearing type, and several other descriptors. The goal is to uncover trends and correlations that can offer insights into the diverse world of yoyos.

''')
st.write("For a comprehensive introduction of this app, please read my personal blog post about it here:")
st.write("https://kadenf17.github.io/2023-12-18-Yoyo-Analysis-Part-1/")
st.write("The yoyo data found in this application was scraped from yoyoexperts webiste of current string trick yoyos for sale. Note that the underlying dataset is not comprehensive.")


st.title("Yo Data, Yo Analysis!")
show_names = st.checkbox("See All Yoyos Included in Data Set")
if show_names:
    st.write("List of Yoyo Names (Click to Expand):")
    st.write(df['name'].tolist())
st.write("To start off this analysis, lets look at the most and least expensive yoyos. Sort by brand to compare.")


st.header('Top 5 Most Expensive Yoyos:')
def display_top_expensive_yoyos(data, brand_filter=None):
    if brand_filter!="All":
        filtered_data = data[data['brand'] == brand_filter]
    else:
        filtered_data = data
    top_expensive_yoyos = filtered_data.nlargest(5, 'price')
    return top_expensive_yoyos[['name', 'price', 'description']]
selected_brand = st.selectbox('Select Brand:', ['All'] + sorted_brands)
top_yoyos = display_top_expensive_yoyos(df, brand_filter=selected_brand)
st.table(top_yoyos)


st.header('Top 5 Least Expensive Yoyos:')
def display_top_least_expensive_yoyos(data, brand_filt=None):
    if brand_filt!="All":
        filtered_data = data[data['brand'] == brand_filt]
    else:
        filtered_data = data
    top_least_expensive_yoyos = filtered_data.nsmallest(5, 'price')
    return top_least_expensive_yoyos[['name', 'price', 'description']]
selected_brd = st.selectbox('Select a Brand:', ['All'] + sorted_brands)
top_yoyos = display_top_least_expensive_yoyos(df, selected_brd)
st.table(top_yoyos)


st.header('Brand Information:')
st.write("This section helps you compare the differences between the top 5 brands with the most unique yoyos.")
show_brands = st.checkbox("See Brand Counts")
if show_brands:
    st.table(brand_counts)
st.write("Compare top 5 Brands: YoYoFactory, Duncan, C3yoyodesign, yoyorecreation, Round Spinning Objects")
def display_brand_summary_stats(data, brand_name):
    brand_data = data[data['brand'] == brand_name]
    avg_price = brand_data['price'].mean()
    avg_weight = brand_data['weight in grams'].mean()
    top_material_group = brand_data['material group'].mode().iloc[0]
    top_bearing_type = brand_data['bearing type'].mode().iloc[0]
    top_response_size = brand_data['response'].mode().iloc[0]
    stats = pd.DataFrame({
        'Average Price': [avg_price],
        'Average Weight': [avg_weight],
        'Top Material Group': [top_material_group],
        'Top Bearing Type': [top_bearing_type],
        'Top Response Pad Size': [top_response_size]
    })
    return stats
st.write("YoYoFactory:")
brand_stats = display_brand_summary_stats(df, 'YoYoFactory')
st.table(brand_stats)
st.write("Duncan:")
brand_stats = display_brand_summary_stats(df, 'Duncan')
st.table(brand_stats)
st.write("C3yoyodesign:")
brand_stats = display_brand_summary_stats(df, 'C3yoyodesign')
st.table(brand_stats)
st.write("yoyorecreation:")
brand_stats = display_brand_summary_stats(df, 'yoyorecreation')
st.table(brand_stats)
st.write("Round Spinning Objects:")
brand_stats = display_brand_summary_stats(df, 'Round Spinning Objects')
st.table(brand_stats)



st.header("Yoyo Analysis:")
st.write("Does material type have an effect on price?")
df_filtered = df[df['material group'].notna()].copy()
material_order = df_filtered['material group'].value_counts().index
selected_material_group = st.selectbox('Select Material Group', ['All'] + list(material_order))
filtered_data = df_filtered if selected_material_group == 'All' else df_filtered[df_filtered['material group'] == selected_material_group]
st.subheader(f'Histogram of Prices for Material Group: {selected_material_group}')
fig = px.histogram(
    filtered_data,
    x='price',
    nbins=min(5, len(filtered_data['price'].dropna().unique())),
    color='material group',
    title=f'Histogram of Prices by Material Group'
)
fig.update_layout(
    xaxis_title='Price',
    yaxis_title='Count',
    xaxis=dict(tickangle=45)
)
st.plotly_chart(fig)


# Display the means for each material group
st.subheader('Means for Each Material Group:')
means_by_material = df_filtered.groupby('material group')['price'].mean().sort_values(ascending=False)
st.write(means_by_material)
st.write("This suggests that price does depend heavily on material. It looks like Titanium and Magnesium yoyos are typically the most expensive. Is this because of weight? Let's investigate!")



st.header('Material Effect on Weight')
material_group_counts = df_filtered['material group'].value_counts()
selected_material_groups = material_group_counts[material_group_counts > 5].index
df_filtered = df_filtered[df_filtered['material group'].isin(selected_material_groups)]
fig = px.box(df_filtered, x='material group', y='weight in grams', color='material group',
             color_discrete_sequence=px.colors.qualitative.Set3, boxmode='overlay', points=False, title='Box Plot of Weights by Material Group (Groups with more than 5 Yoyos, Excluding Outliers)')
fig.update_layout(xaxis_title='Material Group', yaxis_title='Weight in grams')
st.plotly_chart(fig)
st.write("Most yoyos are about the same weight. The ideal seems to be around 65 grams.")
st.write("It doesn't seem like material type has a big impact on the weight of the yoyo. This is surprising, I thought titanium yoyos would be heavier. Maybe the cost of the material has to do more about how it's machined and less about weight. Let's see if the date has anything to do with the price.")



st.header('Date vs. Price Scatter Plot')
df_copy = df.copy()
df_copy['released'] = pd.to_datetime(df_copy['released'], errors='coerce')
df_copy = df_copy[df_copy['price'] < 200]
df_copy = df_copy.dropna(subset=['released', 'price'])
fig = px.scatter(df_copy, x='released', y='price',
                 labels={'released': 'Release Date', 'price': 'Price'},
                 hover_data=['name'], title="Date vs. Price")
fig.update_layout(xaxis_title='Release Date', yaxis_title='Price')
st.plotly_chart(fig)
st.write("There doesn't seem to be a correlation between Date and Price. It seems like yoyos aren't getting cheaper as they get older")


st.header('Discover Relationships')
st.write("This tool is used to help us look at the relationships between different features. One of my favorites is price x made in. Check it out for yourself!")
x_axis_feature = st.selectbox('Select X-Axis Feature:', ['price', 'brand', 'weight in grams', 'material group', 'designed in', 'made in', 'released'])
y_axis_feature = st.selectbox('Select Y-Axis Feature:', ['weight in grams', 'price', 'brand', 'material group', 'designed in', 'made in', 'released'])
color_feature = st.selectbox('Select Color Feature', ['material group', 'designed in', 'made in', 'brand', 'price', 'released'])
fig = px.scatter(df, x=x_axis_feature, y=y_axis_feature, color=color_feature,
                 labels={x_axis_feature: x_axis_feature.capitalize(), y_axis_feature: y_axis_feature.capitalize()},
                 hover_data=['name'], title=f'Scatter Plot: {x_axis_feature.capitalize()} vs. {y_axis_feature.capitalize()}')
st.plotly_chart(fig)


st.subheader('Correlation Matrix for price, weight, diameter, width, and gap width:')
st.write("Let's look at a heatmap correlation matrix to see if we can spot any relationships.")
selected_columns = ['price', 'weight in grams', 'diameter mm', 'width mm', 'gap width mm']
selected_df = df[selected_columns]
correlation_matrix = selected_df.corr()
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5)
st.pyplot(plt.gcf())
st.write("It looks like gap width (mm) might have the biggest correlation with price, but only a slight one if any. This sadly doesn't show any real trends.")

# Individaul Yoyos
st.header("Compare a Yoyo:")
st.write("This tool lets us look at individual yoyos and compare them against others made from the same company. My personal favorite yoyo is the Pragma. It is one of YoyoFactory's more expensive yoyos, but it is a smooth and incredibly fun yoyo.")
selected_name = st.text_input('Enter a yoyo name', 'Pragma') # Default is Pragma
name_df = df[df['name'] == selected_name]
if name_df.empty:
    st.write('Name not found')
else:
    # Scatter plot for all yoyos of the same brand
    brand_name = name_df['brand'].iloc[0]  # Assuming there's only one brand for the selected yoyo
    brand_df = df[df['brand'] == brand_name]
    fig = px.scatter(brand_df, x='price', y='weight in grams',
                     color_discrete_sequence=px.colors.qualitative.Set1,
                     title=f'Price vs Weight Plot for {selected_name} and All {brand_name} Brand Yoyos')
    # Scatter plot for the selected yoyo (overlay)
    if not name_df.empty:
        fig.add_trace(px.scatter(name_df, x='price', y='weight in grams').data[0])
    # Display the combined scatter plot
    st.plotly_chart(fig)
    st.write(f"### Yoyo Specs:")
    st.write(f"# {selected_name}")
    specs_order = ['description', 'price', 'brand', 'weight in grams', 'bearing size',
        'response', 'material group', 'designed in', 'made in',
        'machined in', 'released', 'diameter mm', 'width mm', 'gap width mm']
    for spec in specs_order:
        if spec in name_df.columns and not pd.isna(name_df[spec].iloc[0]):
            st.write(f"**{spec.capitalize()}:** {name_df[spec].iloc[0]}")
    show_table = st.checkbox("Show Full Table")
    if show_table:
        st.write(f"# Full Table")
        st.table(name_df)


st.title("In conclusion:")
st.write('''
        This dataset helped us answer questions such as:

            Q: What are the most expensive yoyos? (what about by brand?)
                A: Titanium and Magnesium yoyos, regardless of brand.
        
            Q: What effect does the material have on yoyo price?
                A: Material is a big factor in determining yoyo price
         
            Q: Do certain manufacturers use better materials in their yoyos?
                A: Manufacturers usually make yoyos of all types,
                but the most common type is usually aluminum or aluminum bi-metal.
         
            Q: Does one brand of yoyo stand out above the rest?
                A: Personally, looking at these graphs, I would say that YoyoFactory stands out.
                They have the widest selection of yoyos, and the majority are under $75. 
                They also have high-end titanium yoyos as well if that's what you're looking for.
         
         ''')
st.write("Thanks for coming on this yoyo analysis journey with me!")
st.write("If you would like to look through my code, check out my GitHub repository. (Link above in top right)")