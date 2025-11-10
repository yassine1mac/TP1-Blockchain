# 🔗 TP N°1 - Implémentation d'une Blockchain avec Python

**Université Abdelmalek Essaâdi - ENSA Tétouan**  
**Filière:** Big Data & Intelligence Artificielle  
**Module:** M356 - Fondamentaux de la Blockchain  
**Professeur:** Imad Sassi  
**Auteur:** Yassine Chmirrou - BDIA 2025-2026

---

## 📚 Table des Matières

1. [Description du Projet](#-description-du-projet)
2. [Architecture](#-architecture)
3. [Installation](#-installation)
4. [Utilisation](#-utilisation)
5. [API REST - Documentation](#-api-rest---documentation)
6. [Tests et Exemples](#-tests-et-exemples)
7. [Concepts Clés](#-concepts-clés)
8. [Améliorations Possibles](#-améliorations-possibles)

---

## 📝 Description du Projet

Ce projet implémente une blockchain fonctionnelle en Python avec les fonctionnalités suivantes:

### **Partie I - Blockchain de Base**
- Création de blocs avec signature numérique (hash SHA256)
- Preuve de travail (PoW) avec difficulté ajustable
- Système de récompense pour les mineurs
- Validation de l'intégrité de la chaîne
- API REST pour interagir avec la blockchain

### **Partie II - Décentralisation**
- Gestion de nœuds multiples
- Synchronisation entre nœuds
- Algorithme de consensus (chaîne la plus longue)
- Découverte automatique de nœuds

---

## 🏗️ Architecture

```
blockchain-tp/
│
├── blockchain.py          # Classes Block et Blockchain (cœur du système)
├── app.py                 # API REST Flask
├── network.py             # Gestion du réseau de nœuds
├── requirements.txt       # Dépendances Python
└── README.md              # Documentation
```

### **Structure des Classes**

```
Block
├── index: int
├── timestamp: float
├── transactions: List[Dict]
├── previous_hash: str
├── nonce: int
├── hash: str
└── calculate_hash() → str

Blockchain
├── chain: List[Block]
├── difficulty: int
├── pending_transactions: List[Dict]
├── mining_reward: int
├── create_genesis_block()
├── add_transaction()
├── mine_pending_transactions()
├── proof_of_work()
├── is_chain_valid() → bool
└── get_balance() → float
```

---

## 🚀 Installation

### **1. Prérequis**
- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

### **2. Installation des dépendances**

```bash
# Installer les dépendances
pip install -r requirements.txt
```

Ou manuellement:
```bash
pip install Flask==3.0.0 requests==2.31.0
```

---

## 💻 Utilisation

### **Option 1: Test en ligne de commande**

```bash
# Tester la blockchain sans API
python blockchain.py
```

Ce script va:
1. Créer une blockchain
2. Ajouter des transactions
3. Miner 2 blocs
4. Afficher toute la chaîne
5. Vérifier l'intégrité
6. Afficher les soldes

### **Option 2: Lancer l'API REST**

```bash
# Démarrer le serveur sur le port 5000 (par défaut)
python app.py

# Ou spécifier un port différent
python app.py --port 5001
```

Le serveur sera accessible sur: `http://127.0.0.1:5000`

### **Option 3: Réseau Multi-Nœuds (Partie II)**

Pour tester la décentralisation, lancer plusieurs nœuds:

```bash
# Terminal 1 - Nœud 1
python app.py --port 5000

# Terminal 2 - Nœud 2
python app.py --port 5001

# Terminal 3 - Nœud 3
python app.py --port 5002
```

---

## 🌐 API REST - Documentation

### **Routes Disponibles**

#### **1. Page d'Accueil**
```http
GET http://127.0.0.1:5000/
```
Retourne la documentation de l'API.

#### **2. Consulter la Blockchain**
```http
GET http://127.0.0.1:5000/chain
```

**Réponse:**
```json
{
  "chain": {
    "length": 3,
    "difficulty": 4,
    "chain": [...]
  },
  "length": 3
}
```

#### **3. Ajouter une Transaction**
```http
POST http://127.0.0.1:5000/transactions/new
Content-Type: application/json

{
  "sender": "Alice",
  "recipient": "Bob",
  "amount": 50
}
```

**Réponse:**
```json
{
  "message": "Transaction ajoutée avec succès",
  "transaction": {
    "sender": "Alice",
    "recipient": "Bob",
    "amount": 50
  },
  "block_index": 2
}
```

#### **4. Miner un Bloc**
```http
POST http://127.0.0.1:5000/mine
Content-Type: application/json

{
  "miner": "Miner1"
}
```

**Réponse:**
```json
{
  "message": "Nouveau bloc miné avec succès! 🎉",
  "block": {
    "index": 2,
    "timestamp": 1699...,
    "transactions": [...],
    "hash": "0000a1b2c3...",
    "nonce": 45789
  },
  "reward": 1
}
```

#### **5. Vérifier la Validité**
```http
GET http://127.0.0.1:5000/validate
```

**Réponse:**
```json
{
  "valid": true,
  "message": "La blockchain est valide ✅",
  "length": 3
}
```

#### **6. Obtenir un Solde**
```http
GET http://127.0.0.1:5000/balance/Alice
```

**Réponse:**
```json
{
  "address": "Alice",
  "balance": -40.0
}
```

#### **7. Enregistrer des Nœuds (Partie II)**
```http
POST http://127.0.0.1:5000/nodes/register
Content-Type: application/json

{
  "nodes": [
    "http://127.0.0.1:5001",
    "http://127.0.0.1:5002"
  ]
}
```

#### **8. Consensus - Résoudre les Conflits**
```http
GET http://127.0.0.1:5000/nodes/resolve
```

Cette route synchronise la blockchain avec le réseau en adoptant la chaîne la plus longue.

---

##  Tests et Exemples

### **Exemple 1: Flux Complet**

```bash
# 1. Démarrer le serveur
python app.py

# 2. Dans un autre terminal, utiliser curl ou Postman

# Ajouter des transactions
curl -X POST http://127.0.0.1:5000/transactions/new \
  -H "Content-Type: application/json" \
  -d '{"sender":"Alice","recipient":"Bob","amount":50}'

curl -X POST http://127.0.0.1:5000/transactions/new \
  -H "Content-Type: application/json" \
  -d '{"sender":"Bob","recipient":"Charlie","amount":25}'

# Miner un bloc
curl -X POST http://127.0.0.1:5000/mine \
  -H "Content-Type: application/json" \
  -d '{"miner":"Miner1"}'

# Consulter la blockchain
curl http://127.0.0.1:5000/chain

# Vérifier la validité
curl http://127.0.0.1:5000/validate

# Obtenir les soldes
curl http://127.0.0.1:5000/balance/Alice
curl http://127.0.0.1:5000/balance/Bob
curl http://127.0.0.1:5000/balance/Miner1
```

### **Exemple 2: Test de Décentralisation**

```bash
# Terminal 1 - Nœud 1 (port 5000)
python app.py --port 5000

# Terminal 2 - Nœud 2 (port 5001)
python app.py --port 5001

# Terminal 3 - Enregistrer le nœud 2 dans le nœud 1
curl -X POST http://127.0.0.1:5000/nodes/register \
  -H "Content-Type: application/json" \
  -d '{"nodes":["http://127.0.0.1:5001"]}'

# Ajouter des transactions et miner sur le nœud 1
curl -X POST http://127.0.0.1:5000/transactions/new \
  -H "Content-Type: application/json" \
  -d '{"sender":"Alice","recipient":"Bob","amount":100}'

curl -X POST http://127.0.0.1:5000/mine \
  -H "Content-Type: application/json" \
  -d '{"miner":"Miner1"}'

# Synchroniser le nœud 2
curl http://127.0.0.1:5001/nodes/resolve
```

### **Exemple 3: Test avec Python**

```python
import requests

BASE_URL = "http://127.0.0.1:5000"

# Ajouter une transaction
response = requests.post(f"{BASE_URL}/transactions/new", json={
    "sender": "Alice",
    "recipient": "Bob",
    "amount": 50
})
print(response.json())

# Miner
response = requests.post(f"{BASE_URL}/mine", json={
    "miner": "Miner1"
})
print(response.json())

# Obtenir la chaîne
response = requests.get(f"{BASE_URL}/chain")
print(response.json())
```

---

## Concepts Clés

### **1. Hachage Cryptographique (SHA256)**
- Fonction à sens unique qui transforme des données en une empreinte unique
- Même une petite modification des données change complètement le hash
- Utilisé pour garantir l'intégrité des blocs

**Exemple:**
```
Input: "Hello World"
SHA256: a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b277d9ad9f146e
```

### **2. Preuve de Travail (Proof of Work)**
- Mécanisme de consensus qui rend le minage difficile
- Le mineur doit trouver un `nonce` tel que le hash commence par "0000"
- Plus la difficulté est élevée, plus le minage est long

**Exemple:**
```python
difficulty = 4  # Hash doit commencer par "0000"
nonce = 0

while hash[:4] != "0000":
    nonce += 1
    hash = calculate_hash(block_data + nonce)

# Après 45789 tentatives:
# nonce = 45789
# hash = "0000a1b2c3d4..."  ✅ Valide!
```

### **3. Chaînage des Blocs**
Chaque bloc contient le hash du bloc précédent, créant une chaîne immuable:

```
Bloc 0 (Genesis)          Bloc 1                    Bloc 2
┌──────────────┐         ┌──────────────┐          ┌──────────────┐
│ prev: "0"    │         │ prev: hash_0 │          │ prev: hash_1 │
│ hash: hash_0 │────────▶│ hash: hash_1 │─────────▶│ hash: hash_2 │
└──────────────┘         └──────────────┘          └──────────────┘
```

Si un bloc est modifié, son hash change, cassant la chaîne.

### **4. Récompense du Mineur**
- Le mineur qui trouve le nonce valide reçoit une récompense
- Dans notre implémentation: 1 unité de cryptomonnaie
- Incite les mineurs à valider les transactions

### **5. Consensus (Chaîne la Plus Longue)**
- En cas de conflit, la chaîne la plus longue est considérée comme valide
- Principe: la chaîne avec le plus de travail computationnel
- Protège contre les attaques (un attaquant devrait contrôler >50% de la puissance de calcul)

---

## 🎯 Bonnes Pratiques et Erreurs à Éviter

### ✅ **Bonnes Pratiques**

1. **Toujours valider la chaîne** après ajout de blocs
2. **Utiliser des nonces aléatoires** au départ pour varier les recherches
3. **Ajuster la difficulté** selon la puissance de calcul disponible
4. **Implémenter des timeouts** pour les requêtes réseau
5. **Logger les opérations** importantes (minage, ajout de blocs)

### ❌ **Erreurs à Éviter**

1. **Ne pas vérifier la validité** de la chaîne régulièrement
2. **Miner sans transactions** (bloc vide)
3. **Oublier la récompense du mineur**
4. **Ne pas gérer les erreurs réseau** en mode décentralisé
5. **Utiliser une difficulté trop élevée** (le minage peut prendre des heures)

---

## 🚀 Améliorations Possibles

### **1. Interface Web**
- Créer une interface HTML/CSS/JavaScript
- Visualiser la blockchain en temps réel
- Formulaires pour ajouter des transactions

### **2. Sécurité Renforcée**
- Signatures numériques (clés publiques/privées)
- Validation des transactions (solde suffisant)
- Protection contre les double-dépenses

### **3. Optimisations**
- Pool de minage (mining pool)
- Difficulté dynamique (ajustement automatique)
- Merkle Trees pour les transactions
- Base de données pour stocker la blockchain

### **4. Fonctionnalités Avancées**
- Smart contracts (contrats intelligents)
- Tokens personnalisés
- Mécanisme de vote pour les upgrades
- Consensus alternatifs (Proof of Stake)

### **5. Scalabilité**
- Sharding (partitionnement de la blockchain)
- Lightning Network (transactions off-chain)
- Compression des blocs
- Pruning (élagage des anciens blocs)

---

## 📊 Résultats Attendus

### **Capture d'Écran 1: Test en Ligne de Commande**
```
🚀 Démarrage du test de la Blockchain...
================================================================================
✅ Genesis Block créé avec succès!

📝 Ajout de transactions...

⛏️  Mining bloc 1...
🎯 Cible: hash commençant par '0000'
   Tentative #100000... Hash: a1b2c3d4e5...
✅ Bloc miné! Nonce trouvé: 187453
🔐 Hash valide: 0000f3a7b2c1d9e8f7a6b5c4d3e2f1a0b9c8d7e6f5a4b3c2d1e0f9a8b7c6d5e4
⏱️  Temps de minage: 12.34 secondes
💰 Récompense de 1 unité(s) envoyée à Miner1
```

### **Capture d'Écran 2: Réponse API**
```json
{
  "message": "Nouveau bloc miné avec succès! 🎉",
  "block": {
    "index": 1,
    "timestamp": 1699528123.456,
    "transactions": [
      {
        "sender": "SYSTEM",
        "recipient": "Miner1",
        "amount": 1,
        "type": "mining_reward"
      },
      {
        "sender": "Alice",
        "recipient": "Bob",
        "amount": 50
      }
    ],
    "previous_hash": "genesis_hash",
    "nonce": 187453,
    "hash": "0000f3a7b2c1..."
  },
  "reward": 1
}
```

---

##  Auteur

**Yassine**  
Étudiant en 5ème année - Big Data & Intelligence Artificielle  
ENSA Tétouan - Université Abdelmalek Essaâdi  
Année Universitaire: 2025-2026

---

