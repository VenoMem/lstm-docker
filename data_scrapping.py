from datetime import datetime, timedelta, date
import time
import http.client
import pandas as pd
import os
import numpy as np



def get_weather_data(start_date, end_date, conn, headers):
    conn.request("GET", f"/history?startDateTime={start_date.strftime('%Y-%m-%d')}T00%3A00%3A00&aggregateHours=1&location=Washington%2CDC%2CUSA&endDateTime={end_date.strftime('%Y-%m-%d')}T00%3A00%3A00&unitGroup=us&dayStartTime=00%3A00%3A00&contentType=csv&dayEndTime=23%3A00%3A00&shortColumnNames=0", headers=headers)
    res = conn.getresponse()
    data = res.read()
    return data.decode("utf-8").split('\n')[1:-1]



def creata_weather_dataframe(start_date):

    conn = http.client.HTTPSConnection("visual-crossing-weather.p.rapidapi.com")

    headers = {
    'X-RapidAPI-Key': "f73756468dmsh2c6cd8ccf464c83p1ab98fjsndefebc2a8d1b",
    'X-RapidAPI-Host': "visual-crossing-weather.p.rapidapi.com"
    }

    end_date = datetime.now()

    date_time = []
    temperature = []

    current_date = start_date
    while current_date < end_date:
        # Przesuń bieżącą datę o 15 dni do przodu
        current_date += timedelta(days=15)

        text = get_weather_data(start_date, current_date, conn, headers)

        for line in text:
                words = line.split(',')
                tmp_date = datetime.strptime(words[3][1:-1], "%m/%d/%Y %H:%M:%S")
                date_time.append(tmp_date)
                temperature.append(float(words[6]))

        start_date = current_date
        time.sleep(2)
   
    return pd.DataFrame(data = {'DATE_TIME': date_time, 'TEMPERATURE': temperature})



def set_index_as_datetime(dataframe):
    dataframe['DATE_TIME'] = pd.to_datetime(dataframe['DATE_TIME'])
    dataframe.index = pd.to_datetime(dataframe['DATE_TIME'], format='%Y-%m-%d %H:%M:%S')
    dataframe = dataframe.iloc[:, [1]]
    return dataframe



def create_working_dataframe():
    # Catalogue path
    dir = './'

    # File name
    file_name = 'dane.csv'

    # File path
    file_path = os.path.join(dir, file_name)

    # Existence of a file
    if os.path.exists(file_path):
        df_temp_from_file = pd.read_csv(file_path)
        df_temp_from_file = set_index_as_datetime(df_temp_from_file)
    
        last_entry = df_temp_from_file.index[-1]
        year, month, day = last_entry.year, last_entry.month, last_entry.day
        df_new_temp= creata_weather_dataframe(datetime(year, month, day))

        df_new_temp = set_index_as_datetime(df_new_temp)

        # Tworzenie maski logicznej dla drugiego DataFrame
        mask = ~df_new_temp.index.isin(df_temp_from_file.index)

        # Filtrowanie drugiego DataFrame na podstawie maski
        new_entries = df_new_temp[mask]

        # Doklejanie tylko wybranych wierszy drugiego DataFrame do pierwszego DataFrame
        df = pd.concat([df_temp_from_file, new_entries])

        
    else:
        print(f"Plik {file_path} nie istnieje w katalogu.")

        df = creata_weather_dataframe(datetime(2015, 1, 1))
        df = set_index_as_datetime(df)
        
    df.to_csv('./dane.csv', mode = 'w')
    return df