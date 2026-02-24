"""
═══════════════════════════════════════════════════════════════
OSINT SERVICES MODULE
Modules OSINT avancés pour la collecte d'intelligence
═══════════════════════════════════════════════════════════════
"""

from .name_variations import NameVariationsGenerator
from .google_dorking import GoogleDorkingEngine
from .harvester_engine import HarvesterEngine, EmailValidator
from .data_correlation import DataCorrelationEngine, OSINTEntity
from .advanced_osint_engine import AdvancedOSINTEngine

__all__ = [
    'NameVariationsGenerator',
    'GoogleDorkingEngine',
    'HarvesterEngine',
    'EmailValidator',
    'DataCorrelationEngine',
    'OSINTEntity',
    'AdvancedOSINTEngine',
]

__version__ = '2.0.0'
__author__ = 'OSINT Platform Team'
