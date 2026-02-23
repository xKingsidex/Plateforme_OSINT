# ═══════════════════════════════════════════════════════════════
# OSINT Platform - Frontend Dockerfile
# ═══════════════════════════════════════════════════════════════

FROM nginx:alpine

# Metadata
LABEL maintainer="OSINT Platform"
LABEL description="Frontend web pour la plateforme OSINT"

# Copier les fichiers du frontend
COPY . /usr/share/nginx/html/

# Copier la configuration Nginx personnalisée
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Exposer le port
EXPOSE 80

# Démarrer Nginx
CMD ["nginx", "-g", "daemon off;"]
