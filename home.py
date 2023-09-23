import streamlit as st
import pandas as pd
import sqlite3
from numerize.numerize import numerize
import matplotlib.pyplot as plt
import plotly.express as px
from query import *
from streamlit_option_menu import option_menu
import time


st.set_page_config(page_title='Dashboard', page_icon="🐘", layout='wide')
st.subheader('🔔Insurance descriptive analytics')
st.markdown('##')


# Fetch your data from the database and table
conn = sqlite3.connect('database.db')
cursor = conn.execute("SELECT * FROM Insuarance")
result = cursor.fetchall()
# Extract column names from cursor description
columns = [desc[0] for desc in cursor.description]

mydata = pd.DataFrame(result, columns=columns)


# Implement sidebar
st.sidebar.image('image\logo 1.jpg', caption='Online Analytics')

# Switcher
st.sidebar.header('Please filter')
region = st.sidebar.multiselect(
    'Select Region',
    options=mydata['Region'].unique(),
    default=mydata['Region'].unique(),
)
st.sidebar.header('Please filter')
location = st.sidebar.multiselect(
    'Select Location',
    options=mydata['Location'].unique(),
    default=mydata['Location'].unique(),
)
st.sidebar.header('Please filter')
state = st.sidebar.multiselect(
    'Select State',
    options=mydata['State'].unique(),
    default=mydata['State'].unique(),
)

st.sidebar.header('Please filter')
construction = st.sidebar.multiselect(
    'Select Construction',
    options=mydata['Construction'].unique(),
    default=mydata['Construction'].unique(),
)

st.sidebar.header('Please filter')
earthquake = st.sidebar.multiselect(
    'Select Earthquake',
    options=mydata['Earthquake'].unique(),
    default=mydata['Earthquake'].unique(),
)
st.sidebar.header('Please filter')
businessType = st.sidebar.multiselect(
    'Select Business Type',
    options=mydata['BusinessType'].unique(),
    default=mydata['BusinessType'].unique(),
)
st.sidebar.header('Please filter')
flood = st.sidebar.multiselect(
    'Select Flood',
    options=mydata['Flood'].unique(),
    default=mydata['Flood'].unique(),
)
mydata_selection=mydata.query(
    "Region ==@region & Location==@location & Construction==@construction"
)
#implement expander

def Home():
    with st.expander("Tabular"):
        showData = st.multiselect('Filter:', mydata_selection.columns, default=[])
        st.write(mydata_selection[showData])

    # Compute top analytics
    total_investment = mydata_selection['Investment'].sum()   
    investment_mode = mydata_selection['Investment'].mode().values[0]
    investment_mean = mydata_selection['Investment'].mean()
    investment_median = mydata_selection['Investment'].median()
    rating = mydata_selection['Rating'].sum().replace('.', '')

    total1, total2, total3, total4, total5 = st.columns(5, gap='large')
    with total1:
        st.info('Total Investment', icon='📁')
        st.metric(label="sum TZS", value=f"{total_investment:,.0f}")

    with total2:
        st.info('Most Frequent', icon='📁')
        st.metric(label="mode TZS", value=f"{investment_mode:,.0f}")

    with total3:
        st.info('Average', icon='📁')
        st.metric(label="mean TZS", value=f"{investment_mean:,.0f}")

    with total4:
        st.info('Middle value', icon='📁')
        st.metric(label="median TZS", value=f"{investment_median:,.0f}")

    with total5:
        st.info('Ratings', icon='📁')
        st.metric(label="Ratings", value=numerize(int(rating)), help=f"Total Rating: {rating}")

    st.markdown("""---""")



#graphs

def graphs():
    # Simple bar graph
    investment_by_business_type = (
        mydata_selection.groupby(by=["BusinessType"]).count()[["Investment"]].sort_values(by="Investment")
    )
    fig_investment = px.bar(
        investment_by_business_type,
        x="Investment",
        y=investment_by_business_type.index,
        orientation="h",
        title="<b>Investment by Business Type</b>",
        color_discrete_sequence=["#0083b8"]*len(investment_by_business_type),
        template="plotly_white"
    )

    fig_investment.update_layout(
        plot_bgcolor="rgba(0, 0, 0, 0)",
        xaxis=dict(showgrid=False)
    )

    # Simple line graph
    investment_state = mydata_selection.groupby(by=["State"]).count()[["Investment"]]

    fig_state = px.line(
        investment_state,
        x=investment_state.index,
        y="Investment",
        orientation="v",
        title="<b>Investment by State</b>",
        color_discrete_sequence=["#0083b8"]*len(investment_state),
        template="plotly_white"
    )

    fig_state.update_layout(
        xaxis=dict(tickmode="linear"),
        plot_bgcolor="rgba(0, 0, 0, 0)",
        yaxis=dict(showgrid=False)
    )

    left, right = st.columns(2)

    left.plotly_chart(fig_state, use_container_width=True)
    right.plotly_chart(fig_investment, use_container_width=True)

#display congess bar
def Progressbar():
    st.markdown("""<style>.stProgress > div > div > div > div {background-image: linear-gradient(to right, #99ff99, #FFFF00)})</style>""", unsafe_allow_html=True,)
    target = 3000000000
    current = mydata_selection['Investment'].sum()
    
    if target == 0:
        st.write("Target cannot be zero.")
        return
    
    percent = round((current / target * 100))
    mybar = st.progress(0)

    if percent > 100:
        st.subheader("Target reached!")
    else:
        st.write("You have ", percent, "% of ", format(target, "d"), " TZS")
        for percent_complete in range(percent):
            time.sleep(0.1)
            mybar.progress(percent_complete + 1, text="Target Percentage")

def sideBar():

    with st.sidebar:
        selected = option_menu (
            menu_title="Main Menu",
            options=["Home","Progress"],
            icons=["house","eye"],
            menu_icon="cast",
            default_index=0
        )
    if selected == "Home":
        st.subheader(f"Page:{selected}") 
        Home()
        graphs()  
    if selected == "Progress":
        st.subheader(f"Page:{selected}") 
        Progressbar()
        graphs()               
sideBar()

#Theme
hide_st_style="""
<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}


</style>





"""


    
    
