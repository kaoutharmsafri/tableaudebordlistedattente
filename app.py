from streamlit_card import card
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from dateutil.relativedelta import relativedelta
import pyodbc

#===========================================
def fetch_data():
    connection_string = "DRIVER={SQL Server};SERVER=VICTUS-COOKIE;DATABASE=alldata;UID=sa;PWD=1234"
    conn = pyodbc.connect(connection_string)
    # Write your SQL query here
    query = "SELECT * FROM all_data"
    # Fetch data into a Pandas DataFrame
    data = pd.read_sql(query, conn)
    # Close the connection
    conn.close()
    return data
#===========================================
def main():
    st.set_page_config(
    page_title='My Streamlit Data Dashboard',
    page_icon=':bar_chart:',
    layout='wide'
    )


    st.title('My Streamlit Data Dashboard')
    
    data = fetch_data()
    data['Archive_Date'] = pd.to_datetime(data['Archive_Date'])
    data['Total'] = pd.to_numeric(data['Total'], errors='coerce')


    if data is  None:
        st.error("Failed to retrieve data from MySQL.")        
        
    st.subheader('Data')
    with st.expander('Data Preview'):
        st.dataframe(data)

    #===========================================

    data['Specialty_Name'] = data['Specialty_Name'].replace({"General Surgery":"General",
                                                            "Gynaecology":"Reproductive System",
                                                            "Small Volume Specialities":"Other",
                                                            "Otolaryngology (ENT)":"ENT",
                                                            "Vascular Surgery":"Vascular Surgery",
                                                            "Orthopaedics":"Bones",
                                                            "General Medicine":"General",
                                                            "Urology":"Urine",
                                                            "Gastro-Enterology":"Gastro-Enterology",
                                                            "Plastic Surgery":"Cosmetic",
                                                            "Respiratory Medicine":"Respiratory",
                                                            "Cardiology":"Heart",
                                                            "Dermatology":"Skin",
                                                            "Pain Relief":"General",
                                                            "Neurology":"Brain",
                                                            "Cardio-Thoracic Surgery":"Heart",
                                                            "Rheumatology":"Bones",
                                                            "Dental Surgery":"Teeth",
                                                            "Ophthalmology":"Eyes",
                                                            "Radiology":"X-ray",
                                                            "Clinical Immunology":"Immune System",
                                                            "Endocrinology":"Hormonal",
                                                            "Oral Surgery":"Oral Surgery",
                                                            "Anaesthetics":"Respiratory",
                                                            "Gastro-Intestinal Surgery":"Gastro-Intestinal Surgery",
                                                            "Breast Surgery":"Breast Surgery",
                                                            "Neurosurgery":"Brain",
                                                            "Hepato-Biliary Surgery":"Hepato-Biliary Surgery",
                                                            "Maxillo-Facial":"Dental",
                                                            "Geriatric Medicine":"Geriatric Medicine",
                                                            "Nephrology":"Kidney",
                                                            "Oncology":"Oncology",
                                                            "Haematology":"Blood",
                                                            "Obstetrics":"Obstetrics",
                                                            "Vitro-Retinal Surgery":"Vitro-Retinal Surgery",
                                                            "Histopathology":"Histopathology",
                                                            "Rehabilitation Medicine":"Rehabilitation Medicine",
                                                            "Diabetes Mellitus":"Hormonal",
                                                            "Other":"Other",
                                                            "Clinical Neurophysiology":"Brain",
                                                            "Psychiatry":"Psychiatry",
                                                            "Infectious Diseases":"Respiratory",
                                                            "Metabolic Medicine":"Blood",
                                                            "Paediatrics":"Child Care",
                                                            "Clinical Pharmacology":"Clinical Pharmacology",
                                                            "Pathology":"Pathology",
                                                            "Chemical Pathology":"Chemical Pathology",
                                                            "Radiotherapy":"Radiotherapy",
                                                            "Clinical (Medical) Genetics":"Genes",
                                                            "Immunology":"Immune System",
                                                            "Tropical":"Tropical",
                                                            "Palliative Medicine":"Pain Relief",
                                                            "Paed Nephrology":"Kidney",
                                                            "Paed Endocrinology":"Hormonal",
                                                            "Paediatric ENT":"ENT",
                                                            "Microbiology":"Microbiology",
                                                            "Paediatric Neurology":"Brain",
                                                            "Paed Cardiology":"Heart",
                                                            "Paediatric Surgery":"General",
                                                            "Paediatric Respiratory Medicine":"Respiratory",
                                                            "Substance Abuse":"Substance Abuse",
                                                            "Occupational Medicine":"Occupational Medicine",
                                                            "Paediatric Neurosurgery":"Brain",
                                                            "Paediatric Urology":"Urine",
                                                            "Paed Gastro-Enterol":"Digestive",
                                                            "Paed Orthopaedic":"Bones",
                                                            "Paediatric Dermatology":"Skin",
                                                            "Paed Metabolic Medicine":"Blood",
                                                            "Paed Haematology":"Blood",
                                                            "Paediatric Anaesthetics":"Respiratory",
                                                            "Paed Oncology":"Cancer",
                                                            "Paediatric Radiology":"X-ray",
                                                            "Paediatric Infectious Diseases":"Immune System",
                                                            "Developmental Paediatrics":"Brain",
                                                            "Child/Adolescent Psychiatry":"Psychatry",
                                                            "Neonatology":"Infant",
                                                            "Intensive Care":"Intensive Care",
                                                            "Accident & Emergency":"Accident & Emergency"})
    #===========================================
        
    select_all_cases = st.sidebar.checkbox('Select All Case Types', value=True)
    if select_all_cases:
        selected_case_types = data['Case_Type'].unique()
    else:
        selected_case_types = st.sidebar.multiselect('Select Case Types', data['Case_Type'].unique(), default=data['Case_Type'].unique())

    select_all_specialties = st.sidebar.checkbox('Select All Specialty Names', value=True)
    if select_all_specialties:
        selected_specialties = data['Specialty_Name'].unique()
    else:
        selected_specialties = st.sidebar.multiselect('Select Specialty Names', data['Specialty_Name'].unique(), default=data['Specialty_Name'].unique())

    select_all_Age_Profile = st.sidebar.checkbox('Select All Age Profile', value=True)
    if select_all_Age_Profile:
        selected_Age_Profile = data['Age_Profile'].unique()
    else:
        selected_Age_Profile = st.sidebar.multiselect('Select Age Profile', data['Age_Profile'].unique(), default=data['Age_Profile'].unique())

    select_all_Time_Bands = st.sidebar.checkbox('Select All Time Bands', value=True)
    if select_all_Time_Bands:
        selected_Time_Bands = data['Time_Bands'].unique()
    else:
        selected_Time_Bands = st.sidebar.multiselect('Select Time Band', data['Time_Bands'].unique(), default=data['Time_Bands'].unique())


    # Filter the DataFrame based on selected Case Types and Specialty Names
    data = data[(data['Case_Type'].isin(selected_case_types)) & (data['Specialty_Name'].isin(selected_specialties))]
    #===========================================

    # Convert 'Archive_Date' to datetime format

    max_archive_date = data['Archive_Date'].max() # Find the maximum 'Archive_Date' in A11_Data

    # First Measure latest month wait list

    lmwl = (data[data['Archive_Date'] == max_archive_date].loc[:, 'Total'].sum())

    # st.write(f"Latest Month Wait List: {lmwl}")
    st.subheader("Latest Month Wait List of :")

    tab1, tab2 = st.tabs(["Previous year", "Current year"])

    with tab2:
        hasClicked1 = card(
        title=f"{lmwl}",
        text="Latest Month Wait List",
        styles={
            "card": {
                "width": "80%",
                # "height": "500px",
                "border-radius": "60px",
                "box-shadow": "0 0 10px rgba(0,0,0,0.5)",
            },
            "filter": {
                "background-color": "rgba(220, 255, 183)"  # <- make the image not dimmed anymore
            },
            "text": {
                "color":"black",
            },
            "title": {
                "color":"black",
            },
        }
        )

    # Second Measure previous latest month wait list

    previous_year_max_date = max_archive_date - relativedelta(months=12) # Calculate the date that is 12 months before the maximum 'Archive_Date'

    plmwl = (data[data['Archive_Date'] == previous_year_max_date].loc[:, 'Total'].sum())

    # st.write(f"PY Latest Month Wait List: {plmwl}")

    with tab1:
        hasClicked2 = card(
        title=f"{plmwl}",
        text="PY Latest Month Wait List",
        styles={
            "card": {
                "width": "80%",
                # "height": "500px",
                "border-radius": "60px",
                "box-shadow": "0 0 10px rgba(0,0,0,0.5)",
            },
            "filter": {
                "background-color": "rgba(220, 255, 183)"  # <- make the image not dimmed anymore
            },
            "text": {
                "color":"black",
            },
            "title": {
                "color":"black",
            },
        }
        )


    # Create an empty DataFrame
    Calculation_method = pd.DataFrame()

    # Add columns to the table
    Calculation_method['Calc Method'] = ['Average', 'Median']

    selected_method = st.sidebar.selectbox('Select Method', Calculation_method['Calc Method'])

    # Third Measure the average waitlist

    awl = data['Total'].mean()

    # Fourth Measure the median waitlist

    mwl = data['Total'].median()

    # Switch between average and median

    result = awl if selected_method == 'Average' else mwl

    #  Filter the DataFrame based on the selected method
    filtered_df = data[data['Case_Type'].isin(data['Case_Type'].unique())]

    # Create a pie chart based on the user's selection

    # fig1 = px.pie(filtered_df, names='Case_Type', values='Total', title=f'{selected_method} Wait List Distribution by Case Type ' , color_discrete_sequence=px.colors.sequential.dense_r)
    fig1 = px.pie(
        filtered_df,
        names='Case_Type',
        values='Total',
        title=f'{selected_method} Wait List Distribution by Case Type',
        color_discrete_sequence=px.colors.sequential.Sunsetdark
    )

    # Customize the legend
    fig1.update_layout(
        legend=dict(
            orientation="h",  # Set the orientation to horizontal
            yanchor="bottom",  # Anchor the legend to the bottom
            y=1.02,  # Adjust the y position
            xanchor="right",  # Anchor the legend to the right
            x=0.1  # Adjust the x position
        )
    )

    col1, col2 = st.columns(2)

    col1.plotly_chart(fig1)

    # Create a stacked bar graph
    filtered_data = data[data['Age_Profile'] != 'no input']
    filtered_data = filtered_data[filtered_data['Time_Bands'] != 'no input']
    # bar = data[data['Archive_Date'] == max_archive_date].groupby(['Time_Bands', 'Age_Profile'])['Total'].agg('mean' if selected_method == 'Average' else 'median').reset_index()
    bar = filtered_data.groupby(['Time_Bands', 'Age_Profile'])['Total'].agg('mean' if selected_method == 'Average' else 'median').reset_index()

    fig2 = px.bar(
        pd.concat([bar]),
        x='Time_Bands',
        y='Total',
        color='Age_Profile',
        title=f'{selected_method} Wait List by Time Bands',
        labels={'Total': f'{selected_method} Wait List', 'Age_Profile': 'Age Profile'},
        color_discrete_sequence=px.colors.sequential.Magenta,
    )
    col1.markdown("")

    col2.plotly_chart(fig2)

    # ===========================================================
    st.subheader("Top 5 Specialities")
    speciality_info = data.groupby('Specialty_Name')['Total'].agg('mean' if selected_method == 'Average' else 'median').reset_index()

    top_specialties = speciality_info.nlargest(5, 'Total', 'all' if selected_method == 'Average' else 'all')

    with st.expander("Top 5 Specialities"):
    # Display the top 5 specialties with a styled layout
        for index, row in top_specialties.iterrows():
            st.write(f"**Speciality Name:** {row['Specialty_Name']}")
            st.write(f"{row['Total']}")
            st.write("-----") 

    speciality_info_sorted = speciality_info.sort_values('Specialty_Name')

    # Display the top 5 specialties alphabetically
    top_specialties_alphabetical = speciality_info_sorted.head(5)

    # ===========================================================
    filtered_data = data[data['Case_Type'] != 'Outpatient']

    sum_data = filtered_data.groupby(['Archive_Date', 'Case_Type'])['Total'].sum().reset_index()

    col3, col4 = st.columns(2)

    fig3 = px.line(sum_data, x="Archive_Date", y="Total",color='Case_Type',title='Sum of Total by Archive_Date and Case_Type', color_discrete_sequence=px.colors.sequential.Sunsetdark  )

    fig3.update_layout(
        legend=dict(
            orientation="h",  # Set the orientation to horizontal
            yanchor="bottom",  # Anchor the legend to the bottom
            y=1.02,  # Adjust the y position
            xanchor="right",  # Anchor the legend to the right
            x=0.1  # Adjust the x position
        )
    )
    col3.markdown("")

    col3.plotly_chart(fig3)

    # ===========================================================
    filtered_data = data[data['Case_Type'] == 'Outpatient']

    sum_data = filtered_data.groupby(['Archive_Date', 'Case_Type'])['Total'].sum().reset_index()

    fig4 = px.line(sum_data, x="Archive_Date", y="Total",color='Case_Type',title='Sum of Total by Archive_Date and Case_Type')

    fig4.update_traces(selector=dict(type='scatter', mode='lines'), line=dict(color='pink'))

    col4.plotly_chart(fig4)

    # ===========================================================

    

if __name__ == "__main__":
    main()
#===========================================

