# AmerInsights  
Dashboard designd and developed by Benny Mattis with Python, Dash, Plotly, and data from the [2017-2021 Current Population Survey Civic Engagement and Volunteering Supplement"](https://data.americorps.gov/Volunteering-and-Civic-Engagement/2021-CEV-Current-Population-Survey-Civic-Engagemen/rgh8-g2uc). (View "pretty" version of these docs at [https://wbmattis2.github.io/docs/amerinsights])

## Purpose  

Displays survey results indicating national and state-level strends in civic engagement. 

## How to Use  

View the user interface of this project at [amerinsights.pythonanywhere.com], or run the files locally with Python 3.9.6.

Use the first dropdown menu to determine if you want to view national or state-specific data.  

Use the second dropdown to determine the metric you would like to examine.  

If you are currently viewing national data, you may compare national general-population rates with national rates for demographic subgroups selected with the third dropdown.  

Use the slider to select a date range. The default is 2017-2021, but you can choose to focus on 2017-2019 or 2019-2021.

Hover over graph portions to display data from each year.  

## Deductive Inferences  

This section displays a table of the average yearly change in points for each selected demographic. These averages are calculated based on the data within the selected date range; the table will be different depending on the date range you have selected.

## Inductive Predictions  

Projections for this year, next year, and the year after that are measured by applying the averages in the "deductive inferences" table to the starting point of the most recent survey results (regardless of selected date range). E.g., if the selected date range is 2017-2019, projections will begin from actual 2021 survey results and predict following years by applying the rates of change observed in 2017-2019. 
