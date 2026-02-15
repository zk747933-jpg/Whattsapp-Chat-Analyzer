from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

extract = URLExtract()

# ================= FETCH STATS =================
def fetch_stats(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    num_message = df.shape[0]

    words = []
    for message in df['message']:
        words.extend(str(message).split())

    num_media_messages = df[df['message'] == '<Media omitted>'].shape[0]

    links = []
    for message in df['message']:
        links.extend(extract.find_urls(str(message)))

    return num_message, len(words), num_media_messages, len(links)


# ================= MOST BUSY USERS =================
def most_busy_users(df):
    # top 5 users by message count
    top_users = df['user'].value_counts().head()

    # percentage of messages
    df_percent = (
        (df['user'].value_counts() / df.shape[0] * 100)
        .head()
        .reset_index()
        .rename(columns={'index': 'name', 'user': 'name/no.'})
    )

    # add count explicitly
    df_percent['count'] = top_users.values

    return top_users, df_percent



# ================= WORDCLOUD =================
def create_wordcloud(selected_user, df):

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['message'] != '<Media omitted>']

    words = []

    for message in temp['message']:
        for word in str(message).lower().split():
            if word not in stop_words:
                words.append(word)

    if len(words) == 0:
        return None  # important

    text = " ".join(words)

    wc = WordCloud(
        width=500,
        height=500,
        min_font_size=10,
        background_color='white'
    )

    df_wc = wc.generate(text)

    return df_wc


    def remove_stop_words(message):
        y = []
        for word in str(message).lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    temp['message'] = temp['message'].apply(remove_stop_words)

    wc = WordCloud(
        width=500,
        height=500,
        min_font_size=10,
        background_color='white'
    )

    df_wc = wc.generate(temp['message'].str.cat(sep=" "))

    return df_wc


# ================= MOST COMMON WORDS =================
def most_common_words(selected_user, df):

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['message'] != '<Media omitted>']

    words = []

    for message in temp['message']:
        for word in str(message).lower().split():
            if word not in stop_words:
                words.append(word)

    if len(words) == 0:
        return pd.DataFrame(columns=['word', 'count'])

    most_common = Counter(words).most_common(20)
    most_common_df = pd.DataFrame(most_common, columns=['word', 'count'])

    return most_common_df


# ================= EMOJI =================
def emoji_helper(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []

    for message in df['message']:
        emojis.extend([c for c in str(message) if c in emoji.EMOJI_DATA])

    if len(emojis) == 0:
        return pd.DataFrame(columns=['emoji', 'count'])

    emoji_counts = Counter(emojis).most_common()
    emoji_df = pd.DataFrame(emoji_counts, columns=['emoji', 'count'])

    return emoji_df



def monthly_timeline(selected_user, df):

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    timeline['time'] = timeline['month'] + "-" + timeline['year'].astype(str)
    timeline.rename(columns={'message': 'num_messages'}, inplace=True)

    return timeline


def daily_timeline(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()
    daily_timeline.rename(columns={'message': 'num_messages'}, inplace=True)

    return daily_timeline


def week_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df['day_name'].value_counts()


def month_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df['month'].value_counts()


def activity_heatmap(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(
        index='day_name',
        columns='period',
        values='message',
        aggfunc='count'
    ).fillna(0)

    return user_heatmap


