"""
TP N°1 - Blockchain Fundamentals
API REST pour interagir avec la Blockchain

Ce fichier implémente une API REST avec Flask pour:
- Consulter la blockchain
- Ajouter des transactions
- Miner des blocs
- Vérifier la validité de la chaîne
- Gérer les nœuds du réseau (Partie II)
"""

from flask import Flask, jsonify, request
from blockchain import Blockchain
import requests
from urllib.parse import urlparse
from typing import Set


# Création de l'application Flask
app = Flask(__name__)

# Création de l'instance de blockchain
blockchain = Blockchain(difficulty=4)

# Ensemble des nœuds du réseau (pour la décentralisation - Partie II)
nodes: Set[str] = set()


# ============================================================================
# ROUTES DE BASE (PARTIE I)
# ============================================================================

@app.route('/', methods=['GET'])
def home():
    """
    Page d'accueil de l'API avec la documentation des routes disponibles.
    """
    documentation = {
        "message": "🔗 Bienvenue sur l'API Blockchain - ENSA Tétouan",
        "author": "Yassine - BDIA 2025-2026",
        "routes": {
            "GET /": "Documentation de l'API",
            "GET /chain": "Afficher toute la blockchain",
            "GET /chain/length": "Obtenir la longueur de la chaîne",
            "POST /transactions/new": "Ajouter une nouvelle transaction",
            "POST /mine": "Miner un nouveau bloc",
            "GET /validate": "Vérifier la validité de la blockchain",
            "GET /balance/<address>": "Obtenir le solde d'une adresse",
            "POST /nodes/register": "Enregistrer de nouveaux nœuds (Partie II)",
            "GET /nodes/list": "Lister tous les nœuds du réseau",
            "GET /nodes/resolve": "Résoudre les conflits (consensus)"
        }
    }
    return jsonify(documentation), 200


@app.route('/chain', methods=['GET'])
def get_chain():
    """
    Retourne l'intégralité de la blockchain.
    
    Returns:
        JSON: Blockchain complète avec tous les blocs
    """
    response = {
        "chain": blockchain.to_dict(),
        "length": len(blockchain.chain)
    }
    return jsonify(response), 200


@app.route('/chain/length', methods=['GET'])
def get_chain_length():
    """
    Retourne uniquement la longueur de la chaîne.
    """
    response = {
        "length": len(blockchain.chain)
    }
    return jsonify(response), 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    """
    Ajoute une nouvelle transaction à la liste des transactions en attente.
    
    Body JSON attendu:
    {
        "sender": "Alice",
        "recipient": "Bob",
        "amount": 50
    }
    
    Returns:
        JSON: Message de confirmation avec l'index du futur bloc
    """
    values = request.get_json()
    
    # Vérification des champs requis
    required_fields = ['sender', 'recipient', 'amount']
    if not all(field in values for field in required_fields):
        return jsonify({
            "error": "Champs manquants",
            "required": required_fields
        }), 400
    
    # Ajout de la transaction
    index = blockchain.add_transaction(
        sender=values['sender'],
        recipient=values['recipient'],
        amount=values['amount']
    )
    
    response = {
        "message": f"Transaction ajoutée avec succès",
        "transaction": {
            "sender": values['sender'],
            "recipient": values['recipient'],
            "amount": values['amount']
        },
        "block_index": index
    }
    
    return jsonify(response), 201


@app.route('/mine', methods=['POST'])
def mine_block():
    """
    Mine un nouveau bloc contenant les transactions en attente.
    
    Body JSON attendu:
    {
        "miner": "Miner1"
    }
    
    Returns:
        JSON: Détails du bloc miné
    """
    values = request.get_json()
    
    # Vérification de l'adresse du mineur
    if not values or 'miner' not in values:
        return jsonify({
            "error": "Adresse du mineur manquante",
            "required": ["miner"]
        }), 400
    
    miner_address = values['miner']
    
    # Vérifier s'il y a des transactions en attente
    if len(blockchain.pending_transactions) == 0:
        return jsonify({
            "message": "Aucune transaction en attente à miner",
            "tip": "Ajoutez d'abord des transactions via POST /transactions/new"
        }), 400
    
    # Minage du bloc
    block = blockchain.mine_pending_transactions(miner_address)
    
    response = {
        "message": "Nouveau bloc miné avec succès! 🎉",
        "block": block.to_dict(),
        "reward": blockchain.mining_reward
    }
    
    return jsonify(response), 200


@app.route('/validate', methods=['GET'])
def validate_chain():
    """
    Vérifie l'intégrité de la blockchain.
    
    Returns:
        JSON: Résultat de la validation (valide ou non)
    """
    is_valid = blockchain.is_chain_valid()
    
    response = {
        "valid": is_valid,
        "message": "La blockchain est valide ✅" if is_valid else "La blockchain est invalide ❌",
        "length": len(blockchain.chain)
    }
    
    return jsonify(response), 200


@app.route('/balance/<address>', methods=['GET'])
def get_balance(address):
    """
    Obtient le solde d'une adresse spécifique.
    
    Args:
        address: Adresse dont on veut connaître le solde
    
    Returns:
        JSON: Solde de l'adresse
    """
    balance = blockchain.get_balance(address)
    
    response = {
        "address": address,
        "balance": balance
    }
    
    return jsonify(response), 200


# ============================================================================
# ROUTES POUR LA DÉCENTRALISATION (PARTIE II)
# ============================================================================

@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    """
    Enregistre de nouveaux nœuds dans le réseau.
    
    Body JSON attendu:
    {
        "nodes": ["http://127.0.0.1:5001", "http://127.0.0.1:5002"]
    }
    
    Returns:
        JSON: Liste des nœuds enregistrés
    """
    values = request.get_json()
    
    new_nodes = values.get('nodes')
    if new_nodes is None:
        return jsonify({
            "error": "Liste de nœuds manquante",
            "format": {"nodes": ["http://host:port"]}
        }), 400
    
    # Ajout de chaque nœud
    for node in new_nodes:
        parsed_url = urlparse(node)
        if parsed_url.netloc:
            nodes.add(parsed_url.netloc)
        elif parsed_url.path:
            # Format sans schéma (ex: "127.0.0.1:5001")
            nodes.add(parsed_url.path)
    
    response = {
        "message": "Nouveaux nœuds ajoutés avec succès",
        "total_nodes": list(nodes),
        "count": len(nodes)
    }
    
    return jsonify(response), 201


@app.route('/nodes/list', methods=['GET'])
def list_nodes():
    """
    Liste tous les nœuds enregistrés dans le réseau.
    
    Returns:
        JSON: Liste de tous les nœuds
    """
    response = {
        "nodes": list(nodes),
        "count": len(nodes)
    }
    
    return jsonify(response), 200


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    """
    Implémente l'algorithme de consensus.
    
    Remplace la chaîne locale par la plus longue chaîne du réseau si nécessaire.
    Principe: La chaîne la plus longue est considérée comme la chaîne valide.
    
    Returns:
        JSON: Résultat du consensus
    """
    replaced = resolve_conflicts()
    
    if replaced:
        response = {
            "message": "La chaîne a été remplacée par une chaîne plus longue",
            "new_chain": blockchain.to_dict()
        }
    else:
        response = {
            "message": "Notre chaîne est la plus longue et reste autoritaire",
            "chain": blockchain.to_dict()
        }
    
    return jsonify(response), 200


def resolve_conflicts() -> bool:
    """
    Algorithme de consensus: remplace la chaîne par la plus longue du réseau.
    
    Returns:
        bool: True si la chaîne a été remplacée, False sinon
    """
    global blockchain
    
    neighbors = nodes
    new_chain = None
    max_length = len(blockchain.chain)
    
    # Vérification de toutes les chaînes des nœuds du réseau
    for node in neighbors:
        try:
            response = requests.get(f'http://{node}/chain')
            
            if response.status_code == 200:
                data = response.json()
                length = data['length']
                chain_data = data['chain']['chain']
                
                # Vérifier si la chaîne est plus longue ET valide
                if length > max_length:
                    temp_blockchain = reconstruct_blockchain(chain_data)
                    if temp_blockchain.is_chain_valid():
                        max_length = length
                        new_chain = temp_blockchain
        except Exception as e:
            print(f"Erreur lors de la connexion au nœud {node}: {e}")
            continue
    
    # Remplacement de la chaîne si une plus longue et valide est trouvée
    if new_chain:
        blockchain = new_chain
        return True
    
    return False


def reconstruct_blockchain(chain_data: list) -> Blockchain:
    """
    Reconstruit une instance de Blockchain à partir de données JSON.
    
    Args:
        chain_data: Liste de blocs au format dictionnaire
    
    Returns:
        Blockchain: Instance reconstruite
    """
    from blockchain import Block
    
    temp_blockchain = Blockchain(difficulty=blockchain.difficulty)
    temp_blockchain.chain = []
    
    for block_data in chain_data:
        block = Block(
            index=block_data['index'],
            transactions=block_data['transactions'],
            previous_hash=block_data['previous_hash']
        )
        block.timestamp = block_data['timestamp']
        block.nonce = block_data['nonce']
        block.hash = block_data['hash']
        
        temp_blockchain.chain.append(block)
    
    return temp_blockchain


# ============================================================================
# DÉMARRAGE DU SERVEUR
# ============================================================================

if __name__ == '__main__':
    from argparse import ArgumentParser
    
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='Port du serveur')
    args = parser.parse_args()
    port = args.port
    
    print("="*80)
    print("🚀 Démarrage de l'API Blockchain")
    print(f"📡 Serveur: http://127.0.0.1:{port}")
    print("="*80)
    print("\n📚 Routes disponibles:")
    print(f"   • http://127.0.0.1:{port}/")
    print(f"   • http://127.0.0.1:{port}/chain")
    print(f"   • http://127.0.0.1:{port}/transactions/new")
    print(f"   • http://127.0.0.1:{port}/mine")
    print(f"   • http://127.0.0.1:{port}/validate")
    print(f"   • http://127.0.0.1:{port}/nodes/register")
    print(f"   • http://127.0.0.1:{port}/nodes/resolve")
    print("\n✅ Prêt à recevoir des requêtes!\n")
    
    app.run(host='0.0.0.0', port=port, debug=True)
