
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud, STOPWORDS
import warnings

warnings.filterwarnings("ignore")


def plot_messages_per_hour(full):
    df=full
    df['hour'] = df['date_time'].dt.hour
    # Count messages per hour
    hour_counts = df['hour'].value_counts().sort_index()

    # Create the bar chart
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(hour_counts.index, hour_counts.values, color='seagreen')
    ax.set_title('Most Active Hour')
    ax.set_xlabel('Hour of the Day')
    ax.set_ylabel('Message Count')
    ax.set_xticks(range(0, 24))
    fig.tight_layout()

    return fig


def plot_messages_per_day(full):
    df = full
    df['day'] = df['date_time'].dt.day_name()  # Ensure 'day' is the full name of the day
    day_counts = df['day'].value_counts().sort_index()
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day_counts = day_counts.reindex(day_order)

    # Create the bar chart
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(day_counts.index, day_counts.values, color='coral')
    ax.set_title('Most Active Day')
    ax.set_xlabel('Day of the Week')
    ax.set_ylabel('Message Count')
    ax.set_xticks(range(0, 7))
    ax.set_xticklabels(day_counts.index, rotation=45)
    fig.tight_layout()

    return fig

def plot_avg_message_length(data,users):
    users = [entry['user'] for entry in data]
    avg_lengths = [entry['avg_message_length'] for entry in data]

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(users, avg_lengths, color='skyblue')
    ax.set_title('Average Message Length (Overall + Users)')
    ax.set_xlabel('User')
    ax.set_ylabel('Average Message Length')
    ax.set_xticklabels(users, rotation=45)
    fig.tight_layout()
    return fig


def plot_active_hours_per_all_users(full):
    df=full
    df['hour'] = df['date_time'].dt.hour

    hour_user_counts = df.groupby(['hour', 'username']).size().unstack(fill_value=0)
    fig, ax = plt.subplots(figsize=(14, 7))
    hour_user_counts.plot(kind='line', marker='o', ax=ax, linewidth=2)
    ax.set_title('Active Hours for All Users', fontsize=16)
    ax.set_xlabel('Hour of the Day', fontsize=12)
    ax.set_ylabel('Messages Sent', fontsize=12)
    ax.set_xticks(range(0, 24))
    ax.set_xticklabels(range(0, 24), rotation=45)
    ax.legend(title='Users', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)
    fig.tight_layout()
    return fig


def plot_message_distribution_by_user_with_other(df):
    user_message_counts = df['username'].value_counts()

    top_users = user_message_counts.head(10)
    other_count = user_message_counts[10:].sum()

    if other_count > 0:
        top_users['Other'] = other_count

    fig, ax = plt.subplots(figsize=(8, 8))
    top_users.plot(kind='pie', autopct='%1.1f%%', colors=sns.color_palette("Set2", len(top_users)),
                   startangle=90, legend=False, wedgeprops={'edgecolor': 'black'}, ax=ax)

    ax.set_title('Message Distribution by Users', fontsize=16)
    ax.set_ylabel('')
    fig.tight_layout()
    return fig

def plot_deleted_message_percent(data):
    users = [entry['user'] for entry in data]
    deleted_percents = [entry['deleted_message_percent'] for entry in data]

    if any(pd.isna(deleted_percents)):
        print("Warning: Some deleted message percentages are missing.")

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(users, deleted_percents, color='salmon')
    ax.set_title('Deleted Message Percentage (Overall + Users)', fontsize=16)
    ax.set_xlabel('User', fontsize=12)
    ax.set_ylabel('Deleted Message Percentage', fontsize=12)
    ax.set_xticklabels(users, rotation=45)
    fig.tight_layout()
    return fig

def display_word_cloud(data):
    user = data['user']
    word_counts = data['most_used_words']

    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(word_counts)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.set_title(f'Word Cloud - {user}')
    ax.axis('off')
    fig.tight_layout()
    return fig


def plot_active_hours_per_user_separate(full, user):
    df=full
    # Extract the hour from the date_time column
    df['hour'] = df['date_time'].dt.hour
    user_df = df[df['username'] == user]
    user_active_hours = user_df.groupby('hour').size()

    fig, ax = plt.subplots(figsize=(10, 6))
    user_active_hours.plot(kind='line', marker='o', color='skyblue', linewidth=2, ax=ax)


    ax.set_title(f'Active Hours for {user}', fontsize=16)
    ax.set_xlabel('Hour of the Day', fontsize=12)
    ax.set_ylabel('Messages Sent', fontsize=12)
    ax.set_xticks(range(0, 24))
    ax.set_xticklabels(range(0, 24), rotation=45)
    fig.tight_layout()
    return fig


def plot_most_active_month(df, deleted_message_keywords,user):
    copy=df
    def sort_months(month_counts):
        months_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        sorted_months = {month: month_counts.get(month, 0) for month in months_order}
        return sorted_months


    if user == 'Overall':
        month_counts = df['month'].value_counts().to_dict()
    else:
        user_df = copy[copy['username'] == user]
        filtered_user_df = user_df[~user_df['message'].isin(deleted_message_keywords)]
        month_counts = filtered_user_df['month'].value_counts().to_dict()

    sorted_month_counts = sort_months(month_counts)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(sorted_month_counts.keys(), sorted_month_counts.values(), color='purple')
    ax.set_title(f'Most Active Month - {user}')
    ax.set_xlabel('Month')
    ax.set_ylabel('Message Count')
    ax.set_xticklabels(sorted_month_counts.keys(), rotation=45)
    fig.tight_layout()
    return fig


def get_most_used_emojis_for_user(data):
    emoji_counts = data['most_used_emojis']
    emoji_df = pd.DataFrame(emoji_counts, columns=['Emoji', 'Count'])
    return emoji_df


