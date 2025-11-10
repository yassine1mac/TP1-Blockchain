"""
TP N°1 - Blockchain Fundamentals
Script de Démonstration Complet

Ce script démontre toutes les fonctionnalités de la blockchain:
- Création de blocs
- Minage avec preuve de travail
- Validation de la chaîne
- Tentative d'altération (pour montrer la sécurité)
"""

from blockchain import Blockchain
import time


def separator(title=""):
    """Affiche un séparateur visuel."""
    print("\n" + "="*80)
    if title:
        print(f"  {title}")
        print("="*80)
    else:
        print("="*80)


def demo_basic_blockchain():
    """Démo 1: Blockchain de base avec minage."""
    separator("DÉMO 1: CRÉATION ET MINAGE DE BLOCS")
    
    # Création d'une blockchain avec difficulté 4
    print("\n1️⃣  Création d'une nouvelle blockchain (difficulté = 4)")
    blockchain = Blockchain(difficulty=4)
    
    input("\n▶️  Appuyez sur Entrée pour ajouter des transactions...")
    
    # Ajout de transactions
    print("\n2️⃣  Ajout de transactions en attente")
    blockchain.add_transaction("Alice", "Bob", 50)
    print("   ✅ Transaction: Alice → Bob (50 unités)")
    
    blockchain.add_transaction("Bob", "Charlie", 25)
    print("   ✅ Transaction: Bob → Charlie (25 unités)")
    
    print(f"\n   📝 Transactions en attente: {len(blockchain.pending_transactions)}")
    
    input("\n▶️  Appuyez sur Entrée pour miner le premier bloc...")
    
    # Minage du premier bloc
    print("\n3️⃣  Minage du bloc #1")
    blockchain.mine_pending_transactions("Miner_Alice")
    
    input("\n▶️  Appuyez sur Entrée pour ajouter plus de transactions...")
    
    # Deuxième série de transactions
    print("\n4️⃣  Ajout de nouvelles transactions")
    blockchain.add_transaction("Charlie", "Alice", 10)
    print("   ✅ Transaction: Charlie → Alice (10 unités)")
    
    blockchain.add_transaction("Alice", "Bob", 15)
    print("   ✅ Transaction: Alice → Bob (15 unités)")
    
    blockchain.add_transaction("Bob", "Miner_Alice", 5)
    print("   ✅ Transaction: Bob → Miner_Alice (5 unités)")
    
    input("\n▶️  Appuyez sur Entrée pour miner le deuxième bloc...")
    
    # Minage du deuxième bloc
    print("\n5️⃣  Minage du bloc #2")
    blockchain.mine_pending_transactions("Miner_Bob")
    
    # Affichage de la blockchain complète
    input("\n▶️  Appuyez sur Entrée pour afficher la blockchain complète...")
    blockchain.display_chain()
    
    # Validation de la chaîne
    input("\n▶️  Appuyez sur Entrée pour vérifier l'intégrité de la chaîne...")
    print("\n6️⃣  Validation de l'intégrité")
    blockchain.is_chain_valid()
    
    # Affichage des soldes
    input("\n▶️  Appuyez sur Entrée pour voir les soldes finaux...")
    print("\n7️⃣  Soldes finaux:")
    print("-"*50)
    for address in ["Alice", "Bob", "Charlie", "Miner_Alice", "Miner_Bob"]:
        balance = blockchain.get_balance(address)
        print(f"   💰 {address:<15} : {balance:>10.2f} unités")
    
    return blockchain


def demo_security():
    """Démo 2: Tentative d'altération pour montrer la sécurité."""
    separator("DÉMO 2: SÉCURITÉ ET IMMUTABILITÉ")
    
    print("\n🔐 Cette démo montre que la blockchain détecte les altérations")
    
    # Création d'une petite blockchain
    print("\n1️⃣  Création d'une blockchain de test")
    blockchain = Blockchain(difficulty=3)  # Difficulté réduite pour aller plus vite
    
    blockchain.add_transaction("Alice", "Bob", 100)
    blockchain.mine_pending_transactions("Miner1")
    
    blockchain.add_transaction("Bob", "Charlie", 50)
    blockchain.mine_pending_transactions("Miner2")
    
    print("   ✅ 2 blocs minés avec succès")
    
    # Validation initiale
    print("\n2️⃣  Validation initiale")
    is_valid = blockchain.is_chain_valid()
    print(f"   Chaîne valide: {is_valid}")
    
    input("\n▶️  Appuyez sur Entrée pour tenter une altération...")
    
    # Tentative d'altération
    print("\n3️⃣  Tentative d'altération du bloc #1")
    print("   ⚠️  Modification: Alice → Bob (100) devient Alice → Bob (1000)")
    
    # Sauvegarder l'ancienne transaction
    original_transaction = blockchain.chain[1].transactions[1].copy()
    
    # Altérer la transaction
    blockchain.chain[1].transactions[1]['amount'] = 1000
    
    print("   ✅ Transaction modifiée!")
    
    input("\n▶️  Appuyez sur Entrée pour vérifier l'intégrité...")
    
    # Re-validation
    print("\n4️⃣  Nouvelle validation")
    is_valid = blockchain.is_chain_valid()
    
    if not is_valid:
        print("\n   ✅ SUCCÈS: La blockchain a détecté l'altération!")
        print("   🔐 L'immutabilité est garantie par le chaînage des hashs")
    
    # Restaurer la transaction originale
    blockchain.chain[1].transactions[1] = original_transaction


def demo_mining_difficulty():
    """Démo 3: Impact de la difficulté sur le temps de minage."""
    separator("DÉMO 3: IMPACT DE LA DIFFICULTÉ")
    
    print("\n⏱️  Cette démo compare le temps de minage selon la difficulté")
    
    difficulties = [2, 3, 4]
    
    for diff in difficulties:
        print(f"\n{'='*50}")
        print(f"Difficulté: {diff} (hash doit commencer par '{'0'*diff}')")
        print('='*50)
        
        # Créer une blockchain avec cette difficulté
        blockchain = Blockchain(difficulty=diff)
        blockchain.add_transaction("Alice", "Bob", 10)
        
        # Mesurer le temps de minage
        start_time = time.time()
        blockchain.mine_pending_transactions("Miner1")
        end_time = time.time()
        
        mining_time = end_time - start_time
        
        print(f"\n📊 Résultat:")
        print(f"   ⏱️  Temps de minage: {mining_time:.2f} secondes")
        print(f"   🔢 Nonce trouvé: {blockchain.chain[-1].nonce}")
        print(f"   🔐 Hash: {blockchain.chain[-1].hash}")
        
        if diff < max(difficulties):
            input("\n▶️  Appuyez sur Entrée pour tester la difficulté suivante...")


def demo_balance_tracking():
    """Démo 4: Suivi des soldes à travers les transactions."""
    separator("DÉMO 4: SUIVI DES SOLDES")
    
    print("\n💰 Cette démo montre comment les soldes évoluent")
    
    blockchain = Blockchain(difficulty=3)
    
    # Scénario avec plusieurs transactions
    print("\n1️⃣  Scénario: Réseau de paiements")
    print("-"*50)
    
    transactions_batch_1 = [
        ("Alice", "Bob", 50, "Alice paie Bob pour un service"),
        ("Bob", "Charlie", 25, "Bob paie Charlie"),
        ("Charlie", "David", 10, "Charlie paie David")
    ]
    
    print("\n📝 Lot 1 de transactions:")
    for sender, recipient, amount, description in transactions_batch_1:
        blockchain.add_transaction(sender, recipient, amount)
        print(f"   • {description}: {sender} → {recipient} ({amount} unités)")
    
    input("\n▶️  Appuyez sur Entrée pour miner...")
    
    print("\n⛏️  Minage du bloc par Miner1...")
    blockchain.mine_pending_transactions("Miner1")
    
    # Afficher les soldes après le premier bloc
    print("\n💰 Soldes après le bloc #1:")
    print("-"*50)
    for person in ["Alice", "Bob", "Charlie", "David", "Miner1"]:
        balance = blockchain.get_balance(person)
        sign = "+" if balance > 0 else ""
        print(f"   {person:<10} : {sign}{balance:>8.2f} unités")
    
    input("\n▶️  Appuyez sur Entrée pour le lot 2...")
    
    # Deuxième lot de transactions
    transactions_batch_2 = [
        ("David", "Alice", 5, "David rembourse Alice"),
        ("Bob", "Alice", 20, "Bob rembourse Alice"),
        ("Miner1", "Charlie", 0.5, "Miner1 donne à Charlie")
    ]
    
    print("\n📝 Lot 2 de transactions:")
    for sender, recipient, amount, description in transactions_batch_2:
        blockchain.add_transaction(sender, recipient, amount)
        print(f"   • {description}: {sender} → {recipient} ({amount} unités)")
    
    input("\n▶️  Appuyez sur Entrée pour miner...")
    
    print("\n⛏️  Minage du bloc par Miner2...")
    blockchain.mine_pending_transactions("Miner2")
    
    # Afficher les soldes finaux
    print("\n💰 Soldes finaux après le bloc #2:")
    print("-"*50)
    for person in ["Alice", "Bob", "Charlie", "David", "Miner1", "Miner2"]:
        balance = blockchain.get_balance(person)
        sign = "+" if balance > 0 else ""
        emoji = "🟢" if balance > 0 else "🔴" if balance < 0 else "⚪"
        print(f"   {emoji} {person:<10} : {sign}{balance:>8.2f} unités")


def main_menu():
    """Menu principal pour choisir la démo."""
    while True:
        separator("🚀 DÉMONSTRATEUR DE BLOCKCHAIN - TP N°1")
        
        print("\nChoisissez une démonstration:\n")
        print("   1️⃣  Démo Complète (Création, Minage, Validation)")
        print("   2️⃣  Démo Sécurité (Détection d'altération)")
        print("   3️⃣  Démo Difficulté (Impact sur le temps de minage)")
        print("   4️⃣  Démo Soldes (Suivi des transactions)")
        print("   5️⃣  Toutes les démos")
        print("   0️⃣  Quitter")
        
        print("\n" + "="*80)
        choice = input("\nVotre choix: ").strip()
        
        if choice == "1":
            demo_basic_blockchain()
        elif choice == "2":
            demo_security()
        elif choice == "3":
            demo_mining_difficulty()
        elif choice == "4":
            demo_balance_tracking()
        elif choice == "5":
            demo_basic_blockchain()
            input("\n▶️  Appuyez sur Entrée pour la démo suivante...")
            demo_security()
            input("\n▶️  Appuyez sur Entrée pour la démo suivante...")
            demo_mining_difficulty()
            input("\n▶️  Appuyez sur Entrée pour la démo suivante...")
            demo_balance_tracking()
        elif choice == "0":
            separator("👋 MERCI D'AVOIR UTILISÉ LE DÉMONSTRATEUR!")
            print("\n✅ Programme terminé")
            print("="*80 + "\n")
            break
        else:
            print("\n❌ Choix invalide. Veuillez réessayer.")
        
        input("\n▶️  Appuyez sur Entrée pour revenir au menu...")


if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\n⚠️  Programme interrompu par l'utilisateur")
        print("👋 Au revoir!\n")
