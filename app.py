import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("WhatsApp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")

if uploaded_file is not None:

    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")

    df = preprocessor.preprocessor(data)

    # User list
    user_list = df['user'].unique().tolist()
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Select User", user_list)

    if st.sidebar.button("Show Analysis"):

        filtered_df = df.copy()

        if selected_user != "Overall":
            filtered_df = filtered_df[filtered_df['user'] == selected_user]

        # ================= FETCH STATS =================
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(
            selected_user, filtered_df
        )

        st.title("Top Statistics")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total Messages", num_messages)

        with col2:
            st.metric("Total Words", words)

        with col3:
            st.metric("Media Shared", num_media_messages)

        with col4:
            st.metric("Links Shared", num_links)

        # ================= MONTHLY TIMELINE =================
        st.title("Monthly Timeline")

        timeline = helper.monthly_timeline(selected_user, filtered_df)

        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['num_messages'])
        plt.xticks(rotation='vertical')

        st.pyplot(fig)

        # ================= DAILY TIMELINE =================
        st.title("Daily Timeline")

        daily_timeline = helper.daily_timeline(selected_user, filtered_df)

        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['num_messages'],color='black')
        plt.xticks(rotation='vertical')

        st.pyplot(fig)

        # ================= ACTIVITY MAP =================
        st.title("Activity Map")

        col1, col2 = st.columns(2)

        with col1:
            st.header("Most Busy Day")
            busy_day = helper.week_activity_map(selected_user, filtered_df)

            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values,color='magenta')
            plt.xticks(rotation='vertical')

            st.pyplot(fig)

        with col2:
            st.header("Most Busy Month")
            busy_month = helper.month_activity_map(selected_user, filtered_df)

            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values,color='orange')
            plt.xticks(rotation='vertical')

            st.pyplot(fig)

        # ================= HEATMAP =================
        st.title("Weekly Activity Map")

        user_heatmap = helper.activity_heatmap(selected_user, filtered_df)

        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(user_heatmap, ax=ax)

        st.pyplot(fig)

        # ================= MOST BUSY USERS =================
        if selected_user == "Overall":

            st.title("Most Busy Users")

            x, new_df = helper.most_busy_users(df)

            col1, col2 = st.columns(2)

            with col1:
                fig, ax = plt.subplots()
                ax.bar(x.index, x.values,color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)

        # ================= WORDCLOUD =================
        st.title("WordCloud")

        df_wc = helper.create_wordcloud(selected_user, filtered_df)

        if df_wc is not None:
            fig, ax = plt.subplots()
            ax.imshow(df_wc)
            ax.axis("off")
            st.pyplot(fig)
        else:
            st.write("No text data available to generate WordCloud.")

        # ================= MOST COMMON WORDS =================
        st.title("Most Common Words")

        most_common_df = helper.most_common_words(selected_user, filtered_df)

        if not most_common_df.empty:
            fig, ax = plt.subplots()
            ax.bar(most_common_df['word'], most_common_df['count'])
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        else:
            st.write("No common words found.")

        # ================= EMOJI ANALYSIS =================
        # ================= EMOJI ANALYSIS =================
        st.title("Emoji Analysis")

        emoji_df = helper.emoji_helper(selected_user, filtered_df)

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)

        with col2:
            if not emoji_df.empty:
                fig, ax = plt.subplots(figsize=(6, 6))
                top_emojis = emoji_df.head(10)

                ax.pie(
                    top_emojis['count'],
                    labels=top_emojis['emoji'],
                    autopct="%0.1f%%"
                )

                st.pyplot(fig)
            else:
                st.write("No emoji data available.")
