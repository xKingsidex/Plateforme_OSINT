# 📂 Organisation du projet OSINT

## Structure du projet

\`\`\`
Plateforme_OSINT/
├── 📄 Scripts CLI (Base - Apprentissage étape par étape)
│   ├── osint_person_search.py
│   ├── osint_social_search.py
│   ├── check_apis.py
│   ├── .env (tes clés API)
│   └── ...
│
└── 📂 plateforme_web_finale/    ← VERSION WEB FINALE
    ├── backend/                  API FastAPI
    ├── frontend/                 Interface web
    ├── docker-compose.yml        Orchestration Docker
    ├── start.sh                  Script de démarrage
    └── README.md                 Documentation
\`\`\`

## Utilisation

### Scripts CLI (Apprentissage)
\`\`\`bash
# Rester à la racine
cd Plateforme_OSINT/
python3 osint_person_search.py test@example.com
python3 osint_social_search.py johndoe
\`\`\`

### Plateforme Web Finale
\`\`\`bash
# Aller dans le sous-dossier
cd Plateforme_OSINT/plateforme_web_finale/
./start.sh
# Ouvrir http://localhost:3000
\`\`\`

## Configuration

Le fichier \`.env\` à la racine contient tes clés API.
Il est partagé entre les 2 versions.

---

**Tu peux utiliser les 2 en parallèle ! 🎉**
