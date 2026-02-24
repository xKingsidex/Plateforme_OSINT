# 🚀 GUIDE DE LANCEMENT - WINDOWS

## 📋 ÉTAPE PAR ÉTAPE

### ✅ 1. PRÉREQUIS

Assurez-vous d'avoir:
- ✅ Python 3.8+ installé
- ✅ Git Bash ou WSL installé

Vérifiez:
```bash
python --version
```

---

### ✅ 2. INSTALLATION

**Ouvrez un terminal dans le dossier `osint_platform/`:**

```bash
# Installer les dépendances
pip install -r requirements.txt
```

---

### ✅ 3. CONFIGURATION DES CLÉS API

**Copiez `.env.example` vers `.env`:**

```bash
cp .env.example .env
```

**Éditez `.env` avec un éditeur de texte (Notepad++, VSCode, etc.):**

```env
# Ajoutez vos vraies clés API ici
HIBP_API_KEY=votre_cle_ici
HUNTER_IO_KEY=votre_cle_ici
NUMVERIFY_API_KEY=votre_cle_ici
SHODAN_API_KEY=votre_cle_ici
VIRUSTOTAL_API_KEY=votre_cle_ici
GITHUB_TOKEN=votre_token_ici
```

> ⚠️ **IMPORTANT:** Sans clés API, certaines fonctionnalités seront limitées, mais la recherche username basique fonctionnera quand même !

---

### ✅ 4. LANCEMENT DE LA PLATEFORME

**Vous devez ouvrir DEUX terminaux:**

#### 🟢 Terminal 1 - Backend (API)

```bash
cd osint_platform/backend/api
python main.py
```

**Vous devriez voir:**
```
╔═══════════════════════════════════════════════════════════╗
║   🔍 OSINT INTELLIGENCE PLATFORM - BACKEND API           ║
╚═══════════════════════════════════════════════════════════╝

🚀 Server starting on http://0.0.0.0:8000
📚 API Documentation: http://0.0.0.0:8000/docs
```

**✅ GARDEZ CE TERMINAL OUVERT !**

---

#### 🟢 Terminal 2 - Frontend (Interface Web)

**Ouvrez un NOUVEAU terminal:**

```bash
cd osint_platform/frontend
python -m http.server 3000
```

**Vous devriez voir:**
```
Serving HTTP on 0.0.0.0 port 3000 (http://0.0.0.0:3000/) ...
```

**✅ GARDEZ CE TERMINAL OUVERT !**

---

### ✅ 5. ACCÈS À LA PLATEFORME

**Ouvrez votre navigateur (Chrome, Firefox, Edge) et allez sur:**

```
http://localhost:3000
```

**Vous devriez voir l'interface OSINT professionnelle ! 🎉**

---

## 🧪 TEST DE LA PLATEFORME

### Test 1: Email
```
Entrez: test@example.com
Cliquez sur "🔍 Analyser"
```

### Test 2: Username
```
Entrez: torvalds
Cliquez sur "🔍 Analyser"
```

### Test 3: Téléphone
```
Entrez: +33612345678
Cliquez sur "🔍 Analyser"
```

---

## ❌ PROBLÈMES FRÉQUENTS

### Problème: "python: command not found"
**Solution:** Python n'est pas installé ou pas dans le PATH
```bash
# Téléchargez Python depuis: https://www.python.org/downloads/
# Cochez "Add Python to PATH" lors de l'installation
```

### Problème: "pip: command not found"
**Solution:**
```bash
python -m ensurepip --upgrade
```

### Problème: "Module 'fastapi' not found"
**Solution:** Les dépendances ne sont pas installées
```bash
pip install -r requirements.txt
```

### Problème: Le frontend ne se connecte pas à l'API
**Solution:**
1. Vérifiez que le backend tourne (Terminal 1)
2. Vérifiez l'URL: http://localhost:8000/api/health dans votre navigateur
3. Si ça retourne `{"status":"healthy"}`, c'est bon !

### Problème: "Address already in use"
**Solution:** Le port est déjà utilisé
```bash
# Pour le backend (port 8000):
netstat -ano | findstr :8000
taskkill /PID [PID_NUMBER] /F

# Pour le frontend (port 3000):
netstat -ano | findstr :3000
taskkill /PID [PID_NUMBER] /F
```

---

## 🔑 OÙ OBTENIR LES CLÉS API ?

| Service | URL | Gratuit ? | Limite |
|---------|-----|-----------|--------|
| **HaveIBeenPwned** | https://haveibeenpwned.com/API/Key | ❌ $3.50/mois | Illimité |
| **Hunter.io** | https://hunter.io/ | ✅ Oui | 50/mois |
| **Numverify** | https://numverify.com/ | ✅ Oui | 100/mois |
| **Shodan** | https://account.shodan.io/ | ✅ Oui | 1 scan/mois |
| **VirusTotal** | https://www.virustotal.com/ | ✅ Oui | 4 req/min |
| **GitHub** | https://github.com/settings/tokens | ✅ Oui | 5000/h |

---

## 📸 CAPTURES D'ÉCRAN

### Backend API
```
http://localhost:8000/docs
```
→ Documentation interactive Swagger

### Frontend
```
http://localhost:3000
```
→ Interface OSINT professionnelle

---

## 🎯 UTILISATION AVANCÉE

### Recherche approfondie
Cochez la case **"🚀 Deep Search"** avant de lancer la recherche.

### Export JSON
Cliquez sur **"📋 Copy"** dans la section "Raw JSON Data" pour copier tous les résultats.

### API directe
Utilisez **http://localhost:8000/docs** pour tester l'API directement.

---

## 🛑 ARRÊT DE LA PLATEFORME

**Dans chaque terminal, appuyez sur:**
```
Ctrl + C
```

---

**✅ TOUT EST PRÊT ! BONNE CHASSE OSINT ! 🔍**
