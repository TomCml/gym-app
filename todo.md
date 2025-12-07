1. 🗓️ Calendrier d'Historique
   Description : Créer une nouvelle vue History.vue qui affiche un calendrier. Les jours où un entraînement a été effectué sont mis en surbrillance. En cliquant sur un jour, l'utilisateur voit un résumé des exercices et des performances de ce jour-là.

Pourquoi ? C'est très visuel et gratifiant. L'utilisateur peut voir sa régularité d'un seul coup d'œil et accéder facilement à ses anciens entraînements.

Complexité estimée : Moyenne. (Nécessite un appel API pour regrouper les logs par date et l'utilisation d'une petite librairie de calendrier sur le frontend).

2. 🏆 Suivi des Records Personnels (PRs)
   Description : Pour chaque exercice, l'application détecte et sauvegarde automatiquement la meilleure performance de l'utilisateur (par exemple, le poids le plus lourd soulevé pour 1, 5 ou 10 répétitions). Ces records pourraient être affichés sur la page d'un exercice ou sur le profil.

Pourquoi ? C'est l'un des aspects les plus motivants de la musculation. Voir ses records progresser est un moteur de motivation énorme.

Complexité estimée : Moyenne. (Nécessite une logique sur le backend pour interroger la table user_exercise_logs et trouver les max(weight) pour un nombre de reps donné).

3. 🔥 Compteur de "Séries" (Streak)
   Description : Sur la page d'accueil, afficher une petite icône (comme une flamme) et un nombre indiquant depuis combien de semaines consécutives l'utilisateur a fait au moins une séance. Le compteur se réinitialise s'il manque une semaine.

Pourquoi ? La "gamification" est un outil psychologique puissant pour encourager la régularité et la rétention des utilisateurs. Personne n'aime "briser sa série".

Complexité estimée : Faible à Moyenne. (Nécessite une logique sur le backend pour analyser les dates des logs de l'utilisateur).

4. ⏱️ Minuteur d'Exercice (pour les planches, etc.)
   Description : Dans l'écran LiveWorkout.vue, si un exercice est basé sur la durée (comme le gainage/planche), au lieu des champs "poids/reps", l'interface affiche un minuteur et un bouton "Start/Stop". La durée effectuée est ensuite enregistrée dans les logs.

Pourquoi ? Votre application ne gère actuellement que les exercices basés sur les répétitions. Cela étendrait sa capacité à tous les types d'exercices isométriques et de cardio à durée fixe.

Complexité estimée : Faible. (Principalement une modification de l'interface dans LiveWorkout.vue et l'utilisation du champ duration_seconds que votre base de données possède déjà).

5. 📝 Notes sur les Entraînements
   Description : Ajouter un champ "Notes" sur les vues NewWorkout et WorkoutEdit. Ces notes pourraient être des indications générales sur l'entraînement (ex: "Focus sur la contraction", "Séance légère aujourd'hui").

Pourquoi ? Permet à l'utilisateur de contextualiser ses séances et de se souvenir de ses intentions ou de son état de forme ce jour-là.

Complexité estimée : Faible. (Nécessite juste d'ajouter la colonne notes à la table workouts et les champs correspondants).

6. Mettre en place cache backend

7. Mettre en place cache frontend

8. Fix le fait qu'on voit encore le workout à faire dans liveWorkout si on l'a déjà fait
