# Améliorations du Profil Utilisateur

## Vue d'ensemble

Le profil utilisateur a été complètement repensé pour offrir une meilleure expérience utilisateur avec plus d'informations pertinentes et la possibilité de gérer son mot de passe.

## Modifications Backend

### 1. Nouveau schéma `PasswordChange`

**Fichier:** `backend/app/schemas/user.py`

Ajout d'un nouveau schéma Pydantic pour gérer le changement de mot de passe :

```python
class PasswordChange(BaseModel):
    current_password: str = Field(min_length=8, description="Current password")
    new_password: str = Field(
        min_length=8, description="New password must be at least 8 characters"
    )
```

### 2. Nouvelle route API `PUT /api/users/me/password`

**Fichier:** `backend/app/routers/users.py`

Ajout d'une route protégée permettant à l'utilisateur de changer son mot de passe :

**Endpoint:** `PUT /api/users/me/password`

**Authentification:** Requise (Bearer Token)

**Body:**
```json
{
  "current_password": "ancien_mot_de_passe",
  "new_password": "nouveau_mot_de_passe"
}
```

**Validations:**
- Vérifie que le mot de passe actuel est correct
- Vérifie que le nouveau mot de passe est différent de l'ancien
- Vérifie que le nouveau mot de passe fait au moins 8 caractères

**Réponses:**
- `200 OK`: Mot de passe changé avec succès
- `400 BAD REQUEST`: Mot de passe actuel incorrect ou nouveau mot de passe invalide
- `401 UNAUTHORIZED`: Token invalide ou manquant

### 3. Utilisation de la fonction existante `update_user_password`

La fonction `update_user_password` du module `crud/user.py` est utilisée pour mettre à jour le mot de passe de manière sécurisée avec hachage Argon2.

## Modifications Frontend

### 1. Service API

**Fichier:** `frontend/gym-app/src/services/api.js`

Ajout de deux nouvelles méthodes :

```javascript
// Mettre à jour les informations du profil
updateCurrentUser(userData) {
  return apiClient.put('/api/users/me', userData)
}

// Changer le mot de passe
changePassword(currentPassword, newPassword) {
  return apiClient.put('/api/users/me/password', {
    current_password: currentPassword,
    new_password: newPassword,
  })
}
```

### 2. Vue Profile Améliorée

**Fichier:** `frontend/gym-app/src/views/Profile.vue`

La vue profil a été complètement remaniée avec les fonctionnalités suivantes :

#### Affichage des informations (Mode Lecture)

**Section Profil:**
- Avatar avec initiale de l'utilisateur
- Nom d'utilisateur
- Email
- Bouton "Modifier"

**Informations personnelles:**
- Genre (formaté en français)
- Date de naissance (formatée)
- Âge calculé automatiquement
- Taille (en cm)
- Poids (en kg)
- Taux de masse grasse (en %)
- Niveau d'activité (formaté en français)
- Objectif (formaté en français)

**Informations du compte:**
- Date de création du compte
- Dernière mise à jour

**Actions:**
- Bouton "Changer le mot de passe"

#### Mode Édition

Formulaire complet permettant de modifier :
- Nom d'utilisateur
- Email
- Genre (sélection)
- Date de naissance
- Taille
- Poids
- Taux de masse grasse
- Niveau d'activité (sélection)
- Objectif (sélection)

**Fonctionnalités:**
- Validation des champs requis
- Gestion des erreurs
- Message de succès après mise à jour
- Boutons "Annuler" et "Enregistrer"
- Désactivation du bouton pendant l'enregistrement

#### Modal de Changement de Mot de Passe

Modal indépendant avec :
- Champ "Mot de passe actuel"
- Champ "Nouveau mot de passe"
- Champ "Confirmer le nouveau mot de passe"

**Validations côté client:**
- Les nouveaux mots de passe doivent correspondre
- Minimum 8 caractères
- Le nouveau mot de passe doit être différent de l'ancien

**Fonctionnalités:**
- Fermeture par clic en dehors du modal
- Bouton de fermeture (×)
- Gestion des erreurs
- Message de succès
- Fermeture automatique après succès

### 3. Fonctions Utilitaires

Le composant inclut plusieurs fonctions de formatage :

- `formatGender(gender)`: Convertit "male"/"female" en "Homme"/"Femme"
- `formatDate(dateString)`: Formate les dates en français (ex: "15 janvier 2024")
- `calculateAge(birthdate)`: Calcule l'âge à partir de la date de naissance
- `formatActivityLevel(level)`: Convertit les niveaux d'activité en français
- `formatGoal(goal)`: Convertit les objectifs en français

### 4. Style et Design

**Caractéristiques:**
- Design moderne avec glassmorphism
- Dégradés de couleurs (violet/bleu)
- Animations et transitions fluides
- Responsive (mobile-friendly)
- Bordures arrondies et effets de flou
- Messages d'erreur et de succès stylisés

**Palette de couleurs:**
- Fond principal : Transparent avec flou
- Accents : #667eea (bleu) et #764ba2 (violet)
- Texte : Blanc avec opacités variées
- Erreurs : #ff6b6b (rouge)
- Succès : #51cf66 (vert)

## Utilisation

### Modifier son profil

1. Aller sur la page "Profil"
2. Cliquer sur le bouton "✏️ Modifier"
3. Modifier les champs souhaités
4. Cliquer sur "Enregistrer" ou "Annuler"

### Changer son mot de passe

1. Aller sur la page "Profil"
2. Cliquer sur "🔒 Changer le mot de passe"
3. Entrer le mot de passe actuel
4. Entrer le nouveau mot de passe (2 fois)
5. Cliquer sur "Changer le mot de passe"

## Sécurité

- Toutes les routes sont protégées par authentification JWT
- Les mots de passe sont hachés avec Argon2
- Validation des entrées côté client et serveur
- Vérification de l'ancien mot de passe avant changement
- Le nouveau mot de passe doit être différent de l'ancien

## Points d'attention

1. **Format de date**: La date de naissance doit être envoyée au format ISO avec timezone
2. **Champs optionnels**: Les champs comme taille, poids, etc. peuvent être null
3. **Validation email**: Le format email est vérifié par Pydantic (EmailStr)
4. **Unicité**: Le nom d'utilisateur et l'email doivent être uniques

## Améliorations futures possibles

- [ ] Upload d'avatar personnalisé
- [ ] Historique des modifications du profil
- [ ] Authentification à deux facteurs (2FA)
- [ ] Export des données personnelles (RGPD)
- [ ] Suppression de compte avec confirmation
- [ ] Statistiques d'utilisation (nombre de workouts, progression, etc.)
- [ ] Intégration avec des appareils de fitness (API externes)
- [ ] Graphiques de progression du poids/masse grasse