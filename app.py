import streamlit as st
import os
from azure.cosmos import CosmosClient, exceptions

# Récupération des informations de connexion à Azure Cosmos DB à partir des variables d'environnement
url = os.environ['ACCOUNT_URI']
key = os.environ['ACCOUNT_KEY']
database_name = 'recodatabase'
container_name = 'recoContainer'

# Création des clients Azure Cosmos DB
client = CosmosClient(url, credential=key)
database = client.get_database_client(database_name)
container = database.get_container_client(container_name)

def get_user_data(user_id):
    """
    Récupère les données de l'utilisateur à partir d'Azure Cosmos DB.

    Args:
        user_id (int): ID de l'utilisateur.

    Returns:
        list or None: Les données de l'utilisateur sous forme de liste si elles sont disponibles, sinon None.
    """
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
        st.error("Une erreur s'est produite lors de la requête à la base de données.")
        return None

def app():
    """
    Fonction principale de l'application Streamlit.
    """
    st.title('Recommender System')

    user_id = st.number_input('Entrez votre ID utilisateur', min_value=1, step=1)
    if st.button('Recommande-moi de supers articles !'):
        user_data = get_user_data(user_id)
        if user_data is not None:
            st.subheader(f"Bonjour User {user_id}:")
            st.write("Bienvenue sur notre application de recommandations.")

            # Récupération des recommandations d'articles
            recommendations = [data['recommended_article'] for data in user_data]
            recommendations_list = "\n".join(f"- {article}" for article in recommendations[:5])

            st.subheader("Voici les 5 articles que nous vous recommandons :")
            st.markdown(recommendations_list)

            # Affichage des périodes d'étude des centres d'intérêt et de publication des articles recommandés
            st.subheader("Période d'étude de vos centres d'intérêt :")
            st.write(" - Début : ", user_data[0]['ref_start_date'])
            st.write(" - Fin : ", user_data[0]['ref_end_date'])
            st.subheader("Période de publication des articles recommandés :")
            st.write(" - Début : ", user_data[0]['pred_start_date'])
            st.write(" - Fin : ", user_data[0]['pred_end_date'])
        else:
            st.write("Nous n'avons pas encore de recommandations pour vous, mais nous examinons vos centres d'intérêt et nous allons vous proposer des articles qui pourraient vous intéresser ! Vous recevrez vos recommandations dans quelques minutes :)")

if __name__ == "__main__":
    app()
