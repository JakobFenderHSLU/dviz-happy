from math import floor, ceil

import numpy as np
import plotly.express as px
import plotly.subplots as sp
import streamlit as st

from helper import custom_color_scale, full_data

st.set_page_config(layout='wide', page_title='Happiness & Economics', page_icon=':smiley:')
custom_css = """
<style>
    html, body, [class*="css"] {
        font-size: 18px;
    }
</style>
"""

# Inject custom CSS with markdown
st.markdown(custom_css, unsafe_allow_html=True)

# Create a container
container = st.container()

# Create three columns
_, wide_layout, _ = container.columns([1, 4, 1])  # The middle column has more space

# Display the plot in the middle column
with wide_layout:
    small_container = st.container()
    _, small_layout, _ = small_container.columns([1, 2, 1])

    with small_layout:
        """
        # WORK IN PROGRESS! The website is not finished yet!
        # Happiness & Economics
        ## Disclaimer
        This data story is a project developed as part of the Data Visualization course at Luzern University of Applied 
        Sciences and Arts. In the spirit of transparency we would like to disclose that some portions of the text have 
        been generated with the assistance of ChatGPT. Every text that has been generated with the assistance of
        ChatGPT have been either edited or completely rewritten by the authors of this data story.
            
        The content of this data story is derived from a notebook authored by Lucy Allan. You can find her notebook and access the datasets she utilized at the following links:
        
        - [Lucy Allan's Notebook](https://www.kaggle.com/code/lucyallan/world-happiness-report-2023-data/notebook)
        - [World Happiness Report 2023](https://www.kaggle.com/datasets/ajaypalsinghlo/world-happiness-report-2023/)
        - [Global Country Information 2023](https://www.kaggle.com/datasets/nelgiriyewithana/countries-of-the-world-2023)
        - [Continent2](https://www.kaggle.com/datasets/semihizinli/continent2)
        
        
        
        ## Introduction
        
        In our quest to understand what influences happiness around the world, we embark on a data-driven story 
        that navigates through various indicators of well-being. With the aid of global data, we plot happiness 
        scores against a myriad of metrics that will give us a better understanding of what makes us happy.
        """

        """
        ### Happiness Score by Country
        Here you can see the countries of the world and their happiness score. Some countries don't have a score and are
        not marked on the map. This plot is interactive, so you can zoom in or hover over the countries to see their 
        score.
        """

        min_score = st.slider('Minimum Happiness Score ', 0.0, 10.0, 0.0, 0.01)

        all_regions = full_data["region"].unique().tolist()
        map_selected_regions = st.multiselect('Selected regions', ['All'] + all_regions, "All",
                                              key="map_selected_regions")

        if 'All' in map_selected_regions or map_selected_regions == []:
            map_selected_regions = all_regions

        map_displayed_data = full_data[(full_data['Ladder score'] > min_score)
                                       & (full_data['region'].isin(map_selected_regions))]

    fig = px.choropleth(map_displayed_data, locations="Country name", locationmode='country names',
                        color="Ladder score",
                        hover_name="Country name",
                        hover_data=['Ladder score'],
                        color_continuous_scale=custom_color_scale,
                        height=800)

    fig.update_layout(autosize=True, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    small_container = st.container()
    _, small_layout, _ = small_container.columns([1, 2, 1])

    with small_layout:
        """
        Something that you can see in the map is that the countries with the highest happiness score are in 
        Europe, North America and Oceania. The countries with the lowest happiness score are in Africa, the Middle
        East and South Asia. Notable exceptions are Israel, Saudi Arabia and the United Arab Emirates, which have a
        high happiness score. for a region that is otherwise not very happy.

        ### Distribution of Happiness Scores by Continent
        """
        fig = px.box(full_data, x='region', y='Ladder score', color='region', height=600,
                     labels={'region': 'Continent', 'Ladder score': 'Happiness Score'})

        fig.update_layout(xaxis_title='Continent', yaxis_title='Happiness Score')
        fig.update_layout(autosize=True)
        st.plotly_chart(fig, use_container_width=True)

        """
        The boxplot proves the point that we made earlier. With a median score of 6.4, a lower fence being at 5.0 and 
        the upper fence at 7.8, Europe is the happiest continent. Asia is the continent with the largest spread of
        happiness scores, ranging from 7.4 to 1.8. The median score for Asia is 5.4. Due to the low number of countries
        in Oceanica, the boxplot is not very representative. The scores of the Americas are closer together and 
        comparable to the scores of Europe. Africa has by far the lowest median score of 4.4 and the lowest upper fence
        at 5.9.
        
        ### Distribution of Happiness Scores by Sub-Region        
        """

        box_selected_regions = st.multiselect('Selected regions', all_regions + ['All']
                                              , "All", key="box_selected_regions")

        if 'All' in box_selected_regions or box_selected_regions == []:
            box_selected_regions = all_regions

        all_eligible_sub_regions = full_data[full_data["region"].isin(box_selected_regions)][
            "sub-region"].unique().tolist()
        box_selected_sub_regions = st.multiselect('Selected sub-regions', ['All'] + all_eligible_sub_regions,
                                                  ["All"],
                                                  key="box_selected_sub_regions")

        if 'All' in box_selected_sub_regions or box_selected_sub_regions == []:
            box_selected_sub_regions = all_eligible_sub_regions

        box_displayed_data = full_data[(full_data['Ladder score'] > min_score)
                                       & (full_data['region'].isin(box_selected_regions)
                                          & (full_data['sub-region'].isin(box_selected_sub_regions)))]

    fig = px.box(box_displayed_data, x='sub-region', y='Ladder score', color='sub-region', height=600,
                 labels={'sub-region': 'Sub Region', 'Ladder score': 'Happiness Score'})

    fig.update_layout(xaxis_title='Sub Region', yaxis_title='Happiness Score')
    fig.update_layout(autosize=True)
    st.plotly_chart(fig, use_container_width=True)

    small_container = st.container()
    _, small_layout, _ = small_container.columns([1, 2, 1])

    with small_layout:
        """
        The boxplot shows that Western Europe is by far the happiest sub-region with a median score of 7.0. The
        unhappiest sub-region is Sub-Saharan Africa with a median score of 4.4. If you want mess with the data yourself
        you can select the regions and sub-regions that you want to see in the boxplot.
        """

    _, col1, col2, _ = st.columns(4)
    with col1:
        """
        ### Happiest Countries
        """
        happiest_countries = full_data[['Country name', 'Ladder score']]
        happiest_countries = happiest_countries.sort_values(by='Ladder score', ascending=False).head(5)

        formatted_happiest_countries = ""
        for index, row in happiest_countries.iterrows():
            formatted_happiest_countries += f"{index + 1}. {row['Country name']} ({row['Ladder score']}) \n"

        st.text(formatted_happiest_countries)

    # Add content to the second column
    with col2:
        """
        ### Unhappiest Countries
        """
        unhappiest_countries = full_data[['Country name', 'Ladder score']]
        unhappiest_countries = unhappiest_countries.sort_values(by='Ladder score', ascending=True).head(5)

        formatted_unhappiest_countries = ""
        rank = 128
        for index, row in unhappiest_countries.iterrows():
            formatted_unhappiest_countries += f"{rank}. {row['Country name']} ({row['Ladder score']}) \n"
            rank -= 1

        st.text(formatted_unhappiest_countries)

    small_container = st.container()
    _, small_layout, _ = small_container.columns([1, 2, 1])

    with small_layout:
        """
        Finland is leading as the happiest country with a score of 7.804, followed closely by Denmark, Iceland, Israel, 
        and the Netherlands in the top five. All of these countries are part of the developed world. Conversely, at the 
        other end of the spectrum, Afghanistan occupies the lowest position, ranking as the unhappiest country with a 
        significantly lower score of 1.859. Lebanon, Sierra Leone, Zimbabwe, and Botswana also find themselves among 
        the unhappiest nations, with scores ranging from 2.392 to 3.435.
        
        
        ### Diverse Metrics and their Influence on Happiness
        
        Now that we have a better understanding of the geographic distribution of happiness scores, let's take a look
        at some of the metrics that may have an influence on the happiness score. Some metrics are social, some are
        economic, and some are a mix of both. This plot is interactive, you can select the continent and zoom in on
        a specific part of the plot.
        """

    # Define the details for subplots
    plots_details = ['Logged GDP per capita',
                     'Social support',
                     'Healthy life expectancy',
                     'Freedom to make life choices',
                     'Generosity',
                     'Perceptions of corruption',
                     'Urban population percentage',
                     'Unemployment rate',
                     'Population']

    num_cols = 3
    num_rows = ceil(len(plots_details) / num_cols)

    # Create a subplot figure with titles
    fig = sp.make_subplots(rows=num_rows, cols=num_cols, subplot_titles=plots_details)

    # Add each scatter plot to the respective column in the subplot
    for i, x_var in enumerate(plots_details):
        correlation = round(np.corrcoef(full_data['Ladder score'], full_data[x_var])[0, 1], 2)

        scatter_plot = px.scatter(full_data, x=x_var, y='Ladder score', color='region',
                                  hover_name='Country name', hover_data=['Ladder score', x_var])

        current_row = floor(i / num_cols) + 1
        current_col = i % num_cols + 1

        # Loop through traces, add to subplot, and update legend visibility
        for trace in scatter_plot.data:
            trace.showlegend = (i == 0)  # Show legend only for the first subplot
            fig.add_trace(trace, row=current_row, col=current_col)

        # Update axes titles
        fig.update_xaxes(title_text=f"{x_var} ({correlation})", row=current_row, col=current_col)
        fig.update_yaxes(title_text='Happiness Score', row=current_row, col=current_col)
        fig.update_layout(height=1000)

    # Update the layout if needed, e.g., autosize, or adjusting margins
    fig.update_layout(height=1200, autosize=True)

    # Display the figure in the Streamlit app
    st.plotly_chart(fig, use_container_width=True)

    small_container = st.container()
    _, small_layout, _ = small_container.columns([1, 2, 1])

    with small_layout:
        """
        Some metrics are more correlated with the happiness score than others. Logged GDP per capita, social support, 
        Healthy life expectancy, Freedom to make life choices and Urban population percentage are all positively 
        correlated with the happiness score. Generosity, Unemployment rate, and Population 
        all have a weak correlation at best. With only Perceptions of corruption having a negative correlation.
        """

        """
        ## Dataset
        """

    st.dataframe(full_data)
