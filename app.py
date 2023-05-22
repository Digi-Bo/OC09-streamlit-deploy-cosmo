import streamlit as st
import os
from azure.cosmos import CosmosClient, exceptions

url = os.environ['ACCOUNT_URI']
key = os.environ['ACCOUNT_KEY']
database_name = 'recodatabase'
container_name = 'recoContainer'

client = CosmosClient(url, credential=key)
database = client.get_database_client(database_name)
container = database.get_container_client(container_name)

def get_user_data(user_id):
    try:
        user_data = list(container.query_items(
            query=f"SELECT * FROM c WHERE c.user_id={user_id}",
            enable_cross_partition_query=True
        ))

        if user_data:
            return user_data
        else:
            return None
    except exceptions.CosmosHttpResponseError:
        st.error("An error occurred while querying the database.")
        return None

def app():
    st.title('Recommender System')

    user_id = st.number_input('Enter User ID', min_value=1, step=1)
    if st.button('Get Recommendations'):
        user_data = get_user_data(user_id)
        if user_data is not None:
            for data in user_data:
                st.subheader(f"Recommendations for User {user_id}:")
                st.write("Reference Start Date: ", data['ref_start_date'])
                st.write("Reference End Date: ", data['ref_end_date'])
                st.write("Prediction Start Date: ", data['pred_start_date'])
                st.write("Prediction End Date: ", data['pred_end_date'])
                st.write("Recommended Articles: ", data['recommended_article'])
        else:
            st.write("We don't have any recommendations for you at the moment, but we'll examine your interests and find articles that you might find interesting! You'll receive your recommendations in a few minutes :)")

if __name__ == "__main__":
    app()
