import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input(" Inter the name of the choosen city ( chicago, new york city, washington ) : ").lower()
    while city not in CITY_DATA.keys():
        print("please insert a valid city ")
        city = input(" Inter the name of the choosen city ( chicago, new york city, washington ) : ").lower()

    # TO DO: get user input for month (all, january, february, ... , june)
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    while True:
        month = input("Choose a month or 'all' : (january, february, march, april, may, june) : ").lower()
        if month in months:
            break
        else:
            print("Please choose a valid input")

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['saturday', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'all']
    while True:
        day = input(
            "please choose a day or 'all' ('saturday', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday) : ").lower()
        if day in days:
            break
        else:
            print("choose a valid input")

    print('-' * 40)
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
    df = pd.read_csv(CITY_DATA[city])

    # convert start time column to ( month, day & hour )
    df["Start Time"] = pd.to_datetime(df["Start Time"])
    # Extract ( month, day & hour
    df['month'] = df["Start Time"].dt.month
    df['day_of_week'] = df["Start Time"].dt.weekday_name
    df['hour'] = df["Start Time"].dt.hour
    # filtering
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        # Craete new dataframe from filtering by month.
        df = df[df['month'] == month]

        # Filter by day if day != 'all'
    if day != "all":
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    print('The most common month is: {}  '.format(df['month'].mode()[0]))

    # TO DO: display the most common day of week
    print('The most common day is: {}  '.format(df['day_of_week'].mode()[0]))

    # TO DO: display the most common start hour
    print('The most common start hour: {} '.format(df['hour'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print(' The most commonly used start station is : {} '.format(df['Start Station'].mode()[0]))

    # TO DO: display most commonly used end station
    print(' The most commonly used end station is : {} '.format(df['End Station'].mode()[0]))

    # TO DO: display most frequent combination of start station and end station trip
    df['route'] = df['Start Station'] + ',' + df['End Station']
    print('The most frequent combination of start station and end station trip is : {}'.format(df['route'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    # TO DO: display total travel time
    print('Total travel time is : {} minutes = {} hours'.format((df['Trip Duration'].sum().round()),
                                                                (df['Trip Duration'].sum() / 60).round()))

    # TO DO: display mean travel time
    print('Mean travel time is : {} mintues = {} hours'.format((df['Trip Duration'].mean().round()),
                                                               (df['Trip Duration'].mean() / 60).round()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print(df['User Type'].value_counts().to_frame())

    # TO DO: Display counts of gender
    if city != "washington":
        print(df['Gender'].value_counts().to_frame())

        # TO DO: Display earliest, most recent, and most common year of birth
        print(' earliest year of birth : ', int(df['Birth Year'].min()))
        print(' most recent year of birth : ', int(df['Birth Year'].max()))
        print(' most common year of birth : ', int(df['Birth Year'].mode()[0]))
    else:
        print("There is no data for (Gender & Birth Year ) for this city ")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def show_data(df):
    i = 0
    user_input = input("would you like to see 5 rows of data ( yes or no ) :").lower()
    if user_input not in ["yes", "no"]:
        print("Invalid input")
        user_input = input("would you like to see 5 rows of data ( yes or no ) :").lower()
    elif user_input != "yes":
        print('Thank you')
    else:
        while i + 5 < df.shape[0]:
            print(df.iloc[i:i + 5])
            i += 5
            user_input = input("would you like to see more 5 rows of data ( yes or no )").lower()
            if user_input != 'yes':
                print('Thank you')
                break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        show_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
    