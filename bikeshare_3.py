import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyse
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Enter the name of the city to analyse: ').lower()
        if city not in CITY_DATA:
            print('Please choose a correct city: Chicago, New York City, Washington')
        else:
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("Enter the name of the month to filter by, or 'all' to apply no month filter: ").lower()
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        if month != 'all' and month not in months:
            print("I'm sorry. That's not 'all' or a month from January to June. Try again")
        else:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Enter the name of the day of week to filter by, or 'all' to apply no day filter: "). lower()
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        if day != 'all' and day not in days:
            print("That's not 'all' or a valid day. Try again")
        else:
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
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['Month'] = df['Start Time'].dt.month
    df['Day of Week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['Month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['Day of Week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['Month'].mode()[0]
    print('Most common month: {}'.format(most_common_month))

    # display the most common day of week
    most_common_day = df['Day of Week'].mode()[0]
    print('Most common day: {}'.format(most_common_day))

    # display the most common start hour
    # extract hour from the Start Time column to create an hour column
    df['Hour'] = df['Start Time'].dt.hour
    most_common_start_hour = df['Hour'].mode()[0]
    print('Most common start hour: {}'.format(most_common_start_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print('Most commonly used start station: {}'.format(most_common_start_station))

    # display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print('Most commonly used end station: {}'.format(most_common_end_station))

    # display most frequent combination of start station and end station trip
    #Use group by show combination of start and end station trips
    most_common_station_combination = df.groupby(['Start Station', 'End Station']).count().idxmax()[0]
    print('Most commonly used station combination: {}'.format(most_common_station_combination))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    tot_time = df['Trip Duration'].sum()
    print('Total travel time is {} seconds or {} minutes or {} hours'.format(tot_time, tot_time/60, tot_time/3600))

    # display mean travel time
    ave_time = df['Trip Duration'].mean()
    print('Average travel time is {} seconds or {} minutes'.format(ave_time, ave_time/60))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # display counts of user types
    count_users_by_type = df['User Type'].value_counts()
    print('Count of users by type:\n{}'.format(count_users_by_type))

    # display counts of gender
    if 'Gender' in df:
        count_users_by_gender = df['Gender'].value_counts()
        print('\nCount of users by gender:\n{}'.format(count_users_by_gender))
    else:
        print('\nThis dataset does not contain "gender" data.')

    # display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        dob_oldest_user = int(df['Birth Year'].min())
        print('\nEarliest date of birth for user: {}\n'.format(dob_oldest_user))
        dob_youngest_user = int(df['Birth Year'].max())
        print('Latest date of birth for user: {}\n'.format(dob_youngest_user))
        most_common_dob = int(df['Birth Year'].mode())
        print('Most common date of birth for user: {}\n'.format(most_common_dob))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def city_raw_data(df):
    """Displays the first 5 rows of raw data in the df.
        Prompts users if they would like to see more."""

    # assign the index as 0 so the loop can iterate through the df
    index = 0

    # ask user if they would like to see raw data (5 rows at a time)
    while True:
        city_raw_data = input("Would you like to see raw data. Enter 'yes' to iterate thorugh raw data 5 rows at a time: ").lower()
        if city_raw_data != "yes":
            break
        else:
            print(df[index:index + 5])
            index += 5


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        city_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
