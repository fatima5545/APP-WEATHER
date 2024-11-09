- [Introduction](#introduction)
- [Fonctionnement global](#fonctionnement-global)
- [Technologies Principales](#technologies-principales)
- [Architecture de l'Application](#architecture-de-lapplication)
  - [Structure du Projet](#structure-du-projet)
  - [Diagramme de Séquence des Appels API](#diagramme-de-séquence-des-appels-api)
    - [Pour les météo actuelle du jour](#pour-les-météo-actuelle-du-jour)
    - [Pour les prévisions des 7 jours](#pour-les-prévisions-des-7-jours)
- [Prérequis et Installation](#prérequis-et-installation)
  - [Prérequis](#prérequis)
  - [Étapes d'installation](#étapes-dinstallation)
- [Surveillance et Gestion des Quotas](#surveillance-et-gestion-des-quotas)
- [Tests unitaires et End-to-End](#tests-unitaires-et-end-to-end)
- [Couverture de Tests](#couverture-de-tests)
- [CI/CD et Déploiement](#cicd-et-déploiement)
  - [Pipeline CI/CD](#pipeline-cicd)
- [Améliorations Futures](#améliorations-futures)

# Introduction

L'application est une API de prévisions météo qui permet aux utilisateurs de récupérer les informations météorologiques actuelles et les prévisions à 7 jours pour une ville donnée. Elle est conçue pour fournir des données claires et accessibles sur la météo, y compris une description concise de la météo, la température, la vitesse du vent, l'humidité, ainsi que des tendances sur la température et la pression.

## Fonctionnement global

L'application fonctionne en tant qu'API backend qui expose deux endpoints principaux :

### Endpoint `/weather/current`

Retourne les conditions météorologiques actuelles pour une ville spécifique.

- La description de la météo
- La température
- La vitesse du vent
- L'humidité

### Endpoint `/weather/forecast`

Cet endpoint retourne les prévisions météorologiques pour les 7 jours suivants. Les prévisions incluent :

- La tendance des températures (en hausse, stable, en baisse)
- La tendance de la pression atmosphérique
- La catégorie de la vitesse moyenne du vent selon l'échelle de Beaufort
- L'évolution générale des conditions météorologiques

#### Indicateurs Météorologiques utilisés pour l'évolution

L'évolution générale des conditions est déterminée en analysant plusieurs indicateurs clés :

- **Tendance de température** Indique si la température est en hausse, stable ou en baisse
- **Tendance de pression** Indique si la pression atmosphérique est en hausse, stable ou en baisse
- **Probabilité de précipitations :** Indique la probabilité de pluie, mesurée en pourcentage.
- **Couverture nuageuse :** Mesure la quantité de nuages dans le ciel, exprimée en pourcentage.
- **Indice UV :** Indique l'intensité des rayons UV, utile pour évaluer la quantité de soleil.

#### Explication de la Logique de l'évolution générale

- **En amélioration :** Lorsque la température et la pression sont en hausse, avec une faible probabilité de précipitations, une faible couverture nuageuse, et un indice UV élevé (plus de soleil).
- **En dégradation :** Lorsque la température ou la pression est en baisse, ou si la probabilité de précipitations est élevée, la couverture nuageuse est importante, ou l'indice UV est faible.
- **Stable :** Lorsque les indicateurs sont globalement équilibrés ou ne montrent pas de tendances marquées.

## Technologies Principales

1. **FastAPI** : Framework Python pour construire des API web rapides et performantes. FastAPI gère les endpoints et la logique de requête/réponse de l'application.
2. **Redis** : Utilisé comme cache pour stocker temporairement les données météorologiques. Cela améliore les performances en réduisant le nombre d'appels à l'API externe et en offrant une réponse plus rapide aux utilisateurs.
3. **WeatherBit API** : Fournisseur de données météorologiques utilisé pour obtenir les informations actuelles et les prévisions sur 7 jours.
4. **Docker & Docker Compose** : Conteneurisation de l'application et de Redis pour une configuration facile et reproductible, facilitant l'installation et l'exécution de l'application dans différents environnements.
5. **GitHub Actions** : Configuration de CI/CD pour automatiser les tests, et la validation de code.

# Architecture de l'Application :

## Structure du Projet

```
Project/
├── api/
│   ├── endpoints/
│   └── schema/
├── services/
├── adapters/
├── settings/
├── tests/
│   ├── unit_tests/
│   └── end_to_end_tests/
├── logs/
├── utils/
└── docker-compose.yml
```

- **api/** : Contient les routes de l'API.
- **services/** : Logique métier, y compris les appels à l'API WeatherBit et la gestion du cache.
- **adapters/** : Interfaces pour les services externes, comme Redis.
- **settings/** : Configuration de l'application.
- **tests/** : Tests unitaires et end-to-end.

## Diagrammes de Séquence des Appels API :

Voici comment chaque composant interagit lorsque l’utilisateur fait une requête pour obtenir les informations météo actuelles ou les prévisions :

**Pour les météo actuelle du jour :**

<div align="center">
    <img width="700" alt="image" src="https://github.com/user-attachments/assets/975660ee-dfe8-4cf3-972f-87e055c49ffb">
</div>

### Explications :

- **Utilisateur :** Envoie une requête pour obtenir les données météo.
- **API :** Vérifie d'abord dans Redis si les données sont en cache.
- **Redis :** Si les données sont en cache, elles sont renvoyées. Sinon, l'API vérifie si le quota d'appels API est respecté.
- **WeatherBit :** Si le quota n'est pas dépassé, l'API fait un appel externe à WeatherBit pour récupérer les données et les met en cache.
- **Gestion du Quota :** Si le quota est dépassé, une erreur est retournée à l'utilisateur.

**Pour les prévisions des 7 jours :**

<div align="center">
  <img width="700" alt="image" src="https://github.com/user-attachments/assets/163f55e3-7705-4d94-938b-2303b3eeb08f">
</div>

### Explications :

- **Utilisateur :** Envoie une requête pour obtenir les prévisions météo sur 7 jours.
- **API :** Vérifie d'abord dans Redis si les données sont en cache.
- **Redis :** Si les données sont en cache, elles sont renvoyées. Sinon, l'API vérifie si le quota d'appels API est respecté.
- **WeatherBit :** Si le quota n'est pas dépassé, l'API fait un appel externe à WeatherBit pour récupérer les données et les met en cache.
- **Gestion du Quota :** Si le quota est dépassé, une erreur est retournée à l'utilisateur.

## Prérequis et Installation

### Prérequis

- **Docker** et **Docker Compose** : Assurez-vous d’avoir Docker et Docker Compose installés.

### Étapes d'installation

1. Clonez le dépôt :

   ```bash
   git clone https://github.com/fatima5545/WEATHER-APP.git
   cd votre-repo

   ```

2. Lancez l'application avec Docker Compose : :

   ```bash
   docker-compose up --build

   ```

3. Accédez à la documentation Swagger : Ouvrez [le Swagger](http://localhost:8000/docs) pour voir les endpoints et tester l'API.

## Surveillance et Gestion des Quotas

Il y'a un module qui gère la mise en cache des données météorologiques et limite le nombre d'appels quotidiens à l'API WeatherBit pour respecter les quotas.

Pour respecter le quota de 50 appels par jour imposé par l'API WeatherBit, l'application utilise Redis comme cache. Les données météo pour chaque ville sont mises en cache avec une durée d'expiration. Si une demande est effectuée pour une ville déjà en cache, l'API retourne les données stockées, réduisant ainsi le nombre d'appels externes.

## Tests unitaires et End-to-End

Les tests unitaires et end-to-end vérifient la fiabilité de l'application. Ils incluent des tests des services et des interactions avec Redis et WeatherBit.

## CI/CD

### Pipeline CI/CD

Le pipeline CI/CD utilise GitHub Actions pour exécuter les tests et valider le code à chaque commit sur la branche principale. Voici les étapes incluses :

- **Linting et formatage :** Vérification du style de code avec black.
- **Tests :** Exécution des tests avec pytest et génération de rapports de couverture.
- **Déploiement :** Construction et publication d'une image Docker sur Docker Hub.

# Améliorations Futures

- **Ajout d'autres fournisseurs de données météo** : Intégrer des API alternatives pour des données plus riches ou en cas de dépassement de quotas.
- **Authentification** : Implémenter une authentification pour restreindre l'accès à certains utilisateurs ou groupes.
- **Support multi-langue** : Fournir les réponses de l'API en différentes langues.
- **Gestion des logs** : Pour une meilleure gestion, on peut envisager d'utiliser un service comme ELK pour centraliser et analyser les logs en temps réel.
