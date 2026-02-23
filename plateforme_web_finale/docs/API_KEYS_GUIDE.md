# 🔑 Guide de Gestion des API Keys

## 📋 Table des Matières
- [Obtenir vos API Keys](#obtenir-vos-api-keys)
- [Configuration Locale](#configuration-locale)
- [Sécurité](#sécurité)
- [APIs Gratuites vs Payantes](#apis-gratuites-vs-payantes)

---

## 🎯 Obtenir vos API Keys

### 1. **NumVerify** (Vérification de numéros de téléphone)
- 🌐 Site: https://numverify.com/
- 📦 Plan gratuit: 100 requêtes/mois
- 🔑 Inscription:
  ```
  1. Créer un compte sur numverify.com
  2. Aller dans "Dashboard" → "API Access Key"
  3. Copier votre clé API
  ```

### 2. **Have I Been Pwned** (Détection de fuites de données)
- 🌐 Site: https://haveibeenpwned.com/API/Key
- 💰 Payant: ~$3.50/mois
- 🔑 Inscription:
  ```
  1. Acheter une clé API sur haveibeenpwned.com
  2. Recevoir la clé par email
  3. Utiliser la clé dans vos requêtes
  ```

### 3. **Shodan** (Recherche d'appareils IoT)
- 🌐 Site: https://account.shodan.io/
- 📦 Plan gratuit: 100 crédits
- 🔑 Inscription:
  ```
  1. Créer un compte Shodan
  2. Aller dans "Account" → "API Key"
  3. Copier votre clé
  ```

### 4. **VirusTotal** (Analyse de malware)
- 🌐 Site: https://www.virustotal.com/
- 📦 Plan gratuit: 500 requêtes/jour
- 🔑 Inscription:
  ```
  1. Créer un compte VirusTotal
  2. Aller dans profil → "API Key"
  3. Copier votre clé
  ```

### 5. **Hunter.io** (Recherche d'emails)
- 🌐 Site: https://hunter.io/
- 📦 Plan gratuit: 25 requêtes/mois
- 🔑 Inscription:
  ```
  1. Créer un compte Hunter.io
  2. Aller dans "API" section
  3. Copier votre clé API
  ```

### 6. **GitHub Token** (Accès API GitHub)
- 🌐 Site: https://github.com/settings/tokens
- 📦 Gratuit avec limitations
- 🔑 Création:
  ```
  1. GitHub → Settings → Developer settings
  2. Personal access tokens → Generate new token
  3. Permissions minimales: public_repo (lecture seule)
  4. ⚠️ JAMAIS de permissions write/admin !
  ```

---

## ⚙️ Configuration Locale

### Étape 1: Copier le fichier d'exemple

```bash
# Copier le template
cp .env.example .env
```

### Étape 2: Éditer votre fichier `.env`

```bash
# Ouvrir avec votre éditeur favori
notepad .env       # Windows
nano .env          # Linux
code .env          # VS Code
```

### Étape 3: Remplir vos clés

```env
# ✅ EXEMPLE - Remplacez avec VOS vraies clés
NUMVERIFY_API_KEY=abc123def456ghi789
HIBP_API_KEY=1234567890abcdef1234567890abcdef
SHODAN_API_KEY=ABCDEF1234567890
VIRUSTOTAL_API_KEY=your_actual_virustotal_key_here
GITHUB_TOKEN=ghp_YourActualGitHubTokenHere123456789
```

### ✅ Vérification

```python
# Tester que les clés sont chargées
from dotenv import load_dotenv
import os

load_dotenv()

print("NumVerify:", "✅" if os.getenv("NUMVERIFY_API_KEY") else "❌")
print("HIBP:", "✅" if os.getenv("HIBP_API_KEY") else "❌")
```

---

## 🔒 Sécurité

### ⚠️ À NE JAMAIS FAIRE

❌ **NE JAMAIS commit le fichier `.env`**
```bash
# ❌ DANGER !
git add .env
git commit -m "Add API keys"  # 🚨 JAMAIS !
```

❌ **NE JAMAIS hardcoder les clés dans le code**
```python
# ❌ MAL
API_KEY = "abc123def456"  # 🚨 Visible dans Git !

# ✅ BIEN
API_KEY = os.getenv("NUMVERIFY_API_KEY")
```

❌ **NE JAMAIS partager vos clés**
- Pas sur Discord, Slack, forums
- Pas dans les screenshots
- Pas dans les logs

### ✅ Bonnes Pratiques

1. **Utiliser `.env` pour les clés locales**
   ```bash
   # Le fichier .env est dans .gitignore
   cat .gitignore | grep .env
   ```

2. **Utiliser `.env.example` comme template**
   ```bash
   # .env.example = template SANS vraies clés
   # Commit ce fichier pour documenter les variables nécessaires
   git add .env.example
   ```

3. **Permissions minimales**
   ```
   🔑 Principe: Donner le MINIMUM de permissions
   - GitHub token: Lecture seule (public_repo)
   - API keys: Créer des clés séparées par projet
   ```

4. **Rotation régulière**
   ```
   🔄 Changer vos clés tous les 3-6 mois
   📅 Si une clé fuite: Révoquer IMMÉDIATEMENT
   ```

5. **Monitoring**
   ```
   📊 Surveiller l'utilisation de vos API
   - Alertes si usage anormal
   - Logs des requêtes
   ```

---

## 💰 APIs Gratuites vs Payantes

### 🆓 APIs Gratuites (avec limitations)

| Service       | Plan Gratuit          | Limitations                |
|---------------|-----------------------|----------------------------|
| NumVerify     | ✅ 100 req/mois       | Pas de lookup avancé       |
| VirusTotal    | ✅ 500 req/jour       | Rate limit: 4 req/min      |
| Shodan        | ✅ 100 crédits        | Pas de scan complet        |
| Hunter.io     | ✅ 25 req/mois        | Emails limités             |
| GitHub API    | ✅ 5000 req/heure     | Auth requise               |

### 💎 APIs Payantes (recommandées pour production)

| Service       | Prix              | Avantages                     |
|---------------|-------------------|-------------------------------|
| HIBP          | ~$3.50/mois       | Accès complet aux breaches    |
| Shodan        | $59/mois          | Scans illimités               |
| NumVerify     | $9.99/mois        | 10,000 requêtes               |

---

## 🧪 Tester vos API Keys

### Script de Test

Créez `test_apis.py`:

```python
#!/usr/bin/env python3
import os
import requests
from dotenv import load_dotenv

load_dotenv()

def test_numverify():
    api_key = os.getenv("NUMVERIFY_API_KEY")
    if not api_key:
        return "❌ Clé manquante"

    url = f"http://apilayer.net/api/validate?access_key={api_key}&number=14158586273"
    response = requests.get(url)

    return "✅ OK" if response.status_code == 200 else f"❌ Erreur {response.status_code}"

def test_shodan():
    api_key = os.getenv("SHODAN_API_KEY")
    if not api_key:
        return "❌ Clé manquante"

    url = f"https://api.shodan.io/api-info?key={api_key}"
    response = requests.get(url)

    return "✅ OK" if response.status_code == 200 else f"❌ Erreur {response.status_code}"

if __name__ == "__main__":
    print("🧪 Test des API Keys")
    print("=" * 40)
    print(f"NumVerify: {test_numverify()}")
    print(f"Shodan: {test_shodan()}")
```

### Exécuter

```bash
python test_apis.py
```

---

## 📚 Ressources

- 📖 [12 Factor App - Config](https://12factor.net/config)
- 🔐 [OWASP - Secrets Management](https://owasp.org/www-community/vulnerabilities/Use_of_hard-coded_password)
- 🛡️ [GitHub - Removing sensitive data](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)

---

## ❓ FAQ

**Q: Puis-je partager mon fichier `.env` ?**
❌ Non, JAMAIS. C'est comme donner votre mot de passe.

**Q: Comment savoir si ma clé a fuité ?**
- Surveiller l'usage dans les dashboards API
- Utiliser GitHub Secret Scanning
- Vérifier les logs de connexion

**Q: Que faire si ma clé a fuité ?**
1. 🚨 Révoquer la clé IMMÉDIATEMENT
2. 🔄 Générer une nouvelle clé
3. 🔍 Vérifier l'historique Git (git log)
4. 🧹 Nettoyer l'historique si nécessaire

**Q: Combien de clés dois-je avoir ?**
💡 Une clé par projet/environnement:
- `dev-project-a`
- `prod-project-a`
- `test-project-b`

---

## 🎯 Checklist de Sécurité

- [ ] ✅ `.env` est dans `.gitignore`
- [ ] ✅ `.env.example` n'a PAS de vraies clés
- [ ] ✅ Permissions minimales sur les tokens
- [ ] ✅ Rotation des clés tous les 3-6 mois
- [ ] ✅ Monitoring activé
- [ ] ✅ Tests API fonctionnels
- [ ] ✅ Documentation à jour

---

**🔐 Rappel**: La sécurité est la PRIORITÉ #1 !
