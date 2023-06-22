#Chris Chapman


import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
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

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city = input('Enter a city (Chicago, New York, or Washington): ')
  #          city = 'Chicago'
  #          city = 'washington'

            print(city)
            
            city = city.lower()
            if city in CITY_DATA:
                break
        except TypeError:
            print('\nThat is not a valid entry.\n')

    # get user input for month (all, january, february, ... , june)
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    while True:
        try:
            month = input('Enter a month between January and June, or select all: ')
            month = month.lower()
            if month in months:
                break
        except TypeError:
            print('\nThat is not a valid entry.\n')  

    # get user input for day of week (monday=0, tuesday=1, ... sunday=6, all=7)
    days = [ 0, 1, 2, 3, 4, 5, 6, 7]
    while True:
        try:
            day = int(input('Enter a numerical value for the day of the week (monday=0, tuesday=1, ... sunday=6, all=7): '))
            if (int(day) in days):
                break
        except ValueError:
            print('\nThat is not a valid entry.\n')  

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
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_of_week

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month_number = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month_number]
     
     #   print('New Dataframe for: ', month)
     #   print(df)

    # filter by day of week if applicable
    if int(day) != 7:
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == int(day)]    
        print(df)

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['month'].mode()
    print('The most common month is:', most_common_month[0])

    # display the most common day of week
    most_common_day = df['day_of_week'].mode()
    print('The most common day is:', most_common_day[0])

    # display the most common start hour
    most_common_start_hour = df['Start Time'].dt.hour.mode()
    print('The most common start hour:', most_common_start_hour[0])


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_stn = df['Start Station'].mode()
    print('The most common Start Station is:', most_common_start_stn[0])

    # display most commonly used end station
    most_common_end_stn = df['End Station'].mode()
    print('The most common End Station is:', most_common_end_stn[0])

    # display most frequent combination of start station and end station trip
    print('The most common trip is:')
    grouped_df = df.groupby(['Start Station', 'End Station']).size().reset_index(name='Count').sort_values('Count', ascending=False)
    print(grouped_df.iloc[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total travel time is (seconds):', df['Trip Duration'].sum())

    # display mean travel time
    print('Mean travel time is (seconds):', round(df['Trip Duration'].mean(),2))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('Counts of', df['User Type'].value_counts().to_string())

    # Display counts of gender
    if 'Gender' in df.columns:
        print('Counts of', df['Gender'].value_counts().to_string())

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print('Earliest year of birth:', int(df['Birth Year'].min()))
        print('Most recent year of birth:', int(df['Birth Year'].max()))
        print('Most common year of birth:', int(df['Birth Year'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data(df):
    """Displays raw data of the selected database in series of 5 rows."""

    counter = 0
    end = 0 

    while True:
        try:
            answer = input('Would you like to see the raw data? (y or n)')
            answer = answer.lower()
            if (answer == 'yes' or answer == 'y'):
                break
            elif answer == 'n':
                break
        except TypeError:
            print('\nThat is not a valid entry.\n')  
    
    if (answer == 'yes' or answer == 'y'):
        num_rows = len(df)
        while True:
            try:
                end = counter + 5
                if end > num_rows:
                    end = num_rows
                for i in range(counter, end):
                    print(df.iloc[i], '\n')
                answer = input('Would you like to see more raw data? (\'y\' to continue)')
                answer = answer.lower()  
                if ((answer != 'yes' and answer != 'y') or end == num_rows):
                    break
                counter += 5
            except TypeError:
                print('\nThat is not a valid entry.\n')  

    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        raw_data(df)

        restart = input('\nWould you like to restart? (\'y\' to continue)')
        if (restart.lower() != 'yes' and restart.lower() != 'y'):
            break


if __name__ == "__main__":
	main()
