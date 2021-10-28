import datetime
import platform

from icecream import ic
import pandas as pd


# Different styles in zero-padding in data append on operating system

if platform.system() == 'Linux':
    STRFTIME_DATA_FRAME_FORMAT = '%-m/%-d/%y'
elif platform.system() == 'Windows':
    STRFTIME_DATA_FRAME_FORMAT = '%#m/%#d/%y'
else:
    STRFTIME_DATA_FRAME_FORMAT = '%-m/%-d/%y'


def daily_report(date_string=None):
    report_directory = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/'

    if date_string is None:
        yesterday = datetime.date.today() - datetime.timedelta(days=2)
        file_date = yesterday.strftime('%m-%d-%Y')
    else:
        file_date = date_string
    df = pd.read_csv(report_directory + file_date +
                     '.csv', dtype={"FIPS": str}
                     )
    return df


def daily_confirmed():
    df = pd.read_csv(
        'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/jhu/new_cases.csv')
    return df


def daily_deaths():
    # returns the daily reported deaths for respective date
    df = pd.read_csv(
        'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/jhu/new_deaths.csv')
    return df


def confirmed_report():
    # Returns time series version of total cases confirmed globally
    df = pd.read_csv(
        'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
    return df


def deaths_report():
    # Returns time series version of total deaths globally
    df = pd.read_csv(
        'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
    return df


def recovered_report():
    # Return time series version of total recoveries globally
    df = pd.read_csv(
        'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv')
    return df


def realtime_growth(date_string=None, weekly=False, monthly=False):

    df1 = confirmed_report()[confirmed_report().columns[4:]].sum()
    df2 = deaths_report()[deaths_report().columns[4:]].sum()
    df3 = recovered_report()[recovered_report().columns[4:]].sum()
    growth_df = pd.DataFrame([])
    growth_df['Confirmed'], growth_df['Deaths'], growth_df['Recovered'] = df1, df2, df3
    growth_df.index = growth_df.index.rename('Date')

    yesterday = pd.Timestamp('now').date() - pd.Timedelta(days=1)

    if date_string is not None:
        return growth_df.loc[growth_df.index == date_string]

    elif weekly is True:
        monthly_df = pd.DataFrame([])
        intervals = pd.date_range(end=yesterday, periods=3, freq='1M').strftime(STRFTIME_DATA_FRAME_FORMAT).tolist()
        for day in intervals:
            monthly_df = monthly_df.append(growth_df.loc[growth_df.index==day])
        return monthly_df

    return growth_df


def percentage_trends():

    current = realtime_growth(weekly=True).iloc[-1]
    last_week = realtime_growth(weekly=True).iloc[-2]
    trends = round(number=((current - last_week)/last_week)*100, ndigits=1)

    rate_change = round(((current.Deaths/current.Confirmed)*100) - ((last_week.Deaths / last_week.Confirmed)*100), ndigits=2)
    trends = trends.append(pd.Series(data=rate_change, index=['Death_rate']))
    
    return trends

def global_cases():
    df = daily_report()[['Country_Region', 'Confirmed', 'Recovered', 'Deaths', 'Active']]
    df.rename(columns={'Country_Region': 'Country'}, inplace=True)
    df = df.groupby('Country', as_index=False).sum()
    df.sort_values(by=['Confirmed'], ascending=False, inplace=True)

    for index, row in df.iterrows():
        countryCases = int(row['Confirmed'])
        countryDeaths = int(row['Deaths'])
        if(countryCases == 0):
            deathRateFormatted = format(0, '.2f')
            df.loc[index, 'Death Rate'] = deathRateFormatted
        else:
            deathRate = float(countryDeaths / countryCases)*100
            deathRateFormatted = format(deathRate, '.2f')
            df.loc[index, 'Death Rate'] = deathRateFormatted
    return df
        

def usa_counties():

    populations = pd.read_csv('https://raw.githubusercontent.com/balsama/us_counties_data/master/data/counties.csv')[['FIPS Code', 'Population']]
    populations.rename(columns={'FIPS Code': 'fips'}, inplace=True)
    df = pd.read_csv('https://raw.githubusercontent.com/nytimes/covid-19-data/master/live/us-counties.csv', dtype={"fips": str}).iloc[:,:6]
    df = pd.merge(df, populations, on='fips')
    df['cases/capita'] = (df.cases / df.Population)*100000

    return df
