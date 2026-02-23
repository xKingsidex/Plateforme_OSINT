"""
SQLAlchemy models for OSINT Platform
"""
from sqlalchemy import Column, String, Float, DateTime, JSON, ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
from models.database import Base


class Investigation(Base):
    """Modèle pour une investigation OSINT"""

    __tablename__ = 'investigations'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    target_type = Column(String(50), nullable=False)  # 'ip', 'domain', 'email', 'username'
    target_value = Column(String(255), nullable=False)
    status = Column(String(50), default='pending')  # 'pending', 'running', 'completed', 'failed'
    risk_score = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Investigation(id={self.id}, target={self.target_value}, status={self.status})>"


class CollectedData(Base):
    """Modèle pour les données collectées par les scrapers"""

    __tablename__ = 'collected_data'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    investigation_id = Column(UUID(as_uuid=True), ForeignKey('investigations.id'), nullable=False)
    source = Column(String(100), nullable=False)  # 'shodan', 'github', 'twitter', etc.
    data_type = Column(String(50))  # 'ip_scan', 'profile', 'leak', etc.
    raw_data = Column(JSON)  # Données brutes du scraper
    processed_data = Column(JSON)  # Données traitées/parsed
    risk_level = Column(String(20))  # 'low', 'medium', 'high', 'critical'
    ai_confidence = Column(Float)  # Score de confiance de l'IA (0.0 - 1.0)
    collected_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<CollectedData(id={self.id}, source={self.source}, risk={self.risk_level})>"


class Alert(Base):
    """Modèle pour les alertes générées automatiquement"""

    __tablename__ = 'alerts'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    investigation_id = Column(UUID(as_uuid=True), ForeignKey('investigations.id'), nullable=False)
    severity = Column(String(20), nullable=False)  # 'low', 'medium', 'high', 'critical'
    alert_type = Column(String(100), nullable=False)  # 'leaked_password', 'exposed_port', etc.
    title = Column(String(255), nullable=False)
    description = Column(Text)
    evidence = Column(JSON)  # Preuves/détails de l'alerte
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Alert(id={self.id}, severity={self.severity}, type={self.alert_type})>"
