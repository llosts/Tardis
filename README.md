# 🚄 TARDIS - Predicting the Unpredictable

> Projet Epitech - Analyse prédictive des retards de trains pour la SNCF

TARDIS est une application de data science développée dans le cadre du cursus EPITECH. Elle vise à prédire les retards de trains à partir de données historiques via une interface web interactive. Ce projet s'inscrit dans une démarche d'amélioration de l'efficacité du réseau ferroviaire français.

---

## 📁 Livrables

- `tardis_eda.ipynb` – Analyse exploratoire et nettoyage des données
- `tardis_model.ipynb` – Entraînement du modèle de prédiction
- `tardis_dashboard.py` – Tableau de bord interactif via Streamlit
- `requirements.txt` – Dépendances Python
- `README.md` – Documentation du projet

---

## 🧰 Stack technique

- **Langage** : Python 3
- **Librairies** :  
  - Data Science : `pandas`, `numpy`  
  - Visualisation : `matplotlib`, `seaborn`  
  - Modélisation : `scikit-learn`  
  - Web App : `streamlit`  
- **Formatage du code** : `ruff`

---

## 📊 Objectifs

- ✅ Nettoyage et prétraitement des données
- ✅ Analyse exploratoire et visualisation
- ✅ Modélisation prédictive des retards
- ✅ Création d’un tableau de bord utilisateur

---

## 🔍 Étapes du projet

### 1. Data Cleaning & Preprocessing
- Traitement des valeurs manquantes
- Suppression des doublons
- Conversion des types de données
- Feature engineering (jour, heure de pointe, etc.)

### 2. Visualisation & Analyse
- Statistiques descriptives
- Graphiques de distribution des retards
- Comparaison par station / heure
- Corrélations via heatmaps

### 3. Modélisation
- Sélection des variables pertinentes
- Modèles testés : LinearRegression, DecisionTree, RandomForest
- Évaluation : RMSE, R², accuracy
- Comparaison et sélection du meilleur modèle

### 4. Dashboard Streamlit
- Graphiques interactifs : histogrammes, boxplots, heatmaps
- Sélection dynamique de station, heure, ligne
- Intégration des prédictions
- Indicateurs : retards moyens, taux d'annulation, ponctualité

---

## 🚀 Installation

```bash
git clone https://github.com/votre-utilisateur/tardis.git
cd tardis
python -m venv venv
source venv/bin/activate  # ou .\venv\Scripts\activate sous Windows
pip install -r requirements.txt
```

---

## ▶️ Lancement

### 1.Nettoyez les données :
Lancez tardis_eda.ipynb pour produire cleaned_dataset.csv

### 2.Entraînez un modèle :
Exécutez tardis_model.ipynb pour entraîner et enregistrer le modèle

### 3.Lancez le tableau de bord :
```bash
streamlit run tardis_dashboard.py
```

---

## 🙋‍♀️ Author
- Made with ❤️ by [@llosts](https://github.com/llosts)
