# Ventashop

Application de gestion des commandes de produits marketing

## Comment installer Ventasite/Ventashop en local : 
---

0. Pré-requis : 
 - Avoir installé Python v10. ou plus sur la machine locale. https://www.python.org/downloads/
 - Avoir installé PostgreSQL sur la machine locale. https://www.postgresql.org/download/
 - Avoir installé Git sur la machine locale. https://git-scm.com/book/en/v2/Getting-Started-Installing-Git

1. Cloner le projet : 
 - Copier le lien Github en haut à droite de la page "code" du dépôt.
 - Dans un terminal, se placer à l'emplacement local où l'on veut que le dossier source soit cloné.
 - Exécuter la commande git clone : 
````
$ git clone https://github.com/Thomas-N-GEORGE/Ventalis.git
````

 - En principe un dossier nommé Ventalis s'est crée. S'y déplacer : 
````
$ cd Ventalis
````
2. Créer un environnement virtuel (ici nommé *env* ) à l'aide de la commande : 
````
$ python venv env
````

3. Activer l'environnement virtuel à l'aide de la commande : 
 
* pour les plateformes Unix/Linux : 
````
$ source env/bin/activate
````

* pour la plateforme Windows (cmd.exe):
````
$ source env\bin\activate.bat
````
 * autre : consulter https://docs.python.org/3/library/venv.html


4. Installer les dépendances du projet : 
````
(env) $ pip install -r requirements.txt
````

5. Base de données : on peut installer rapidemnt une bdd postgresql .

6. settings.py : accorder le dictionnaire DATABASES avec vos propres clés NAME et USER 
````
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'username',
        'USER': 'username',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
````

7. Jouer les migrations pour créer les tables dans la BDD : 
````
(env) $ python manage.py makemigrations ventashop
(env) $ python manage.py migrate
````

8. Lancer l'application : 
````
(env) $ python manage.py ventashop
````

Si tout se passe bien on peut retrouver la page d'ouverture à l'adresse locale : 
````
http://127.0.0.1:8000/
````


## Utilisation : 
---

On peut peupler la BDD à l'aide de la **fixture** se trouvant dans le dossier **ventashop/fixtures**.

Pour intégrer des données, utiliser la commande **loaddata** (Django trouve le fichier tout seul en principe):
````
(env) $ python manage.py loaddata ventadata.json
````
---
Et sinon, en partant de zéro, on effectue ces étapes dans l'ordre : 

1. Créer un superuser Django avec la commande : 
````
(env) $ python manage.py createsuperuser
````

2. Ensuite, avec ce super utilisateur, on accède à la partie admin de Django ici http://127.0.0.1:8000/admin

    Ceci nous permet de créer un compte adminisrateur pour l'application.

3. En se connectant avec ce compte administrateur dans l'application, on accède à l'Espace Administrateur pour créer un/des Employé(s).

4. Ensuite le compte Employé quant à lui permet de créer et gérer produits, commandes, etc. à partir de son espace "Intranet"

Se référer au mode d'emploi SVP pour retrouver ces étapes à l'utilisation en détail, y compris en tant que Visiteur / Utilisateur.

---
Pour créer des fixtures avec **dumpdata**, un exemple : 
````
python manage.py dumpdata ventashop.product --indent 4 > ventashop/fixtures/product.json
````


