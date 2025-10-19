# Guide de Test - Fonctionnalités du Profil

## Prérequis

- Backend lancé sur `http://localhost:8000`
- Frontend lancé sur `http://localhost:5173` (ou votre port Vite)
- Compte utilisateur créé et connecté

## Tests Backend

### 1. Test de la Route de Changement de Mot de Passe

#### Cas de succès

```bash
# 1. Se connecter et obtenir un token
curl -X POST "http://localhost:8000/api/users/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=votre@email.com&password=votreMotDePasse"

# 2. Changer le mot de passe (remplacer YOUR_TOKEN)
curl -X PUT "http://localhost:8000/api/users/me/password" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "current_password": "votreMotDePasse",
    "new_password": "nouveauMotDePasse123"
  }'
```

**Résultat attendu:** `{"message": "Password updated successfully"}`

#### Cas d'erreur - Mauvais mot de passe actuel

```bash
curl -X PUT "http://localhost:8000/api/users/me/password" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "current_password": "mauvaisMotDePasse",
    "new_password": "nouveauMotDePasse123"
  }'
```

**Résultat attendu:** `400 BAD REQUEST` avec message "Current password is incorrect"

#### Cas d'erreur - Même mot de passe

```bash
curl -X PUT "http://localhost:8000/api/users/me/password" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "current_password": "votreMotDePasse",
    "new_password": "votreMotDePasse"
  }'
```

**Résultat attendu:** `400 BAD REQUEST` avec message "New password must be different from current password"

#### Cas d'erreur - Mot de passe trop court

```bash
curl -X PUT "http://localhost:8000/api/users/me/password" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "current_password": "votreMotDePasse",
    "new_password": "1234567"
  }'
```

**Résultat attendu:** `422 UNPROCESSABLE ENTITY` (validation Pydantic)

### 2. Test de Mise à Jour du Profil

```bash
curl -X PUT "http://localhost:8000/api/users/me" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "nouveauUsername",
    "email": "newemail@example.com",
    "gender": "male",
    "birthdate": "1990-01-15T00:00:00Z",
    "height_cm": 180,
    "weight_kg": 75.5,
    "body_fat_percentage": 15.2,
    "activity_level": "moderate",
    "goal": "gain_muscle"
  }'
```

**Résultat attendu:** Objet UserOut avec les données mises à jour

## Tests Frontend

### 1. Affichage du Profil

**Actions:**
1. Se connecter à l'application
2. Naviguer vers la page "Profil"

**Vérifications:**
- [ ] L'avatar affiche la première lettre du nom d'utilisateur en majuscule
- [ ] Le nom d'utilisateur est affiché correctement
- [ ] L'email est affiché correctement
- [ ] Le bouton "Modifier" est visible
- [ ] Le bouton "Changer le mot de passe" est visible

**Informations personnelles:**
- [ ] Genre affiché en français (Homme/Femme)
- [ ] Date de naissance formatée correctement (ex: "15 janvier 1990")
- [ ] Âge calculé correctement
- [ ] Taille affichée avec "cm" ou "Non renseigné"
- [ ] Poids affiché avec "kg" ou "Non renseigné"
- [ ] Taux de masse grasse affiché avec "%" ou "Non renseigné"
- [ ] Niveau d'activité en français ou "Non renseigné"
- [ ] Objectif en français ou "Non renseigné"

**Informations du compte:**
- [ ] Date de création du compte formatée
- [ ] Date de dernière mise à jour formatée

### 2. Édition du Profil

**Actions:**
1. Cliquer sur le bouton "✏️ Modifier"

**Vérifications:**
- [ ] Le formulaire d'édition s'affiche
- [ ] Tous les champs sont pré-remplis avec les valeurs actuelles
- [ ] La date de naissance est au format `YYYY-MM-DD`
- [ ] Les champs obligatoires sont marqués avec *
- [ ] Les boutons "Annuler" et "Enregistrer" sont visibles

**Modification des données:**
1. Modifier un ou plusieurs champs
2. Cliquer sur "Enregistrer"

**Vérifications:**
- [ ] Le bouton "Enregistrer" se désactive pendant la sauvegarde
- [ ] Le texte du bouton change en "Enregistrement..."
- [ ] Un message de succès s'affiche après sauvegarde
- [ ] Le formulaire se ferme automatiquement après 2 secondes
- [ ] Les nouvelles données sont affichées dans la vue profil
- [ ] La page ne se recharge pas (SPA)

**Test du bouton Annuler:**
1. Cliquer sur "✏️ Modifier"
2. Modifier des champs
3. Cliquer sur "Annuler"

**Vérifications:**
- [ ] Le formulaire se ferme sans sauvegarder
- [ ] Les données restent inchangées
- [ ] Aucune requête API n'est envoyée

### 3. Changement de Mot de Passe

**Actions:**
1. Cliquer sur "🔒 Changer le mot de passe"

**Vérifications:**
- [ ] Un modal s'ouvre
- [ ] Le fond est flouté (backdrop-filter)
- [ ] Le modal contient 3 champs de mot de passe
- [ ] Les boutons "Annuler" et "Changer le mot de passe" sont visibles
- [ ] Le bouton de fermeture (×) est visible en haut à droite

**Test de succès:**
1. Entrer le mot de passe actuel correct
2. Entrer un nouveau mot de passe (8+ caractères)
3. Confirmer le nouveau mot de passe (identique)
4. Cliquer sur "Changer le mot de passe"

**Vérifications:**
- [ ] Le bouton se désactive pendant le changement
- [ ] Le texte change en "Changement..."
- [ ] Un message de succès vert s'affiche
- [ ] Le modal se ferme automatiquement après 2 secondes
- [ ] Le nouveau mot de passe fonctionne pour se connecter

**Test d'erreur - Mots de passe ne correspondent pas:**
1. Entrer le mot de passe actuel
2. Entrer un nouveau mot de passe
3. Entrer une confirmation différente
4. Cliquer sur "Changer le mot de passe"

**Vérifications:**
- [ ] Message d'erreur: "Les mots de passe ne correspondent pas"
- [ ] Aucune requête API n'est envoyée
- [ ] Le modal reste ouvert

**Test d'erreur - Mot de passe actuel incorrect:**
1. Entrer un mauvais mot de passe actuel
2. Entrer un nouveau mot de passe valide (2 fois)
3. Cliquer sur "Changer le mot de passe"

**Vérifications:**
- [ ] Requête API envoyée
- [ ] Message d'erreur rouge affiché
- [ ] Le modal reste ouvert

**Test d'erreur - Mot de passe trop court:**
1. Entrer le mot de passe actuel
2. Entrer "1234567" comme nouveau mot de passe (7 caractères)
3. Confirmer avec "1234567"
4. Cliquer sur "Changer le mot de passe"

**Vérifications:**
- [ ] Message d'erreur: "Le nouveau mot de passe doit contenir au moins 8 caractères"
- [ ] Aucune requête API n'est envoyée

**Test d'erreur - Même mot de passe:**
1. Entrer le mot de passe actuel
2. Entrer le même mot de passe comme nouveau
3. Cliquer sur "Changer le mot de passe"

**Vérifications:**
- [ ] Message d'erreur: "Le nouveau mot de passe doit être différent de l'ancien"
- [ ] Aucune requête API n'est envoyée

**Fermeture du modal:**
1. Tester la fermeture en cliquant en dehors du modal
2. Tester la fermeture avec le bouton (×)
3. Tester la fermeture avec le bouton "Annuler"

**Vérifications:**
- [ ] Le modal se ferme dans tous les cas
- [ ] Les champs sont réinitialisés
- [ ] Les messages d'erreur/succès sont effacés

### 4. Responsive Design

**Tests sur mobile (< 768px):**
- [ ] Le header du profil passe en colonne
- [ ] La grille d'informations affiche une colonne
- [ ] Le formulaire d'édition affiche une colonne
- [ ] Les boutons d'action prennent toute la largeur
- [ ] Le modal s'adapte à la largeur de l'écran
- [ ] Tout reste lisible et utilisable

**Tests sur tablette (768px - 1024px):**
- [ ] La grille affiche 2 colonnes
- [ ] Le layout général reste cohérent

**Tests sur desktop (> 1024px):**
- [ ] La grille affiche 2-3 colonnes selon l'espace
- [ ] Le profil est centré avec max-width: 900px

### 5. Tests de Validation

**Champs requis:**
1. Tenter de soumettre le formulaire d'édition avec des champs vides

**Vérifications:**
- [ ] Les champs requis empêchent la soumission
- [ ] Des messages de validation HTML5 apparaissent

**Format email:**
1. Entrer un email invalide (ex: "test@")
2. Tenter de soumettre

**Vérifications:**
- [ ] Message de validation HTML5 pour format email invalide

### 6. Tests d'Intégration

**Scénario complet:**
1. Se connecter
2. Aller sur le profil
3. Modifier plusieurs informations
4. Sauvegarder
5. Se déconnecter
6. Se reconnecter
7. Vérifier que les modifications sont persistées
8. Changer le mot de passe
9. Se déconnecter
10. Se reconnecter avec le nouveau mot de passe

**Vérifications:**
- [ ] Toutes les étapes fonctionnent correctement
- [ ] Les données sont persistées en base de données
- [ ] L'authentification fonctionne avec le nouveau mot de passe

## Tests de Sécurité

### 1. Test sans authentification

```bash
curl -X PUT "http://localhost:8000/api/users/me/password" \
  -H "Content-Type: application/json" \
  -d '{
    "current_password": "test",
    "new_password": "newtest123"
  }'
```

**Résultat attendu:** `401 UNAUTHORIZED`

### 2. Test avec token expiré ou invalide

```bash
curl -X PUT "http://localhost:8000/api/users/me/password" \
  -H "Authorization: Bearer invalid_token" \
  -H "Content-Type: application/json" \
  -d '{
    "current_password": "test",
    "new_password": "newtest123"
  }'
```

**Résultat attendu:** `401 UNAUTHORIZED`

### 3. Test SQL Injection

Essayer d'injecter du SQL dans les champs:
- `' OR '1'='1`
- `admin'--`
- `'; DROP TABLE users;--`

**Résultat attendu:** Les requêtes sont paramétrées, pas d'injection possible

### 4. Test XSS

Essayer d'injecter du JavaScript:
- `<script>alert('XSS')</script>`
- `<img src=x onerror=alert('XSS')>`

**Résultat attendu:** Le contenu est échappé, pas d'exécution de code

## Checklist Finale

### Backend
- [ ] Route `/api/users/me/password` fonctionne
- [ ] Route `/api/users/me` (PUT) fonctionne
- [ ] Validation des mots de passe fonctionne
- [ ] Hachage Argon2 appliqué
- [ ] Erreurs appropriées retournées

### Frontend
- [ ] Affichage du profil complet
- [ ] Édition du profil
- [ ] Changement de mot de passe
- [ ] Gestion des erreurs
- [ ] Messages de succès
- [ ] Design responsive
- [ ] Animations et transitions
- [ ] Aucune erreur console

### Base de données
- [ ] Les modifications sont persistées
- [ ] Les mots de passe sont hachés en base
- [ ] Les timestamps sont mis à jour

## Problèmes Connus et Solutions

### Problème: "body_fat_percentage" vs "body_fat"

Si vous rencontrez une erreur concernant le champ de masse grasse:
- Vérifier que le modèle User utilise bien `body_fat` dans la base
- Vérifier que les schémas Pydantic utilisent `body_fat_percentage`
- S'assurer de la cohérence entre les deux

### Problème: Format de date

Si la date de naissance pose problème:
- S'assurer qu'elle est au format ISO avec timezone: `2024-01-15T00:00:00Z`
- Vérifier la conversion côté frontend: `new Date(editForm.value.birthdate + 'T00:00:00').toISOString()`

### Problème: Token expiré

Si le token expire pendant les tests:
- Se reconnecter pour obtenir un nouveau token
- Augmenter temporairement `ACCESS_TOKEN_EXPIRE_MINUTES` pour les tests

## Rapports de Bugs

Si vous trouvez des bugs pendant les tests, documentez:
1. Étapes pour reproduire
2. Résultat attendu
3. Résultat obtenu
4. Messages d'erreur (console et réseau)
5. Environnement (navigateur, OS, etc.)