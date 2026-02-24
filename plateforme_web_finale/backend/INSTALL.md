# 🚀 GUIDE D'INSTALLATION - PLATEFORME OSINT WEB

## ✅ CE QUE J'AI CORRIGÉ POUR TOI

- ✅ Imports Python réparés
- ✅ Script de lancement créé (`run_app.py`)
- ✅ Requirements minimal créé
- ✅ Chemins PYTHONPATH configurés automatiquement

---

## 📦 INSTALLATION RAPIDE

### **Étape 1 : Aller dans le bon répertoire**

```bash
cd /mnt/c/Users/enzo-/OneDrive/Documents/PST13-4A/OSINT/Plateforme_OSINT/plateforme_web_finale/backend
```

### **Étape 2 : Activer le venv (si pas déjà fait)**

```bash
source /home/enzo/osint-venv/bin/activate
```

### **Étape 3 : Installer les dépendances minimales**

```bash
pip install -r requirements-minimal.txt
```

⏱️ **Durée : 2-3 minutes** (au lieu de 30+ avec tous les packages AI)

### **Étape 4 : Lancer la plateforme !**

```bash
python run_app.py
```

---

## 🎯 ACCÉDER À LA PLATEFORME

Une fois lancée, ouvre ton navigateur :

- **🏠 Accueil API** : http://localhost:8000
- **📚 Documentation interactive** : http://localhost:8000/api/docs
- **💚 Health Check** : http://localhost:8000/api/health

---

## 🧪 TESTER L'API

### **Test 1 : Health Check**

```bash
curl http://localhost:8000/api/health
```

### **Test 2 : Détection automatique**

```bash
curl -X POST http://localhost:8000/api/detect \
  -H "Content-Type: application/json" \
  -d '{"query": "john.doe@gmail.com"}'
```

### **Test 3 : Recherche OSINT complète**

```bash
curl -X POST http://localhost:8000/api/search \
  -H "Content-Type: application/json" \
  -d '{"query": "johndoe", "deep_search": false}'
```

---

## 🐛 DÉPANNAGE

### Erreur : `ModuleNotFoundError`

**Solution :** Utilise toujours `run_app.py` au lieu de `main.py` directement :

```bash
# ❌ NE PAS FAIRE
python app/main.py

# ✅ FAIRE ÇA
python run_app.py
```

### Erreur : `Port 8000 already in use`

**Solution :** Tuer le processus qui utilise le port :

```bash
# Trouver le processus
lsof -i :8000

# Le tuer
kill -9 <PID>
```

Ou changer le port dans `run_app.py` ligne 62 :
```python
port=8080,  # Au lieu de 8000
```

### Erreur : Dépendances manquantes

**Solution :** Installer le package manquant :

```bash
pip install <nom-du-package>
```

---

## 📊 FONCTIONNALITÉS DISPONIBLES

### ✅ Détection automatique
- Email
- Téléphone
- Nom de personne
- Username
- Adresse IP
- Nom de domaine

### ✅ Recherches OSINT
- **Email** : Validation, recherche de comptes
- **Username** : Recherche sur réseaux sociaux
- **Téléphone** : Parsing international
- **IP** : Géolocalisation (si Shodan configuré)
- **Domaine** : WHOIS, DNS

### 🚧 En développement
- Intégration complète Maigret, Sherlock, Holehe
- Recherche approfondie avec variations
- Corrélation de données
- Export PDF/HTML

---

## 🎉 C'EST PARTI !

**Lance maintenant :**

```bash
python run_app.py
```

Puis ouvre http://localhost:8000/api/docs dans ton navigateur ! 🚀
