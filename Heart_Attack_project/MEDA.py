# Import Libraries
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datasist.structdata import detect_outliers
from sklearn.impute import SimpleImputer


# Reading the data
data_source = pd.read_csv("./Heart_Attack_project/Sourse/heart_2022_with_nans.zip", compression='gzip')


## Data Cleaning ##

# Handle column names to lowercase
data_source.columns = data_source.columns.str.strip().str.lower()

# Drop unneeded columns 
data_source = data_source.drop(['lastcheckuptime', 'removedteeth', 'chestscan', 'hivtesting', 'fluvaxlast12', 'pneumovaxever', 'tetanuslast10tdap'], axis= 1)

# Drop null values in hadheartattack column after that reset index 
data_source.dropna(subset=['hadheartattack'], inplace=True)
data_source.reset_index(drop=True, inplace=True)

# Drop duplicates after that reset index 
data_source.drop_duplicates(inplace=True)
data_source.reset_index(drop=True, inplace=True)

# Put columns with numeric values in a new data frame 
numeric_columns = data_source.select_dtypes(include=['number']).columns
# Fill nulls in numeric data with median using simple imputer
imputer = SimpleImputer(strategy='median')
for col in numeric_columns:
    data_source[col] = imputer.fit_transform(data_source[[col]])


# Put columns with categorical values in a new data frame
categorical_columns = ['covidpos', 'highrisklastyear', 'alcoholdrinkers', 'ecigaretteusage', 'smokerstatus', 'difficultyerrands',
                     'difficultydressingbathing', 'difficultywalking', 'difficultyconcentrating', 'blindorvisiondifficulty',
                     'deaforhardofhearing']
# Fill nulls in categorical data with mode using simple imputer
new_data = data_source[categorical_columns].copy()
imputer = SimpleImputer(strategy='most_frequent')
for col in new_data.columns:
    data_source[col] = imputer.fit_transform(new_data[[col]]).flatten()   


# Drop remaining nulls and reset indes
data_source.dropna(inplace=True)
data_source.reset_index(drop=True, inplace=True)

# Detecting and removing outliers using module detect_outliers from datasist.structdata library and reset data index
outliers_indices = detect_outliers(data_source, 0, ['sleephours', 'weightinkilograms', 'heightinmeters', 'bmi'])
data_source.drop(outliers_indices, inplace=True)
data_source.reset_index(inplace= True, drop= True)


## Feature Engineering ##

# Handle some categorical columns variables
data_source['haddiabetes'].replace({'No, pre-diabetes or borderline diabetes' : 'Borderline', 'Yes, but only during pregnancy (female)' : 'During Pregnancy'} , inplace=True)
data_source['smokerstatus'].replace({'Current smoker - now smokes some days' : 'Current smoker(Some days)',
                                    'Current smoker - now smokes every day' : 'Current smoker(Every day)'}, inplace=True)


data_source['ecigaretteusage'].replace({'Not at all (right now)' : 'Not at all',
                                        'Never used e-cigarettes in my entire life' : 'Never',
                                        'Use them every day' : 'Everyday',
                                        'Use them some days' : 'Somedays'}, inplace=True)

                                        
data_source['raceethnicitycategory'].replace({'White only, Non-Hispanic' : 'White',
                                             'Black only, Non-Hispanic' : 'Black',
                                             'Other race only, Non-Hispanic' : 'Other Race',
                                             'Multiracial, Non-Hispanic' : 'Multi Racial'}, inplace=True)    

data_source['covidpos'].replace({'Tested positive using home test without a health professional' : 'Yes'}, inplace=True)


# Change the format of the Age column to make it clearer
def handle_age(age):
    age = age.copy()  
    age[age == 'Age 80 or older'] = '80+'
    age[age != '80+'] = age.str.split(' ').str[1] + '-' + age.str.split(' ').str[3]
    return age

# Apply handel_age function on data
data_source['agecategory'] = handle_age(data_source['agecategory'])



## Functions for first tab (Overall vision) ##

# Count number of males and females
gender_count = data_source['sex'].value_counts()
# Pie chart to show number of males to females
fig_gender_count = px.pie(data_source, names='sex', color_discrete_sequence=px.colors.sequential.Cividis)

# Count number of each age category
age_category_count = data_source['agecategory'].value_counts()
# Histogram to show number of each age category
fig_age_count = px.histogram(data_source, x='agecategory', marginal='box')


# count healthy and patient depending on gender 
counts_gender_patient = data_source.groupby(['hadheartattack', 'sex']).size().reset_index(name='count')
# bar chart to shows the counts
fig_count_patient_gender = px.bar(counts_gender_patient, x='hadheartattack', y='count', color='sex',
             title="Prevalence of Heart Attacks Among Different Genders",
             labels={'hadheartattack': 'Had Heart Attack', 'count': 'Count'},
             barmode='group',
             template='plotly_dark')



# count healthy and patient depending on age category
counts_age_patient = data_source.groupby(['hadheartattack', 'agecategory']).size().reset_index(name='count')
# bar chart to shows the counts
fig_count_patient_age = px.bar(counts_age_patient, x='agecategory', y='count', color='hadheartattack',
             title="Prevalence of Heart Attacks Among Different Ages",
             labels={'hadheartattack': 'Had Heart Attack', 'count': 'Count', 'agecategory': 'Age Category'},
             barmode='group',
             template='plotly_dark')



## Functions for first tab (Life Style) ##

# dataframe for life style data from data source
life_style_df = data_source[['physicalactivities', 'smokerstatus', 'ecigaretteusage', 'alcoholdrinkers']]

# function for calculating highest category of both genders performing life style factors
def highest_category(col):
    counts = data_source.groupby([col, 'sex']).size().reset_index(name='count')
    counts = counts.sort_values(by='count', ascending=False)
    return counts

# function for plotting bar chart for both genders performing life style factors 
def bar_fig(data, col, fac):
    if col in data.columns:
        counts = data.groupby([col, fac]).size().reset_index(name='count')
        fig = px.bar(counts, x=col, y='count', color=fac,
                    title=f"Prevalence of {col} Among Different {fac}",
                    labels={col: col , 'count': 'Count'},
                    barmode='group',
                    template='plotly_dark')
        
    return fig

# function for calculating percentage 
def calculate_percentage(data, group_columns, count_column, percentage_column):
    grouped_data = data.groupby(group_columns).size().reset_index(name='count')
    grouped_data[percentage_column] = 0
    for i in range(len(grouped_data)):
        group_value = grouped_data[group_columns[-1]][i]
        total_count = grouped_data[grouped_data[group_columns[-1]] == group_value]['count'].sum()
        percentage_value = float(grouped_data['count'][i]) / total_count * 100
        grouped_data.loc[i, percentage_column] = np.round(percentage_value, decimals=2).astype(int) 
    return grouped_data

# plot pie chart for show the percentage of some life style factors
def pie_fig(col_1, col_2, name, data1, data2):
    fig = px.pie(names=[data1, data2],
        values=[col_1, col_2], 
        title=f'Prevalence of {name} among had heart attack status', 
        color_discrete_sequence=px.colors.sequential.Blues_r,
        template='plotly_dark')
    return fig

# plot pie chart for distribution of sleep hours
fig_sleep_hours = px.pie(data_source, names='sleephours', title='Distribution of Sleep Hours', template='plotly_dark', hole=0.5, color_discrete_sequence=px.colors.sequential.Cividis)


# calculate percentage of sleep hours by age category
hadheartattack_sleephours = calculate_percentage(data_source, ['hadheartattack', 'sleephours'], 'count', 'percentage')


## Tab 5 (Analysis) ##

# Distribution of personal factors among different genders
personal_factor_among_genders = data_source.groupby('sex').agg({'physicalhealthdays':'mean', 'mentalhealthdays':'mean', 'sleephours':'mean'})

# dataframe for personal factors data from data source
dff = data_source[['physicalhealthdays', 'mentalhealthdays', 'sleephours']]

# plot pie chart for distribution of personal factors among different genders
def plot_pie(dff, col):
    fig = px.pie(personal_factor_among_genders, values=col, names=personal_factor_among_genders.index, color=col , title=f"Distribution of {col} Among Different Genders",
                  template='plotly_dark', hole=0.5, color_discrete_sequence=px.colors.sequential.Cividis)
    
    return fig

# Distribution of personal factors among different age groups 
personal_factor_among_agegroups = data_source.groupby('agecategory').agg({'physicalhealthdays':'mean', 'mentalhealthdays':'mean', 'sleephours':'mean'})

# plot line chart for distribution of personal factors among different age groups
line_fig_age = px.line(personal_factor_among_agegroups, x=personal_factor_among_agegroups.index, y=['physicalhealthdays', 'mentalhealthdays', 'sleephours'], template='plotly_dark')

# Distribution of personal factors among different general health
personal_factor_among_gneral_health = data_source.groupby('generalhealth').agg({'physicalhealthdays':'mean', 'mentalhealthdays':'mean', 'sleephours':'mean'})

# plot line chart for distribution of personal factors among different general health
line_fig_general_health = px.line(personal_factor_among_gneral_health, x=personal_factor_among_gneral_health.index, y=['physicalhealthdays', 'mentalhealthdays', 'sleephours'], template='plotly_dark')\

# plot bar chart for distribution of personal factors among different general health
def plot_bar_general_health(data_source,col):
    counts = data_source.groupby([col, 'generalhealth']).size().reset_index(name='count') 
    fig = px.bar(counts, x=col, y='count', color='generalhealth',
                title=f"Prevalence of {col} Among Different General Health",
                labels={'generalhealth': 'General Health', 'count': 'Count', col: col},
                barmode='group',
                template='plotly_dark')
    return fig

# top 10 states with the most heart attacks 
top_10_states_with_heart_attacks = data_source.groupby('state')['hadheartattack'].count().nlargest(10)

# bar chart for top 10 states with the most heart attacks
bar_fig_top_10 = px.bar(top_10_states_with_heart_attacks, x=top_10_states_with_heart_attacks.index, y=top_10_states_with_heart_attacks.values, template='plotly_dark')

# least 10 states with the most heart attacks
least_10_states_with_heart_attacks = data_source.groupby('state')['hadheartattack'].count().nsmallest(10)

# bar chart for least 10 states with the most heart attacks 
bar_fig_least_10 = px.bar(least_10_states_with_heart_attacks, x=least_10_states_with_heart_attacks.index, y=least_10_states_with_heart_attacks.values, template='plotly_dark')

# distribution of general health 
general_health_distribution = data_source['generalhealth'].value_counts()

# pie chart for distribution of general health 
pie_fig_general_health = px.pie(data_source, names='generalhealth', color_discrete_sequence=px.colors.sequential.Cividis)

# top 10 states with best general health
top_10_states_with_best_general_health = data_source.groupby('state')['generalhealth'].value_counts().nlargest(10).reset_index()

# least 10 states with worst general health 
worst_10_states_with_worst_general_health = data_source.groupby('state')['generalhealth'].value_counts().nsmallest(10).reset_index()
