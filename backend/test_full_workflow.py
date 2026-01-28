#!/usr/bin/env python3
"""
Test complet : Investigation -> Scraping -> Stockage DB
"""
import asyncio
from models.database import SessionLocal
from models.models import Investigation, CollectedData, Alert
from scrapers.shodan_scraper import ShodanScraper
from datetime import datetime


async def test_full_workflow():
    """Test du workflow complet"""

    print("=" * 70)
    print("🧪 TEST DU WORKFLOW COMPLET")
    print("=" * 70)

    # 1. Créer une investigation
    print("\n📝 Étape 1 : Création de l'investigation...")
    db = SessionLocal()

    investigation = Investigation(
        name="Test Shodan - Google DNS",
        target_type="ip",
        target_value="8.8.8.8",
        status="pending"
    )
    db.add(investigation)
    db.commit()
    db.refresh(investigation)

    print(f"✅ Investigation créée : {investigation.id}")
    print(f"   Target : {investigation.target_value}")
    print(f"   Type : {investigation.target_type}")

    # 2. Mettre à jour le statut
    investigation.status = "running"
    db.commit()

    # 3. Lancer le scraper Shodan
    print("\n🔍 Étape 2 : Lancement du scraper Shodan...")
    scraper = ShodanScraper()
    result = await scraper.process('8.8.8.8')

    if result['status'] == 'success':
        data = result['data']

        print(f"✅ Scraping réussi")
        print(f"   IP : {data.get('ip')}")
        print(f"   Organisation : {data.get('organization')}")
        print(f"   Pays : {data.get('country')}")
        print(f"   Ports ouverts : {data.get('ports_open')}")
        print(f"   Score de risque : {data.get('risk_score')}/100")

        # 4. Sauvegarder les données collectées
        print("\n💾 Étape 3 : Sauvegarde dans la base de données...")
        collected = CollectedData(
            investigation_id=investigation.id,
            source='shodan',
            data_type='ip_scan',
            raw_data=result,
            processed_data=data,
            risk_level=data.get('risk_level', 'unknown'),
            ai_confidence=None,  # Pas encore d'IA
            collected_at=datetime.utcnow()
        )
        db.add(collected)

        # 5. Créer des alertes si nécessaire
        print("\n⚠️  Étape 4 : Génération des alertes...")

        alerts_created = 0

        # Alerte si vulnérabilités détectées
        if data.get('vulnerabilities'):
            alert = Alert(
                investigation_id=investigation.id,
                severity='high',
                alert_type='vulnerabilities_detected',
                title=f"{len(data['vulnerabilities'])} vulnérabilités détectées",
                description=f"Vulnérabilités CVE trouvées sur l'IP {data['ip']}",
                evidence={'vulnerabilities': data['vulnerabilities'][:10]}
            )
            db.add(alert)
            alerts_created += 1
            print(f"   🚨 Alerte : Vulnérabilités détectées ({len(data['vulnerabilities'])})")

        # Alerte si ports critiques ouverts
        critical_ports = {21: 'FTP', 22: 'SSH', 23: 'Telnet', 3389: 'RDP', 445: 'SMB'}
        open_critical = [p for p in data.get('ports_open', []) if p in critical_ports]

        if open_critical:
            ports_info = [f"{p} ({critical_ports[p]})" for p in open_critical]
            alert = Alert(
                investigation_id=investigation.id,
                severity='medium',
                alert_type='critical_ports_open',
                title=f"{len(open_critical)} port(s) critique(s) ouvert(s)",
                description=f"Ports sensibles détectés : {', '.join(ports_info)}",
                evidence={'ports': open_critical}
            )
            db.add(alert)
            alerts_created += 1
            print(f"   ⚠️  Alerte : Ports critiques ouverts ({len(open_critical)})")

        # Alerte si score de risque élevé
        if data.get('risk_score', 0) >= 50:
            alert = Alert(
                investigation_id=investigation.id,
                severity='high',
                alert_type='high_risk_score',
                title=f"Score de risque élevé : {data['risk_score']}/100",
                description="L'IP présente un niveau de risque important",
                evidence={'score': data['risk_score']}
            )
            db.add(alert)
            alerts_created += 1
            print(f"   🔴 Alerte : Score de risque élevé")

        if alerts_created == 0:
            print(f"   ✅ Aucune alerte (tout semble normal)")

        # 6. Mettre à jour l'investigation
        print("\n📊 Étape 5 : Mise à jour de l'investigation...")
        investigation.risk_score = data.get('risk_score', 0)
        investigation.status = 'completed'
        investigation.updated_at = datetime.utcnow()

        db.commit()

        print(f"✅ Investigation terminée")
        print(f"   Status : {investigation.status}")
        print(f"   Risk Score : {investigation.risk_score}/100")

        # 7. Afficher le résumé
        print("\n" + "=" * 70)
        print("📋 RÉSUMÉ DE L'INVESTIGATION")
        print("=" * 70)

        print(f"\n🎯 Investigation : {investigation.name}")
        print(f"   ID : {investigation.id}")
        print(f"   Target : {investigation.target_value}")
        print(f"   Status : {investigation.status}")
        print(f"   Risk Score : {investigation.risk_score}/100")
        print(f"   Créée le : {investigation.created_at.strftime('%Y-%m-%d %H:%M:%S')}")

        print(f"\n📦 Données collectées : 1 source")
        print(f"   - Shodan : {len(data.get('ports_open', []))} ports ouverts, "
              f"{len(data.get('vulnerabilities', []))} vulnérabilités")

        print(f"\n⚠️  Alertes générées : {alerts_created}")

        # Récupérer toutes les alertes
        all_alerts = db.query(Alert).filter(
            Alert.investigation_id == investigation.id
        ).all()

        for alert in all_alerts:
            severity_emoji = {
                'low': '🟢',
                'medium': '🟡',
                'high': '🔴',
                'critical': '🔥'
            }
            print(f"   {severity_emoji.get(alert.severity, '⚪')} [{alert.severity.upper()}] {alert.title}")

        print("\n" + "=" * 70)
        print("✅ TEST COMPLET RÉUSSI !")
        print("=" * 70)

    else:
        print(f"❌ Erreur lors du scraping : {result.get('error')}")
        investigation.status = 'failed'
        db.commit()

    db.close()


if __name__ == "__main__":
    asyncio.run(test_full_workflow())
