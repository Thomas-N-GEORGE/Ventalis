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

5. Créer la Base De Données PostgreSQL : 

A l'aide de SQLShell :
````
CREATE DATABASE dbname;
````
 
ou à l'aide d'un utlilitaire comme createdb :
````
createdb -h localhost -p 5432 -U postgres testdb
````

6. Adapter les settings.py de Django :  


7. Jouer les migrations pour créer les tables dans la BDD : 
````
(env) $ python manage.py makemigrations ventashop
(env) $ python manage.py migrate
````

8. Lancer l'application : 
````
(env) $ python manage.py ventashop
````

Ainsi l'application doit se lancer et on peut retrouver la page d'ouverture à l'adresse locale : 
````
http://127.0.0.1:8000/
````


## Utilisation : 
---

Créer un superuser Django avec la commande : 
````
$ python manage.py createsuperuser
````

Et ensuite, avec ce super utilisateur, on accède à la partie admin/Webmaster de Django :
````
http://127.0.0.1:8000/admin
````

qui nous permet ainsi la création d'un compte admin pour l'application.

Ainsi on pourra à l'aide de ce compte accéder à l'Espace Administrateur et créer un/des Employé(s).

L'Espace Emplyé quant à lui permet de gérer produits, commandes, etc.

Se référer au mode d'emploi SVP pour retrouver ces étapes en détail, y compris l'utilisation en tant que Visiteur / Utilisateur.


 - A moins que je ne fasse ça dans un script !!! Comme c'était le cas avec changelog.
Je ne sais plus quelle classe il faut utiliser mais c'est un truc du genre Command.
