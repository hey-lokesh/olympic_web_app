import pandas as pd
import plotly.express as px

def med_tally(df):
    medal_tally = df.drop_duplicates(subset=['Team', 'Medal', 'Games', 'Sport', 'Event', 'Year', 'NOC'])
    medal_tally = medal_tally.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                              ascending=False).reset_index()
    medal_tally['Total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']

    return medal_tally
def year_country_list(df):
    df['Year'] = df['Year'].astype(str)
    year_list = df['Year'].sort_values().unique().tolist()
    year_list.insert(0, 'Overall')

    country_list = df['Team'].sort_values().unique().tolist()
    country_list.insert(0, 'Overall')
    return year_list,country_list

def fetch_medal_tally(df,year, country):
    medal_df = df.drop_duplicates(subset=['Team', 'Medal', 'Games', 'Sport', 'Year', 'Event', 'NOC'])
    medal_df['Year'] = medal_df['Year'].astype(str)
    if (year == 'Overall' and country == 'Overall'):
        tal = medal_df
        x = tal.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()
    if (year == 'Overall' and country != 'Overall'):
        tal = medal_df[medal_df['region'] == country]
        x = tal.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    if (year != 'Overall' and country == 'Overall'):
        tal = medal_df[medal_df['Year'] == year]
        x = tal.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()
    if (year != 'Overall' and country != 'Overall'):
        tal = medal_df[(medal_df['Year'] == year) & (medal_df['region'] == country)]
        x = tal.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()

    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']
    return x
def data_over_years(df,data):
    kiki = df.drop_duplicates(['Year', data])['Year'].value_counts().reset_index()
    kiki = kiki.sort_values('Year')
    kiki.rename(columns={'count': data },inplace=True)
    fig = px.line(kiki, x="Year", y= data)
    return fig

def sport_list(df):
    s_list = df['Sport'].sort_values().unique().tolist()
    s_list.insert(0, 'Overall')
    return s_list

def success_players(df,sport):
    temp = df.dropna(subset=['Medal'])
    if(sport!='Overall'):
        sport_df = temp[temp['Sport']==sport]['Name'].value_counts().reset_index().merge(temp,on='Name',how='left').drop_duplicates(subset=['Name'])
        sport_df =sport_df[['Name','count','Sport','region']].head(15)
        return sport_df
    return temp['Name'].value_counts().reset_index().merge(temp,on='Name',how='left').drop_duplicates(subset=['Name'])[['Name','count','Sport','region']].head(15)

def cwmt(df,country):
    new = df.drop_duplicates(subset=['Team', 'Medal', 'Games', 'Sport', 'Year', 'Event', 'NOC'])
    new = new.dropna(subset=['Medal'])

    new_df = new[new['region'] == country]
    new_df= new_df.groupby('Year').count()['Medal'].reset_index()
    fig = px.line(new_df, x="Year", y='Medal')
    return fig
def country_event_heatmap(df,country):
    new = df.drop_duplicates(subset=['Team', 'Medal', 'Games', 'Sport', 'Year', 'Event', 'NOC'])
    new = new.dropna(subset=['Medal'])

    new_df = new[new['region'] == country]
    pt = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
    return pt

def success_players2(temp,country):
    temp = temp.dropna(subset=['Medal'])
    country_df = temp[temp['region']==country]['Name'].value_counts().reset_index().merge(temp,on='Name',how='left').drop_duplicates(subset=['Name'])
    country_df =country_df[['Name','count','Sport']].head(15)
    country_df.rename(columns = {'count':'Medals'},inplace=True)
    return country_df