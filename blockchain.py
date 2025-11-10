"""
Ce fichier contient les classes Block et Blockchain qui constituent le cœur du système.
"""

import hashlib
import time
import json
from typing import List, Dict, Any


class Block:
    """
    Classe représentant un bloc dans la blockchain.
    
    Attributs:
        index (int): Position du bloc dans la chaîne
        timestamp (float): Moment de création du bloc
        transactions (List): Liste des transactions du bloc
        previous_hash (str): Hash du bloc précédent
        nonce (int): Nombre utilisé pour la preuve de travail
        hash (str): Hash du bloc courant
    """
    
    def __init__(self, index: int, transactions: List[Dict], previous_hash: str = "0"):
        """
        Initialise un nouveau bloc.
        
        Args:
            index: Position du bloc dans la chaîne
            transactions: Liste des transactions à inclure dans le bloc
            previous_hash: Hash du bloc précédent (défaut: "0" pour le genesis block)
        """
        self.index = index
        self.timestamp = time.time()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = 0  # Initialisé à 0, sera incrémenté pendant le minage
        self.hash = self.calculate_hash()
    
    def calculate_hash(self) -> str:
        """
        Calcule le hash SHA256 du bloc.
        
        Le hash est calculé à partir de toutes les données du bloc :
        - index, timestamp, transactions, previous_hash, nonce
        
        Returns:
            str: Hash hexadécimal du bloc (64 caractères)
        """
        # Création d'une chaîne contenant toutes les informations du bloc
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }, sort_keys=True)
        
        # Calcul du hash SHA256
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convertit le bloc en dictionnaire pour faciliter la sérialisation JSON.
        
        Returns:
            dict: Représentation du bloc sous forme de dictionnaire
        """
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
            "hash": self.hash
        }


class Blockchain:
    """
    Classe représentant la blockchain complète.
    
    Attributs:
        chain (List[Block]): Liste des blocs de la chaîne
        difficulty (int): Difficulté du minage (nombre de zéros au début du hash)
        pending_transactions (List): Transactions en attente de validation
        mining_reward (int): Récompense pour le mineur qui valide un bloc
    """
    
    def __init__(self, difficulty: int = 4):
        """
        Initialise une nouvelle blockchain.
        
        Args:
            difficulty: Nombre de zéros requis au début du hash (défaut: 4 pour "0000")
        """
        self.chain: List[Block] = []
        self.difficulty = difficulty  # Difficulté = 4 pour "0000"
        self.pending_transactions: List[Dict] = []
        self.mining_reward = 1  # Récompense en unité de cryptomonnaie
        
        # Création du bloc genesis (premier bloc)
        self.create_genesis_block()
    
    def create_genesis_block(self) -> None:
        """
        Crée le bloc genesis (bloc 0) de la blockchain.
        
        Le genesis block est le premier bloc, il n'a pas de bloc précédent.
        """
        genesis_block = Block(0, [{"message": "Genesis Block"}], "0")
        genesis_block.hash = genesis_block.calculate_hash()
        self.chain.append(genesis_block)
        print("✅ Genesis Block créé avec succès!")
    
    def get_latest_block(self) -> Block:
        """
        Retourne le dernier bloc de la chaîne.
        
        Returns:
            Block: Le dernier bloc de la blockchain
        """
        return self.chain[-1]
    
    def add_transaction(self, sender: str, recipient: str, amount: float) -> int:
        """
        Ajoute une transaction à la liste des transactions en attente.
        
        Args:
            sender: Adresse de l'expéditeur
            recipient: Adresse du destinataire
            amount: Montant de la transaction
            
        Returns:
            int: Index du bloc qui contiendra cette transaction
        """
        transaction = {
            "sender": sender,
            "recipient": recipient,
            "amount": amount,
            "timestamp": time.time()
        }
        
        self.pending_transactions.append(transaction)
        return self.get_latest_block().index + 1
    
    def proof_of_work(self, block: Block) -> None:
        """
        Implémente la preuve de travail (Proof of Work).
        
        Cette méthode incrémente le nonce jusqu'à trouver un hash qui commence
        par un nombre de zéros égal à la difficulté (ex: "0000...").
        
        Args:
            block: Le bloc à miner
        """
        target = "0" * self.difficulty  # Ex: "0000" si difficulty = 4
        
        print(f"\n⛏️  Mining bloc {block.index}...")
        print(f"🎯 Cible: hash commençant par '{target}'")
        
        start_time = time.time()
        
        # Boucle jusqu'à trouver un hash valide
        while block.hash[:self.difficulty] != target:
            block.nonce += 1
            block.hash = block.calculate_hash()
            
            # Affichage de progression tous les 100000 essais
            if block.nonce % 100000 == 0:
                print(f"   Tentative #{block.nonce}... Hash: {block.hash[:10]}...")
        
        end_time = time.time()
        mining_time = end_time - start_time
        
        print(f"✅ Bloc miné! Nonce trouvé: {block.nonce}")
        print(f"🔐 Hash valide: {block.hash}")
        print(f"⏱️  Temps de minage: {mining_time:.2f} secondes")
    
    def mine_pending_transactions(self, miner_address: str) -> Block:
        """
        Mine un nouveau bloc contenant toutes les transactions en attente.
        
        Cette méthode:
        1. Crée un bloc avec les transactions en attente
        2. Effectue la preuve de travail (mining)
        3. Ajoute le bloc à la chaîne
        4. Récompense le mineur
        
        Args:
            miner_address: Adresse du mineur qui recevra la récompense
            
        Returns:
            Block: Le bloc nouvellement miné
        """
        # Ajout de la transaction de récompense pour le mineur
        reward_transaction = {
            "sender": "SYSTEM",
            "recipient": miner_address,
            "amount": self.mining_reward,
            "timestamp": time.time(),
            "type": "mining_reward"
        }
        
        # Création du nouveau bloc
        block = Block(
            index=len(self.chain),
            transactions=[reward_transaction] + self.pending_transactions,
            previous_hash=self.get_latest_block().hash
        )
        
        # Minage du bloc (preuve de travail)
        self.proof_of_work(block)
        
        # Ajout du bloc à la chaîne
        self.chain.append(block)
        
        # Réinitialisation des transactions en attente
        self.pending_transactions = []
        
        print(f"💰 Récompense de {self.mining_reward} unité(s) envoyée à {miner_address}")
        
        return block
    
    def add_block(self, transactions: List[Dict], miner_address: str) -> Block:
        """
        Méthode alternative pour ajouter un bloc avec des transactions spécifiques.
        
        Args:
            transactions: Liste de transactions à inclure
            miner_address: Adresse du mineur
            
        Returns:
            Block: Le bloc ajouté
        """
        self.pending_transactions = transactions
        return self.mine_pending_transactions(miner_address)
    
    def is_chain_valid(self) -> bool:
        """
        Vérifie l'intégrité de la blockchain.
        
        Vérifie que:
        1. Chaque bloc pointe correctement vers le bloc précédent
        2. Le hash de chaque bloc est valide
        3. Le hash respecte la difficulté (commence par "0000")
        
        Returns:
            bool: True si la chaîne est valide, False sinon
        """
        print("\n🔍 Vérification de l'intégrité de la blockchain...")
        
        # Vérification de chaque bloc (sauf le genesis block)
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            # Vérification 1: Le hash du bloc est-il correct?
            if current_block.hash != current_block.calculate_hash():
                print(f"❌ Bloc {i}: Hash invalide!")
                return False
            
            # Vérification 2: Le bloc pointe-t-il vers le bon bloc précédent?
            if current_block.previous_hash != previous_block.hash:
                print(f"❌ Bloc {i}: previous_hash ne correspond pas!")
                return False
            
            # Vérification 3: Le hash respecte-t-il la difficulté?
            target = "0" * self.difficulty
            if current_block.hash[:self.difficulty] != target:
                print(f"❌ Bloc {i}: Hash ne respecte pas la difficulté!")
                return False
            
            print(f"✅ Bloc {i}: Valide")
        
        print("✅ Blockchain intègre et valide!")
        return True
    
    def get_balance(self, address: str) -> float:
        """
        Calcule le solde d'une adresse en parcourant toutes les transactions.
        
        Args:
            address: Adresse dont on veut connaître le solde
            
        Returns:
            float: Solde de l'adresse
        """
        balance = 0
        
        # Parcourir tous les blocs
        for block in self.chain:
            # Parcourir toutes les transactions du bloc
            for transaction in block.transactions:
                if transaction.get("recipient") == address:
                    balance += transaction.get("amount", 0)
                if transaction.get("sender") == address:
                    balance -= transaction.get("amount", 0)
        
        return balance
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convertit la blockchain en dictionnaire pour la sérialisation JSON.
        
        Returns:
            dict: Représentation de la blockchain
        """
        return {
            "length": len(self.chain),
            "difficulty": self.difficulty,
            "chain": [block.to_dict() for block in self.chain]
        }
    
    def display_chain(self) -> None:
        """
        Affiche toute la blockchain de manière formatée.
        """
        print("\n" + "="*80)
        print("📊 BLOCKCHAIN COMPLÈTE")
        print("="*80)
        print(f"Longueur de la chaîne: {len(self.chain)} blocs")
        print(f"Difficulté: {self.difficulty}")
        print("-"*80)
        
        for block in self.chain:
            print(f"\n📦 BLOC #{block.index}")
            print(f"   Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(block.timestamp))}")
            print(f"   Transactions: {len(block.transactions)}")
            for tx in block.transactions:
                print(f"      • {tx.get('sender', 'N/A')} → {tx.get('recipient', 'N/A')}: {tx.get('amount', 0)} unités")
            print(f"   Previous Hash: {block.previous_hash}")
            print(f"   Nonce: {block.nonce}")
            print(f"   Hash: {block.hash}")
        
        print("\n" + "="*80)


# Code de test (si ce fichier est exécuté directement)
if __name__ == "__main__":
    print("🚀 Démarrage du test de la Blockchain...")
    print("="*80)
    
    # Création d'une blockchain avec difficulté 4 (hash doit commencer par "0000")
    blockchain = Blockchain(difficulty=4)
    
    # Ajout de transactions
    print("\n📝 Ajout de transactions...")
    blockchain.add_transaction("Alice", "Bob", 50)
    blockchain.add_transaction("Bob", "Charlie", 25)
    
    # Minage du premier bloc
    blockchain.mine_pending_transactions("Miner1")
    
    # Ajout d'autres transactions
    blockchain.add_transaction("Charlie", "Alice", 10)
    blockchain.add_transaction("Alice", "Bob", 15)
    
    # Minage du deuxième bloc
    blockchain.mine_pending_transactions("Miner2")
    
    # Affichage de la blockchain
    blockchain.display_chain()
    
    # Vérification de l'intégrité
    blockchain.is_chain_valid()
    
    # Affichage des soldes
    print("\n💰 SOLDES:")
    for address in ["Alice", "Bob", "Charlie", "Miner1", "Miner2"]:
        balance = blockchain.get_balance(address)
        print(f"   {address}: {balance} unités")
