import re
import pandas as pd
import emoji
from whatstk import WhatsAppChat

def clean_text(text):
    text = text.replace('<Media omitted>', '').replace('\n', ' ').strip()
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'[0-9]+','', text)
    text = re.sub(r'\s+',' ', text)
    text = re.sub(r'[^\w\s]|_', '', text)
    text = re.sub(r'([a-zA-Z])\1\1','\\1', text)
    return text.lower()

def preprocess(file,key):
    df = WhatsAppChat.from_source(
        filepath=file,
        hformat='%d/%m/%y, %I:%M %p - %name:'
    ).df

    print("Columns in parsed DataFrame:", df.columns)

    if 'date' in df.columns:
        df.rename(columns={'date': 'date_time'}, inplace=True)

    if 'date_time' not in df.columns:
        raise ValueError("The datetime column is missing. Ensure the hformat matches the df format.")

    df['date_time'] = pd.to_datetime(df['date_time'], errors='coerce')
    df = df.dropna(subset=['date_time'])  # Remove rows with invalid dates
    df['day'] = df['date_time'].dt.strftime('%a')
    df['month'] = df['date_time'].dt.strftime('%b')
    df['date'] = df['date_time'].apply(lambda x: x.date())
    df['emoji'] = df['message'].apply(lambda x: ''.join(c for c in x if c in emoji.EMOJI_DATA))

    # Clean text messages
    df['clean_msg'] = df['message'].apply(clean_text)
    df = df.drop(columns=['message']).rename(columns={'clean_msg': 'message'})
    return df