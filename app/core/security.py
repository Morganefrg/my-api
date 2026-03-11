import os # pour accéder aux variables d'environnement, qui est un endroit plus sûr pour stocker des secrets que de les mettre en dur dans le code
from datetime import datetime, timedelta, timezone #  # ← ajouter # datetime pour gérer les dates et heures, timedelta pour faire des calculs de temps (comme ajouter des minutes), timezone pour s'assurer que les dates sont en UTC
from dotenv import load_dotenv 
from jose import jwt # jose est une bibliothèque qui permet de créer et vérifier des JWT (JSON Web Tokens), qui sont des tokens d'authentification couramment utilisés dans les API.
# jose permet de créer des tokens sécurisés en les signant avec une clé secrète, et de vérifier ces tokens pour s'assurer qu'ils sont valides et n'ont pas été altérés.

load_dotenv(".secrets/.env")

SECRET_KEY = os.getenv("SECRET_KEY", "CHANGE_ME_IN_ENV") # sert à signer les JWT, ne pas oublier de le changer pour une valeur plus sécurisée et de ne pas le commiter dans le code !
ALGORITHM = "HS256" # l'algorithme de signature utilisé pour les JWT. HS256 signifie HMAC avec SHA-256, qui est un algorithme de signature symétrique. Cela signifie que la même clé secrète est utilisée à la fois pour signer et vérifier les tokens. C'est un choix courant pour les API simples, mais pour des applications plus complexes ou nécessitant une sécurité renforcée, on pourrait envisager d'utiliser un algorithme asymétrique comme RS256.
EXPIRE_MINUTES = 20 # la durée de validité des tokens JWT en minutes. Après cette période, les tokens expireront et ne seront plus valides, ce qui oblige les utilisateurs à se réauthentifier pour obtenir un nouveau token. 

def create_access_token(username: str, expires_minutes: int | None = None) -> str: # cette fonction crée un token d'accès JWT pour un utilisateur donné. Elle prend en paramètre le nom d'utilisateur et une durée d'expiration optionnelle en minutes. Si la durée d'expiration n'est pas fournie, elle utilisera la valeur par défaut définie dans EXPIRE_MINUTES.
    now = datetime.now(timezone.utc) # on utilise datetime.now() pour obtenir l'heure actuelle, et timezone.utc pour s'assurer que l'heure est en UTC. Cela est important pour éviter les problèmes de fuseaux horaires lors de la validation des tokens.
    minutes = expires_minutes if expires_minutes is not None else EXPIRE_MINUTES # on détermine la durée d'expiration du token. Si expires_minutes est fourni, on l'utilise, sinon on utilise la valeur par défaut EXPIRE_MINUTES.

    payload = { 
        "sub": username,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=minutes)).timestamp()),
    } # le payload du token JWT est un dictionnaire qui contient les informations que nous voulons inclure dans le token.
    # "sub" (subject) est une revendication standard qui représente l'identité de l'utilisateur, ici le nom d'utilisateur.
    # "iat" (issued at) est une revendication standard qui indique le moment où le token a été émis, exprimé en secondes depuis l'époque Unix (1er janvier 1970).
    # "exp" (expiration) est une revendication standard qui indique le moment où le token expire, également exprimé en secondes depuis l'époque Unix. Nous calculons cela en ajoutant la durée d'expiration (en minutes) à l'heure actuelle.
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM) # enfin, nous utilisons la fonction jwt.encode() pour créer le token JWT. Nous passons le payload, la clé secrète et l'algorithme de signature. La fonction retourne une chaîne de caractères qui est le token JWT signé, que nous pouvons ensuite envoyer au client pour qu'il l'utilise dans les requêtes d'authentification.