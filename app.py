import streamlit as st
import preprocessor,helper1
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')
st.sidebar.title("Olympics Analysis")
st.sidebar.image('https://img.freepik.com/premium-photo/logo-olympic-paris_1220283-9526.jpg?size=626&ext=jpg')
user_input = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally','Overall Analysis','Country Wise Analysis')
)
medal = preprocessor.preprocess(df,region_df)
medal2 = preprocessor.preprocess2(df,region_df)

if(user_input=='Medal Tally'):
    st.sidebar.header('Medal Tally')
    year,country = helper1.year_country_list(df)
    selected_year=st.sidebar.selectbox("Select Year",year)
    selected_country=st.sidebar.selectbox("Select Country", country)
    if (selected_year == 'Overall' and selected_country == 'Overall'):
        st.title('Overall Tally')
    if (selected_year == 'Overall' and selected_country != 'Overall'):
        st.title('Medal tally of '+selected_country)
    if (selected_year != 'Overall' and selected_country == 'Overall'):
        st.title(f"Medal tally in {selected_year}")
    if (selected_year != 'Overall' and selected_country != 'Overall'):
        st.title('Medal tally of ' + selected_country + " in " + str(selected_year))
    st.table(helper1.fetch_medal_tally(medal,selected_year,selected_country))

if user_input=='Overall Analysis':
    st.title('Top Statistics')
    col1,col2,col3 = st.columns(3)
    with col1:
        st.title("Athletes")
        st.header(medal['Name'].unique().shape[0])

    with col2:
        st.title("City")
        st.header(medal['City'].unique().shape[0])

    with col3:
        st.title("Teams")
        st.header(medal['region'].unique().shape[0])
    col1, col2, col3 = st.columns(3)
    with col1:
        st.title("Sports")
        st.header(medal['Sport'].unique().shape[0])

    with col2:
        st.title("Events")
        st.header(medal['Event'].unique().shape[0])

    with col3:
        st.title("Years")
        st.header(medal['Year'].unique().shape[0])


    region_fig = helper1.data_over_years(medal,'region')
    st.title("No. of Countries over Years")
    st.plotly_chart(region_fig)

    event_fig = helper1.data_over_years(medal, 'Event')
    st.title("No. of Events over Years")
    st.plotly_chart(event_fig)

    athlete_fig = helper1.data_over_years(medal, 'Name')
    st.title("No. of Athlete over Years")
    st.plotly_chart(athlete_fig)

    selected_sport = st.selectbox("Select sports",helper1.sport_list(df))
    st.title("Most Successful Athletes")
    st.table(helper1.success_players(medal2,selected_sport))

if user_input=='Country Wise Analysis':
    country_list = medal['region'].dropna().sort_values().unique().tolist()
    selected_country=st.sidebar.selectbox("Select Country",country_list)
    med_tally_fig = helper1.cwmt(medal2, selected_country)
    st.title(selected_country+ " medal tally over Years")
    st.plotly_chart(med_tally_fig)

    pt = helper1.country_event_heatmap(medal2,selected_country)
    fig,ax = plt.subplots(figsize=(20,20))
    ax= sns.heatmap(pt,annot=True)
    st.title(selected_country + " excels in the following sport ")
    st.pyplot(fig)

    st.title("Most successful athletes in " + selected_country)
    success= helper1.success_players2(medal2,selected_country)
    st.table(success)



