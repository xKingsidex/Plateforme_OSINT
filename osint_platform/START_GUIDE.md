# 🚀 GUIDE DE DÉMARRAGE RAPIDE - OSINT PLATFORM ULTIMATE

## ⚡ INSTALLATION ULTRA-RAPIDE (3 étapes)

### **ÉTAPE 1: Installation automatique**
```bash
cd osint_platform
bash INSTALL_ULTIMATE.sh
```

**Cela installe TOUS les outils :**
- ✅ Sherlock (300+ sites)
- ✅ Maigret (400+ sites)
- ✅ Holehe (120+ sites email)
- ✅ h8mail (breach hunting)
- ✅ Socialscan
- ✅ theHarvester
- ✅ Sublist3r

---

### **ÉTAPE 2: Configuration des clés API**

```bash
# Le script a déjà créé .env pour toi
# Édite-le et ajoute tes clés API

nano .env   # ou: notepad .env sur Windows
```

**Ajoute tes clés (tu les as déjà) :**
```env
# Email OSINT
HUNTER_IO_KEY=ta_cle_hunter

# Domain/IP OSINT
VIRUSTOTAL_API_KEY=ta_cle_virustotal
SHODAN_API_KEY=ta_cle_shodan

# Social OSINT
GITHUB_TOKEN=ton_token_github
```

> 💡 **BON À SAVOIR** : Sherlock, Maigret, Holehe, h8mail, Socialscan fonctionnent **SANS clés API** !

---

### **ÉTAPE 3: Lancement**

**🟢 Terminal 1 - Backend ULTIMATE:**
```bash
cd backend/api
python main_ultimate.py
```

**Tu verras :**
```
╔═══════════════════════════════════════════════════════════╗
║   🔍 OSINT INTELLIGENCE PLATFORM ULTIMATE v4.0.0         ║
║   Maximum OSINT avec TOUS les outils open source         ║
╚═══════════════════════════════════════════════════════════╝

✅ ULTIMATE Tools Enabled:
   📛 USERNAME: Sherlock (300+) + Maigret (400+) + Socialscan
   📧 EMAIL: Holehe (120+) + h8mail + HaveIBeenPwned
   🌐 DOMAIN: Sublist3r + theHarvester + VirusTotal

🎯 TOTAL COVERAGE: 800+ sites web
```

**🟢 Terminal 2 - Frontend:**
```bash
cd frontend
python -m http.server 3000
```

**Puis ouvre ton navigateur:**
```
http://localhost:3000/index_pro.html
```

---

## 🎯 MODES DE RECHERCHE

### **Mode NORMAL (30-60 secondes)**
- ✅ Holehe (120+ sites)
- ✅ Socialscan (6 sites majeurs)
- ✅ APIs basiques

**Utilisation :**
```
Coche: [PRO TOOLS]
Décoche: [DEEP SCAN]
Décoche: [ULTRA DEEP]
```

---

### **Mode DEEP SEARCH (2-3 minutes)**
- ✅ Tout le mode NORMAL
- ✅ **Sherlock** (300+ sites)
- ✅ **theHarvester** (email harvesting)

**Utilisation :**
```
Coche: [PRO TOOLS]
Coche: [DEEP SCAN]
Décoche: [ULTRA DEEP]
```

---

### **Mode ULTRA DEEP (5-10 minutes) 🔥**
- ✅ Tout le mode DEEP
- ✅ **Maigret** (400+ sites - meilleur que Sherlock)
- ✅ **h8mail** (breach hunting complet)

**Utilisation :**
```
Coche: [PRO TOOLS]
Coche: [DEEP SCAN]
Coche: [ULTRA DEEP]
```

> ⚠️ **ATTENTION** : Mode ULTRA DEEP peut prendre **jusqu'à 10 minutes** !

---

## 📊 CE QUE TU VAS OBTENIR

### **Email OSINT:**
```
✅ Holehe: Comptes sur Discord, Spotify, Netflix, GitHub, etc. (120+ sites)
✅ h8mail: Mots de passe dans les breaches
✅ HaveIBeenPwned: Fuites de données détaillées
✅ EmailRep: Score de réputation
```

### **Username OSINT:**
```
✅ Sherlock: 300+ sites (GitHub, Twitter, Instagram, Reddit, etc.)
✅ Maigret: 400+ sites (encore plus complet)
✅ Socialscan: Vérification rapide (6 sites majeurs)
✅ GitHub: Profil complet (repos, followers, etc.)
```

### **Domain OSINT:**
```
✅ Sublist3r: Tous les subdomains
✅ theHarvester: Emails associés au domaine
✅ VirusTotal: Réputation malware
✅ DNS: Tous les enregistrements
✅ SSL: Certificat et validité
```

---

## 🔑 CLÉS API RECOMMANDÉES

| Outil | Nécessaire ? | Gratuit ? | Lien |
|-------|--------------|-----------|------|
| **Sherlock** | ❌ Non | ✅ Gratuit | - |
| **Maigret** | ❌ Non | ✅ Gratuit | - |
| **Holehe** | ❌ Non | ✅ Gratuit | - |
| **h8mail** | ❌ Non | ✅ Gratuit | - |
| **GitHub** | ✅ Recommandé | ✅ Gratuit | https://github.com/settings/tokens |
| **Hunter.io** | ⚠️ Optionnel | ✅ 50/mois | https://hunter.io/ |
| **VirusTotal** | ⚠️ Optionnel | ✅ 4/min | https://www.virustotal.com/ |
| **Shodan** | ⚠️ Optionnel | ✅ 1 scan/mois | https://account.shodan.io/ |

---

## 🧪 EXEMPLES DE TESTS

### **Test 1: Email complet (Mode NORMAL)**
```
Email: test@example.com
Options: [PRO TOOLS] seulement
Temps: ~30 secondes
Résultats: Holehe trouvera les comptes associés
```

### **Test 2: Username exhaustif (Mode DEEP)**
```
Username: torvalds
Options: [PRO TOOLS] + [DEEP SCAN]
Temps: ~2 minutes
Résultats: Sherlock trouvera 40+ profils
```

### **Test 3: Username ULTIME (Mode ULTRA DEEP)**
```
Username: johndoe
Options: [PRO TOOLS] + [DEEP SCAN] + [ULTRA DEEP]
Temps: ~5-10 minutes
Résultats: Maigret trouvera 60+ profils (meilleur que Sherlock)
```

---

## ⚠️ IMPORTANT

1. **Mode ULTRA DEEP est TRÈS LENT** : Réserve-le pour des recherches importantes
2. **Pas besoin de toutes les clés API** : Commence avec GitHub seulement
3. **Sherlock/Maigret/Holehe fonctionnent seuls** : Aucune clé API nécessaire
4. **Respecte la légalité** : Utilise la plateforme de manière éthique

---

## ✅ TOUT EST PRÊT !

**Lance les commandes ci-dessus et profite de la plateforme ULTIMATE ! 🚀**

**Tu as maintenant accès à :**
- 🎯 800+ sites web couverts
- 🛠️ 7 outils OSINT professionnels
- 🎨 Interface terminal cybersécurité
- ⚡ 3 modes de recherche (Normal, Deep, Ultra Deep)

**BON OSINT ! 🔍**
