import logging
from datetime import datetime
from math import floor, ceil

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
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
logging.basicConfig(filename='feedback.log', level=logging.DEBUG)

WIDE_CONTAINER_COLUMNS = [1, 5, 1]
SMALL_CONTAINER_COLUMNS = [1, 3, 1]
BIG_SPACER_HTML = '<br><br><br>'
SMALL_SPACER_HTML = '<br>'

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
        # How the economy influences our happiness
        #### Money can't buy happiness, but it makes living a lot easier. 
        """
        st.markdown(SMALL_SPACER_HTML, unsafe_allow_html=True)
        """
        ## Disclaimer
        This data story is a project developed as part of the Data Visualization course at Luzern University of Applied 
        Sciences and Arts. In the spirit of transparency we would like to disclose that some portions of the text have 
        been generated with the assistance of ChatGPT. Every text that has been generated with the assistance of
        ChatGPT have been either edited or completely rewritten by the authors of this data story.
            
        The content of this data story is derived from a notebook authored by Lucy Allan. You can find her notebook 
        [here](https://www.kaggle.com/code/lucyallan/world-happiness-report-2023-data/notebook)

        
        Names of countries, and their borders are not intended to be a political statement. We are aware that some 
        countries have disputed borders. We are using the data as it is provided by the datasets!
        """
        st.markdown(SMALL_SPACER_HTML, unsafe_allow_html=True)
        """
        ## Introduction
        
        In our quest to understand what influences happiness around the world, we embark on a data-driven story 
        that navigates through various indicators of well-being. With the aid of global data, we plot happiness 
        scores against a myriad of metrics that will give us a better understanding of what makes us happy. We will also
        explore the geographic distribution of happiness scores and how they vary across continents. 
        """
        st.markdown(SMALL_SPACER_HTML, unsafe_allow_html=True)
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
        """
        st.markdown(SMALL_SPACER_HTML, unsafe_allow_html=True)
        """
        ### Where are the happiest people?
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
        """
        st.markdown(SMALL_SPACER_HTML, unsafe_allow_html=True)
        """        
        ### Where _exactly_ are the happiest people?
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
        surprise there. These regions perfectly match what people call "The West". The most interesting region is by far
        West Asia. The happiness scores in this region varies from the second lowest to one of the highest. And regions
        with the lowest happiness score are Sub-Saharan Africa and South Asia. Sub-Saharan Africa have been plagued by
        political instability and poverty for decades. South Asia is home to some of the poorest countries in the world.
        """
        st.markdown(SMALL_SPACER_HTML, unsafe_allow_html=True)
        """
        ### The Extremes
        """

        # Creating top 10 and bottom 10 data frames and concatinating them
        top10 = full_data.set_index('Country name')['Happiness Score'].nlargest(5).to_frame()
        bottom10 = full_data.set_index('Country name')['Happiness Score'].nsmallest(5).to_frame()
        df_concat = pd.concat([top10, bottom10], axis=0)
        df_concat = df_concat.sort_values(by="Happiness Score")

        # bar chart horizontal
        fig = px.bar(df_concat, x="Happiness Score", y=df_concat.index, orientation='h', height=600, color='Happiness Score', color_continuous_scale='viridis')
        fig.update_layout(xaxis_title='Happiness Score', yaxis_title='Country name')
        fig.update_layout(autosize=True)
        st.plotly_chart(fig, use_container_width=True)

        """
        Finland is leading as the happiest country with a score of 7.804, followed closely by Denmark, Iceland, Israel, 
        and the Netherlands in the top five. All of these countries are part of the developed world. Conversely, at the 
        other end of the spectrum, Afghanistan occupies the lowest position, ranking as the unhappiest country with a 
        significantly lower score of 1.859. Lebanon, Sierra Leone, Zimbabwe, and Botswana also find themselves among 
        the unhappiest nations, with scores ranging from 2.392 to 3.435. A very interesting observation is that Israel
        and Lebanon are neighbors, but have a very different happiness score. 
        
        """
        st.markdown(SMALL_SPACER_HTML, unsafe_allow_html=True)
        """
        ### What Factors Influence Happiness the most?
        
        Now that we have a better understanding of the geographic distribution of happiness scores, let's take a look
        at some of the metrics that may have an influence on the happiness score. Some metrics are social, some are
        economic, and some are a mix of both. The number in the brackets is the correlation between the metric and the
        happiness score.
        """

        # Define the details for subplots
        all_metrics = ['Social support',
                       'Logged GDP per capita',
                       'Healthy life expectancy',
                       'Freedom to make life choices',
                       'Generosity',
                       'Urban population percentage',
                       'Perceptions of corruption',
                       'Unemployment rate',
                       'Population']

        with st.expander("Change Parameters"):
            default_metrics = ['Social support',
                               'Logged GDP per capita',
                               'Healthy life expectancy',
                               'Freedom to make life choices',
                               'Urban population percentage',
                               'Perceptions of corruption']
            selected_metrics = st.multiselect('correlation_scatter', all_metrics, default_metrics)

    num_cols = 3
    num_rows = ceil(len(selected_metrics) / num_cols)

    # Create a subplot figure with titles
    fig = sp.make_subplots(rows=num_rows, cols=num_cols, subplot_titles=selected_metrics)

    # Add each scatter plot to the respective column in the subplot
    for i, x_var in enumerate(selected_metrics):
        correlation = round(np.corrcoef(full_data['Happiness Score'], full_data[x_var])[0, 1], 2)

        scatter_plot = px.scatter(full_data, x=x_var, y='Happiness Score', color='Continent',
                                  hover_name='Country name', hover_data=['Happiness Score', x_var])

        # Calculate the regression line
        coefficients = np.polyfit(full_data[x_var], full_data['Happiness Score'], 1)
        m = coefficients[0]
        b = coefficients[1]
        y_fit = m * full_data[x_var] + b

        regression_line = go.Scatter(
            x=full_data[x_var],
            y=y_fit,
            mode='lines',
            line=dict(color='white', width=2),
            name='Trendlinie'
        )
        regression_line.showlegend = False
        scatter_plot.add_trace(regression_line)

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
        st.markdown(SMALL_SPACER_HTML, unsafe_allow_html=True)
        """
        Here you can see, that the strongest correlation is between the happiness score and Social Support, which makes
        sense. People are more happy, if a good social support network that allows them to live a fulfilling
        life, even if they get injured or go into retirement. The second strongest correlation is between the happiness
        and the GDP per capita. This is also not surprising. People are more happy, if they have more money. Another 
        correlation that feels very intuitive is the correlation between the happiness score and the healthy life
        expectancy. People are more happy, if they are healthy. The correlation between the happiness score and the
        freedom to make life choices is also very intuitive, although it is not as strong as expected. 
        Urban population percentage, and perceptions of corruption are also correlated with the happiness score, but
        not as strong as the other metrics.
        """
        st.markdown(BIG_SPACER_HTML, unsafe_allow_html=True)
        """
        ## Conclusion
        Through the course of this data story, we have explored the geographic distribution of happiness scores, and
        how they vary across continents and regions. We have also explored the correlation between happiness scores and
        various metrics that may influence happiness. We have found that the happiness score is strongly correlated
        with social support, GDP per capita, and healthy life expectancy. We have also found that the happiest countries
        are in Europe and North America, while the unhappiest countries are in Africa and South Asia.
        """
    st.markdown(BIG_SPACER_HTML, unsafe_allow_html=True)

    """
    ## Feedback
    """

    with st.form(key='feedback_form'):
        # Text area for feedback message
        message = st.text_area(label="Your Feedback")

        # Submit button
        submit_button = st.form_submit_button(label='Submit')

        if submit_button:
            logging.debug(message)
            st.success('Thank you for your feedback!')
            st.balloons()

    st.markdown(BIG_SPACER_HTML, unsafe_allow_html=True)

    """
    ## Appendix - Data
    All data used in this data story is available on Kaggle. You can find the links to the datasets below.
    - [World Happiness Report 2023](https://www.kaggle.com/datasets/ajaypalsinghlo/world-happiness-report-2023/)
    - [Global Country Information 2023](https://www.kaggle.com/datasets/nelgiriyewithana/countries-of-the-world-2023)
    - [Continent2](https://www.kaggle.com/datasets/semihizinli/continent2)
    """
    with st.expander("Cleaned dataset used in this data story"):
        st.dataframe(full_data)
