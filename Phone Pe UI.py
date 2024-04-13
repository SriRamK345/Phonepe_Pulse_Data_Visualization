import pandas as pd
import mysql.connector  # Modified import statement
import streamlit as st
import plotly.express as px
from streamlit_option_menu import option_menu
from PIL import Image
import os

# Setting up page configuration
st.set_page_config(layout= "wide",
                   initial_sidebar_state= "expanded")

st.sidebar.header(":wave: :violet[**Welcome to the dashboard!**]")

with st.sidebar:
    selected = option_menu("Menu", ["Home", "Top Charts", "Explore Data","About"],
                           icons=["house", "graph-up-arrow", "bar-chart-line", "exclamation-circle"],
                           menu_icon="menu-button-wide",
                           default_index=0,
                           styles={"nav-link": {"font-size": "15px", "text-align": "left", "margin": "-2px",
                                                "--hover-color": "#c44a2f"},
                                   "nav-link-selected": {"background-color": "#4a1252"}})
# MENU 1 - HOME
if selected == "Home": 
    st.markdown("# :violet[Data Visualization and Exploration]")
    st.markdown("## :violet[A User-Friendly Tool Using Streamlit and Plotly]")
    st.markdown(
        "### :rainbow[Technologies used :] Github Cloning, Python, Pandas, MySQL, Streamlit, and Plotly.")  # Changed PostgreSQL to MySQL
    st.markdown(
        "### :rainbow[Overview :] In this streamlit web app you can visualize the phonepe pulse data and gain lot of insights on transactions, number of users, top 10 state, district, pincode and which brand has most number of users and so on. Bar charts, Pie charts and Geo map visualization are used to get some insights.")

# Establish a connection to the MySQL server
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="India@123",
    database="Phonepe",
    port=3306
)
cursor = conn.cursor()

if selected == "Top Charts":
    st.markdown("## :violet[Top Charts]")
    Type = st.sidebar.selectbox("**Type**", ("Transactions", "Users"))
    Year = st.sidebar.slider("**Year**", min_value=2018, max_value=2023)
    Quarter = st.sidebar.slider("Quarter", min_value=1, max_value=4)

    if Type == "Transactions":
        # State Pie Chart
        col1 = st.columns([1])[0]
        with col1:
            st.markdown("### :blue[State]")
            cursor.execute(
                f"""select state, sum(Trans_count) as Total_Transactions_Count, sum(Trans_amount) as Total from aggregated_transaction 
                    where year = {Year} and quarter = {Quarter} group by State order by Total desc limit 10""")
            df = pd.DataFrame(cursor.fetchall(), columns=['State', 'Transactions_Count', 'Total_Amount'])
            fig = px.pie(df, values='Total_Amount',
                        names='State',
                        title='Top 10 States Of Transaction',
                        color_discrete_sequence=px.colors.sequential.Agsunset,
                        hover_data=['Transactions_Count'],
                        labels={'Transactions_Count': 'Transactions_Count'})
            
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)

        # District Pie Chart
        col2 = st.columns([1])[0]
        with col2:
            st.markdown("### :blue[District]")
            cursor.execute(
                f"""select District , sum(Trans_Count) as Total_Count, sum(Trans_Amount) as Total from map_transaction 
                    where year = {Year} and quarter = {Quarter} group by District order by Total desc limit 10""")
            df = pd.DataFrame(cursor.fetchall(), columns=['District', 'Transactions_Count', 'Total_Amount'])

            fig = px.pie(df, values='Total_Amount',
                        names='District',
                        title='Top 10 Districts of transaction',
                        color_discrete_sequence=px.colors.sequential.Agsunset,
                        hover_data=['Transactions_Count'],
                        labels={'Transactions_Count': 'Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)

        # Pincode Pie Chart
        col3 = st.columns([1])[0]
        with col3:
            st.markdown("### :blue[Pincode]")
            cursor.execute(
                f"""select District_Pincode, sum(Trans_count) as Total_Transactions_Count, sum(Trans_amount) as Total from top_transaction 
                    where year = {Year} and quarter = {Quarter} group by District_Pincode order by Total desc limit 10""")
            df = pd.DataFrame(cursor.fetchall(), columns=['Pincode', 'Transactions_Count', 'Total_Amount'])
            fig = px.pie(df, values='Total_Amount',
                        names='Pincode',
                        title='Top 10 Pincodes of transaction',
                        color_discrete_sequence=px.colors.sequential.Agsunset,
                        hover_data=['Transactions_Count'],
                        labels={'Transactions_Count': 'Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)

    if Type == "Users":
        col1 = st.columns([1])[0]
        with col1:
            st.markdown("### :blue[Brands]")
            if Year == 2023 and Quarter in [ 1, 2, 3, 4]:
                st.markdown("#### :red[Sorry No Data for selected year and quarter]")
            elif Year == 2022 and Quarter in [2, 3, 4]: 
                st.markdown("#### :red[Sorry No Data for selected year and quarter]")
            else:
                cursor.execute(
                    f"""select Brands, sum(User_Count) as Total_Count, avg(User_Percentage)*100 as Avg_Percentage from aggregated_user 
                        where year = {Year} and quarter = {Quarter} group by Brands order by Total_Count desc limit 10""")
                df = pd.DataFrame(cursor.fetchall(), columns=['Brand', 'Total_Users', 'Avg_Percentage'])
                fig = px.bar(df,
                             title='Top 10 Brands in user',
                             x="Total_Users",
                             y="Brand",
                             orientation='h',
                             color='Avg_Percentage',
                             color_continuous_scale=px.colors.sequential.Agsunset)
                st.plotly_chart(fig, use_container_width=True)

        col2 = st.columns([1])[0]
        with col2:
            st.markdown("### :blue[District]")
            cursor.execute(
                f"""select District, sum(User_id) as Total_Users from map_user 
                    where year = 2018 and quarter = 1 group by District order by Total_Users desc limit 10""")
            df = pd.DataFrame(cursor.fetchall(), columns=['District', 'Total_Users'])
            df.Total_Users = df.Total_Users.astype(float)
            fig = px.bar(df,
                         title='Top 10 Districts in user',
                         x="Total_Users",
                         y="District",
                         orientation='h',
                         color='Total_Users',
                         color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig, use_container_width=True)

        col3 = st.columns([1])[0]    
        with col3:
            st.markdown("### :blue[Pincode]")
            cursor.execute(
                f"""select District_Pincode, sum(User_id) as Total_Users from top_user 
                    where year = {Year} and quarter = {Quarter} group by District_Pincode order by Total_Users desc limit 10""")
            df = pd.DataFrame(cursor.fetchall(), columns=['Pincode', 'Total_Users'])
            fig = px.pie(df,
                         values='Total_Users',
                         names='Pincode',
                         title='Top 10 Pincode in user',
                         color_discrete_sequence=px.colors.sequential.Agsunset,
                         hover_data=['Total_Users'])
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)

if selected == "Explore Data":
    Type = st.sidebar.selectbox("**Type**", ("Transactions", "Users"))
    Year = st.sidebar.slider("**Year**", min_value=2018, max_value=2023)
    Quarter = st.sidebar.slider("Quarter", min_value=1, max_value=4)
    col1,col2 = st.columns(2)

    # EXPLORE DATA - TRANSACTIONS
    if Type == "Transactions":
        # Overall State Data - TRANSACTIONS AMOUNT - INDIA MAP
        col1 = st.columns([1])[0]
        with col1:
            st.markdown("## :violet[Overall State Data - Transactions Amount]")
            cursor.execute(
                f"""select State, sum(Trans_Count) as Total_Transactions, sum(Trans_Amount) as Total_amount from map_transaction 
                    where year = {Year} and quarter = {Quarter} group by State order by State""")
            df1 = pd.DataFrame(cursor.fetchall(), columns=['State', 'Total_Transactions', 'Total_amount'])
            df2 = pd.read_csv(r"G:\Guvi\VS code\.venv\Phonepe pro\state_names.csv")
            df1.State = df2

            fig = px.choropleth(df1,
                                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                                featureidkey='properties.ST_NM',
                                locations='State',
                                color='Total_amount',
                                color_continuous_scale='sunset')

            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig, use_container_width=True)

        # Overall State Data - TRANSACTIONS COUNT - INDIA MAP
        col2 = st.columns([1])[0]
        with col2:
            st.markdown("## :violet[Overall State Data - Transactions Count]")
            cursor.execute(
                f"""select State, sum(Trans_Count) as Total_Transactions, sum(Trans_Amount) as Total_amount from map_transaction 
                    where year = {Year} and quarter = {Quarter} group by State order by State""")
            df1 = pd.DataFrame(cursor.fetchall(), columns=['State', 'Total_Transactions', 'Total_amount'])
            df2 = pd.read_csv(r"G:\Guvi\VS code\.venv\Phonepe pro\state_names.csv")
            df1.Total_Transactions = df1.Total_Transactions.astype(int)
            df1.State = df2

            fig = px.choropleth(df1,
                                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                                featureidkey='properties.ST_NM',
                                locations='State',
                                color='Total_Transactions',
                                color_continuous_scale='sunset')

            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig, use_container_width=True)

        # BAR CHART TRANSACTIONS - DISTRICT WISE DATA
        st.markdown("# ")
        st.markdown("## :violet[Select any State]")
        selected_state = st.selectbox("",
                                      ('ANDAMAN-&-NICOBAR-ISLANDS','ANDHRA-PRADESH', 'ARUNACHAL-PRADESH', 'ASSAM',
                                       'BIHAR',
                                       'CHANDIGARH', 'CHHATTISGARH', 'DADRA-&-NAGAR-HAVELI-&-DAMAN-&-DIU', 'DELHI',
                                       'GOA', 'GUJARAT', 'HARYANA',
                                       'HIMACHAL-PRADESH', 'JAMMU-&-KASHMIR', 'JHARKHAND', 'KARNATAKA', 'KERALA',
                                       'LADAKH', 'LAKSHADWEEP',
                                       'MADHYA-PRADESH', 'MAHARASHTRA', 'MANIPUR', 'MEGHALAYA', 'MIZORAM',
                                       'NAGALAND', 'ODISHA', 'PUDUCHERRY', 'PUNJAB', 'RAJASTHAN', 'SIKKIM',
                                       'TAMIL-NADU', 'TELANGANA', 'TRIPURA', 'UTTAR-PRADESH', 'UTTARAKHAND',
                                       'WEST-BENGAL'), index=30)

        cursor.execute(
            f"""select State, District, Year, Quarter, sum(Trans_Count) as Total_Transactions, sum(Trans_Amount) as Total_amount from map_transaction 
                where year = {Year} and quarter = {Quarter} and State = '{selected_state}' group by State, District, Year, Quarter order by State,District""")

        df1 = pd.DataFrame(cursor.fetchall(), columns=['State', 'District', 'Year', 'Quarter',
                                                         'Total_Transactions', 'Total_amount'])
        fig = px.bar(df1,
                     title=selected_state,
                     x="District",
                     y="Total_Transactions",
                     orientation='v',
                     color='Total_amount',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig, use_container_width=True)

        # BAR CHART TOTAL USER - DISTRICT WISE DATA
        st.markdown("## :violet[Select any State]")
        selected_state = st.selectbox("",
                                      ('ANDAMAN-&-NICOBAR-ISLANDS','ANDHRA-PRADESH', 'ARUNACHAL-PRADESH', 'ASSAM',
                                       'BIHAR',
                                       'CHANDIGARH', 'CHHATTISGARH', 'DADRA-&-NAGAR-HAVELI-&-DAMAN-&-DIU', 'DELHI',
                                       'GOA', 'GUJARAT', 'HARYANA',
                                       'HIMACHAL-PRADESH', 'JAMMU-&-KASHMIR', 'JHARKHAND', 'KARNATAKA', 'KERALA',
                                       'LADAKH', 'LAKSHADWEEP',
                                       'MADHYA-PRADESH', 'MAHARASHTRA', 'MANIPUR', 'MEGHALAYA', 'MIZORAM',
                                       'NAGALAND', 'ODISHA', 'PUDUCHERRY', 'PUNJAB', 'RAJASTHAN', 'SIKKIM',
                                       'TAMIL-NADU', 'TELANGANA', 'TRIPURA', 'UTTAR-PRADESH', 'UTTARAKHAND',
                                       'WEST-BENGAL'))

        cursor.execute(
            f"""select State,Year,Quarter,District,sum(User_id) as Total_Users from map_user 
                where year = {Year} and quarter = {Quarter} and state = '{selected_state}' group by State, District,Year, Quarter order by State,District""")

        df = pd.DataFrame(cursor.fetchall(),
                          columns=['State', 'Year', 'Quarter', 'District', 'Total_Users'])
        df.Total_Users = df.Total_Users.astype(int)

        fig = px.bar(df,
                     title=selected_state,
                     x="District",
                     y="Total_Users",
                     orientation='v',
                     color='Total_Users',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig, use_container_width=True)


    # EXPLORE DATA - USERS      
    if Type == "Users":
        
        # Overall State Data - TOTAL APPOPENS - INDIA MAP
        st.markdown("## :violet[Overall State Data - Total User]")
        cursor.execute(f"""select State, sum(User_id) as Total_Users from map_user 
                        where year = {Year} and quarter = {Quarter} group by State order by State""")
        df1 = pd.DataFrame(cursor.fetchall(), columns=['State', 'Total_Users'])
        df2 = pd.read_csv(r"G:\Guvi\VS code\.venv\Phonepe pro\state_names.csv")
        df1.Total_Users = df1.Total_Users.astype(float)
        df1.State = df2
        
        fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                  featureidkey='properties.ST_NM',
                  locations='State',
                  color='Total_Users',
                  color_continuous_scale='sunset')

        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig,use_container_width=True)
        
        # BAR CHART TOTAL UERS - DISTRICT WISE DATA 
        st.markdown("## :violet[Select any State to explore more]")
        selected_state = st.selectbox("",
                             ('andaman-&-nicobar-islands','andhra-pradesh','arunachal-pradesh','assam','bihar',
                              'chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi','goa','gujarat','haryana',
                              'himachal-pradesh','jammu-&-kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep',
                              'madhya-pradesh','maharashtra','manipur','meghalaya','mizoram',
                              'nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                              'tamil-nadu','telangana','tripura','uttar-pradesh','uttarakhand','west-bengal'),index=30)
        
        cursor.execute(f"""select State,Year,Quarter,District,sum(User_id) as Total_Users from map_user 
                        where year = {Year} and quarter = {Quarter} and state = '{selected_state}' group by State, District,Year, Quarter order by State,District""")
        
        df = pd.DataFrame(cursor.fetchall(), columns=['State','year', 'quarter', 'District', 'Total_Users'])
        df.Total_Users = df.Total_Users.astype(int)
        
        fig = px.bar(df,
                     title=selected_state,
                     x="District",
                     y="Total_Users",
                     orientation='v',
                     color='Total_Users',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig,use_container_width=True)

if selected == "About":
    st.write(" ")
    st.markdown("### :violet[About PhonePe Pulse:] ")
    st.write(
        "##### BENGALURU, India, On Sept. 3, 2021 PhonePe, India's leading fintech platform, announced the launch of PhonePe Pulse, India's first interactive website with data, insights and trends on digital payments in the country. The PhonePe Pulse website showcases more than 2000+ Crore transactions by consumers on an interactive map of India. With  over 45% market share, PhonePe's data is representative of the country's digital payment habits.")
    st.write(
        "##### The insights on the website and in the report have been drawn from two key sources - the entirety of PhonePe's transaction data combined with merchant and customer interviews. The report is available as a free download on the PhonePe Pulse website and GitHub.")
    st.markdown("### :violet[About PhonePe:] ")
    st.write(
        "##### PhonePe is India's leading fintech platform with over 300 million registered users. Using PhonePe, users can send and receive money, recharge mobile, DTH, pay at stores, make utility payments, buy gold and make investments. PhonePe forayed into financial services in 2017 with the launch of Gold providing users with a safe and convenient option to buy 24-karat gold securely on its platform. PhonePe has since launched several Mutual Funds and Insurance products like tax-saving funds, liquid funds, international travel insurance and Corona Care, a dedicated insurance product for the COVID-19 pandemic among others. PhonePe also launched its Switch platform in 2018, and today its customers can place orders on over 600 apps directly from within the PhonePe mobile app. PhonePe is accepted at 20+ million merchant outlets across Bharat")
