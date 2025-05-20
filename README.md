# 🎟️ JO 2024 - Billetterie en ligne

Ce projet est une application Django complète permettant aux utilisateurs de consulter des épreuves sportives, acheter des billets selon des offres prédéfinies, et recevoir un e-billet sécurisé avec QR code.

---

## 🔧 Fonctionnalités principales

- Affichage dynamique des épreuves sportives
- Consultation des offres (solo, duo, familial)
- Réservation de billets (avec login requis)
- Paiement simulé avec génération de QR code unique
- Téléchargement de l’e-billet en PDF
- Interface administrateur pour gestion des offres, épreuves, billets
- Authentification sécurisée avec clés UUID
- Tableau de bord Django admin pour visualiser les réservations

---

## 🚀 Technologies utilisées

- **Framework** : Django 5+
- **Base de données** : PostgreSQL
- **Front-end** : Django Templates + Tailwind CSS
- **QR Code** : `qrcode` + `base64`
- **PDF** : `reportlab`
- **Déploiement** : Heroku & Railway

---

## ⚙️ Installation locale

### 1. Cloner le dépôt

```bash
git clone https://github.com/Projectsul22/jo-ticket-reservation.git
cd jo-ticket-reservation
```
### 2. Créer un environnement virtuel

```bash
python -m venv venv
source venv/bin/activate      # Linux/macOS
venv\Scripts\activate         # Windows
```
### 3. Installer les dépendances

```bash
3. Installer les dépendances
```

### 4. Configurer les variables d’environnement

SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_URL=postgres://...
NB : Le projet utilise python-decouple pour gérer les secrets.

### 5. Appliquer les migrations

```bash
python manage.py makemigrations
python manage.py migrate
```
### 6. Démarrer le serveur

```bash
python manage.py runserver
```
### 7. Compte admin

```bash
python manage.py createsuperuser
```
### 8. Tests unitaires

Lancer les tests :
```bash
python manage.py test

```
Les tests couvrent :
-Création de compte
-Réservations
-Paiement
-Génération des billets

🔐 Sécurité

-Mot de passe utilisateur sécurisé (min 8 caractères)
-Clés UUID pour cle_reservation et cle_paiement
-Accès protégé par @login_required
-Authentification via django.contrib.auth
-CSRF activé
-Variables sensibles chargées depuis .env (jamais versionnées)

🛠 Évolutions futures

-Ajout de la réinitialisation de mot de passe
-Tableau statistique dans l’admin avec des graphiques
-Paiement réel avec Stripe
-Recherche d’épreuves ou d’offres
-Interface utilisateur plus immersive

📄 Licence

Projet à but pédagogique — Studi Python Bloc 3 

