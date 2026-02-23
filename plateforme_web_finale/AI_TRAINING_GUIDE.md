# 🧠 Guide d'Entraînement IA pour OSINT

## 📚 Table des Matières

1. [Classification de Texte (Risque)](#1-classification-de-risque)
2. [Named Entity Recognition (NER)](#2-named-entity-recognition)
3. [Détection de Faux Profils](#3-détection-de-faux-profils)
4. [Graph Neural Networks](#4-graph-neural-networks)
5. [Datasets & Annotation](#5-datasets--annotation)

---

## 1. Classification de Risque

### Objectif
Classifier automatiquement les données collectées en 4 niveaux de risque :
- **Low** : Informations banales, publiques normales
- **Medium** : Informations sensibles mais pas critiques
- **High** : Données compromises, vulnérabilités
- **Critical** : Menaces immédiates, credentials leakés

### 1.1 Créer le Dataset

```python
# backend/ai/data_preparation/create_risk_dataset.py
import pandas as pd
import json

# Exemples manuels (starter dataset)
data = [
    # LOW RISK
    {"text": "User posted a vacation photo on Instagram", "label": 0},
    {"text": "GitHub profile shows 50 public repositories", "label": 0},
    {"text": "LinkedIn profile: Software Engineer at Google", "label": 0},
    {"text": "Domain registered 5 years ago with valid WHOIS", "label": 0},

    # MEDIUM RISK
    {"text": "Email found in public mailing list archive", "label": 1},
    {"text": "Port 8080 open with HTTP service exposed", "label": 1},
    {"text": "Old social media post reveals home city", "label": 1},
    {"text": "Phone number listed in public directory", "label": 1},

    # HIGH RISK
    {"text": "Email found in 2 data breaches on HIBP", "label": 2},
    {"text": "Open port 3389 (RDP) detected on server", "label": 2},
    {"text": "Credentials posted in Pastebin 2 months ago", "label": 2},
    {"text": "CVE-2021-44228 Log4j vulnerability detected", "label": 2},

    # CRITICAL RISK
    {"text": "Plain text password found in public GitHub commit", "label": 3},
    {"text": "Active exploit code targeting server detected", "label": 3},
    {"text": "Database dump with 10000 user records leaked", "label": 3},
    {"text": "SSH private key exposed in public repository", "label": 3},
]

df = pd.DataFrame(data)
df.to_csv('data/risk_classification_training.csv', index=False)
print(f"✅ Created dataset with {len(df)} examples")
```

**Pour un vrai projet, collectez au moins 1000+ exemples par classe !**

### 1.2 Entraîner le Modèle

```python
# backend/ai/train_risk_classifier.py
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer
)
from datasets import load_dataset
import numpy as np
from sklearn.metrics import accuracy_score, f1_score
import torch

# Configuration
MODEL_NAME = 'distilbert-base-uncased'
NUM_LABELS = 4  # low, medium, high, critical
OUTPUT_DIR = './models/risk_classifier'

# 1. Charger dataset
dataset = load_dataset('csv', data_files='data/risk_classification_training.csv')
dataset = dataset['train'].train_test_split(test_size=0.2, seed=42)

# 2. Tokenizer
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

def tokenize_function(examples):
    return tokenizer(
        examples['text'],
        padding='max_length',
        truncation=True,
        max_length=128
    )

tokenized_datasets = dataset.map(tokenize_function, batched=True)

# 3. Modèle
model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_NAME,
    num_labels=NUM_LABELS
)

# 4. Métriques
def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    return {
        'accuracy': accuracy_score(labels, predictions),
        'f1': f1_score(labels, predictions, average='weighted')
    }

# 5. Training Arguments
training_args = TrainingArguments(
    output_dir=OUTPUT_DIR,
    evaluation_strategy='epoch',
    learning_rate=2e-5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=5,
    weight_decay=0.01,
    save_strategy='epoch',
    load_best_model_at_end=True,
)

# 6. Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets['train'],
    eval_dataset=tokenized_datasets['test'],
    compute_metrics=compute_metrics,
)

# 7. Entraîner
print("🚀 Starting training...")
trainer.train()

# 8. Sauvegarder
model.save_pretrained(OUTPUT_DIR)
tokenizer.save_pretrained(OUTPUT_DIR)
print(f"✅ Model saved to {OUTPUT_DIR}")

# 9. Tester
test_texts = [
    "User has 1000 followers on Twitter",
    "Email appeared in 3 data breaches",
    "API key exposed in public GitHub repo"
]

for text in test_texts:
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=128)
    outputs = model(**inputs)
    probs = torch.softmax(outputs.logits, dim=1)
    predicted_class = torch.argmax(probs).item()

    labels = ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']
    print(f"\nText: {text}")
    print(f"Predicted: {labels[predicted_class]} (confidence: {probs[0][predicted_class]:.2%})")
```

**Lancer l'entraînement :**

```bash
cd backend/ai
python train_risk_classifier.py
```

### 1.3 Utiliser le Modèle en Production

```python
# backend/ai/risk_classifier.py
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

class RiskClassifier:
    def __init__(self, model_path='./models/risk_classifier'):
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_path)
        self.model.eval()
        self.labels = ['low', 'medium', 'high', 'critical']

    def predict(self, text: str):
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            max_length=128
        )

        with torch.no_grad():
            outputs = self.model(**inputs)
            probs = torch.softmax(outputs.logits, dim=1)

        predicted_class = torch.argmax(probs).item()
        confidence = probs[0][predicted_class].item()

        return {
            'risk_level': self.labels[predicted_class],
            'confidence': confidence,
            'probabilities': {
                label: prob.item()
                for label, prob in zip(self.labels, probs[0])
            }
        }

# Test
if __name__ == "__main__":
    classifier = RiskClassifier()

    tests = [
        "Email found in 5 data breaches including Ashley Madison",
        "User has public GitHub profile with 20 repos",
        "SSH server on port 22 with weak authentication"
    ]

    for text in tests:
        result = classifier.predict(text)
        print(f"\n📝 {text}")
        print(f"🎯 Risk: {result['risk_level'].upper()} ({result['confidence']:.1%})")
```

---

## 2. Named Entity Recognition (NER)

### 2.1 Utiliser spaCy pré-entraîné

```python
# backend/ai/ner_extractor.py
import spacy
import re
from typing import Dict, List

class NERExtractor:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_lg")

    def extract_all(self, text: str) -> Dict[str, List[str]]:
        """Extrait toutes les entités"""
        entities = {
            'persons': [],
            'organizations': [],
            'locations': [],
            'emails': [],
            'ips': [],
            'urls': [],
            'phones': [],
            'crypto_addresses': []
        }

        # spaCy NER
        doc = self.nlp(text)
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                entities['persons'].append(ent.text)
            elif ent.label_ == "ORG":
                entities['organizations'].append(ent.text)
            elif ent.label_ in ["GPE", "LOC"]:
                entities['locations'].append(ent.text)

        # Regex pour patterns spécifiques
        entities['emails'] = self._extract_emails(text)
        entities['ips'] = self._extract_ips(text)
        entities['urls'] = self._extract_urls(text)
        entities['phones'] = self._extract_phones(text)
        entities['crypto_addresses'] = self._extract_crypto(text)

        # Dédupliquer
        for key in entities:
            entities[key] = list(set(entities[key]))

        return entities

    def _extract_emails(self, text: str) -> List[str]:
        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return re.findall(pattern, text)

    def _extract_ips(self, text: str) -> List[str]:
        pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
        ips = re.findall(pattern, text)
        # Valider que ce sont de vraies IPs
        valid_ips = []
        for ip in ips:
            parts = ip.split('.')
            if all(0 <= int(part) <= 255 for part in parts):
                valid_ips.append(ip)
        return valid_ips

    def _extract_urls(self, text: str) -> List[str]:
        pattern = r'https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&/=]*)'
        return re.findall(pattern, text)

    def _extract_phones(self, text: str) -> List[str]:
        # US/International formats
        patterns = [
            r'\+?\d{1,3}[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}',
            r'\(\d{3}\)\s?\d{3}-?\d{4}'
        ]
        phones = []
        for pattern in patterns:
            phones.extend(re.findall(pattern, text))
        return phones

    def _extract_crypto(self, text: str) -> List[str]:
        # Bitcoin addresses
        btc_pattern = r'\b[13][a-km-zA-HJ-NP-Z1-9]{25,34}\b'
        # Ethereum addresses
        eth_pattern = r'\b0x[a-fA-F0-9]{40}\b'

        return re.findall(btc_pattern, text) + re.findall(eth_pattern, text)

# Test
if __name__ == "__main__":
    extractor = NERExtractor()

    sample_text = """
    John Doe works at Acme Corporation in New York.
    His email is john.doe@acme.com and phone is +1 (555) 123-4567.
    The server IP is 192.168.1.100 and website is https://acme.com.
    Bitcoin address: 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa
    """

    entities = extractor.extract_all(sample_text)

    print("🔍 EXTRACTED ENTITIES\n")
    for entity_type, values in entities.items():
        if values:
            print(f"{entity_type.upper()}:")
            for val in values:
                print(f"  - {val}")
```

### 2.2 Fine-tuning NER pour domaine spécifique

```python
# backend/ai/train_custom_ner.py
import spacy
from spacy.training import Example
import random

# 1. Créer training data (format spaCy)
TRAIN_DATA = [
    ("Password: admin123 found in database", {
        "entities": [(10, 18, "CREDENTIAL")]
    }),
    ("API key: AKIA1234567890EXAMPLE exposed", {
        "entities": [(9, 33, "API_KEY")]
    }),
    ("CVE-2021-44228 Log4Shell vulnerability", {
        "entities": [(0, 14, "CVE")]
    }),
    ("AWS Access Key: AKIAIOSFODNN7EXAMPLE", {
        "entities": [(16, 36, "AWS_KEY")]
    }),
]

# 2. Créer modèle vide ou charger existant
nlp = spacy.load("en_core_web_lg")

# Ajouter NER si pas présent
if "ner" not in nlp.pipe_names:
    ner = nlp.add_pipe("ner")
else:
    ner = nlp.get_pipe("ner")

# 3. Ajouter labels
for _, annotations in TRAIN_DATA:
    for ent in annotations.get("entities"):
        ner.add_label(ent[2])

# 4. Entraîner
other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
with nlp.disable_pipes(*other_pipes):
    optimizer = nlp.create_optimizer()

    for epoch in range(30):
        random.shuffle(TRAIN_DATA)
        losses = {}

        for text, annotations in TRAIN_DATA:
            doc = nlp.make_doc(text)
            example = Example.from_dict(doc, annotations)
            nlp.update([example], drop=0.3, losses=losses, sgd=optimizer)

        print(f"Epoch {epoch + 1}: Loss = {losses['ner']:.2f}")

# 5. Sauvegarder
nlp.to_disk("./models/custom_ner")
print("✅ Custom NER model saved")

# 6. Tester
test_text = "AWS key AKIAI44QH8DHBEXAMPLE leaked in commit"
doc = nlp(test_text)
for ent in doc.ents:
    print(f"{ent.text} → {ent.label_}")
```

---

## 3. Détection de Faux Profils

### 3.1 Collecter Features

```python
# backend/ai/profile_feature_extractor.py
from datetime import datetime
import numpy as np

class ProfileFeatureExtractor:
    """Extrait features d'un profil social"""

    def extract(self, profile: dict) -> np.ndarray:
        """
        Features:
        1. Followers count
        2. Following count
        3. Posts count
        4. Account age (days)
        5. Follower/following ratio
        6. Has profile picture (binary)
        7. Has bio (binary)
        8. Posts per day
        9. Avg likes per post
        10. Avg comments per post
        11. % posts with links
        12. % posts with hashtags
        """

        # Account age
        created = datetime.fromisoformat(profile.get('created_at', '2020-01-01'))
        age_days = (datetime.now() - created).days

        # Ratios
        followers = profile.get('followers_count', 0)
        following = profile.get('following_count', 1)  # Éviter division par 0
        posts_count = profile.get('posts_count', 0)

        follower_ratio = followers / following if following > 0 else 0
        posts_per_day = posts_count / age_days if age_days > 0 else 0

        # Stats posts
        posts = profile.get('posts', [])
        avg_likes = np.mean([p.get('likes', 0) for p in posts]) if posts else 0
        avg_comments = np.mean([p.get('comments', 0) for p in posts]) if posts else 0

        posts_with_links = sum(1 for p in posts if 'http' in p.get('text', ''))
        posts_with_hashtags = sum(1 for p in posts if '#' in p.get('text', ''))
        pct_links = posts_with_links / len(posts) if posts else 0
        pct_hashtags = posts_with_hashtags / len(posts) if posts else 0

        features = np.array([
            followers,
            following,
            posts_count,
            age_days,
            follower_ratio,
            int(profile.get('has_profile_picture', False)),
            int(profile.get('has_bio', False)),
            posts_per_day,
            avg_likes,
            avg_comments,
            pct_links,
            pct_hashtags
        ])

        return features
```

### 3.2 Entraîner Isolation Forest

```python
# backend/ai/train_fake_detector.py
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import numpy as np
import pickle

# 1. Créer dataset (exemple)
# Dans la vraie vie, collectez 1000+ profils réels + 100+ bots connus
real_profiles = np.array([
    [500, 450, 200, 365, 1.1, 1, 1, 0.5, 50, 10, 0.1, 0.3],  # Profil normal
    [1200, 1100, 500, 730, 1.09, 1, 1, 0.68, 80, 15, 0.15, 0.4],
    [300, 280, 150, 200, 1.07, 1, 1, 0.75, 30, 5, 0.2, 0.25],
    # ... ajouter 100+ exemples réels
])

fake_profiles = np.array([
    [10000, 50, 5000, 30, 200, 0, 0, 166, 5, 1, 0.8, 0.9],  # Bot classique
    [5000, 5000, 10000, 10, 1, 0, 0, 1000, 2, 0, 0.9, 0.95],  # Spam bot
    [50, 10000, 100, 5, 0.005, 0, 0, 20, 3, 0, 0.5, 0.8],  # Follower bot
])

# 2. Combiner (on entraîne principalement sur réels)
X_train = np.vstack([real_profiles, fake_profiles[:2]])  # Contamination faible

# 3. Normaliser
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_train)

# 4. Entraîner Isolation Forest
clf = IsolationForest(
    contamination=0.1,  # 10% de profils anormaux attendus
    random_state=42,
    n_estimators=100
)
clf.fit(X_scaled)

# 5. Sauvegarder
with open('models/fake_detector.pkl', 'wb') as f:
    pickle.dump(clf, f)
with open('models/scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)

print("✅ Fake profile detector trained and saved")

# 6. Tester
test_profiles = [
    real_profiles[0],  # Devrait être normal
    fake_profiles[0]   # Devrait être anomalie
]

for i, profile in enumerate(test_profiles):
    profile_scaled = scaler.transform([profile])
    prediction = clf.predict(profile_scaled)
    score = clf.score_samples(profile_scaled)

    print(f"\nProfile {i + 1}:")
    print(f"  Prediction: {'FAKE' if prediction[0] == -1 else 'REAL'}")
    print(f"  Anomaly score: {abs(score[0]):.3f}")
```

### 3.3 Production Detector

```python
# backend/ai/fake_profile_detector.py
import pickle
import numpy as np
from ai.profile_feature_extractor import ProfileFeatureExtractor

class FakeProfileDetector:
    def __init__(self):
        with open('models/fake_detector.pkl', 'rb') as f:
            self.model = pickle.load(f)
        with open('models/scaler.pkl', 'rb') as f:
            self.scaler = pickle.load(f)
        self.feature_extractor = ProfileFeatureExtractor()

    def predict(self, profile: dict) -> dict:
        """Prédit si un profil est fake"""
        # Extraire features
        features = self.feature_extractor.extract(profile)
        features_scaled = self.scaler.transform([features])

        # Prédiction
        prediction = self.model.predict(features_scaled)
        anomaly_score = abs(self.model.score_samples(features_scaled)[0])

        is_fake = prediction[0] == -1
        confidence = min(anomaly_score * 100, 100)

        # Red flags spécifiques
        red_flags = []
        if profile.get('followers_count', 0) / max(profile.get('following_count', 1), 1) > 50:
            red_flags.append("Follower/following ratio too high")
        if profile.get('posts_count', 0) > 500 and (datetime.now() - datetime.fromisoformat(profile.get('created_at', '2020-01-01'))).days < 30:
            red_flags.append("Too many posts for account age")
        if not profile.get('has_profile_picture'):
            red_flags.append("No profile picture")

        return {
            'is_fake': is_fake,
            'confidence': confidence,
            'anomaly_score': anomaly_score,
            'red_flags': red_flags
        }
```

---

## 4. Graph Neural Networks

### 4.1 Construire un Graphe dans Neo4j

```python
# backend/ai/graph_builder.py
from neo4j import GraphDatabase

class GraphBuilder:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def create_person(self, name: str, email: str, investigation_id: str):
        """Crée un nœud Person"""
        with self.driver.session() as session:
            session.run("""
                MERGE (p:Person {name: $name})
                SET p.email = $email, p.investigation_id = $investigation_id
                RETURN p
            """, name=name, email=email, investigation_id=investigation_id)

    def create_relationship(self, person1: str, person2: str, rel_type: str):
        """Crée une relation entre deux personnes"""
        with self.driver.session() as session:
            session.run(f"""
                MATCH (p1:Person {{name: $person1}})
                MATCH (p2:Person {{name: $person2}})
                MERGE (p1)-[r:{rel_type}]->(p2)
                RETURN r
            """, person1=person1, person2=person2)

    def find_communities(self, investigation_id: str):
        """Détecte communautés avec Louvain"""
        with self.driver.session() as session:
            # Créer graphe projection
            session.run("""
                CALL gds.graph.project(
                    'social-network',
                    'Person',
                    {KNOWS: {orientation: 'UNDIRECTED'}}
                )
            """)

            # Run Louvain
            result = session.run("""
                CALL gds.louvain.stream('social-network')
                YIELD nodeId, communityId
                RETURN gds.util.asNode(nodeId).name AS name, communityId
                ORDER BY communityId
            """)

            communities = {}
            for record in result:
                comm_id = record['communityId']
                if comm_id not in communities:
                    communities[comm_id] = []
                communities[comm_id].append(record['name'])

            return communities

# Usage
builder = GraphBuilder("bolt://localhost:7687", "neo4j", "password")
builder.create_person("Alice", "alice@example.com", "inv-123")
builder.create_person("Bob", "bob@example.com", "inv-123")
builder.create_relationship("Alice", "Bob", "KNOWS")
communities = builder.find_communities("inv-123")
print(communities)
```

---

## 5. Datasets & Annotation

### 5.1 Setup Label Studio pour Annotation

```bash
# Installer Label Studio
pip install label-studio

# Lancer
label-studio start

# Ouvre http://localhost:8080
```

**Configuration pour classification de risque :**

```xml
<View>
  <Text name="text" value="$text"/>
  <Choices name="risk" toName="text" choice="single">
    <Choice value="low"/>
    <Choice value="medium"/>
    <Choice value="high"/>
    <Choice value="critical"/>
  </Choices>
</View>
```

### 5.2 Augmentation de Données

```python
# backend/ai/data_augmentation.py
import nlpaug.augmenter.word as naw
import nlpaug.augmenter.sentence as nas

class DataAugmenter:
    def __init__(self):
        self.synonym_aug = naw.SynonymAug(aug_src='wordnet')
        self.back_translation_aug = naw.BackTranslationAug(
            from_model_name='facebook/wmt19-en-de',
            to_model_name='facebook/wmt19-de-en'
        )

    def augment(self, text: str, n_augmentations: int = 3):
        """Génère n variations d'un texte"""
        augmented = [text]  # Texte original

        for _ in range(n_augmentations):
            # Synonymes
            aug_text = self.synonym_aug.augment(text)
            augmented.append(aug_text)

        return augmented

# Usage
augmenter = DataAugmenter()
original = "Email found in 3 data breaches"
variations = augmenter.augment(original, n_augmentations=2)

for i, var in enumerate(variations):
    print(f"{i}. {var}")
```

---

## 📊 Métriques et Évaluation

### Évaluer votre modèle

```python
# backend/ai/evaluate_model.py
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

def evaluate_classifier(model, tokenizer, test_data):
    """Évalue un classifier"""
    predictions = []
    true_labels = []

    for text, label in test_data:
        inputs = tokenizer(text, return_tensors="pt", truncation=True)
        outputs = model(**inputs)
        pred = torch.argmax(outputs.logits).item()

        predictions.append(pred)
        true_labels.append(label)

    # Classification report
    print(classification_report(true_labels, predictions,
                                target_names=['low', 'medium', 'high', 'critical']))

    # Confusion matrix
    cm = confusion_matrix(true_labels, predictions)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.title('Confusion Matrix')
    plt.savefig('confusion_matrix.png')
    print("✅ Confusion matrix saved to confusion_matrix.png")
```

---

## 🎯 Checklist IA

- [ ] Collecter minimum 500 exemples par classe
- [ ] Annoter avec Label Studio
- [ ] Séparer train/validation/test (70/15/15)
- [ ] Entraîner modèle baseline
- [ ] Évaluer avec métriques (F1, Accuracy)
- [ ] Fine-tuner hyperparamètres
- [ ] Tester en production sur données réelles
- [ ] Itérer et améliorer avec feedback

**🚀 Vous êtes maintenant prêt à entraîner vos modèles IA !**
