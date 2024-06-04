import pandas as pd

def apply_filters(users_info, filter_token_usage, filter_email):
    filtered_users = users_info
    if filter_token_usage:
        filtered_users = filtered_users[filtered_users['total_tokens_used'] >= int(filter_token_usage)]
    if filter_email:
        filtered_users = filtered_users[filtered_users['email'].str.contains(filter_email, case=False, na=False)]
    return filtered_users