# AmerInsights
# A civic engagement data dashboard designed and developed by Benny Mattis

import pandas as pd
import dash
from dash import html, dcc, dash_table
from dash.dependencies import Input, Output
import plotly.express as px
import datetime

national_whole_df = pd.read_csv('./national_findings_whole_population.csv').sort_values('Year')
state_whole_df = pd.read_csv('./state_findings_whole_population.csv')
national_demo_df = pd.read_csv('./national_findings_by_demographic.csv')
demo_dict = {
    'Age': ['16 to 17','18 to 24','25 to 44','45 to 54','55 to 59','60 to 69','70 to 79','80 to 84','85 and over','16 to 54','55 and over'],
    'Sex': ['Female','Male'],
    'Education':['Graduate degree','Bachelor\'s degree','Some college, no degree','Associate degree, academic','Associate degree, occupational','High school graduate','Less than high school'],
    'Military service': ['Non-veteran','Veteran'],
    'Parental status': ['No child in household','Parent of child under 18'],
    'Race': ['American Indian or Alaskan Native','Asian','Black or African American','Native Hawaiian or Pacific Islander','White','Two or more races'],
    'Ethnicity': ['Hispanic', 'Non-Hispanic'],
    'Family income': ['$24,999 or less','$25,000 to $39,999','$40,000 to $59,999','$60,000 to $74,999','$75,000 to $99,999','$100,000 to $149,999','$150,000 or more']
}
survey_years = [2017, 2019, 2021]
current_year = datetime.datetime.now().year
next_year = current_year + 1
third_year = current_year + 2
app = dash.Dash(__name__)
app.title = 'AmerInsights'
app.layout = html.Div(children=[html.H1('AmerInsights',
                                        style={'textAlign': 'center',
                                            'font-size': 40}),
                                html.P('Data from 2017-2021 CEV Findings: Current Population Survey Civic Engagement and Volunteering Supplement.',
                                        style={'textAlign': 'center',
                                            'font-size': 20}),
                                html.P('Data downloaded from data.americorps.gov in September 2023.',
                                        style={'textAlign': 'center',
                                        'font-size': 20}),
                                html.P('Documentation available at wbmattis2.github.io/docs/amerinsights.',
                                        style={'textAlign': 'center',
                                        'font-size': 20}),
                                dcc.Dropdown(id='region-dropdown',
                                    options=['National','AL','AK','AZ','AR','CA','CO','CT','DE','DC','FL','GA','HI','ID','IL','IN','IA','KS','KY','LA','ME','MD','MA','MI','MN','MS','MO','MT','NE','NV','NH','NJ','NM','NY','NC','ND','OH','OK','OR','PA','RI','SC','SD','TN','TX','UT','VT','VA','WA','WV','WI','WY'],
                                    value='National',
                                    placeholder="Select a Region",
                                    searchable=True
                                ),
                                html.Br(),
                                dcc.Dropdown(id='metric-dropdown',
                                    options=['Formal Volunteering Rate','Organizational Membership Rate','Charitable Giving Rate','Informal Helping Rate','Talking with Friends and Family Rate','Talking with Neighbors Rate','Learning About Issues Rate','Discussing Issues with Friends and Family Rate','Discussing Issues with Neighbors Rate','Posting Views Online Rate','Voting in Local Elections Rate','Contacting Public Officials Rate','Donating to a Political Cause Rate','Attending Public Meetings Rate','Taking Action with Neighbors Rate','Buycotting or Boycotting Rate'],
                                    value='Formal Volunteering Rate',
                                    placeholder="Select a Civic Engagement Metric",
                                    searchable=True
                                ),
                                html.Br(),
                                dcc.Dropdown(id='demographic-dropdown',
                                    options=['Select a Demographic (National Data Only)', *demo_dict.keys()],
                                    searchable=True,
                                    value='Select a Demographic (National Data Only)'
                                ),
                                html.Br(),
                                dcc.RangeSlider(id='range-slider',
                                    min=2017, max=2021, step=2,
                                    value=[2017, 2021],
                                    marks={2017: '2017',
                                        2019: '2019',
                                        2021: '2021'},
                                        allowCross=False),
                                html.Br(),
                                html.Div(dcc.RadioItems(['Zoom graph scaling to fit data', 'Scale graphs at 0-100%'], 'Zoom graph scaling to fit data', id='display-type', labelStyle={'display': 'inline-block', 'margin': '0 2em'}), style={'textAlign': 'center'}),
                                html.H2(id='results-heading',
                                        style={'textAlign': 'center',
                                        'font-size': 30}),
                                html.Div(dcc.Graph(id='line-graph')),
                                html.H2(id='deduction-heading',
                                        style={'textAlign': 'center',
                                        'font-size': 30}),
                                html.Div(id='rate-of-change',
                                    style={'textAlign': 'center',
                                        'font-size': 20}),
                                html.H2(id='induction-heading',
                                        style={'textAlign': 'center',
                                        'font-size': 30}),
                                html.Div(dcc.Graph(id='projection-graph')),
                                html.Footer('AmerInsights Dashboard designed and developed by Benny Mattis. This page is not affiliated with AmeriCorps.',
                                        style={'textAlign': 'center',
                                        'font-size': 20}),
                                ])
@app.callback([Output(component_id='results-heading', component_property='children'),
              Output(component_id='deduction-heading', component_property='children'),
              Output(component_id='induction-heading', component_property='children')],
              Input(component_id='range-slider', component_property='value'))
def get_headings(daterange):
    results_heading = 'CEV Results, ' + str(daterange[0]) + '-' + str(daterange[1])
    deduction_heading = 'Deductive Inferences, ' + str(daterange[0]) + '-' + str(daterange[1])
    induction_heading = 'Inductive Predictions, ' + str(current_year) + '-' + str(third_year)
    return results_heading, deduction_heading, induction_heading


@app.callback([Output(component_id='demographic-dropdown', component_property='value'),
              Output(component_id='demographic-dropdown', component_property='disabled')],
              Input(component_id='region-dropdown', component_property='value'))
def disable_demographics(region):
    return 'Select a Demographic (National Data Only)', not (region == 'National')

@app.callback([Output(component_id='line-graph', component_property='figure'),
              Output(component_id='rate-of-change', component_property='children'),
              Output(component_id='projection-graph', component_property='figure')],
              [Input(component_id='metric-dropdown', component_property='value'),
              Input(component_id='range-slider', component_property='value'),
              Input(component_id='region-dropdown', component_property='value'),
              Input(component_id='demographic-dropdown', component_property='value'),
              Input(component_id='display-type', component_property='value')])
def display_data(selected_metric, daterange, selected_region, selected_demo, display_type):
    if daterange[0] == daterange[1]:
        return px.pie(title='Please select a valid date range.'), dash_table.DataTable(), px.pie(title='Please select a valid date range.')
    demographics = ['General Population']
    base_title = selected_region + ' ' + selected_metric
    
    #get survey results based on user's query
    if selected_region == 'National':
        if selected_metric == 'Voting in Local Elections Rate':
            selected_metric_column = 'Rate of Voting in Local Elections'
        else:
            selected_metric_column = selected_metric
        region_values = national_whole_df.sort_values('Year')['National ' + selected_metric_column]
    else:
        state_filtered_df = state_whole_df[state_whole_df['State'] == selected_region]
        region_values = []
        for year in survey_years:
            region_values.append(state_filtered_df.iloc[0]['State ' + str(year) + ' ' + selected_metric])
    
    df = pd.DataFrame({
            'Year': survey_years,
            'General Population' : region_values
        })
    if selected_demo != 'Select a Demographic (National Data Only)':
        subgroups = demo_dict[selected_demo]
        subgroup_results = {}
        for subgroup in subgroups:
            if not (selected_demo == 'Age' and subgroup == '16 to 17' and selected_metric == 'Voting in Local Elections Rate'):
                demographics.append(subgroup)
                subgroup_results[subgroup] = []
                filtered_src_df = national_demo_df[national_demo_df['Demographic Subgroup'] == selected_demo + ': ' + subgroup].reset_index()
                for survey_year in survey_years:
                    subgroup_results[subgroup].append(filtered_src_df[selected_region + ' ' + str(survey_year) + ' ' + selected_metric][0])
                df[subgroup] = subgroup_results[subgroup]
        base_title += ' by ' + selected_demo
    
    #get graph of survey results
    results_title = base_title + ', ' + str(daterange[0]) + '-' + str(daterange[1])
    df_filtered_years = df[(df['Year'] >= daterange[0]) & (df['Year'] <= daterange[1])]
    fig = px.line(df_filtered_years,
    x = 'Year',
    y = demographics,
    markers=True,
    title = results_title)
    fig.update_layout(yaxis_tickformat = '.1%',
    legend_title = selected_region + ' Demographic',
    yaxis_title = 'Survey Results',
    hovermode = 'x unified')
    fig.update_xaxes(type='date', tickformat='%Y', tickvals=survey_years)
    fig.update_traces(hovertemplate='%{y}')

    #get table of average point changes per year and graph of projected rates for next 3 years
    avg_dict = {selected_region + ' Demographic': [], 'Average Yearly Change in Points': []}
    pre_dict = {'Year': [current_year, current_year + 1, current_year + 2]}
    for group in demographics:
        latest_in_daterange = df_filtered_years.iloc[-1][group]
        earliest_in_daterange = df_filtered_years.iloc[0][group]
        diff = latest_in_daterange - earliest_in_daterange
        avg_pts_per_year = diff / (daterange[1] - daterange[0])
        avg_dict[selected_region + ' Demographic'].append(group)
        avg_dict['Average Yearly Change in Points'].append(round(avg_pts_per_year * 100, 1))
        last_result = df.iloc[-1][group]
        projection = last_result + avg_pts_per_year * (current_year - survey_years[-1])
        next_projection = projection + avg_pts_per_year
        third_projection = next_projection + avg_pts_per_year
        pre_dict[group] = [projection, next_projection, third_projection]
    avg_df = pd.DataFrame(avg_dict)
    avg_table = dash_table.DataTable(avg_df.to_dict('records'), [{"name": i, "id": i} for i in avg_df.columns], style_cell = {'text-align': 'center'})
    p_df = pd.DataFrame(pre_dict)
    pfig = px.line(data_frame = p_df,
    x = 'Year',
    y = demographics,
    markers=True,
    title ='Projected ' + base_title + ', ' + str(current_year) + '-' + str(third_year))
    pfig.update_layout(yaxis_tickformat = '.1%',
    legend_title = selected_region + ' Demographic',
    yaxis_title = 'Projected Rate',
    hovermode = 'x unified')
    pfig.update_xaxes(type='date', tickformat='%Y', tickvals=[current_year, next_year, third_year])
    pfig.update_traces(hovertemplate='%{y}')
    if display_type == 'Scale graphs at 0-100%':
        fig.update_yaxes(range = [0,1])
        pfig.update_yaxes(range = [0,1])

    return fig, avg_table, pfig
    
   

if __name__ == '__main__':
    app.run_server()