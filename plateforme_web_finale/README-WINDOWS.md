# 🪟 Guide d'utilisation des outils OSINT sous Windows

## 🎯 Situation actuelle

Vous êtes sur **Windows avec Docker Desktop**. Les outils OSINT sont installés dans un **conteneur Linux Docker**.

## 🚀 Utilisation rapide

### **1️⃣ Trouver le nom de votre conteneur**

Ouvrez PowerShell et tapez :

```powershell
docker ps
```

Cherchez le conteneur qui contient votre plateforme OSINT (probablement quelque chose comme `plateforme_osint`, `osint-container`, ou un nom similaire).

### **2️⃣ Configurer le script**

Ouvrez `osint-tools.ps1` et modifiez la ligne 11 avec le vrai nom de votre conteneur :

```powershell
$ContainerName = "VOTRE_NOM_DE_CONTENEUR_ICI"
```

### **3️⃣ Utiliser les outils**

```powershell
# Lister les conteneurs Docker
.\osint-tools.ps1 containers

# Tester que tout fonctionne
.\osint-tools.ps1 test

# Rechercher un email
.\osint-tools.ps1 holehe test@gmail.com --only-used

# Rechercher un username
.\osint-tools.ps1 sherlock johndoe

# Ouvrir un shell dans le conteneur
.\osint-tools.ps1 shell
```

## 🔧 Si ça ne marche pas

### **Erreur: "script désactivé"**

Si PowerShell refuse d'exécuter le script, activez l'exécution des scripts :

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### **Erreur: "conteneur introuvable"**

1. Vérifiez que Docker Desktop est lancé
2. Vérifiez le nom du conteneur avec `docker ps`
3. Modifiez `$ContainerName` dans le script

### **Solution alternative : Accès direct**

Si le script PowerShell ne marche pas, accédez directement au conteneur :

```powershell
# Remplacez NOM_CONTENEUR par le vrai nom
docker exec -it NOM_CONTENEUR bash

# Une fois dans le conteneur :
cd /home/user/Plateforme_OSINT/plateforme_web_finale
./osint-tools.sh test
./osint-tools.sh holehe test@gmail.com --only-used
./osint-tools.sh sherlock johndoe
```

## 📊 Outils disponibles

| Outil | Sites | Description |
|-------|-------|-------------|
| **Holehe** | 121 sites | Recherche d'emails (Amazon, Twitter, Netflix, etc.) |
| **Sherlock** | 300+ sites | Recherche d'usernames (GitHub, Instagram, Reddit, etc.) |
| **Maigret** | 1500+ sites | Recherche avancée avec extraction de données |

## 💡 Conseils

- **Performance** : Les recherches prennent entre 10s et 2min selon l'outil
- **Rate limiting** : Certains sites limitent les requêtes. Utilisez `--only-used` pour voir seulement les résultats positifs
- **Exports** : Sherlock peut exporter en JSON, CSV ou XLSX avec les options `--json`, `--csv`, `--xlsx`

## 🆘 Support

Si vous avez des problèmes, ouvrez un shell dans le conteneur et testez directement :

```powershell
docker exec -it NOM_CONTENEUR bash
source /home/user/osint-venv/bin/activate
holehe --help
sherlock --help
maigret --help
```
