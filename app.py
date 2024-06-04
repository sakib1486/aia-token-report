import streamlit as st  # type: ignore
from collections import defaultdict
from dbOps import init_connection, get_users_token, update_token_limit
from applyFilters import apply_filters

def main():
    st.set_page_config(layout="wide")
    st.title('Token Usage Reporting - AI Assistant')
    # inti connection, and connect to the intended DB
    client = init_connection()
    db = client['ai-assistant-testing']
    
    ### FILTERS
    
    col1, col2 = st.columns(2)
    # Filter input for token usage
    filter_token_usage = col1.text_input("Filter users by token usage (>=)", 0)
    # Filter input for email
    filter_email = col2.text_input("Search a user by email")
    # adding spaces
    st.markdown("")
    st.markdown("")
    st.markdown("")

    ### Display the DataFrame
    # get token usage based on users
    filtered_users_info = apply_filters(get_users_token(db), filter_token_usage, filter_email)

    if not filtered_users_info.empty:
        cols = st.columns([2.5,2.5,2,1,0.8,1])
        cols[0].write("Name")
        cols[1].write("Email Address")
        cols[2].write("LawDepot ID")
        cols[3].write("Token Usage")
        cols[4].write("Token Limit")
        cols[5].write("Action")

        for index, user in filtered_users_info.iterrows():
            with st.form(key=f"form_{index}"):
                cols = st.columns([2.5,2.5,2,1,0.8,1])
                cols[0].write(user['name'])
                cols[1].write(user['email'])
                cols[2].write(user['lawdepotId'])
                cols[3].write(user['total_tokens_used'])
                new_limit = cols[4].text_input(label="",value=str(user['tokenLimit']), label_visibility="collapsed")
                submit_button = cols[5].form_submit_button(label='Set New Limit')

                # Write logic to update the new limit in the MongoDB
                if submit_button:
                    st.write(f"New limit for {user['name']} ({user['email']}): {new_limit}")
                    # Update the token limit in MongoDB
                    update_token_limit(db, user['email'], int(new_limit))
                    
                    # Refresh the data for UI
                    filtered_users_info = apply_filters(get_users_token(db), filter_token_usage, filter_email)
                    st.experimental_rerun()  # Rerun the script to update the UI
    else:
        st.write("No users found")

if __name__=="__main__":
    main()