import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
'new york city': 'new_york_city.csv',
'washington': 'washington.csv' }
days = ['Sunday','Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday','Saturday', 'All']
months = ['January','February', 'March', 'April', 'May', 'June','All']
input_filter = ['month', 'day', 'both']

def raw_data(df):
    '''
    prompt the user if they would like to see raw data
    '''

    print('\nIndividual user data and trip duration...\n')
    print('-'*40)
    count = 5
    while True:
        user_input1 = input('Would you like to view individual user data and trip duration? Enter yes or no.\n')
        if user_input1.lower() != 'yes':
            break
        new_df = pd.DataFrame(df, columns=['User Type','Gender','Birth Year','Trip Duration'])
        print(new_df.iloc[:count])
        count = count + 5

def check_m_input(entry, mylist):
    '''
    function that checks for input data type(string or integer) , then checks
    again if that input is inside the list.

    parameters : input , list

    returns : True if the input matches the data type and is inside the list.
              False if input doesn't match and is not inside the list.
    '''
    entry_index = range(1,len(mylist)+1)
    if entry.isdigit() and int(entry) in entry_index:
        return True
    elif isinstance(entry, str) and entry.title() in mylist:
        return True
    else:
        return False

def get_city():
    '''
        Enumerate the CITY_DATA dictionary keys and displays them.
        Asks the user to specify city

        returns : name of the city from user input in lower case
    '''
    for num, city_ in enumerate(CITY_DATA.keys(), start=1):
        print(" {}. {}".format(num, city_.capitalize()))
    city = input('Enter the city you would like to view data for : ')
    return city.lower()

def get_month():
    '''
        Enumerate month from the months list and displays months.
        Asks the user to specify month to filter data

        returns:  month from user input
    '''
    print('Enter month(or number next to month, e.g 1 = January) or "all" to apply no month filter')
    for num, month_ in enumerate(months, start=1):
        print(" {}. {}".format(num, month_))
    month = input('Please enter month  : ')
    return month.lower()

def get_day():
    '''
        Enumerate days of week from days list and displays them.
        Asks user to  specify day to filter data

        returns:day from user input
    '''
    print('Enter day of week(or number next to day, e.g 1 = sunday) or "all" to apply no day filter')
    for num, day_ in enumerate(days, start=1):
        print(" {}. {}".format(num, day_))
    day = input('Please enter Day of week : ')
    return day

def day_of_week_format(day):
    '''
        Formats the day from user input.
        returns: formatted day input
    '''
    if day.isdigit():
        return days[int(day)-1]
    else:
        if day.capitalize() in days:
            return day.capitalize()

def format_month(month):
    '''
        Formats the month from user input.
        returns: formatted month input
    '''
    if month.isdigit():
        return int(month)
    else:
        if month.capitalize() in months:
            #return(months.index(month.capitalize())+1)
            return('All' if  month.capitalize() == 'All' else months.index(month.capitalize())+1)

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
        city = get_city()
        if city.lower() not in CITY_DATA.keys():
            print('Oops! you have entered {} as a city. Try Again'.format(city))
        else:
            print('you have selected :',city)
            break
    while True:
        print('Would you like to filter by month, day or both?')
        date_filter = input('Please enter response: ')
        if date_filter.lower() not in input_filter:
            print('Please enter the correct filter')
        else:
            print('you have selected {} filter'.format(date_filter))
            # get user input for day of week (all, monday, tuesday, ... sunday)
            if date_filter.lower() == 'day':
                month = months[-1]
                day = get_day()
                if check_m_input(day, days) != True:
                    print('Oops!,Wrong entry for day. Try Again')
                else:
                    print('you have selected day : ',day)
                    break
            # get user input for month (all, january, february, ... , june)
            elif date_filter.lower() == 'month':
                month = get_month()
                day = days[-1]
                if check_m_input(month, months) != True:
                    print('Oops!,Wrong entry for month. Try Again')
                else:
                    print('you have selected month : ',month)
                    break
            # get user input fot both month and day
            elif date_filter.lower() == 'both':
                month = get_month()
                day = get_day()
                if check_m_input(month, months) != True  and check_m_input(day, days) != True:
                    print('Oops!,Wrong entry for month or day. Try Again')
                else:
                    print('you have selected to filter by both month :{} and day :{} '.format(month, day))
                    break
    return city, format_month(month), day_of_week_format(day)

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
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    if month != 'All':
        df = df[df['month'] == month]
    if day != 'All':
        df = df[df['day_of_week'] == day]
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    print('-'*40)
    start_time = time.time()

    # display the most common month
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    common_month = df['month'].mode()[0]
    print('Most common month: ',months[int(common_month)-1])
    # display the most common day of week
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    common_day_of_week  = df['day_of_week'].mode()[0]
    print('Most common day of week: ',common_day_of_week)
    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print('Most common travel start hour: ', common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    print('-'*40)
    start_time = time.time()

    # display most commonly used start station
    start_station = df['Start Station'].mode()[0]
    trip_count_start = df['Start Station'].value_counts()
    print('Most commonly used start station: {} \tTrip Count: {}'.format(start_station, trip_count_start[0]))
    # display most commonly used end station
    end_station = df['End Station'].mode()[0]
    trip_count_end = df['Start Station'].value_counts()
    print('Most commonly used end station:  {} \tTrip count : {}'.format(end_station, trip_count_end[0]))
    # display most frequent combination of start station and end station trip
    df['start_end_station'] = df['Start Station'] +'-'+df['End Station']
    start_end_station = df['start_end_station'].mode()[0]
    trip_count_startend = df['start_end_station'].value_counts()
    print('Most frequent combination of start and end station trip: {} \tTrip count: {}'.format(start_end_station, trip_count_startend[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    print('-'*40)
    start_time = time.time()

    # display total travel time
    total_t_time = df['Trip Duration'].sum()
    print('Total travel time: ', total_t_time)
    # display mean travel time
    total_t_time = df['Trip Duration'].mean()
    print('Mean travel time: ', total_t_time)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    print('-'*40)
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('User types Count\n',user_types)

    # Display counts of gender
    df['Gender'] = df['Gender'].dropna()
    gender_count = df['Gender'].value_counts()
    print('Gender Count\n', gender_count)

    # Display earliest, most recent, and most common year of Birth
    print('The earliest year of birth: ',df['Birth Year'].min())
    print('The most recent year of birth: ',df['Birth Year'].max())
    print('The most common year of birth', df['Birth Year'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        try:
            city, month, day = get_filters()
            df = load_data(city, month, day)
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            if city != 'washington':
                user_stats(df)
            else:
                print('Please note, No User data for {}.User stats will not be displayed'.format(city))
            raw_data(df)
            restart = input('\nWould you like to restart? Enter yes or no.\n')
            if restart.lower() != 'yes':
                break
        except Exception as e:
            print('Encounted error(s): ', e)

if __name__ == "__main__":
    main()
