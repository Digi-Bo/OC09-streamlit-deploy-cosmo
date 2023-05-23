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
            st.subheader(f"Bonjour User {user_id}:")
            st.write("Voici 5 articles que nous vous recommandons :")
            recommendations = user_data[0]['recommended_article']
            st.write(recommendations[:5])
            st.write("Période d'étude de vos centres d'intérêt :")
            st.write(" - Reference Start Date: ", user_data[0]['ref_start_date'])
            st.write(" - Reference End Date: ", user_data[0]['ref_end_date'])
            st.write("Période de publication des articles recommandés :")
            st.write(" - Prediction Start Date: ", user_data[0]['pred_start_date'])
            st.write(" - Prediction End Date: ", user_data[0]['pred_end_date'])
        else:
            st.write("Nous n'avons pas encore de recommandations pour vous, mais nous examinerons vos centres d'intérêt et trouverons des articles qui pourraient vous intéresser ! Vous recevrez vos recommandations dans quelques minutes :)")

if __name__ == "__main__":
    app()
