# Guide Developpeur

## Premier pas

### Lancement du serveur de developpement django

Dans un terminal, initialiser l'environnmemnt python/django;
 
```
cd /home/franck/Local/Projects/django/earthenv
source bin/activate
```

puis lancer le serveur de developpement django

```
cd /home/franck/Local/Projects/django/earthresist
python manage.py runserver --setting=earthresist.settings.dev
```

Puis entrer l'URL suivante dans un browser : `http://localhost:8000`


### Import de données dans la base de données

```
python manage.py importHelloAssoData `pwd`/helloasso.csv
 ```
 
### Effacer le contenu de la base de données

```
python manage.py shell
>>> from member.models import *
>>> Don.objects.all().delete()
>>> Member.objects.all().delete()
 ```
 
### Migrer la base de données

```
python manage.py makemigrations member --setting=earthresist.settings.dev
python manage.py migrate --setting=earthresist.settings.dev
```

### Post raw json data

```
curl -H "Content-Type: application/json" -X POST \
    -d '{"nom":"franck","prenom":"pujol", "email": "franck.puj@gm.com"}' \
    http://localhost:8000/api/v1.0/members/
```

## urls

```
http://localhost:8000/api/v1.0/members/
```

## Déployer une nouvelle version

pull, stop, up

## En prod
pour chaque commande, entrer dans le container
suffixer toutes les commandes par --setting=earthresist.settings.prod

