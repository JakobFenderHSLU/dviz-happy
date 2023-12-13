from math import floor, ceil

import numpy as np
import plotly.express as px
import plotly.subplots as sp
import streamlit as st

from helper import full_data, continent_color_map, region_color_map

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

WIDE_CONTAINER_COLUMNS = [1, 5, 1]
SMALL_CONTAINER_COLUMNS = [1, 3, 1]

# Create a container
container = st.container()

# Create three columns
_, wide_layout, _ = container.columns(WIDE_CONTAINER_COLUMNS)  # The middle column has more space

# Display the plot in the middle column
with wide_layout:
    small_container = st.container()
    _, small_layout, _ = small_container.columns(SMALL_CONTAINER_COLUMNS)

    with small_layout:
        """
        # WORK IN PROGRESS! The website is not finished yet!
        # How the economy influences our happiness
        #### Money can't buy happiness, but it makes living a lot easier. 
        ## Disclaimer
        This data story is a project developed as part of the Data Visualization course at Luzern University of Applied 
        Sciences and Arts. In the spirit of transparency we would like to disclose that some portions of the text have 
        been generated with the assistance of ChatGPT. Every text that has been generated with the assistance of
        ChatGPT have been either edited or completely rewritten by the authors of this data story.
            
        The content of this data story is derived from a notebook authored by Lucy Allan. You can find her notebook and 
        access the datasets she utilized at the following links:
        
        - [Lucy Allan's Notebook](https://www.kaggle.com/code/lucyallan/world-happiness-report-2023-data/notebook)
        - [World Happiness Report 2023](https://www.kaggle.com/datasets/ajaypalsinghlo/world-happiness-report-2023/)
        - [Global Country Information 2023](https://www.kaggle.com/datasets/nelgiriyewithana/countries-of-the-world-2023)
        - [Continent2](https://www.kaggle.com/datasets/semihizinli/continent2)
        
        Names of countries, and their borders are not intended to be a political statement. We are aware that some 
        countries have disputed borders. We are using the data as it is provided by the datasets!
        
        ## Introduction
        
        In our quest to understand what influences happiness around the world, we embark on a data-driven story 
        that navigates through various indicators of well-being. With the aid of global data, we plot happiness 
        scores against a myriad of metrics that will give us a better understanding of what makes us happy. We will also
        explore the geographic distribution of happiness scores and how they vary across continents. 
        """

        """
        ### Happiness, on a Map?
        The World Happiness Report is a landmark survey of the state of global happiness. The survey is conducted by the
        Gallup World Poll.  It surveys participants from 137 countries and ranks determines a happiness score for each 
        country. The happiness score in a number between 0 and 10, with 10 being the happiest. Sadly not every country
        is included in the survey. These countries have a white color on the map. 
        
        _Hint: You can change the regions that are displayed on the plot_
        """

        with st.expander("Change Parameters"):
            min_score = st.slider('Minimum Happiness Score ', 0.0, 10.0, 0.0, 0.01)

            all_regions = full_data["Continent"].unique().tolist()
            map_selected_regions = st.multiselect('Selected regions', ['All'] + all_regions, "All",
                                                  key="map_selected_regions")

            if 'All' in map_selected_regions or map_selected_regions == []:
                map_selected_regions = all_regions

            map_displayed_data = full_data[(full_data['Happiness Score'] > min_score)
                                           & (full_data['Continent'].isin(map_selected_regions))]

    happiness_map = px.choropleth(map_displayed_data,
                                  locations="Country name",
                                  locationmode='country names',
                                  color="Happiness Score",
                                  hover_name="Country name",
                                  hover_data=['Happiness Score'],
                                  color_continuous_scale='viridis',
                                  height=800)

    happiness_map.update_geos(showocean=True, oceancolor="#0e1117")
    happiness_map.update_layout(dragmode=False)
    happiness_map.update_traces(marker_line_width=0)

    st.plotly_chart(happiness_map, use_container_width=True)

    small_container = st.container()
    _, small_layout, _ = small_container.columns(SMALL_CONTAINER_COLUMNS)

    with small_layout:
        """
        Something that you can see in the map is that the countries with the highest happiness score are in 
        Europe, North America and Oceania. The countries with the lowest happiness score are in Africa, the Middle
        East and South Asia. 
        
        ### Does your continent influence your happiness?
        """
        continent_order = {"Continent": full_data.groupby("Continent")["Happiness Score"].median()
        .sort_values(ascending=False).index.tolist()}

        fig = px.box(full_data, y='Continent', x='Happiness Score', color='Continent', height=600, orientation='h',
                     color_discrete_map=continent_color_map, category_orders=continent_order,
                     hover_data=['Country name'])

        fig.update_layout(xaxis_title='Happiness Score', yaxis_title='Continent')
        fig.update_layout(autosize=True)
        st.plotly_chart(fig, use_container_width=True)

        """
        Oceanica is by far the happiest continent. But this is not a fair comparison, because Oceanica only has 2
        countries with data. This scews the data in their favor. The next best continent is Europe. With the highest
        upper fence and the highest median score. The Americas are not that far off. With their upper and lower fences 
        being very close to each other. Asia has the largest spread of happiness scores. Africa is the unhappiest
        continent by far. Their median score is lower than the lower fence of Europe.
        
        ### Let's take an even closer look  
        The following boxplot shows the happiness scores of the regions of a continent. The boxplots have been sorted
        by their median score and colored by their continent. 
        
        _Hint: You can change the regions that are displayed on the plot_
        """

        with st.expander("Change Parameters"):
            box_selected_regions = st.multiselect('Selected regions', all_regions + ['All']
                                                  , "All", key="box_selected_regions")

            if 'All' in box_selected_regions or box_selected_regions == []:
                box_selected_regions = all_regions

            all_eligible_sub_regions = full_data[full_data["Continent"].isin(box_selected_regions)][
                "Region"].unique().tolist()
            box_selected_sub_regions = st.multiselect('Selected sub-regions', ['All'] + all_eligible_sub_regions,
                                                      ["All"],
                                                      key="box_selected_sub_regions")

            if 'All' in box_selected_sub_regions or box_selected_sub_regions == []:
                box_selected_sub_regions = all_eligible_sub_regions

            box_displayed_data = full_data[(full_data['Happiness Score'] > min_score)
                                           & (full_data['Continent'].isin(box_selected_regions)
                                              & (full_data['Region'].isin(box_selected_sub_regions)))]

    region_order = {"Region": box_displayed_data.groupby("Region")["Happiness Score"].median()
    .sort_values(ascending=False).index.tolist()}

    fig = px.box(box_displayed_data, y='Region', x='Happiness Score', color='Region', height=1200,
                 orientation='h', color_discrete_map=region_color_map,
                 category_orders=region_order, hover_data=['Country name'])

    fig.update_layout(yaxis_title='Sub Region', xaxis_title='Happiness Score')
    fig.update_layout(autosize=True)
    st.plotly_chart(fig, use_container_width=True)

    small_container = st.container()
    _, small_layout, _ = small_container.columns(SMALL_CONTAINER_COLUMNS)

    with small_layout:
        """
        Something that is very easy to see is that the happiest regions are from Europe and North America. No big
        surprise there. These regions perfectly match "The West". The most interesting region is by far West Asia. The 
        happiness scores in this region varies from the second lowest to one of the highest.
        
                
        ### 
        You don't have to be an economist to see that the happiest countries are all developed countries. But do 
        """


        # Calculate the average Happiness Score and Logged GDP by continent
        avg_data = full_data.groupby('Continent')[['Normalized Happiness Score','Normalized Logged GDP per capita',
                                                   'Normalized Social support','Normalized Healthy life expectancy',
                                                   'Normalized Freedom to make life choices']].mean().reset_index()
        # Create a grouped bar chart for normalized data
        fig = px.bar(
            avg_data.melt(id_vars='Continent', var_name='Metric', value_name='Percentage'),
            y='Continent',
            x='Percentage',
            color='Metric',
            barmode='group',
            title='Normalized Metrics by Continent',
            orientation='h',
            height=800
        ) # todo:  sort by happiness score, labels
        # Show the combined bar chart
        st.plotly_chart(fig, use_container_width=True)

    _, col1, col2, _ = st.columns(4)
    with col1:
        """
        ### Happiest Countries
        """
        happiest_countries = full_data[['Country name', 'Happiness Score']]
        happiest_countries = happiest_countries.sort_values(by='Happiness Score', ascending=False).head(5)

        formatted_happiest_countries = ""
        for index, row in happiest_countries.iterrows():
            formatted_happiest_countries += f"{index + 1}. {row['Country name']} ({row['Happiness Score']}) \n"

        st.text(formatted_happiest_countries)

    # Add content to the second column
    with col2:
        """
        ### Unhappiest Countries
        """
        unhappiest_countries = full_data[['Country name', 'Happiness Score']]
        unhappiest_countries = unhappiest_countries.sort_values(by='Happiness Score', ascending=True).head(5)

        formatted_unhappiest_countries = ""
        rank = 128
        for index, row in unhappiest_countries.iterrows():
            formatted_unhappiest_countries += f"{rank}. {row['Country name']} ({row['Happiness Score']}) \n"
            rank -= 1

        st.text(formatted_unhappiest_countries)

    small_container = st.container()
    _, small_layout, _ = small_container.columns(SMALL_CONTAINER_COLUMNS)

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
        correlation = round(np.corrcoef(full_data['Happiness Score'], full_data[x_var])[0, 1], 2)

        scatter_plot = px.scatter(full_data, x=x_var, y='Happiness Score', color='Continent',
                                  hover_name='Country name', hover_data=['Happiness Score', x_var])

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
    _, small_layout, _ = small_container.columns(SMALL_CONTAINER_COLUMNS)

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
