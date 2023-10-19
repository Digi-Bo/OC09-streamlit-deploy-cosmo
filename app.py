import streamlit as st
import os
import pandas as pd
import plotly.graph_objects as go

from azure.cosmos import CosmosClient, exceptions

# Récupération des informations de connexion à Azure Cosmos DB à partir des variables d'environnement
url = os.environ.get('ACCOUNT_URI')
key = os.environ.get('ACCOUNT_KEY')
database_name = 'recodatabase'
container_name = 'recoContainer'

if not url or not key:
    st.error("Les variables d'environnement pour Azure Cosmos DB ne sont pas définies.")

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

        return user_data if user_data else None
    except exceptions.CosmosHttpResponseError:
        st.error("Une erreur s'est produite lors de la requête à la base de données.")
        return None


def display_dashboard():
    """
    Affiche le tableau de bord avec les données des algorithmes.
    """
    try:
        df_results = pd.read_csv('Resultats_oc-10.csv')

        # Filtrer le dataframe pour la "strategie 2"
        df_strategie2 = df_results[df_results['Stratégie'] == "Stratégie 1"]

        # Filtrer le dataframe filtré en fonction du type d'algorithme
        df_implemente = df_strategie2[df_strategie2["Type d'algorithme"] == "implémenté"]
        df_default = df_strategie2[df_strategie2["Type d'algorithme"] == "Par défaut"]

        # Tri des dataframes par 'test_rmse'
        df_implemente = df_implemente.sort_values(by='test_rmse', ascending=False)
        df_default = df_default.sort_values(by='test_rmse', ascending=False)

        # Créer le graphique
        fig = go.Figure()

        # Ajouter les barres pour les algorithmes "implémenté"
        fig.add_trace(go.Bar(
            x=df_implemente['Algorithm'],
            y=df_implemente['test_rmse'],
            name='Implémenté',
            marker_color='indianred'
        ))

        # Ajouter les barres pour les algorithmes "Par défaut"
        fig.add_trace(go.Bar(
            x=df_default['Algorithm'],
            y=df_default['test_rmse'],
            name='Par défaut',
            marker_color='lightsalmon'
        ))

        # Mettre à jour le layout
        fig.update_layout(
            title="Comparaison des RMSE des algorithmes pour la stratégie 1",
            xaxis_title="Algorithmes",
            yaxis_title="Test RMSE",
            barmode='group'
        )

        st.plotly_chart(fig)
    except Exception as e:
        st.error(f"Une erreur s'est produite lors de l'affichage du tableau de bord: {e}")


def app():
    """
    Fonction principale de l'application Streamlit.
    """
    st.title('Recommender System')

    user_id = st.number_input('Entrez votre ID utilisateur', min_value=1, step=1)
    if st.button('Recommande-moi de supers articles !'):
        user_data = get_user_data(user_id)
        if user_data:
            st.subheader(f"Bonjour User {user_id}:")
            st.write("Bienvenue sur notre application de recommandations.")

            # Récupération des recommandations d'articles
            recommendations = [data['recommended_article'] for data in user_data]
            recommendations_list = "\n".join(f"- {article}" for article in recommendations[:5])

            st.subheader("Voici les 5 articles que nous vous recommandons :")
            st.markdown(recommendations_list)

            # Affichage des périodes
            st.subheader("Période d'étude de vos centres d'intérêt :")
            st.write(" - Début : ", user_data[0]['ref_start_date'])
            st.write(" - Fin : ", user_data[0]['ref_end_date'])
            st.subheader("Période de publication des articles recommandés :")
            st.write(" - Début : ", user_data[0]['pred_start_date'])
            st.write(" - Fin : ", user_data[0]['pred_end_date'])
        else:
            st.write("Nous n'avons pas encore de recommandations pour vous, mais nous examinons vos centres d'intérêt...")

        # Dashboard button
        if st.button("Découvrir le dashboard"):
            st.session_state.dashboard_view = True

    if st.session_state.get('dashboard_view', False):
        display_dashboard()


if __name__ == "__main__":
    app()
