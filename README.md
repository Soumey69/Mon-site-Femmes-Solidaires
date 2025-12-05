# Femmes Solidaires 
 
# 📖 Femmes Solidaires

## 🌟 Introduction

**Femmes Solidaires** est un site vitrine développé pour une association locale engagée dans l’émancipation des femmes par la formation et l’emploi.  

Le projet met en avant :  
- Les valeurs de l’association  
- Les formations proposées  
- Un espace de contact avec formulaire  
- Une navigation claire et intuitive  

Lors du diagnostic de la première version, nous avons constaté que la structure n’était pas suffisamment claire et que certains éléments (comme les liens vers les réseaux sociaux) n’étaient pas optimisés.  
Les améliorations apportées incluent :  
- Une refonte du footer avec des icônes SVG cliquables pour Facebook, LinkedIn et Instagram  
- Une meilleure hiérarchie des contenus pour guider l’utilisateur  
- Une navigation plus simple et lisible  

---

## 📌 1. Prérequis

Avant de commencer, assurez-vous d’avoir installé :

- Python 3.12+  
- Git  
- VS Code (ou tout autre éditeur de code)  
- Une connexion internet  

Vérifiez que Python fonctionne : 

```bash
python --version
```

Vérifiez Git :
```bash
git --version
```

## 📌 2. Cloner le projet depuis GitHub

## 2.1. Copier l’URL du dépôt
Cliquez sur Code → Copy dans GitHub pour récupérer l’URL du dépôt.

Exemple :
```Code
https://github.com/votrecompte/femmes-solidaires.git
```

## 2.2. Ouvrir un terminal et cloner

Placez-vous dans le dossier où vous souhaitez mettre votre projet :
```bash
cd C:\Users\VotreNom\Documents
```

Clonez le dépôt :
```bash
git clone https://github.com/votrecompte/femmes-solidaires.git
```

Entrez dans le projet :
```bash
cd femmes-solidaires
```

## 2.3. Ouvrir dans VS Code
```bash
code .
```

## 📌 3. Installer et lancer le projet

3.1. Créer un environnement virtuel
```bash
python -m venv venv
```

Activer :
**Windows** :
```bash
venv\Scripts\Activate.ps1
```

**macOS / Linux** :
```bash
source venv/bin/activate
```

## 3.2. Installer les dépendances

Si le projet contient un requirements.txt :
```bash
pip install -r requirements.txt
```

Sinon :
```bash
pip install "Django>=5.2,<5.3" "wagtail>=7.2,<7.3"
```

## 3.3. Appliquer les migrations
```bash
python manage.py migrate
```

## 3.4. Créer un utilisateur admin
```bash
python manage.py createsuperuser
```

## 3.5. Lancer le serveur
```bash
python manage.py runserver
```

Accéder au site : ➡️ http://127.0.0.1:8000/

Accéder à l’administration : ➡️ http://127.0.0.1:8000/admin/

## 📌 4. Structure du projet
```Code
Voici les fichiers les plus importants du projet :

home/
│
├── models.py                  ← Définit les types de pages et leurs champs
│
└── templates/
       ├── base.html           ← Structure globale (header, footer)
       ├── home_page.html      ← Page d'accueil
       ├── formations_page.html← Page "Nos formations"
       ├── about_page.html     ← Page "À propos"
       └── contact_page.html   ← Page "Contact"

femmes_solidaires/
   └── templates/
       ├── base.html           ← Structure globale (header, footer)
       └── ...
```




