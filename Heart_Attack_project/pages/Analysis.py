# Import necessary libraries
import streamlit as st
import sys                                                  # sys module to manipulate the Python system path
sys.path.append(r"C:\Users\Lenovo\Desktop\mid\Heart_Attack_project")  # Appending the directory containing custom modules
import MEDA as md
 
# Creating tabs using Streamlit
tab_overall_vision, tab_life_style, tab_chronic_diseas, tab_difficulties, tab_related_analysis, tab_conclusion = st.tabs(['Overall Vision', 'Life_Style', 'Chronic_Diseas', 'Difficulties', 'Related_Analysis', 'Conclusion']) 

with tab_overall_vision:
    # Title of tab
    st.title('Some statistcs over the data') 
    # insights in this tab
    st.write('The information in this tab can answer the following questions :') 
    st.write('1. How many males and females are there in our data?')
    st.write('2. What is the distribution of age groups in our data?')
    st.write('3. What is the ratio of sick to healthy people depending on the gender?')
    st.write('4. What is the ratio of sick to healthy people depending on the age group?')

    # First section: Displaying a header indicating the question about the distribution of males and females in the data
    st.header('1. How many males and females are there in our data?') 
    
    # Displaying the gender count from the MEDA module
    st.write(md.gender_count)
    # Displaying a Plotly chart showing the distribution of males and females
    st.plotly_chart(md.fig_gender_count)
    # Adding a markdown statement to provide additional information about the observation
    st.markdown(f"<span style='font-size: 20px;'>-Females are more than males in the sample data population.</span>", unsafe_allow_html=True)


    # Second section: Distribution of age groups
    st.header('2. What is the distribution of age groups in our data?')

    # Displaying the count of individuals in each age category
    st.write(md.age_category_count)
    # Displaying a Plotly chart showing the distribution of age groups
    st.plotly_chart(md.fig_age_count)
    # Adding a markdown statement to provide additional information about the observation
    st.markdown(f"<span style='font-size: 20px;'>-Most individuals are aged around 65-69</span>", unsafe_allow_html=True)

    # Third section: Ratio of sick to healthy people depending on gender
    st.header('3. What is the ratio of sick to healthy people depending on the gender?')

    # Displaying the count of sick and healthy individuals based on gender
    st.write(md.counts_gender_patient)
    # Displaying a Plotly chart showing the ratio of sick to healthy people by gender
    st.plotly_chart(md.fig_count_patient_gender)
    # Adding markdown statements to provide additional information about the observation
    st.markdown(f"<span style='font-size: 20px;'>-Many individuals did not have any heart disease.</span>", unsafe_allow_html=True)
    st.markdown(f"<span style='font-size: 20px;'>-Many individuals who have heart diseas is males although males less than females</span>", unsafe_allow_html=True)

    # Fourth section: Ratio of sick to healthy people depending on age group
    st.header('4. What is the ratio of sick to healthy people depending on the age group?')
     
    # Displaying the count of sick and healthy individuals based on age group 
    st.write(md.counts_age_patient)
    # Displaying a Plotly chart showing the ratio of sick to healthy people by age group
    st.plotly_chart(md.fig_count_patient_age)
    # Adding markdown statements to provide additional information about the observation

    st.markdown(f"<span style='font-size: 20px;'>-People who are older than 80 are the largest group to suffer from heart disease.</span>", unsafe_allow_html=True)
    st.markdown(f"<span style='font-size: 20px;'>-People who are between 18-24 and 25-29 are the Lowest group to suffer from heart disease.</span>", unsafe_allow_html=True)
          


with tab_life_style:
    life_style_df = md.data_source[['physicalactivities', 'smokerstatus', 'ecigaretteusage', 'alcoholdrinkers']]
    # Title of tab
    st.title('Looking at the lifestyle  and habits') 

    # insights in this tab
    st.write('The information in this tab can answer the following questions :')
    st.write('1. Who is in the highest category of both genders performing physical activities?')
    st.write('2. What is the ratio between the risk of having a heart attack between smokers and non-smokers?')
    st.write('3. What is the ratio between the risk of having a heart attack between alcohol users and non-alcohol users?')
    st.write('4. What is the ratio between the risk of having a heart attack between physical activities status?')
    st.write('5. Who is the highest gender group addicted to alcohol?')
    st.write('6. What is the correlation between gender, age group, heart attack, general health and lifestyle factors?')
    st.write('7. What is the distribution of sleep hours?')
    st.write('8. What is the correlation between sleep hours and heart attack?')
   
    # function to display the highest category of both genders 
    def highest_category(col):
        # Get the highest category data
        highest_category = md.highest_category(col)
        # Create a container for the best gender information
        con_best_gender = st.container()
        # Divide the container into two columns
        col1_best_gender, col2_best_gender = con_best_gender.columns(2)
        # Display the best gender information in the first column
        with col1_best_gender:
            best_gender = highest_category['sex'].iloc[0]
            st.subheader(best_gender)
            # Get the count of the best gender
        best_gender_count = highest_category['count'].iloc[0] 
        # Display the count of the best gender in the second column    
        with col2_best_gender: 
            col2_best_gender.metric('Count',int(best_gender_count), int(best_gender_count))



    # First section
    st.header('1. Who is in the highest category of both genders performing physical activities?')
    st.write(highest_category('physicalactivities'))

    # Second section
    st.header('2. What is the ratio between the risk of having a heart attack between smokers and non-smokers?')
    # Displaying the percentage of people with a heart attack who smoke regularly every day and people who never smoke 
    hadheartattack_smoker = md.calculate_percentage(md.data_source, ['hadheartattack', 'smokerstatus'], 'count', 'percentage')
    never_count = hadheartattack_smoker.loc[hadheartattack_smoker['smokerstatus'] == 'Never smoked', 'percentage'].iloc[1]
    everyday_count = hadheartattack_smoker.loc[hadheartattack_smoker['smokerstatus'] == 'Current smoker(Every day)', 'percentage'].iloc[1]
    # Displaying a Plotly pie chart showing the ratio of people with a heart attack who smoke regularly every day and people who never smoke
    st.plotly_chart(md.pie_fig(never_count, everyday_count, "smoking status", "Current smoker(Every day)", "Never smoked"))
    # Calculating the ratio between people with a heart attack who smoke regularly every day and people who never smoke
    ratio = round(everyday_count / never_count, 2)
    # Adding markdown statements to provide additional information about the observation
    st.markdown(f"<span style='font-size: 24px;'>-Ratio between the risk of having a heart attack between smoker status: {ratio}</span>", unsafe_allow_html=True)
    st.markdown(f"<span style='font-size: 20px;'>-The percentage of people with a heart attack who smoke regularly every day is approximately two and a half times the percentage of non-smokers.</span>", unsafe_allow_html=True)
    
    # Third section
    st.header('3. What is the ratio between the risk of having a heart attack between alcohol users and non-alcohol users?')
    # Displaying the percentage of people with a heart attack who drinking alcohol and people who never drink
    hadheartattack_alchol = md.calculate_percentage(md.data_source, ['hadheartattack', 'alcoholdrinkers'], 'count', 'percentage')
    never_count = hadheartattack_alchol.loc[hadheartattack_alchol['alcoholdrinkers'] == 'Yes', 'percentage'].iloc[1]
    everyday_count = hadheartattack_alchol.loc[hadheartattack_alchol['alcoholdrinkers'] == 'No', 'percentage'].iloc[1]
    # Displaying a Plotly pie chart showing the ratio of people with a heart attack who drink alcohol and people who never drink
    ratio = round(everyday_count / never_count, 2)
    # Displaying a Plotly pie chart showing the ratio of people with a heart attack who drink alcohol and people who never drink
    st.plotly_chart(md.pie_fig(never_count, everyday_count, "alcohol usage", "non-alcohol", "alcohol"))
    # Adding markdown statements to provide additional information about the observation 
    st.markdown(f"<span style='font-size: 24px;'>-Ratio between the risk of having a heart attack between alcohol users: {ratio}</span>", unsafe_allow_html=True)
    st.markdown(f"<span style='font-size: 20px;'>-Almost the percentage of people who have a heart attack and do not drink alcohol is approximately 2 times the percentage of people who drink alcohol.</span>", unsafe_allow_html=True)

    # Fourth section
    st.header('4. What is the ratio between the risk of having a heart attack between physical activities status?')
    # Displaying the percentage of those who have a heart attack who practising physical activities and those who do not
    hadheartattack_physicalactivities = md.calculate_percentage(md.data_source, ['hadheartattack', 'physicalactivities'], 'count', 'percentage')
    yes_physicalactivities_count = hadheartattack_physicalactivities.loc[hadheartattack_physicalactivities['physicalactivities'] == 'Yes', 'percentage'].iloc[1]
    no_physicalactivities_count = hadheartattack_physicalactivities.loc[hadheartattack_physicalactivities['physicalactivities'] == 'No', 'percentage'].iloc[1]
    # Calculating the ratio between those who have a heart attack who practising physical activities and those who do not
    ratio = no_physicalactivities_count / yes_physicalactivities_count
    # Displaying a Plotly pie chart showing the ratio of those who have a heart attack who practising physical activities and those who do not
    st.plotly_chart(md.pie_fig(yes_physicalactivities_count, no_physicalactivities_count, "physical activities status", "practising physical activities", "not practising physical activities"))
    st.markdown(f"<span style='font-size: 24px;'>-Ratio between the risk of having a heart attack between physical activities status: {ratio}</span>", unsafe_allow_html=True)
    st.markdown(f"<span style='font-size: 20px;'>-The percentage of those who exert physical effort who suffer from heart attacks is half the percentage of those who do not exert physical effort.</span>", unsafe_allow_html=True)


    # Fifth section
    st.header('5. Who is the highest gender group addicted to alcohol?')
    # Displaying the highest category of both genders who drink alcohol
    st.write(highest_category('alcoholdrinkers'))

    # Sixth section
    st.header('6. What is the correlation between gender, age group, heart attack, general health and lifestyle factors?')
    
    # Create a container for the correlation analysis 
    con_corr = st.container()
    # Divide the container into two columns
    con_life_style_fac, con_fac = con_corr.columns(2)

    # Radio button for selecting lifestyle factor
    with con_life_style_fac:
        # variable for each radio button to save the choosed value
        fac = st.radio(
                "Select your interest",
                ['Sex', 'Age Category', 'Had Heart Attack', 'General Health'],
                horizontal= True,
                key= 'life_style_factor',
            )
        
    # Radio button for selecting specific factor within the chosen lifestyle factor    
    with con_fac:
        
        life_style_fac = st.radio(
                "Select value you interest",
                ['Physical Activities', 'Smoker Status', 'Ecigarette Usage', 'Alcohol Drinkers'],
                horizontal= True,
                key= 'factor',
            )

    # Convert the radio button value to lowercase and replace spaces with underscores (for the column names in the data source)    
    fac = str(fac).lower().replace(' ','')    
    life_style_fac = str(life_style_fac).lower().replace(' ','')

    # Display the correlation between the chosen factor and the chosen lifestyle factor in a bar chart
    fig_bar = md.bar_fig (md.data_source,fac,life_style_fac)
    col1_bar, col2_bar = con_corr.columns(2)
    col1_bar.plotly_chart(fig_bar)

    # Seventh section
    st.header('7. What is the distribution of sleep hours?')
    
    st.markdown(f"<span style='font-size: 20px;'>-Many people sleep between 6 to 8 hours, which is the normal rate.</span>", unsafe_allow_html=True)
    # Displaying a Plotly chart showing the distribution of sleep hours 
    st.plotly_chart(md.fig_sleep_hours)



    # Eighth section
    st.header('8. What is the correlation between sleep hours and heart attack?')

    st.markdown(f"<span style='font-size: 20px;'>-People who sleep an average of 7 hours are less likely to have heart attacks.</span>", unsafe_allow_html=True)
    st.markdown(f"<span style='font-size: 20px;'>-People who sleep less than 6 hours or more than 8 hours are more susceptible to heart attacks.</span>", unsafe_allow_html=True)
    # Displaying the correlation between sleep hours and heart attack 
    st.write(md.hadheartattack_sleephours)
    

with tab_chronic_diseas:
    cronic_diseas_df = md.data_source[['hadangina', 'hadstroke', 'hadasthma',
       'hadskincancer', 'hadcopd', 'haddepressivedisorder', 'hadkidneydisease',
       'hadarthritis', 'haddiabetes' ]]

    # Title of tab
    st.title('Looking at some chronic diseases')
    # insights in this tab
    st.write('The information in this tab can answer the following questions :')
    st.write('1. What is the distribution of  chronic diseases among different genders, age groups, heart attack status, and general health?')
    st.write('2. What are we noticing from this bars graph?')
    
    # First section
    st.header('1. What is the distribution of  chronic diseases among different genders, age groups, heart attack status, and general health?')
    # Create a container for the correlation analysis
    con_corr = st.container()
    # Divide the container into two columns
    con_chronic_diseas, con_fac = con_corr.columns(2)
    # Radio button for selecting factor 
    with con_chronic_diseas:
        # variable for each radio button to save the choosed value
        fac = st.radio(
                "Select your interest",
                ['Sex', 'Age Category', 'Had Heart Attack', 'General Health'],
                horizontal= True,
                key= 'chronic_diseas_factor',
            )
    # Radio button for selecting chronic disease    
    with con_fac:
        
        chronic_diseas_factor = st.radio(
                "Select value you interest",
                ['Had Angina', 'Had Stroke', 'Had Asthma',
                'Had Skin Cancer', 'Had Copd', 'Had Depressive Disorder',
                'Had Kidney Disease', 'Had Arthritis', 'Had Diabetes'],
                horizontal= True,
                key= 'factors',
            )
    # Convert the radio button value to lowercase and replace spaces with underscores (for the column names in the data source)
    fac = str(fac).lower().replace(' ','')
    chronic_diseas_factor = str(chronic_diseas_factor).lower().replace(' ','')
    
    # Display the correlation between the chosen factor and the chosen chronic disease in a bar chart
    fig_bar = md.bar_fig (md.data_source,fac,chronic_diseas_factor)
    col1_bar, col2_bar = con_corr.columns(2)
    col1_bar.plotly_chart(fig_bar)

    # Second section
    st.header('2. What are we noticing from this bars graph?')
    st.markdown(f"<span style='font-size: 20px;'>-The percentage of males and females suffering from these chronic diseases is very similar.</span>", unsafe_allow_html=True)

    st.markdown(f"<span style='font-size: 20px;'>-There is no strong relationship between heart attacks and these diseases.</span>", unsafe_allow_html=True)

    st.markdown(f"<span style='font-size: 20px;'>-Most of these diseases are prevalent in people over the age of 60.</span>", unsafe_allow_html=True)



with tab_difficulties:

    other_problems_df = md.data_source[['deaforhardofhearing',
                'blindorvisiondifficulty', 'difficultyconcentrating',
                'difficultywalking', 'difficultydressingbathing', 'difficultyerrands']]
    # Title of tab
    st.title('Looking at some difficulties')
    # insights in this tab
    st.write('The information in this tab can answer the following questions :')
    st.write('1. What is the distribution of  difficulties among different genders, age groups, heart attack status, and general health?')
    st.write('2. What are we noticing from this bars graph?')

    # First section
    st.header('1. What is the distribution of  difficulties among different genders, age groups, heart attack status, and general health?')
    # Create a container for the correlation analysis
    con_corr = st.container()
    # Divide the container into two columns
    con_some_difficulties, con_fac = con_corr.columns(2)
    # Radio button for selecting factor
    with con_some_difficulties:
        # variable for each radio button to save the choosed value
        fac = st.radio(
                "Select your interest",
                ['Sex', 'Age Category', 'Had Heart Attack', 'General Health'],
                horizontal= True,
                key= 'some_difficulties_factor',
            )
    # Radio button for selecting some difficulties
    with con_fac:
        
        some_difficulties_factor = st.radio(
                "Select value you interest",
                ['Deaf or Hard of Hearing',
                'Blind or Vision Difficulty', 'Difficulty Concentrating',
                'Difficulty Walking', 'Difficulty Dressing Bathing', 'Difficulty Errands'],
                horizontal= True,
                key= 'fac',
            )
    # Convert the radio button value to lowercase and replace spaces with underscores (for the column names in the data source)
    fac = str(fac).lower().replace(' ','')
    some_difficulties_factor = str(some_difficulties_factor).lower().replace(' ','')
    # Display the correlation between the chosen factor and the chosen difficulties in a bar chart
    fig_bar = md.bar_fig (md.data_source,fac,some_difficulties_factor)
    col1_bar, col2_bar = con_corr.columns(2)
    col1_bar.plotly_chart(fig_bar) 

    # Second section
    st.header('2. What are we noticing from this bars graph?')
    st.markdown(f"<span style='font-size: 20px;'>-The percentage of males and females suffering from these difficulties is very similar.</span>", unsafe_allow_html=True)
    st.markdown(f"<span style='font-size: 20px;'>-There is no strong relationship between heart attacks and these difficulties.</span>", unsafe_allow_html=True)
    st.markdown(f"<span style='font-size: 20px;'>-Most of these difficulties are prevalent in people over the age of 50 except difficulty concentrating , it is almost the same in all age category.</span>", unsafe_allow_html=True)




with tab_related_analysis:
     dff = md.data_source[['physicalhealthdays', 'mentalhealthdays', 'sleephours']]
     # Title of tab
     st.title('Looking at some related data analysis questions')
     # insights in this tab
     st.write('The information in this tab can answer the following questions :')
     st.write('1. What are the distribution of  personal factors among different genders?')
     st.write('2. What are the distribution of  personal factors among different age groups?')    
     st.write('3. what is our general health distribution?')
     st.write('4. What are the distribution of  personal factors among different general health measures?')
     st.write('5. What is the percentage of each gender, age group, and sleep hours among different general health measures?')
     st.write('6. What are the top ten states in terms of the number of heart attacks?')
     st.write('7. What are the ten lowest states in terms of the number of heart attacks?')
     st.write('8. What are the top ten states on the general health scale?')
     st.write('9. What are the ten lowest states on the general health scale?')


     # First section
     st.header('1. What are the distribution of  personal factors among different genders?')
     # Display personal factors among genders
     st.write(md.personal_factor_among_genders)
     # Create a container for the correlation analysis
     con_corr = st.container()
     # Divide the container into one column
     con_dff_factor = con_corr.columns(1)
     # Radio button for selecting different factors
     with con_dff_factor[0]: 
            fac = st.radio(
                "Select your interest",
                ['Physical Health Days', 'Mental Health Days', 'Sleep Hours'],
                horizontal=True,
                key="dff_factor"
            )
    
     # Convert the radio button value to lowercase and replace spaces with underscores (for the column names in the data source)
     fac = str(fac).lower().replace(' ','')
     # Display the correlation between the chosen factor and the chosen difficulties in a pie chart
     st.plotly_chart(md.plot_pie(md.data_source, fac))

     st.markdown(f"<span style='font-size: 20px;'>-Females sleep better than males, which makes them less susceptible to heart disease.</span>", unsafe_allow_html=True)
     st.markdown(f"<span style='font-size: 20px;'>-Females experience more days of physical and mental fatigue than males.</span>", unsafe_allow_html=True)

     # Second section
     st.header('2. What are the distribution of  personal factors among different age groups?')
     # Display personal factors among age groups
     st.write(md.personal_factor_among_agegroups)
     # Display a line chart showing the distribution of personal factors among age groups
     st.plotly_chart(md.line_fig_age)

     st.markdown(f"<span style='font-size: 20px;'>-People older than 50 are most susceptible to physical fatigue.</span>", unsafe_allow_html=True)
     st.markdown(f"<span style='font-size: 20px;'>-Young people between the ages of 18 and 45 are the most suffering from mental problems.</span>", unsafe_allow_html=True)
     
     # Third section
     st.header('3. what is our general health distribution?')
     # Display the distribution of general health
     st.write(md.general_health_distribution)
     # Display a pie chart showing the distribution of general health
     st.plotly_chart(md.pie_fig_general_health)
     st.markdown(f"<span style='font-size: 20px;'>-Most of the people in our data have a general health rate between very good and good.</span>", unsafe_allow_html=True)
 
     # Fourth section
     
     st.header('4. What are the distribution of  personal factors among different general health measures?')
     # Display personal factors among general health
     st.write(md.personal_factor_among_gneral_health)
     # Display a line chart showing the distribution of personal factors among general health
     st.plotly_chart(md.line_fig_general_health)

     st.markdown(f"<span style='font-size: 20px;'>-The healthiest people sleep for approximately 7 hours. They suffer from physical and mental problems at a rate of only one to two times a month. The fewer hours of sleep and the greater the number of times the problems recur, the less healthy they are.</span>", unsafe_allow_html=True)
    
     # Fifth section
     
     st.header('5. What is the percentage of each gender, age group, and sleep hours among different general health measures?')
     # Create a container for the correlation analysis 
     con_corr = st.container()
     con_personal_factor = con_corr.columns(1)
     # Radio button for selecting different factors
     with con_personal_factor[0]:  
      fac = st.radio(
        "Select your interest",
        ['Sex', 'Age Category', 'Sleep Hours'],
        horizontal=True,
        key="_factor"
    )
     fac = str(fac).lower().replace(' ','')
     # Display the correlation between the chosen factor and the chosen difficulties in a bar chart
     st.plotly_chart(md.plot_bar_general_health(md.data_source, fac))
    
     st.markdown(f"<span style='font-size: 20px;'>-The general health of females is better than that of males.</span>", unsafe_allow_html=True)
     st.markdown(f"<span style='font-size: 20px;'>-The general health of those who sleep 6 to 8 hours is the highest among all.</span>", unsafe_allow_html=True)
     st.markdown(f"<span style='font-size: 20px;'>-Most of those who suffer from poor general health are those over 50.</span>", unsafe_allow_html=True)

     # Sixth section
     
     st.header('6. What are the top ten states in terms of the number of heart attacks?')
     # Display top ten states in terms of the number of heart attacks
     st.write(md.top_10_states_with_heart_attacks)
     # Display a bar chart showing the top ten states in terms of the number of heart attacks
     st.plotly_chart(md.bar_fig_top_10)
    

     # Seventh section
     
     st.header('7. What are the ten lowest states in terms of the number of heart attacks?')
     # Display ten lowest states in terms of the number of heart attacks
     st.write(md.least_10_states_with_heart_attacks)
     # Display a bar chart showing the ten lowest states in terms of the number of heart attacks
     st.plotly_chart(md.bar_fig_least_10)

     # Eight section
     st.header('8. What are the top ten states on the general health scale?')
     # Display top ten states on the general health scale
     st.write(md.top_10_states_with_best_general_health)

     # Ninth section
     st.header('9. What are the ten lowest states on the general health scale?')
     # Display ten lowest states on the general health scale
     st.write(md.worst_10_states_with_worst_general_health)

     st.markdown(f"<span style='font-size: 20px;'>-Washington is the state with the most cases of heart attacks, while Virgin Islands is the least.</span>", unsafe_allow_html=True)
     st.markdown(f"<span style='font-size: 20px;'>-Washington is the best states in terms of public health, while District of Columbia is the least.</span>", unsafe_allow_html=True)




with tab_conclusion:
    st.title("An overview about analysis:") 


    st.markdown('''<span style='font-size: 25px;'>This study found that females make up a larger portion of the sample population than males.
                The majority of participants were aged around 65-69 and reported no history of heart disease. While heart disease risk increased with age,
                it was more prevalent in males over 80. Interestingly, those who slept an average of 7 hours and exercised regularly exhibited the lowest risk of heart attack.
                There were no significant differences between genders regarding chronic diseases or general health, although females reported better sleep quality and more fatigue.
                Overall, the data suggests that maintaining a healthy weight, exercising regularly, and getting sufficient sleep (around 7 hours) are crucial for promoting good health and reducing the risk of heart disease,
                especially as we age.</span>''', unsafe_allow_html=True)