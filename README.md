# CodeMirror 6 IDE Demo

Petit prototype d'IDE web basé sur CodeMirror 6.

Le projet contient :
- un frontend Angular avec un éditeur Python CodeMirror 6 ;
- un backend FastAPI ;
- un endpoint de complétion Python simple, prévu comme base avant une intégration LSP plus complète avec Pyrefly.

## Fichiers intéressants

- [frontend/src/app/editor/editor.ts](/Users/victorgauthier/dev/dev_test/codemirror6/frontend/src/app/editor/editor.ts) : configuration principale de l'éditeur CodeMirror.
- [backend/main.py](/Users/victorgauthier/dev/dev_test/codemirror6/backend/main.py) : API FastAPI et endpoint de complétion.
- [backend/pyrefly.toml](/Users/victorgauthier/dev/dev_test/codemirror6/backend/pyrefly.toml) : configuration liée à Pyrefly. (pas encore configuré)


## Lancer le projet

### Frontend

```bash
cd frontend
npm install
npm start
```

Le frontend démarre sur `http://localhost:4200`.

### Backend

```bash
cd backend
uvicorn main:app --reload
```

Le backend démarre sur `http://localhost:8000`.

## État actuel

Aujourd'hui :
- l'éditeur affiche un buffer Python dans CodeMirror 6 ;
- l'autocomplétion passe par un `fetch` du frontend vers le backend ;
- l'intégration LSP/Pyrefly reste à brancher.
