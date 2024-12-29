import re
from collections import Counter
import generate
import warnings


warnings.filterwarnings("ignore")


def calculate_deleted_message_percent(df):
    total_messages = len(df)
    deleted_messages = df['message'].isin(['this message was deleted']).sum()

    return (deleted_messages / total_messages) * 100 if total_messages > 0 else 0

def avg_message_length(df):
    return df['message'].str.len().mean()
def most_message_date(df):
    return df['date'].value_counts().idxmax()

def most_used_emojis(df):
    emoji_counter = Counter(''.join(df['emoji']))
    return emoji_counter.most_common(10)

def deleted_message_percent(df):
    total_messages = len(df)
    deleted_messages = df['message'].isin(['this message was deleted']).sum()
    return (deleted_messages / total_messages) * 100

def most_used_words_for_wordcloud(df):
    all_messages = ' '.join(df['message'])
    words = re.findall(r'\b\w+\b', all_messages.lower())
    word_counter = Counter(words)
    return word_counter

def calculate_total_messages(df):
    return len(df)

def analyze_all(full,top_users,data):
    df=full
    deletecopy=df

    deleted_message_keywords = ['this message was deleted']
    df = df[~df['message'].isin(deleted_message_keywords)]

    fullcopy=df
    deletecopy = deletecopy[deletecopy['username'].isin(top_users)]

    graphs = []
    graphs.append(generate.plot_active_hours_per_all_users(deletecopy))
    graphs.append(generate.plot_most_active_month(df, deleted_message_keywords, 'Overall'))
    df=fullcopy
    user_list = top_users.tolist()
    graphs.append(generate.plot_messages_per_hour(df))
    graphs.append(generate.plot_messages_per_day(df))
    graphs.append(generate.plot_avg_message_length(data,top_users))

    graphs.append(generate.plot_message_distribution_by_user_with_other(df))
    graphs.append(generate.plot_deleted_message_percent(data))
    graphs.append(generate.display_word_cloud(data[0]))
    table1 = generate.get_most_used_emojis_for_user(data[0])
    return graphs, table1


def analyze_user(full, top_users, data, selected_user):
    df = full

    deleted_message_keywords = ['this message was deleted']
    df = df[~df['message'].isin(deleted_message_keywords)]
    user_list = top_users.tolist()
    graphs = []
    graphs.append(generate.plot_active_hours_per_user_separate(df, selected_user))
    graphs.append(generate.plot_most_active_month(df, deleted_message_keywords, selected_user))
    graphs.append(generate.display_word_cloud(data[user_list.index(selected_user) + 1]))

    table1 = generate.get_most_used_emojis_for_user(data[user_list.index(selected_user) + 1])
    return graphs, table1


def data_generate(full, top_users):
    df = full
    deletecopy = df
    top_users = df['username'].value_counts().head(10).index

    deleted_message_keywords = ['this message was deleted']
    df = df[~df['message'].isin(deleted_message_keywords)]

    data = []
    data.append({
        'user': 'Overall',
        'avg_message_length': avg_message_length(df),
        'most_message_date': most_message_date(df),
        'most_used_emojis': most_used_emojis(df),
        'most_used_words': most_used_words_for_wordcloud(df),
        'deleted_message_percent': calculate_deleted_message_percent(deletecopy),
        'total_messages': calculate_total_messages(df)
    })
    deletecopy = deletecopy[deletecopy['username'].isin(top_users)]
    for user in top_users:
        user_df = deletecopy[deletecopy['username'] == user]
        filtered_user_df = user_df[~user_df['message'].isin(deleted_message_keywords)]

        data.append({
            'user': user,
            'avg_message_length': avg_message_length(filtered_user_df),
            'most_message_date': most_message_date(filtered_user_df),
            'most_used_emojis': most_used_emojis(filtered_user_df),
            'most_used_words': most_used_words_for_wordcloud(filtered_user_df),
            'deleted_message_percent': calculate_deleted_message_percent(user_df),
            'total_messages': calculate_total_messages(filtered_user_df)
        })
    return data