# ═══════════════════════════════════════════════════════════════
# OSINT Platform - Backend Dockerfile
# ═══════════════════════════════════════════════════════════════

FROM python:3.11-slim

# Metadata
LABEL maintainer="OSINT Platform"
LABEL description="Backend API pour la plateforme OSINT"

# Variables d'environnement
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Créer le répertoire de travail
WORKDIR /app

# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copier les requirements
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copier le code de l'application
COPY . .

# Créer un utilisateur non-root
RUN useradd -m -u 1000 osint && \
    chown -R osint:osint /app

USER osint

# Exposer le port
EXPOSE 8000

# Commande de démarrage
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
