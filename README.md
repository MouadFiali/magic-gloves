# Magic Gloves

## Table des matières
- [Description](#description)
- [Problématique](#problématique)
- [Matériel Utilisé](#matériel-utilisé)
- [Collecte de Données](#collecte-de-données)
- [Scénario d'utilisation](#scénario-dutilisation)
    - [Schéma logique d'utilisation](#schéma-logique-dutilisation)
    - [Diagramme de séquence](#diagramme-de-séquence)
    - [Vidéo de démonstration](#vidéo-de-démonstration)
- [Budget](#budget)
- [Bilan](#bilan)
- [Pistes d'Amélioration](#pistes-d'Amélioration)

## Description

Notre projet vise à créer un pont de communication pour les personnes sourdes, muettes ou ayant des difficultés à parler. Nous avons développé des gants innovants capables de traduire le langage des signes en texte écrit, rendant la communication avec le grand public fluide et compréhensible.

### Membres de l'Équipe

- FIALI Mouad
- GHAZAOUI Badr
- MAROUANE Kamal
- RIMAOUI Nabila
- ZERKTOUNI Ismail

## Problématique

Le langage des signes est un outil de communication essentiel pour les personnes sourdes, muettes ou ayant des difficultés de parole. Cependant, il constitue un défi majeur : sa maîtrise reste peu répandue dans la population générale, ce qui crée un obstacle significatif à l'intégration sociale et professionnelle des personnes dépendant de cette forme de communication.

Notre projet aborde cette problématique en fournissant une solution technologique qui permet de traduire le langage des signes en langage écrit. Cette innovation vise à briser les barrières de communication, facilitant ainsi l'interaction et l'intégration des personnes sourdes ou muettes dans la société. En transformant les gestes en texte, nous créons un pont entre deux mondes, permettant une compréhension mutuelle et une interaction enrichissante pour tous.

## Matériel Utilisé

Pour la réalisation de nos gants de traduction du langage des signes, nous avons utilisé les composants suivants :

- **Capteurs de Flexion** : Notre conception originale prévoyait l'équipement de chaque gant avec cinq capteurs de flexion pour une captation optimale des mouvements des doigts. Cependant, une contrainte d'approvisionnement a conduit à équiper un gant de cinq capteurs et l'autre de quatre, toutefois, la sensibilité suffisante des capteurs restants assure une détection précise et une mesure efficace des mouvements.
- **Résistances** : Les capteurs de flexion sont connectés à des résistances de 10 kΩ.
- **Capteurs Accéléromètre/Gyroscope** : Chaque main est équipé d'un capteur accéléromètre/gyroscope utilisé pour capter les mouvements et l'orientation de la main dans l'espace.
- **Arduino UNO** : Deux cartes Arduino UNO servent de plateforme de contrôle et de traitement des signaux provenant des capteurs.
- **Matériel de Connexion** : Câbles, connecteurs, et tout le nécessaire pour connecter les capteurs aux cartes Arduino.

<div style="display:flex; justify-content:center;">
    <img src="https://github.com/MouadFiali/magic-gloves/raw/wiki/images/Gants_2.jpeg" width="500">
    <img src="https://github.com/MouadFiali/magic-gloves/raw/wiki/images/Gants_3.jpeg" width="500">
    <img src="https://github.com/MouadFiali/magic-gloves/raw/wiki/images/Gants_1.jpeg" width="500">
</div>

## Collecte de Données

Nous avons collecté manuellement les données car nous n'avons pas trouvé de base de données adaptée à notre projet et au matériel que nous utilisions. Les données comprennent les mouvements en langage des signes de six mots traduits en anglais, capturés à l'aide de capteurs de flexion et d'un gyroscope/accéléromètre. Un signe de pause, ajouté également, marque la fin de la phrase lorsque l'utilisateur ne réalise aucun mouvement. Chaque mouvement est enregistré sous forme de 20 frames (pour chaque capteur). Au total, nous avons enregistré 2400 données (6 mots * 400 enregistrements par mot, donnant 2400 en plus du signe de pause) avec 440 colonnes comprenant les valeurs des capteurs de flexion gauche/droite, de l'orientation gauche/droite, et de l'accélération gauche/droite.

Voici le lien Kaggle vers dataset enregistré : [Sign Language Data](https://www.kaggle.com/datasets/mouadfiali/sensor-based-american-sign-language-recognition)

## Scénario d'utilisation

Voici le déroulement typique d'utilisation de nos gants de traduction du langage des signes :

1. **Mise en Place et Calibration :**

- L'utilisateur démarre une phase de calibration de 10 secondes pour les capteurs gyroscopiques/accéléromètres, permettant de les ajuster à ses mouvements spécifiques.
- Suit une seconde phase de calibration, également de 10 secondes, pour les capteurs de flexion, afin de calibrer les courbures des doigts.

2. **Enregistrement et Traduction des Mouvements :**

- L'utilisateur effectue des gestes en langage des signes.
- Les gants captent les mouvements et les transmettent en temps réel aux cartes Arduino UNO.
- Les données sont envoyées à l'ordinateur où le modèle d'IA analyse et traduit les gestes en texte écrit.

3. **Pause et Préparation pour le Mouvement Suivant :**

- Après chaque geste, une pause de 2 secondes est observée. Cette période permet à l'utilisateur de se préparer pour le signe suivant et assure que les mouvements soient clairement délimités et correctement interprétés. Ce delai est aussi une solution pour faire face à quelques limitation quant à l'utilisation du module NLP utilisé pour la prochaine phase du déroulement du processus.

4. **Formation de Phrases et Correction Grammaticale :**

- Après chaque prédiction de mot, le système évalue deux critères : si le numéro de prédiction est pair ou si le mot prédit correspond au mot de fin (mot d'arrêt). Si l'un de ces critères est rempli, le système procède à l'envoi de la séquence accumulée des mots prédits vers un module de traitement du langage naturel (NLP) (l'API de chatGPT en l'occurence). Ce module a pour rôle d'affiner la structure grammaticale, garantissant ainsi la clarté et la précision de la phrase formulée.
- Suite à la structuration de la phrase par le module NLP, le système vérifie si le dernier mot prédit était le mot d'arrêt. Si c'est le cas, la phrase est considérée comme complète et le processus peut se terminer. Sinon, le système reprend à l'étape d'enregistrement du mouvement suivant, continuant ainsi la séquence jusqu'à l'identification du mot d'arrêt.

### Schéma logique d’utilisation

<img src="https://github.com/MouadFiali/magic-gloves/raw/wiki/images/Schema_logic.png" width="600">

### Diagramme de séquence

<img src="https://github.com/MouadFiali/magic-gloves/raw/wiki/images/Diagramme_sequence.png" width="700">

### Vidéo de démonstration

Voici une vidéo de démonstration de notre projet (Cliquer sur l'image pour accéder à la vidéo) :

[![Vidéo de démonstration](/images/app.png)](https://drive.google.com/file/d/1rZYFMr-MuG-sYjRMZ9x--nTnDmlXHhr3/view?usp=sharing)

## Budget

Une étude budgétaire des composants par rapport aux prix trouvables sur internet nous indique les prix suivant :

- Gants : 10 €
- Capteurs de Flexion : 90 € (pour 9 capteurs)
- Modules Accéléromètre/Gyroscope : 40 € (pour 2 modules)
- Cartes Arduino UNO : 50 € (pour 2 cartes)
- Matériel de Connexion (câbles, connecteurs, etc.) : 20 €

  **Sous-total** : 210 €

Concernant le budget horaire, avec une considération approximative des temps de travail cumulés et d’un taux horaire du SMIC, on arrive au détail des heures suivantes :

- Brainstorming : 4 h
- Formation : 8 h
- Assemblage des gants : 10 h
- Développement Software (algorithme de calibrage, de collecte de données et de modèles IA) : 30 h
  
  **Sous-total** au SMIC 605.8 €

**Total Estimatif** : 815.8 €

## Bilan

Notre projet a considérablement avancé vers l'objectif de permettre aux personnes sourdes ou muettes de communiquer via le langage des signes traduit en texte. La précision de traduction de 99% témoigne de l'efficacité des gants et du modèle d'IA que nous avons développés. Les résultats encourageants soulignent le potentiel d'amélioration et de commercialisation futur.

## Pistes d'Amélioration

Pour la suite, nous envisageons plusieurs axes d'amélioration qui augmenteraient considérablement la portée et l'utilité de nos gants de traduction du langage des signes :

- **Traduction en Audio** : Afin d'améliorer le produit, il serait utile d'intégrer une fonctionnalité de synthèse vocale qui convertirait le texte traduit en parole, rendant la communication encore plus accessible et naturelle.
- **Traduction Inverse** : Un autre développement majeur serait la traduction de la langue orale en un language de vibration  pour permettre aux personnes sourdes une experience "auditive" à travers le touché, c'est un concept connu par le nom de "senses subsitution". Cela permettrait une conversation bidirectionnelle, où la parole peut être traduite en texte pour les personnes sourdes ou ayant des difficultés à entendre.
- **Portabilité** : Rendre le système autonome et portable via une application mobile qui pourrait effectuer le traitement et la traduction sans nécessiter un ordinateur.
- **Vocabulaire Élargi** : Étendre la base de données du modèle d'IA pour couvrir un vocabulaire plus large, afin de pouvoir traduire une variété de phrases et d'expressions plus étendue.

Ces améliorations visent à rendre le dispositif non seulement plus complet en termes de communication mais aussi plus pratique et accessible pour un usage quotidien. L'ajout de ces fonctionnalités ouvrirait la voie à une commercialisation réussie et à un impact social encore plus grand.
