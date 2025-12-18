AeroStream souhaite développer un système intelligent capable de classifier automatiquement les avis clients relatifs aux services des compagnies aériennes. L’objectif principal est d’analyser le niveau de satisfaction des clients à partir des données textuelles issues des avis utilisateurs.

Objectifs
Développer un système de classification automatique des avis clients en temps réel, Le système devra permettre de:

Collecter et prétraiter les avis clients,
Analyser automatiquement le sentiment et la satisfaction,
Générer des indicateurs de performance par compagnie aérienne,
Visualiser les résultats via un tableau de bord interactif.
Partie Batch
Chargement des données : Importer le dataset US Airlines depuis Hugging Face en utilisant le nom “7Xan7der7/usairlinesentiment”.
Analyse exploratoire des données (EDA) : Étudier la répartition des classes, les distributions et les statistiques principales.
Nettoyage des données : Suppression des doublons, Gestion des valeurs manquantes, Nettoyage du texte (suppression des URLs, mentions, ponctuation, caractères spéciaux).
Normalisation des données : Conversion du texte en minuscules pour homogénéiser les données.
Génération des embeddings : Utilisation de Sentence Transformers, avec le modèle “paraphrase-multilingual-MiniLM-L12-v2” ou un autre modèle disponible sur Hugging Face.
Sauvegarde des métadonnées : Stockage du label et de l’identifiant de chaque avis.
Stockage des embeddings : Enregistrement des vecteurs et de leurs métadonnées dans la base vectorielle ChromaDB : Une collection pour les données d’entraînement, Une collection pour les données de test.
Entraînement des modèles : Récupération des embeddings pour entraîner les modèles de classification.
Évaluation et sauvegarde du modèle : Évaluation des performances des modèles et conservation du meilleur modèle pour la prédiction future.
Développer une API REST pour le déploiement du modèle
Partie Streaming
Récupération des données en micro-batch : Collecte des avis via l’API.
Préparation des données : Nettoyage et prétraitement des avis pour la prédiction des sentiments.
Stockage des résultats : Enregistrement des avis prédits dans une base PostgreSQL.
Agrégation des données :
Mesure du volume de tweets par compagnie,
Répartition des sentiments par compagnie,
Calcul du taux de satisfaction par compagnie,
Identification des principales causes de tweets négatifs.
Visualisation : Affichage des résultats des requêtes dans un tableau de bord Streamlit, intégrant les KPI suivants:
Nombre total de tweets,
Nombre de compagnies aériennes,
Pourcentage de tweets négatifs.
Le dashboard doit se mettre à jour automatiquement à chaque récupération de données depuis l’API.
Automatisation : L’ensemble du pipeline doit être orchestré via un DAG Airflow exécuté toutes les minutes.
Modalités pédagogiques
Brief : Jury Blanc

Travail individuel

Temporalité : 5 jours

Période : Du 15/12/2025 au 19/12/2025 à 23h59

Modalités d'évaluation
Date de soutenance (22/12/2025)
Durée de soutenance jury blanc (45 min), organisée comme suit : :
Présentation rapide (10 minutes) : Démonstration du contenu et des fonctionnalités principales de l’application.
Analyse du code (10 minutes) : Montrez et expliquez le code source, en soulignant vos choix techniques.
Mise en situation (20 minutes) : L’examinateur propose des cas d’usage pour tester votre application.
Code Review et questions techniques (5 minutes).
Livrables
Présentation pptx
Code Source(Github)
Tableaux de bord interactifs avec Streamlit
Planification et gestion du projet
Un bon README + Architecture de la solution
Critères de performance
1- Qualité des données : pertinence, cohérence, complétude et qualité du prétraitement des données.
2- Optimisation du modèle de classification : choix justifié des algorithmes, réglage des hyperparamètres et performances du modèle.
3- Traitement des données en temps réel : fiabilité, automatisation et efficacité du pipeline de streaming.
4- Tableaux de bord interactifs : clarté des visualisations, pertinence des indicateurs (KPIs) et mise à jour dynamique des données.