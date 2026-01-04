# Guide d'Installation et d'Utilisation du Serveur C2

## 1. Prérequis

### 1.1 Environnement Requis

Avant d'installer et d'exécuter le système C2 (Command and Control), assurez-vous que votre environnement répond aux exigences suivantes. Le système a été développé et testé sur un environnement Linux, mais devrait fonctionner également sur Windows et macOS avec quelques adaptations mineures. Vous aurez besoin de Python 3.8 ou une version supérieure, car le code utilise des fonctionnalités récentes du langage, notamment le typage statique et les f-strings qui améliorent la lisibilité du code. L'espace disque requis est minimal, environ 5 Mo pour les fichiers source et les dépendances, mais prévoyez un espace supplémentaire pour les logs d'exécution qui peuvent s'accumuler au fil du temps. La mémoire RAM minimale requise est de 512 Mo, bien que 1 Go soit recommandé pour une exécution fluide, especialmente si vous prévoyez de gérer plusieurs connexions clients simultanées.

Le système nécessite également une connexion réseau pour permettre la communication entre le serveur et les clients. Le protocole TLS est utilisé pour sécuriser toutes les communications, ce qui nécessite une configuration réseau appropriée pour autoriser le trafic sur les ports utilisés. Assurez-vous que votre pare-feu est configuré pour autoriser les connexions entrantes et sortantes sur le port spécifié dans la configuration du serveur. Une connexion Internet stable est recommandée pour le téléchargement initial des dépendances, bien que le système puisse fonctionner en mode hors ligne une fois les dépendances installées.

### 1.2 Dépendances Python

Le projet repose sur plusieurs bibliothèques Python qui doivent être installées avant d'exécuter le système. Flask est utilisé comme framework web pour le serveur C2, permettant de créer des interfaces d'administration et des API REST pour la communication avec les clients. La bibliothèque `ssl` est intégrée à Python et assure le chiffrement des communications via le protocole TLS. Les bibliothèques `socket` et `subprocess` font également partie de la bibliothèque standard et sont utilisées pour la gestion des connexions réseau et l'exécution des commandes sur les machines clients.

Voici la liste complète des dépendances avec leurs versions recommandées. Flask 3.1.2 ou supérieure est requis pour bénéficier des dernières fonctionnalités de sécurité et de performance. Jinja2 3.1.6 ou supérieure est nécessaire pour le moteur de templates utilisé par Flask. Itsdangerous 2.2.0 ou supérieure assure la sécurité des sessions et des données sensibles. Click 8.3.1 ou supérieure est utilisé pour l'interface en ligne de commandes. Blinker 1.9.0 ou supérieure est requis pour le système de signaux de Flask. Vous pouvez installer ces dépendances manuellement via pip ou utiliser le fichier requirements.txt fourni avec le projet.

### 1.3 Outils Complémentaires

Outre les dépendances Python, plusieurs outils complémentaires sont recommandés pour une utilisation optimale du système. Un éditeur de code tel que VS Code, PyCharm ou Vim facilitera le développement et le débogage. Git est nécessaire si vous souhaitez cloner le dépôt et contribuer au projet. Un terminal SSH comme OpenSSH sous Linux/macOS ou PuTTY sous Windows sera utile pour les connexions à distance. Wireshark ou tcpdump peuvent être utilisés pour analyser le trafic réseau et vérifier que les communications sont correctement chiffrées. Un outil de gestion des certificats comme OpenSSL sera nécessaire si vous souhaitez générer de nouveaux certificats pour la production.

Pour la documentation et les rapports, un éditeur Markdown tel que Typora, VS Code avec l'extension Markdown All in One, ou même un simple éditeur de texte suffira. La présentation finale peut être réalisée avec des outils comme LibreOffice Impress, Microsoft PowerPoint, ou des solutions web comme Reveal.js pour des présentations interactives. Un environnement de test virtuel (VM) avec VirtualBox ou VMware permettra d'isoler le système de votre environnement de production pour les tests de sécurité.

## 2. Installation

### 2.1 Cloner le Dépôt

La première étape de l'installation consiste à cloner le dépôt GitHub contenant le code source du projet. Ouvrez un terminal et exécutez la commande suivante pour cloner le dépôt dans le répertoire de votre choix. Cette commande téléchargera tous les fichiers du projet, y compris l'historique Git complet, ce qui vous permettra de revenir à des versions antérieures si nécessaire. Assurez-vous d'avoir Git installé sur votre système avant d'exécuter cette commande. Si vous n'avez pas Git, vous pouvez télécharger l'archive ZIP du projet depuis la page GitHub et l'extraire dans le répertoire souhaité.

```bash
git clone https://github.com/Dhiasaid/dhiasaidC2_part2.git
cd dhiasaidC2_part2
```

Une fois le clonage terminé, vérifiez que tous les fichiers ont été correctement téléchargés en listant le contenu du répertoire. Vous devrait voir les fichiers principaux du projet, notamment le fichier client.py et le certificat cert.pem. Si certains fichiers manquent, essayez de renouveler le clonage ou vérifiez votre connexion Internet. Le dépôt contient également un environnement virtuel Python préconfiguré dans le répertoire dhia/, qui peut être utilisé directement sans installation supplémentaire des dépendances.

### 2.2 Configuration de l'Environnement Virtuel

L'environnement virtuel Python inclus dans le projet se trouve dans le répertoire dhia/ et contient toutes les dépendances nécessaires préinstallées. Pour activer cet environnement sur un système Linux ou macOS, exécutez la commande suivante dans le terminal. Cette commande configure l'environnement pour utiliser l'interpréteur Python et les packages installés dans le répertoire dhia/, isolant ainsi votre installation du système global. L'utilisation d'un environnement virtuel est une bonne pratique qui évite les conflits entre les dépendances de différents projets.

```bash
source dhia/bin/activate
```

Sur Windows, l'activation de l'environnement virtuel se fait différemment. Ouvrez l'invite de commandes ou PowerShell et naviguez vers le répertoire du projet, puis exécutez le script d'activation approprié. Pour l'invite de commandes, utilisez `dhia\Scripts\activate.bat`, et pour PowerShell, utilisez `dhia\Scripts\Activate.ps1`. Une fois l'environnement activé, vous devriez voir le nom de l'environnement (dhia) apparaître au début de votre ligne de commande, indiquant que vous travaillez désormais dans l'environnement virtuel isolé.

Si vous préférez créer un nouvel environnement virtuel ou installer les dépendances manuellement, vous pouvez le faire en suivant ces étapes. Créez d'abord un nouvel environnement virtuel avec la commande `python -m venv mon_env`, puis activez-le avec la commande appropriée pour votre système. Ensuite, installez les dépendances en exécutant `pip install -r requirements.txt` si un fichier requirements.txt est disponible, ou installez chaque dépendance individuellement avec `pip install flask`. L'avantage de cette approche est que vous aurez un contrôle total sur les versions des packages installés.

### 2.3 Génération des Certificats

Le système C2 utilise des certificats TLS pour sécuriser les communications entre le serveur et les clients. Un certificat auto-signé (cert.pem) est fourni avec le projet à des fins de développement et de test. Pour un environnement de production, il est fortement recommandé d'utiliser des certificats signés par une autorité de certification reconnue. Les certificats auto-signés sont pratiques pour les tests mais ne doivent jamais être utilisés en production car ils exposent les utilisateurs à des attaques de type "man-in-the-middle".

Pour générer un nouveau certificat auto-signé avec OpenSSL, exécutez la commande suivante. Cette commande crée une clé privée et un certificat X.509 valide pour un an. Remplacez les valeurs des champs CN (Common Name), O (Organization), et C (Country) par vos propres informations. Le certificat généré sera stocké dans le fichier server.crt et la clé privée dans server.key. Conservez la clé privée dans un emplacement sécurisé et ne la partagez jamais, car elle permet de déchiffrer toutes les communications.

```bash
openssl req -x509 -newkey rsa:4096 -keyout server.key -out server.crt \
    -days 365 -nodes -subj "/CN=localhost/O=MyOrganization/C=FR"
```

Si vous devez générer des certificats pour un domaine spécifique ou une adresse IP publique, vous devrez peut-être ajouter des extensions SAN (Subject Alternative Name) au certificat. OpenSSL requiert un fichier de configuration pour cela. Créez un fichier openssl.cnf contenant les extensions nécessaires, puis générez le certificat avec la commande modifiée pour inclure ce fichier de configuration. Pour un déploiement en production, envisagez d'utiliser des certificats gratuits de Let's Encrypt ou des certificats commerciaux de fournisseurs comme DigiCert ou GlobalSign.

### 2.4 Configuration du Projet

La configuration du système se fait principalement dans le fichier client.py pour la partie cliente, et dans les fichiers de configuration du serveur que vous devrez créer ou adapter. Le client est configuré pour se connecter à l'adresse IP 127.0.0.1 (localhost) sur le port 1234 par défaut. Ces valeurs peuvent être modifiées directement dans le code source en изменянт les variables `server_ip` et `server_port` au début du fichier client.py. Pour un déploiement réel, vous devrez configurer le serveur avec l'adresse IP publique de votre machine et un port qui n'est pas bloqué par les pare-feux.

Voici un exemple de configuration avancée avec des options supplémentaires. Vous pouvez ajouter des variables d'environnement pour rendre la configuration plus flexible et éviter de modifier le code source à chaque changement. Cette approche est particulièrement utile lorsque vous déployez le système sur plusieurs machines ou lorsque vous utilisez des conteneurs Docker. Les variables d'environnement peuvent être définies dans un fichier .env chargé au démarrage de l'application, ou configurées directement dans votre environnement système.

```python
import os

# Configuration via variables d'environnement
server_ip = os.getenv('C2_SERVER_IP', '127.0.0.1')
server_port = int(os.getenv('C2_SERVER_PORT', '1234'))
cert_path = os.getenv('C2_CERT_PATH', 'cert.pem')

# Utilisation du certificat personnalisé
context = ssl.create_default_context()
context.load_verify_locations(cert_path)
context.check_hostname = False
context.verify_mode = ssl.CERT_REQUIRED
```

## 3. Utilisation

### 3.1 Lancement du Serveur

Le lancement du serveur C2 est la première étape pour mettre en place l'infrastructure de contrôle. Assurez-vous d'abord que toutes les dépendances sont installées et que la configuration est correcte. Le serveur doit être lancé avant les clients, car les clients tenteront de se connecter immédiatement au démarrage. Dans un environnement de production, le serveur devrait être lancé en tant que service système pour garantir son redémarrage automatique en cas de plantage ou de redémarrage de la machine.

Pour lancer le serveur, vous devez d'abord créer le script serveur si celui-ci n'existe pas déjà dans le projet. Le serveur écoutera les connexions entrantes sur le port configuré, gérera l'authentification des clients via les certificats TLS, et distribuera les commandes aux clients connectés. Chaque client connecté sera associé à une session unique permettant de suivre les commandes exécutées et les résultats obtenus. Le serveur devrait également logger toutes les activités pour faciliter le débogage et l'audit de sécurité.

Voici un exemple de script serveur basique utilisant Flask et les sockets. Ce script crée un serveur HTTP simple qui peut servir d'interface d'administration et gérer les connexions des clients. Pour un système C2 complet, vous devrez développer une logique plus sophistiquée pour la gestion des commandes, la persistance des sessions, et l'interface d'administration.

```python
#!/usr/bin/env python3
import socket
import ssl
import threading
from flask import Flask, jsonify

app = Flask(__name__)

# Configuration du serveur
SERVER_IP = '0.0.0.0'
SERVER_PORT = 1234
CERT_FILE = 'server.crt'
KEY_FILE = 'server.key'

# Liste des clients connectés
connected_clients = []

def handle_client(client_socket, client_address):
    """Gère la connexion d'un client individuel."""
    print(f"[+] Nouveau client connecté: {client_address}")
    connected_clients.append((client_socket, client_address))
    
    try:
        while True:
            data = client_socket.recv(4096)
            if not data:
                break
            print(f"[*] Données reçues de {client_address}: {data.decode()}")
    except Exception as e:
        print(f"[-] Erreur avec {client_address}: {e}")
    finally:
        client_socket.close()
        connected_clients.remove((client_socket, client_address))
        print(f"[-] Client déconnecté: {client_address}")

def start_tcp_server():
    """Démarre le serveur TCP pour les connexions clients."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(CERT_FILE, KEY_FILE)
    server_socket = context.wrap_socket(server_socket, server_side=True)
    
    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.listen(5)
    print(f"[*] Serveur C2 en écoute sur {SERVER_IP}:{SERVER_PORT}")
    
    while True:
        client_socket, client_address = server_socket.accept()
        client_thread = threading.Thread(
            target=handle_client, 
            args=(client_socket, client_address)
        )
        client_thread.daemon = True
        client_thread.start()

if __name__ == '__main__':
    # Démarrer le serveur TCP dans un thread séparé
    server_thread = threading.Thread(target=start_tcp_server)
    server_thread.daemon = True
    server_thread.start()
    
    # Démarrer l'interface d'administration Flask
    app.run(host='0.0.0.0', port=5000, debug=False)
```

### 3.2 Connexion des Clients

Une fois le serveur en cours d'exécution, vous pouvez lancer les clients qui se connecteront automatiquement au serveur. Le client fourni dans le projet (client.py) est préconfiguré pour se connecter à localhost sur le port 1234. Pour chaque machine que vous souhaitez contrôler, déployez le fichier client.py et le certificat cert.pem, puis lancez le client. Le client établira une connexion TLS sécurisée avec le serveur et attendra les commandes.

Pour exécuter le client, utilisez la commande suivante dans un terminal. Le client affichera des messages de débogage indiquant l'état de la connexion et les commandes reçues. En mode normal, le client fonctionne en arrière-plan et ne nécessite aucune interaction utilisateur. Vous pouvez rediriger la sortie vers un fichier de log pour faciliter le suivi des activités.

```bash
python client.py
```

Le client affichera les messages suivants lors d'une connexion réussie. Le message "[+] Connected securely to C2 Server (TLS)" indique que la connexion TLS a été établie avec succès. Le message "[*] Received command:" suivi d'une commande montre qu'une commande a été reçue du serveur. Le message "[*] Sending output" indique que les résultats de la commande sont envoyés au serveur. Si la connexion est perdue, le client affichera "[-] Connection lost. Exiting..." et se fermera proprement.

### 3.3 Envoi de Commandes

L'envoi de commandes aux clients connectés se fait via l'interface d'administration du serveur ou directement via le socket TCP. Chaque commande reçue par un client est exécutée via le shell système du client, ce qui permet un contrôle total sur la machine distante. Cependant, cette fonctionnalité présente des risques de sécurité importants si elle est mal configurée, car elle permet théoriquement l'exécution de n'importe quelle commande sur les machines clientes.

Voici quelques exemples de commandes que vous pouvez envoyer aux clients. La commande "whoami" renvoie le nom de l'utilisateur actuel sur le client, permettant d'identifier le contexte d'exécution. La commande "ipconfig" (Windows) ou "ifconfig" (Linux/macOS) affiche la configuration réseau du client, utile pour le diagnostic des problèmes de connectivité. La commande "pwd" affiche le répertoire de travail courant. La commande "ls" ou "dir" liste les fichiers du répertoire courant. La commande "quit" provoque la déconnexion propre du client et la fermeture de la connexion.

Pour automatiser l'envoi de commandes à plusieurs clients, vous pouvez développer des scripts qui interagissent avec l'API du serveur ou qui se connectent directement aux sockets clients. Une approche courante consiste à créer un système de files d'attente où les commandes sont stockées et distribuées aux clients selon un calendrier ou en réponse à des événements spécifiques. Cette architecture permet de gérer des milliers de clients simultanément et d'exécuter des campagnes de commands à grande échelle.

### 3.4 Interface d'Administration

L'interface d'administration basée sur Flask fournit une vue d'ensemble des clients connectés et permet d'envoyer des commandes de manière centralisée. L'interface affiche la liste des clients avec leur adresse IP, l'heure de connexion, et le statut actuel. Vous pouvez sélectionner un ou plusieurs clients et entrer une commande à exécuter sur les machines sélectionnées. Les résultats sont affichés en temps réel ou peuvent être consultés ultérieurement dans l'historique des sessions.

L'API REST du serveur expose plusieurs endpoints pour l'interaction programmatique avec le système. L'endpoint GET /api/clients renvoie la liste de tous les clients connectés au format JSON. L'endpoint GET /api/clients/<id> renvoie les détails d'un client spécifique. L'endpoint POST /api/commands permet d'envoyer une commande à un ou plusieurs clients. L'endpoint GET /api/history/<client_id> renvoie l'historique des commandes exécutées sur un client particulier. Ces endpoints permettent l'intégration avec d'autres outils d'administration ou l'automatisation de tâches complexes.

## 4. Maintenance

### 4.1 Surveillance et Logs

La surveillance du système C2 est essentielle pour garantir son bon fonctionnement et détecter les anomalies. Les logs doivent être configurés pour capturer tous les événements importants, notamment les connexions et déconnexions des clients, les commandes exécutées, les erreurs de communication, et les tentatives d'accès non autorisées. Une rotation des logs doit être mise en place pour éviter la saturation de l'espace disque, avec une conservation configurable selon vos besoins de rétention.

Le système de logging Python offre des fonctionnalités avancées qui peuvent être exploitées pour améliorer la visibilité sur les activités du système. Vous pouvez configurer différents niveaux de log (DEBUG, INFO, WARNING, ERROR, CRITICAL) et diriger les logs vers différents destinations (fichier, console, serveur syslog distant). Pour un système de production, il est recommandé d'utiliser un système de gestion des logs centralisé comme ELK Stack (Elasticsearch, Logstash, Kibana) ou Splunk pour l'analyse et la corrélation des événements.

Voici un exemple de configuration de logging avancée pour le serveur C2. Cette configuration envoie les logs vers un fichier avec une rotation automatique basée sur la taille et la date, et applique un format détaillé incluant le timestamp, le niveau de log, et le nom du module source.

```python
import logging
from logging.handlers import RotatingFileHandler

# Configuration du logging
log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# Handler pour la console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter(log_format))

# Handler pour fichier avec rotation
file_handler = RotatingFileHandler(
    'c2_server.log', 
    maxBytes=10*1024*1024,  # 10 Mo par fichier
    backupCount=10,
    encoding='utf-8'
)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter(log_format))

# Configuration du logger racine
logging.basicConfig(
    level=logging.DEBUG,
    handlers=[console_handler, file_handler]
)

logger = logging.getLogger(__name__)
```

### 4.2 Sauvegarde et Restauration

La sauvegarde régulière des données du système C2 est cruciale pour la continuité des opérations et la récupération après incident. Les données à sauvegarder incluent la base de données des sessions clients (si utilisée), les logs d'activité, les certificats et clés, les fichiers de configuration, et le code source du système. La fréquence de sauvegarde dépend de la criticité du système et de la fréquence des changements de configuration.

Pour restaurer le système après un incident, suivez cette procédure. Restaurez d'abord les fichiers de configuration et les certificats, puis le code source si des modifications locales ont été effectuées. Restaurez ensuite les données de la base de données des sessions clients si elle existe. Vérifiez l'intégrité des fichiers restaurés et redémarrez le serveur. Testez la connectivité avec quelques clients de test avant de réactiver tous les clients en production.

Un script de sauvegarde automatisé peut être créé pour simplifier ce processus. Ce script peut utiliser des outils comme rsync pour la synchronisation incrémentale des fichiers et des bases de données, et cron (Linux) ou le Planificateur de tâches (Windows) pour l'exécution automatique selon un calendrier défini. Les sauvegardes doivent être testées régulièrement pour s'assurer qu'elles peuvent être restaurées correctement.

### 4.3 Mise à Jour du Système

La mise à jour régulière du système C2 est nécessaire pour corriger les vulnérabilités de sécurité et bénéficier des nouvelles fonctionnalités. Avant d'effectuer une mise à jour, créez une sauvegarde complète du système et testez la mise à jour dans un environnement de test. Les mises à jour doivent être planifiées pendant une fenêtre de maintenance où l'indisponibilité du service est acceptable.

Pour mettre à jour les dépendances Python, activez l'environnement virtuel et exécutez `pip install --upgrade <package>` pour chaque package à mettre à jour, ou `pip install -r requirements.txt` avec un fichier requirements.txt mis à jour pour mettre à jour tous les packages. Après la mise à jour, testez le système pour vous assurer que toutes les fonctionnalités fonctionnent correctement. Documentez les changements effectués et les éventuels problèmes rencontrés pour référence ultérieure.

## 5. Dépannage

### 5.1 Problèmes Courants

Plusieurs problèmes courants peuvent survenir lors de l'utilisation du système C2. Si les clients ne peuvent pas se connecter au serveur, vérifiez que le pare-feu autorise les connexions sur le port utilisé, que le serveur est bien en écoute sur l'interface réseau correcte, et que les certificats TLS sont valides et compatibles. Les erreurs de certificat peuvent être causées par des certificats expirés, des certificats auto-signés non reconnus, ou des incompatibilités de version de TLS.

Si les commandes ne sont pas exécutées correctement sur les clients, vérifiez que les commandes sont valides pour le système d'exploitation du client, que les chemins d'accès sont corrects, et que l'utilisateur sous lequel le client s'exécute dispose des permissions nécessaires. Les commandes qui nécessitent des privilèges administratifs ne fonctionneront pas si le client n'est pas lancé avec les droits appropriés. Utilisez la commande "quit" uniquement lorsque vous souhaitez arrêter définitivement le client, car elle provoque la déconnexion et la fermeture du programme.

Les problèmes de performance peuvent être causés par un trop grand nombre de clients simultanés, des ressources système insuffisantes, ou des problèmes réseau. Surveillez l'utilisation des ressources (CPU, mémoire, bande passante réseau) et ajustez la configuration du système en conséquence. Si nécessaire, distribuez la charge sur plusieurs serveurs en utilisant un système de load balancing.

### 5.2 Diagnostic Réseau

Le diagnostic des problèmes de connectivité réseau peut être effectué avec plusieurs outils. La commande `ping` permet de vérifier la connectivité de base entre le serveur et les clients. La commande `telnet` ou `nc` (netcat) permet de tester si un port est ouvert et accessible. Pour tester la connexion TLS, vous pouvez utiliser `openssl s_client -connect <ip>:<port>` qui affiche les détails de la négociation TLS et permet de vérifier que le certificat est correct.

Wireshark est un outil puissant pour analyser le trafic réseau en détail. Vous pouvez capturer les paquets échangés entre le serveur et les clients et vérifier que les données sont correctement chiffrées (les paquets TLS apparaissent comme des données illisibles dans Wireshark). Cet outil est particulièrement utile pour diagnostiquer les problèmes de négociation TLS et les pertes de paquets.

### 5.3 Support et Ressources

Si vous rencontrez des problèmes non couverts par ce guide, plusieurs ressources sont disponibles pour obtenir de l'aide. La documentation officielle de Python, Flask, et les bibliothèques SSL fournit des informations détaillées sur le fonctionnement de ces technologies. Les forums de développeurs comme Stack Overflow contiennent des réponses à de nombreux problèmes courants. Les communautés GitHub et les issues du projet peuvent contenir des informations sur les bogues connus et leurs solutions.

Pour les problèmes de sécurité, suivez les bonnes pratiques de sécurité et ne partagez jamais d'informations sensibles comme les clés privées ou les mots de passe dans les forums publics. Si vous découvre une vulnérabilité dans le système, signalez-la de manière responsable aux mainteneurs du projet avant de la publier.
