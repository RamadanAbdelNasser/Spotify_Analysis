import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st          # streamlit run app/app.py
from wordcloud import WordCloud
import matplotlib.pyplot as plt

st.set_page_config( 'Analysis Dashboard', ':bar_chart:', 'wide' )

df = pd.read_csv( 'data/cleaned data/cleaned_data.csv' )


# Filter SideBar

explicit_filter = st.sidebar.multiselect( 'explicit',
                                  options= df['explicit'].unique(),
                                  default= df['explicit'].unique()
                                  )

mode_filter = st.sidebar.multiselect(label= 'Mode',
                             options= df['mode'].unique(),
                             default= df['mode'].unique(),
                             )

energy_filter = st.sidebar.slider( 'Energy',
                                  min_value= df['energy'].min(),
                                  max_value= df['energy'].max()
                                  )



filtered_df =df.query(' explicit == @explicit_filter and mode == @mode_filter and energy >= @energy_filter' )

df_sorted_by_popular_songs = filtered_df.drop_duplicates(subset=['track_name'], keep='first')
df_sorted_by_popular_songs = df_sorted_by_popular_songs.sort_values(by='popularity',axis=0,ascending=False).head(10).reset_index().drop(columns= 'index')

df_sorted_by_popular_artists = filtered_df.drop_duplicates(subset=['artists'], keep='first')
df_sorted_by_popular_artists = df_sorted_by_popular_artists.sort_values(by='popularity',axis=0,ascending=False).head(10).reset_index().drop(columns= 'index')

df_sorted_by_most_loud_songs= filtered_df.sort_values(by='loudness',ascending=False).head(7).reset_index().drop(columns= 'index')

df_sorted_by_most_dance_artists= filtered_df.sort_values(by='danceability',ascending=False).head(7).reset_index().drop(columns= 'index')


# KPIs Calculation
no_of_tracks = filtered_df['track_name'].nunique()
no_of_artists = filtered_df['artists'].nunique()
no_of_albums = filtered_df['album_name'].nunique()
Avg_song_duration_min = filtered_df['Duration_Min'].mean()
no_of_generes = filtered_df['track_genre'].nunique()

kpi_1, kpi_2, kpi_3, kpi_4, kpi_5 = st.columns( 5 )

kpi_1.markdown(
f"""<div style="
background: white;
padding: 20px;
border-radius: 16px;
box-shadow: 0 6px 18px rgba(0,0,0,0.08);
border-left: 6px solid #FD4A4D;
">

<p style="
margin:0;
font-size:14px;
color:#6c757d;
font-weight:500;
letter-spacing:0.5px;
">
TOTAL NO. OF TRACKS
</p>

<hr style="
margin:10px 0;
border: none;
height: 1px;
background-color: #f0f0f0;
">

<h1 style="
margin:0;
font-size:48px;
font-weight:800;
color:#FD4A4D;
">
{no_of_tracks}
</h1>

</div>""",
unsafe_allow_html=True
)

kpi_2.markdown(
f"""<div style="
background: white;
padding: 20px;
border-radius: 16px;
box-shadow: 0 6px 18px rgba(0,0,0,0.08);
border-left: 6px solid #FD4A4D;
">

<p style="
margin:0;
font-size:14px;
color:#6c757d;
font-weight:500;
letter-spacing:0.5px;
">
TOTAL NO. OF ARTISTS
</p>

<hr style="margin:10px 0;border:none;height:1px;background-color:#f0f0f0;">

<h1 style="
margin:0;
font-size:48px;
font-weight:800;
color:#FD4A4D;
">
{no_of_artists}
</h1>

</div>""",
unsafe_allow_html=True
)

kpi_3.markdown(
f"""<div style="
background: white;
padding: 20px;
border-radius: 16px;
box-shadow: 0 6px 18px rgba(0,0,0,0.08);
border-left: 6px solid #FD4A4D;
">

<p style="margin:0;font-size:14px;color:#6c757d;font-weight:500;letter-spacing:0.5px;">
TOTAL NO. OF ALBUMS
</p>

<hr style="margin:10px 0;border:none;height:1px;background-color:#f0f0f0;">

<h1 style="margin:0;font-size:48px;font-weight:800;color:#FD4A4D;">
{no_of_albums}
</h1>

</div>""",
unsafe_allow_html=True
)

kpi_4.markdown(
f"""<div style="
background: white;
padding: 20px;
border-radius: 16px;
box-shadow: 0 6px 18px rgba(0,0,0,0.08);
border-left: 6px solid #FD4A4D;
">

<p style="margin:0;font-size:14px;color:#6c757d;font-weight:500;letter-spacing:0.5px;">
AVG. SONG DURATION (MIN)
</p>

<hr style="margin:10px 0;border:none;height:1px;background-color:#f0f0f0;">

<h1 style="margin:0;font-size:48px;font-weight:800;color:#FD4A4D;">
{round(Avg_song_duration_min,1)}
</h1>

</div>""",
unsafe_allow_html=True
)

kpi_5.markdown(
f"""<div style="
background: white;
padding: 20px;
border-radius: 16px;
box-shadow: 0 6px 18px rgba(0,0,0,0.08);
border-left: 6px solid #FD4A4D;
">

<p style="margin:0;font-size:14px;color:#6c757d;font-weight:500;letter-spacing:0.5px;">
TOTAL NO. OF GENRES
</p>

<hr style="margin:10px 0;border:none;height:1px;background-color:#f0f0f0;">

<h1 style="margin:0;font-size:48px;font-weight:800;color:#FD4A4D;">
{no_of_generes}
</h1>

</div>""",
unsafe_allow_html=True
)

colors = ['#085D70','#1A6A7F','#2C768D','#3E839C','#508FAB','#619CB9','#73A8C8','#85B5D7','#97C1E5','#A9CEF4']

Top_10_most_popular_tracks_fig = px.histogram(df_sorted_by_popular_songs,x='track_name',y='popularity',histfunc='max',color='popularity',color_discrete_sequence=colors)
Top_10_most_popular_songs_artists_fig = px.histogram(df_sorted_by_popular_artists,x='artists',y='popularity',histfunc='max',color='track_name',color_discrete_sequence= colors)
Top_7_most_loud_songs_fig = px.histogram(df_sorted_by_most_loud_songs,x='track_name',y='loudness',histfunc='max',color='track_name',color_discrete_sequence= colors)
# Top_7_most_loud_songs_fig = px.pie(df_sorted_by_most_loud_songs,names='track_name',values='loudness',color='loudness',color_discrete_sequence= colors)
Top_7_most_dance_artists_fig = px.pie(df_sorted_by_most_dance_artists,names='artists',values='danceability',color='danceability',color_discrete_sequence= colors)


row_0_col_1, row_0_col_2 = st.columns( 2, border = False )

row_1_col_1, row_1_col_2 = st.columns( 2, border = True )
row_1_col_1.plotly_chart(Top_10_most_popular_tracks_fig)
row_1_col_2.plotly_chart(Top_10_most_popular_songs_artists_fig  )

row_2_col_1, row_2_col_2 = st.columns(2, border= True)
row_2_col_1.plotly_chart(Top_7_most_loud_songs_fig)
row_2_col_2.plotly_chart(Top_7_most_dance_artists_fig)

# kpi_5.markdown( f'<h2>Total No. of genres</h2><br><h3>{ no_of_generes }<h3>', unsafe_allow_html=True )

# sales_volume_product_pos = px.histogram( filtered_df, x = 'Sales_Volume', y = 'Product_Position', color = 'Product_Position' ,
# color_discrete_map= {'Aisle' : '#000926', 'End-cap' : '#0F52BA','Front of Store' :  '#A6C5D7'},
# template = 'simple_white', title = 'Sum of Sales Volume By Product Position', width = 800)

# total_sales_by_terms = px.histogram( filtered_df, x = 'terms', y = 'Total_Sales', color = 'terms',
# color_discrete_sequence= px. colors.qualitative.Prism, template = 'simple_white',
# title = 'Total Sales By Term (Category)')
# row_1_col_1, row_1_col_2, row_1_col_3 = st.columns( 3, border = False )

# row_1_col_1.plotly_chart( sales_volume_product_pos )
# row_1_col_2.plotly_chart( total_sales_by_terms )

# value_to_use = row_1_col_3.selectbox( 'Select a column to calc. below sunburst',
# options = [ 'price', 'Total_Sales', 'Sales_Volume' ])


# sunburst_section_and_terms = px. sunburst( filtered_df, path = ['section', 'terms' ], values = value_to_use,
# title = f'{value_to_use} by section & terms')
# row_1_col_3.plotly_chart( sunburst_section_and_terms )


# row_2_col_1, row_2_col_2 = st.columns( 2)

# fig, ax = plt.subplots( figsize=(15,7))

# wc_name = WordCloud( background_color= 'white' ).generate( ' '.join( filtered_df['name' ] ) )
# ax.imshow( wc_name ); ax.axis( 'off' )

# row_2_col_1.pyplot( fig )

# fig, ax = plt.subplots( figsize=(15,7))

# wc_description = WordCloud( background_color= 'white' ).generate( ' '.join( filtered_df['description' ] ) )
# ax.imshow( wc_description ); ax.axis( 'off' )

# row_2_col_2.pyplot( fig )