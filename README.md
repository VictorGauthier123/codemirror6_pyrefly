# CodeMirror 6 + Pyrefly IDE Demo

Petit prototype d'IDE web Python basé sur CodeMirror 6.

Le projet contient :
- un frontend Angular avec CodeMirror 6 ;
- un backend FastAPI ;
- une connexion WebSocket LSP vers `pyrefly` via `@codemirror/lsp-client`.

## Ce que fait le projet

Aujourd'hui, l'éditeur :
- ouvre un buffer Python ;
- se connecte au backend en WebSocket sur `/lsp` ;
- relaye les messages LSP vers `pyrefly` ;
- récupère l'autocomplétion via `pyrefly`.

## Fichiers intéressants

- [frontend/src/app/editor/editor.ts](/Users/victorgauthier/dev/dev_test/codemirror6/frontend/src/app/editor/editor.ts) : configuration CodeMirror et client LSP.
- [backend/main.py](/Users/victorgauthier/dev/dev_test/codemirror6/backend/main.py) : serveur FastAPI et endpoint WebSocket `/lsp`.
- [backend/pyrefly_lsp.py](/Users/victorgauthier/dev/dev_test/codemirror6/backend/pyrefly_lsp.py) : pont entre WebSocket et processus `pyrefly`.
- [backend/test.py](/Users/victorgauthier/dev/dev_test/codemirror6/backend/test.py) : petit script manuel pour tester `pyrefly` en direct.
- [backend/pyrefly.toml](/Users/victorgauthier/dev/dev_test/codemirror6/backend/pyrefly.toml) : configuration `pyrefly`.
- [backend/requirements.txt](/Users/victorgauthier/dev/dev_test/codemirror6/backend/requirements.txt) : dépendances Python du backend.

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
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Le backend démarre sur `http://localhost:8000`.

## Notes

- `pyrefly` doit être installé dans l'environnement Python du backend.
- Le frontend utilise maintenant `@codemirror/lsp-client`, plus le vieux provider `fetch` pour l'autocomplete.
- Le fichier [backend/test.py](/Users/victorgauthier/dev/dev_test/codemirror6/backend/test.py) permet de tester rapidement que `pyrefly lsp` répond bien.
