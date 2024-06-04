import pymongo
import streamlit as st # type: ignore
import pandas as pd
from collections import defaultdict
from datetime import datetime, timedelta

@st.cache_resource
def init_connection():
    connection_string = "mongodb+srv://librechat:rq8f05zDHa0MVIFV@cluster0.zldyfvl.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    return pymongo.MongoClient(connection_string)

def get_users_token(db):
    users = db['users']
    transactions = db['transactions']

    # return the list of all users
    users = list(users.find({}, {"name": 1, "email": 1, "lawdepotId": 1, "tokenLimit": 1}))

    # date 28days ago
    start_date = datetime.now()-timedelta(days=28)
    transactions = list(transactions.find({
        "createdAt": {"$gte": start_date}
    }))

    # user token sum
    user_token_sums = defaultdict(lambda: {"tokenUsage": 0})

    for tx in transactions:
        user_id = str(tx['user'])
        token_value = tx['tokenValue'] * -1
        user_token_sums[user_id]["tokenUsage"] += token_value
    
    collection = []

    for user in users:
        user_id = str(user['_id'])
        user_data = {
            "name": user.get('name'),
            "email": user.get('email'),
            "lawdepotId": user.get('lawdepotId'),
            "tokenLimit": user.get('tokenLimit'),
            "total_tokens_used": user_token_sums[user_id]["tokenUsage"]
        }
        collection.append(user_data)
    return pd.DataFrame(collection)

def update_token_limit(db, email, new_limit):
    db['users'].update_one(
         {"email": email},
         {"$set": {"tokenLimit": new_limit}}
         )
    st.success(f"Token limit for {email} updated to {new_limit}")