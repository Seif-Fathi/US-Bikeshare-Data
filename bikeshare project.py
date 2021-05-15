# -*- coding: utf-8 -*-
import pandas as pd
import time

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # Request the city name from the user
    while True:
        city = input("which city's data would you like to see: Chicago or New York city or Washington: ").lower()
        #check input
        if city not in ['chicago','new york city','new york','washington']:
            print('Please enter a vaild city name')
            continue
        if city in ['chicago','new york city','new york','washington']:
            break
    print('-'*40)    
    # Request month from the user
    while True:   
        month = input("which months data would you like to see: ").lower()
        #check input
        if month not in ['all','january','february','march','april','may','june']:
            print('please enter a vaild month name')
            continue
        if month in ['all','january','february','march','april','may','june']:
            break
    print('-'*40)    
    # Request the day from the user
    while True:
        
        day = input("which day's data would you like to see: ") .lower()
        if day not in ['all','sunday','monday','tuesday','wednesday','thursday','friday','saturday']:
            print('please enter a valid day')
            continue
        if day in ['all','sunday','monday','tuesday','wednesday','thursday','friday','saturday']:
            break 
    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """
    
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    print('most common month:' ,df['month'].mode()[0])

    # Display the most common day of week
    print('most common day of :',df['day_of_week'].mode()[0])

    # Display the most common start hour
    print('most common start hour:',df['hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    print('most commonly used start sation:',df['Start Station'].mode()[0])

    # Display most commonly used end station
    print('most commonly used end staion:',df['End Station'].mode()[0])

    # Display most frequent combination of start station and end station trip
    start_end_group = df.groupby(['Start Station','End Station'])
    print('most most frequent combination of start station and end station trip:',start_end_group.size().sort_values(ascending = False).head(1))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    print('total travel time:',df['Trip Duration'].sum())

    # Display mean travel time
    print('mean travel time:',df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('counts of user type:',df['User Type'].value_counts())

    # Display counts of gender
    if city !='washington':
         print('counts of gender:',df['Gender'].value_counts())

    # Display earliest, most recent, and most common year of birth
         print('earliest year of birth: ',df['Birth Year'].min(),'\n'
              'most recent year of birth:',df['Birth Year'].max(),'\n'
              'most common year of birth:',df['Birth Year'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    while True:
        view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n').lower()
        if view_data not in ['yes','no']:
            print('\n')
            print('Please enter yes or no: ')
            continue
        else:
            break
    rows = 5
    start = 0
    while view_data == 'yes':
        try:
            print(df.iloc[start:rows,:])
            print('_'*40)
            start+=5
            rows+=5
            view_data=input('do you wish to view the next 5 rows? Enter yes or no\n').lower()
            while True:
                if view_data not in ['yes','no']:
                    view_data = input('Please enter yes or no\n').lower()
                    continue
                else:
                    break
        except IndexError:
            print('no more rows to view')
            view_data = ' '
        continue

def main():
    while True:
        user_input = get_filters()
        df = load_data(*user_input)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,user_input[0])
        display_data(df)
        restart = input("woud you to see another cities data?,if so enter 'Yes', if not enter 'No'\n").lower()
        if restart not in ['yes','no']:
            print("please enter 'Yes' or 'No'")
        if restart != 'yes':
            break
        else:
            print('_'*40)
            continue

if __name__ == '__main__':
    main()    
