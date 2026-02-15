import re
import pandas as pd

def preprocessor(data):

    pattern = re.compile(r'(\d{2}/\d{2}/\d{4}, \d{2}:\d{2}) - (.*?): (.*)')
    matches = pattern.findall(data)

    df_list = []

    for match in matches:
        date, user, message = match

        df_list.append({
            'message_date': pd.to_datetime(date, format='%d/%m/%Y, %H:%M'),
            'user': user.strip(),
            'message': message.strip()
        })

    df = pd.DataFrame(df_list)

    # Date columns
    df['only_date'] = df['message_date'].dt.date
    df['year'] = df['message_date'].dt.year
    df['month'] = df['message_date'].dt.month_name()
    df['month_num'] = df['message_date'].dt.month
    df['day'] = df['message_date'].dt.day
    df['day_name'] = df['message_date'].dt.day_name()
    df['hour'] = df['message_date'].dt.hour
    df['minute'] = df['message_date'].dt.minute

    period = []
    for hour in df['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df
