"""
TP N°1 - Blockchain Fundamentals
Module de Gestion du Réseau Décentralisé (Partie II)

Ce fichier contient les classes et fonctions pour gérer un réseau
de nœuds blockchain décentralisés avec synchronisation.
"""

import requests
from typing import Set, List, Dict
from urllib.parse import urlparse
import time


class Node:
    """
    Représente un nœud dans le réseau blockchain décentralisé.
    
    Attributs:
        address (str): Adresse du nœud (host:port)
        last_seen (float): Timestamp de la dernière connexion réussie
        active (bool): Indique si le nœud est actif
    """
    
    def __init__(self, address: str):
        """
        Initialise un nœud.
        
        Args:
            address: Adresse du nœud au format "host:port"
        """
        self.address = address
        self.last_seen = time.time()
        self.active = True
    
    def ping(self) -> bool:
        """
        Vérifie si le nœud est accessible.
        
        Returns:
            bool: True si le nœud répond, False sinon
        """
        try:
            response = requests.get(f'http://{self.address}/chain/length', timeout=2)
            if response.status_code == 200:
                self.last_seen = time.time()
                self.active = True
                return True
        except Exception as e:
            print(f"❌ Nœud {self.address} inaccessible: {e}")
            self.active = False
            return False
        
        return False
    
    def get_chain(self) -> Dict:
        """
        Récupère la blockchain du nœud.
        
        Returns:
            dict: Données de la blockchain ou None si erreur
        """
        try:
            response = requests.get(f'http://{self.address}/chain', timeout=5)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"❌ Erreur lors de la récupération de la chaîne du nœud {self.address}: {e}")
        
        return None
    
    def to_dict(self) -> Dict:
        """
        Convertit le nœud en dictionnaire.
        
        Returns:
            dict: Représentation du nœud
        """
        return {
            "address": self.address,
            "last_seen": self.last_seen,
            "active": self.active
        }


class NetworkManager:
    """
    Gestionnaire du réseau de nœuds blockchain.
    
    Gère l'enregistrement, la découverte et la synchronisation des nœuds.
    """
    
    def __init__(self):
        """
        Initialise le gestionnaire de réseau.
        """
        self.nodes: Dict[str, Node] = {}
    
    def register_node(self, address: str) -> bool:
        """
        Enregistre un nouveau nœud dans le réseau.
        
        Args:
            address: Adresse du nœud (URL complète ou host:port)
            
        Returns:
            bool: True si le nœud a été ajouté, False s'il existait déjà
        """
        # Parser l'URL pour extraire host:port
        parsed_url = urlparse(address)
        if parsed_url.netloc:
            node_address = parsed_url.netloc
        elif parsed_url.path:
            node_address = parsed_url.path
        else:
            print(f"❌ Format d'adresse invalide: {address}")
            return False
        
        # Vérifier si le nœud existe déjà
        if node_address in self.nodes:
            print(f"ℹ️  Nœud {node_address} déjà enregistré")
            return False
        
        # Créer et ajouter le nœud
        node = Node(node_address)
        self.nodes[node_address] = node
        
        print(f"✅ Nœud {node_address} enregistré avec succès")
        return True
    
    def remove_node(self, address: str) -> bool:
        """
        Supprime un nœud du réseau.
        
        Args:
            address: Adresse du nœud à supprimer
            
        Returns:
            bool: True si le nœud a été supprimé
        """
        if address in self.nodes:
            del self.nodes[address]
            print(f"🗑️  Nœud {address} supprimé")
            return True
        return False
    
    def get_active_nodes(self) -> List[Node]:
        """
        Retourne la liste des nœuds actifs.
        
        Returns:
            list: Liste des nœuds actifs
        """
        return [node for node in self.nodes.values() if node.active]
    
    def ping_all_nodes(self) -> Dict[str, bool]:
        """
        Vérifie la disponibilité de tous les nœuds.
        
        Returns:
            dict: Dictionnaire {adresse: status} pour chaque nœud
        """
        print("\n🔍 Vérification de tous les nœuds...")
        results = {}
        
        for address, node in self.nodes.items():
            status = node.ping()
            results[address] = status
            
            status_icon = "✅" if status else "❌"
            print(f"   {status_icon} {address}: {'Actif' if status else 'Inactif'}")
        
        return results
    
    def discover_neighbors(self, seed_node: str) -> None:
        """
        Découvre automatiquement les nœuds du réseau via un nœud seed.
        
        Args:
            seed_node: Adresse d'un nœud connu pour démarrer la découverte
        """
        try:
            response = requests.get(f'http://{seed_node}/nodes/list', timeout=5)
            if response.status_code == 200:
                data = response.json()
                discovered_nodes = data.get('nodes', [])
                
                print(f"\n🔍 Découverte de {len(discovered_nodes)} nœud(s) via {seed_node}")
                
                for node_address in discovered_nodes:
                    self.register_node(node_address)
        except Exception as e:
            print(f"❌ Erreur lors de la découverte des nœuds: {e}")
    
    def broadcast_new_block(self, block_data: Dict) -> None:
        """
        Diffuse un nouveau bloc à tous les nœuds actifs du réseau.
        
        Args:
            block_data: Données du bloc à diffuser
        """
        print("\n📡 Diffusion du nouveau bloc à tous les nœuds...")
        
        for node in self.get_active_nodes():
            try:
                # Note: Ceci nécessiterait une route /block/new dans l'API
                response = requests.post(
                    f'http://{node.address}/block/new',
                    json=block_data,
                    timeout=5
                )
                
                if response.status_code == 200:
                    print(f"✅ Bloc diffusé à {node.address}")
                else:
                    print(f"⚠️  Échec de diffusion à {node.address}")
            except Exception as e:
                print(f"❌ Erreur lors de la diffusion à {node.address}: {e}")
    
    def sync_with_network(self, current_blockchain) -> bool:
        """
        Synchronise la blockchain locale avec le réseau.
        
        Implémente l'algorithme de consensus en trouvant la chaîne
        la plus longue et valide parmi tous les nœuds.
        
        Args:
            current_blockchain: Instance de la blockchain locale
            
        Returns:
            bool: True si la chaîne a été mise à jour
        """
        print("\n🔄 Synchronisation avec le réseau...")
        
        max_length = len(current_blockchain.chain)
        longest_chain_data = None
        longest_chain_source = None
        
        # Parcourir tous les nœuds actifs
        for node in self.get_active_nodes():
            chain_data = node.get_chain()
            
            if chain_data:
                length = chain_data.get('length', 0)
                
                if length > max_length:
                    # Vérifier la validité de la chaîne
                    # (simplification: on fait confiance aux nœuds ici)
                    max_length = length
                    longest_chain_data = chain_data
                    longest_chain_source = node.address
                    
                    print(f"📊 Chaîne plus longue trouvée sur {node.address}: {length} blocs")
        
        # Mettre à jour si une chaîne plus longue a été trouvée
        if longest_chain_data:
            print(f"\n✅ Mise à jour de la chaîne depuis {longest_chain_source}")
            # Note: La reconstruction de la blockchain serait faite dans app.py
            return True
        else:
            print("\n✅ La chaîne locale est à jour")
            return False
    
    def get_network_status(self) -> Dict:
        """
        Retourne le statut complet du réseau.
        
        Returns:
            dict: Statistiques du réseau
        """
        total_nodes = len(self.nodes)
        active_nodes = len(self.get_active_nodes())
        
        return {
            "total_nodes": total_nodes,
            "active_nodes": active_nodes,
            "inactive_nodes": total_nodes - active_nodes,
            "nodes": [node.to_dict() for node in self.nodes.values()]
        }
    
    def display_network(self) -> None:
        """
        Affiche l'état du réseau de manière formatée.
        """
        status = self.get_network_status()
        
        print("\n" + "="*80)
        print("🌐 ÉTAT DU RÉSEAU BLOCKCHAIN")
        print("="*80)
        print(f"Total des nœuds: {status['total_nodes']}")
        print(f"Nœuds actifs: {status['active_nodes']}")
        print(f"Nœuds inactifs: {status['inactive_nodes']}")
        print("-"*80)
        
        for node_data in status['nodes']:
            status_icon = "🟢" if node_data['active'] else "🔴"
            last_seen = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(node_data['last_seen']))
            print(f"{status_icon} {node_data['address']:<30} | Dernière activité: {last_seen}")
        
        print("="*80)


# Code de test
if __name__ == "__main__":
    print("🚀 Test du module de gestion réseau")
    print("="*80)
    
    # Création du gestionnaire réseau
    network = NetworkManager()
    
    # Enregistrement de nœuds
    network.register_node("http://127.0.0.1:5000")
    network.register_node("http://127.0.0.1:5001")
    network.register_node("127.0.0.1:5002")
    
    # Affichage du réseau
    network.display_network()
    
    # Test de ping (ne fonctionnera que si les serveurs sont lancés)
    print("\nTest de connectivité:")
    network.ping_all_nodes()
