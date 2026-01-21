#!/usr/bin/env python3
"""Script to test API keys configuration"""

import os
from dotenv import load_dotenv
import sys

load_dotenv()

def test_shodan():
    """Test Shodan API"""
    api_key = os.getenv('SHODAN_API_KEY')
    if not api_key or api_key == 'your_shodan_api_key_here':
        return False, "❌ Shodan API key not configured"

    try:
        import shodan
        api = shodan.Shodan(api_key)
        api.info()
        return True, "✅ Shodan API key valid"
    except Exception as e:
        return False, f"❌ Shodan API error: {str(e)}"

def test_virustotal():
    """Test VirusTotal API"""
    api_key = os.getenv('VIRUSTOTAL_API_KEY')
    if not api_key or api_key == 'your_virustotal_api_key_here':
        return False, "❌ VirusTotal API key not configured"

    try:
        import requests
        headers = {'x-apikey': api_key}
        resp = requests.get('https://www.virustotal.com/api/v3/users/current', headers=headers)
        if resp.status_code == 200:
            return True, "✅ VirusTotal API key valid"
        else:
            return False, f"❌ VirusTotal API error: {resp.status_code}"
    except Exception as e:
        return False, f"❌ VirusTotal API error: {str(e)}"

def test_github():
    """Test GitHub API"""
    token = os.getenv('GITHUB_TOKEN')
    if not token or token == 'ghp_your_github_token_here':
        return False, "❌ GitHub token not configured"

    try:
        import requests
        headers = {'Authorization': f'token {token}'}
        resp = requests.get('https://api.github.com/user', headers=headers)
        if resp.status_code == 200:
            return True, f"✅ GitHub token valid (user: {resp.json()['login']})"
        else:
            return False, f"❌ GitHub API error: {resp.status_code}"
    except Exception as e:
        return False, f"❌ GitHub API error: {str(e)}"

def test_database():
    """Test database connection"""
    try:
        from sqlalchemy import create_engine
        db_url = os.getenv('DATABASE_URL')
        if not db_url:
            return False, "❌ DATABASE_URL not configured"

        engine = create_engine(db_url)
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        return True, "✅ PostgreSQL connection successful"
    except Exception as e:
        return False, f"❌ PostgreSQL error: {str(e)}"

def test_neo4j():
    """Test Neo4j connection"""
    try:
        from neo4j import GraphDatabase
        uri = os.getenv('NEO4J_URI')
        user = os.getenv('NEO4J_USER')
        password = os.getenv('NEO4J_PASSWORD')

        if not all([uri, user, password]):
            return False, "❌ Neo4j credentials not configured"

        driver = GraphDatabase.driver(uri, auth=(user, password))
        with driver.session() as session:
            session.run("RETURN 1")
        driver.close()
        return True, "✅ Neo4j connection successful"
    except Exception as e:
        return False, f"❌ Neo4j error: {str(e)}"

def test_redis():
    """Test Redis connection"""
    try:
        import redis
        url = os.getenv('REDIS_URL')
        if not url:
            return False, "❌ REDIS_URL not configured"

        r = redis.from_url(url)
        r.ping()
        return True, "✅ Redis connection successful"
    except Exception as e:
        return False, f"❌ Redis error: {str(e)}"

def main():
    print("🔍 Testing API Keys and Services Configuration\n")
    print("=" * 60)

    tests = [
        ("Database (PostgreSQL)", test_database),
        ("Neo4j", test_neo4j),
        ("Redis", test_redis),
        ("Shodan API", test_shodan),
        ("VirusTotal API", test_virustotal),
        ("GitHub API", test_github),
    ]

    results = []
    for name, test_func in tests:
        print(f"\n{name}:")
        success, message = test_func()
        print(f"  {message}")
        results.append(success)

    print("\n" + "=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"\n📊 Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed! You're ready to go.")
        sys.exit(0)
    else:
        print("⚠️  Some tests failed. Please check your configuration.")
        sys.exit(1)

if __name__ == "__main__":
    main()
