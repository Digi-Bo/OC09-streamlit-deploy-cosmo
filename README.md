# OC09-streamlit-deploy-cosmo


Voici une explication détaillée du fonctionnement de `app.py` et son déploiement sur une appliation web azure en utilisant github action.


## Fonctionnement `app.py`
1. Importation des bibliothèques et des modules nécessaires :
   - `streamlit` : bibliothèque pour la création d'applications web interactives.
   - `os` : module pour accéder aux variables d'environnement.
   - `azure.cosmos` : module pour interagir avec Azure Cosmos DB.

2. Récupération des informations de connexion à Azure Cosmos DB à partir des variables d'environnement :
   - `url` : URL de votre instance Azure Cosmos DB.
   - `key` : Clé d'accès à votre instance Azure Cosmos DB.
   - `database_name` : Nom de la base de données dans Azure Cosmos DB.
   - `container_name` : Nom du conteneur (collection) dans Azure Cosmos DB.

3. Création des clients Azure Cosmos DB :
   - `client` : Client pour se connecter à Azure Cosmos DB en utilisant l'URL et la clé.
   - `database` : Client de base de données pour accéder à la base de données spécifiée.
   - `container` : Client de conteneur pour accéder au conteneur spécifié.

4. Définition d'une fonction `get_user_data` pour récupérer les données de l'utilisateur à partir de Azure Cosmos DB :
   - La fonction exécute une requête SQL pour sélectionner les éléments correspondant à l'ID utilisateur spécifié.
   - Si des données sont trouvées, elles sont renvoyées sous forme de liste.
   - Si aucune donnée n'est trouvée ou s'il y a une erreur, `None` est renvoyé.

5. Définition de la fonction principale `app` :
   - La fonction configure le titre de l'application et demande à l'utilisateur d'entrer son ID.
   - Lorsque l'utilisateur clique sur le bouton "Recommande-moi de supers articles !", la fonction `get_user_data` est appelée pour récupérer les données de l'utilisateur.
   - Si des données sont disponibles, elles sont affichées à l'aide de différentes commandes `st`.
   - Les recommandations d'articles sont extraites des données et affichées sous forme de liste à puce.
   - Les périodes d'étude des centres d'intérêt et de publication des articles recommandés sont également affichées.
   - Si aucune donnée n'est disponible, un message indiquant que les recommandations seront fournies ultérieurement est affiché.

6. Bloc d'exécution principal :
   - La fonction `app` est appelée si le script est exécuté directement.

En résumé, le code définit une application Streamlit qui permet aux utilisateurs de saisir leur ID et d'obtenir des recommandations d'articles à partir d'une base de données Azure Cosmos DB. Les informations sont récupérées à partir de la base de données, et les résultats sont affichés dans l'application Streamlit.



# Déploiement avec github action 

- Le processus de Git Actions est déclenché lorsqu'il y a un push sur la branche "main" du référentiel. Il se compose des étapes définies dans le fichier yml :
- L'objectif est ici de déployer automatiquement sur l'application web azure "resultreco"  https://resultreco.azurewebsites.net/
- Pour que le déploiement s'effectue, il faut aussi paramètrer les secrêts sur github
- Une fois que toutes ces étapes sont exécutées avec succès, l'application Streamlit est déployée sur le service Azure App Service.

## Sur github, créer un repo 


## En local, sur VS code, intialiser le dépôt git et le connecter au repo github


## En local, sur VS code, créer un Dockerfile qui va permettre créer une image Docker

Le Dockerfile est un fichier texte qui contient les instructions pour créer une image Docker. Lorsque vous exécutez la commande `docker build` en spécifiant le chemin vers le Dockerfile, Docker utilise ces instructions pour créer une image Docker prête à être exécutée.

Expliquons chaque instruction du Dockerfile et comment elle s'intègre dans le processus de déploiement avec GitHub Actions :

1. `FROM python:3.9-slim-buster`
   - Cette instruction indique à Docker d'utiliser une image de base Python 3.9 basée sur l'image `slim-buster`. Cette image fournit un environnement minimal avec Python préinstallé.

2. `RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc build-essential libgomp1 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*`
   - Cette instruction met à jour les packages du système d'exploitation de l'image et installe les packages supplémentaires nécessaires, tels que `gcc`, `build-essential` et `libgomp1`. Cela garantit que les dépendances requises pour votre application sont présentes dans l'image Docker.

3. `WORKDIR /app`
   - Cette instruction définit le répertoire de travail à `/app`. C'est l'emplacement dans l'image où les fichiers de votre application seront copiés et où les commandes ultérieures seront exécutées.

4. `COPY requirements.txt ./`
   - Cette instruction copie le fichier `requirements.txt` de votre répertoire local dans le répertoire de travail de l'image Docker. Ce fichier contient la liste des dépendances Python requises par votre application.

5. `RUN pip install --no-cache-dir -r requirements.txt`
   - Cette instruction exécute la commande `pip install` pour installer les dépendances Python spécifiées dans le fichier `requirements.txt`. Les dépendances sont installées dans l'image Docker, ce qui garantit que votre application a accès à ces dépendances lors de son exécution.

6. `COPY . .`
   - Cette instruction copie tous les fichiers et répertoires du répertoire local (où se trouve le Dockerfile) dans le répertoire de travail de l'image Docker. Cela inclut votre fichier `app.py` et tout autre fichier nécessaire à l'exécution de votre application.

7. `EXPOSE 8501`
   - Cette instruction spécifie le port sur lequel votre application écoute. Dans ce cas, le port 8501 est exposé pour l'application Streamlit.

8. `CMD ["streamlit", "run", "app.py"]`
   - Cette instruction définit la commande par défaut à exécuter lorsque l'image Docker est lancée. Dans ce cas, il exécute la commande `streamlit run app.py` pour démarrer votre application Streamlit.

Lorsque vous exécutez la commande `docker build` avec le chemin vers votre Dockerfile, Docker construit une image Docker en suivant les instructions du Dockerfile. Cette image est ensuite utilisée pour exécuter votre application Streamlit dans un conteneur.

Dans le processus de déploiement avec GitHub Actions, le Dockerfile est utilisé pour créer l'image Docker de votre application. L'étape `Build and push Docker image` dans votre fichier `deploy.yml` utilise l'action `docker/build-push-action` pour construire l'image Docker en spécifiant le chemin vers le Dockerfile et d'autres options nécess


## En local, sur VS code, créer le fichier de déploiement (ici deploy.yml)
Dans le dossier `github/workflows`, vous trouverez le fichier `deploy.yml` qui définit le flux de travail (workflow) de déploiement de votre application Streamlit sur Azure à l'aide de Git Actions.

Le contenu du fichier `deploy.yml` est le suivant :

```yaml
name: Deploy Streamlit App to Azure

on:
  push:
    branches:
      - main

jobs:
  build_and_deploy:
    runs-on: ubuntu-latest

    steps:
      ...
```

Ce fichier est écrit en format YAML, qui est un langage de sérialisation de données. Il définit un workflow nommé "Deploy Streamlit App to Azure" qui sera déclenché lorsqu'un push est effectué sur la branche "main" du référentiel.

La section `jobs` définit une ou plusieurs tâches à exécuter dans le flux de travail. Dans ce cas, il y a une seule tâche appelée "build_and_deploy" qui s'exécutera sur un système d'exploitation Ubuntu (version latest). Les étapes de cette tâche sont définies à l'intérieur de la section `steps`.

Les étapes du workflow sont les suivantes :

1. **Checkout repository**: Cette étape utilise l'action `actions/checkout` pour récupérer le contenu du référentiel Git dans l'environnement d'exécution. Cela permet d'accéder aux fichiers et au code source de votre application.

2. **Login to Azure Container Registry**: Cette étape utilise l'action `azure/docker-login` pour vous connecter au registre de conteneurs Azure. Vous devez spécifier le nom du serveur de connexion, ainsi que le nom d'utilisateur et le mot de passe associés. Les informations d'identification sont récupérées à partir des secrets configurés dans les paramètres de votre référentiel Git.

3. **Build and push Docker image**: Cette étape utilise l'action `docker/build-push-action` pour construire l'image Docker de votre application. Vous spécifiez le contexte de construction (le répertoire actuel), et l'action se charge de construire l'image et de la pousser vers le registre de conteneurs Azure. L'image est taguée avec l'étiquette "latest".

4. **Deploy to Azure App Service**: Cette étape utilise l'action `azure/webapps-deploy` pour déployer l'image Docker sur le service Azure App Service. Vous devez spécifier le nom de l'application Azure App Service ainsi que le profil de publication. L'action se charge de déployer l'image sur le service Azure App Service, mettant ainsi votre application Streamlit en ligne.

Le flux de travail est configuré pour s'exécuter sur une machine virtuelle Ubuntu, mais vous pouvez également choisir une autre version d'environnement selon vos besoins.

Ce fichier `deploy.yml` doit être placé dans le dossier `github/workflows` de votre référentiel Git pour que Git Actions puisse le détecter et l'exécuter automatiquement lorsqu'un push est effectué sur la branche "main".


# Créer les bons secrêts sur github pour le déploiement


Voici les étapes pour créer un secret avec le profil de publication de votre application Web:

1. Connectez-vous au [portail Azure](https://portal.azure.com/).
2. Accédez à votre application Web (Web App) que vous avez créée précédemment.
3. Dans le menu de gauche, recherchez la section "Settings" (Paramètres) et cliquez sur "Deployment Center" (Centre de déploiement).
4. Dans le Centre de déploiement, choisissez, au niveau de **source** , il faut choisir "GitHub action" comme source de code, puis cliquez sur "Get Publish Profile" (Gérer le profil de publication) en haut de la page. Un fichier XML sera téléchargé sur votre ordinateur.
5. Ouvrez le fichier XML téléchargé avec un éditeur de texte (comme Notepad ou Visual Studio Code) et copiez son contenu.
6. Allez dans votre dépôt GitHub, cliquez sur l'onglet "Settings" (Paramètres), puis sur "Secrets" dans le menu de gauche.
7. Cliquez sur "New repository secret" (Nouveau secret de dépôt) en haut à droite.
8. Entrez un nom pour le secret, par exemple `WEB_APP_PUBLISH_PROFILE`, et collez le contenu du fichier XML dans la zone "Value" (Valeur). Cliquez sur "Add secret" (Ajouter un secret).

Maintenant que vous avez créé le secret `WEB_APP_PUBLISH_PROFILE`, vous pouvez le consommer dans votre workflow GitHub. Dans votre fichier `.github/workflows/workflow.yml`, mettez à jour l'étape "Deploy to Azure App Service" pour utiliser le nouveau secret:

```yaml
    - name: Deploy to Azure App Service
      uses: azure/webapps-deploy@v2
      with:
        app-name: hybridrec
        publish-profile: ${{ secrets.WEB_APP_PUBLISH_PROFILE }}
        images: OC09Recommender.azurecr.io/streamlit_app:latest
```

Après avoir modifié votre fichier de workflow, effectuez une nouvelle push sur la branche `main`. Le déploiement s'effectue normalement sans problème.

