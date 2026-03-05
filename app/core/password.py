from passlib.context import CryptContext # importation de la classe CryptContext depuis la bibliothèque passlib, qui est utilisée pour gérer le hachage des mots de passe de manière sécurisée.
# passlib est une bibliothèque qui fournit des fonctions pour hacher et vérifier les mots de passe en utilisant des algorithmes de hachage sécurisés comme bcrypt, argon2, etc. CryptContext est une classe qui permet de configurer et d'utiliser ces algorithmes de manière flexible.

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # création d'une instance de CryptContext avec la configuration suivante :
# schemes=["bcrypt"] : cela indique que nous voulons utiliser l'algorithme de hachage bcrypt pour hacher les mots de passe. bcrypt est un algorithme de hachage sécurisé qui est largement recommandé pour le stockage des mots de passe.
# deprecated="auto" : cela signifie que passlib marquera automatiquement les anciens hachages comme obsolètes si nous changeons de schéma de hachage à l'avenir. Cela permet de gérer la transition vers de nouveaux algorithmes de hachage sans casser les anciens mots de passe.

def hash_password(password: str) -> str: # 
    return pwd_context.hash(password) # cette fonction prend un mot de passe en clair (string) et retourne son hachage sécurisé. Elle utilise la méthode hash() de l'instance pwd_context, qui applique l'algorithme de hachage configuré (dans ce cas, bcrypt) pour générer un hachage du mot de passe. Ce hachage peut ensuite être stocké dans la base de données à la place du mot de passe en clair, ce qui améliore la sécurité de l'application en cas de fuite de données.

def verify_password(plain_password: str, hashed_password: str) -> bool: # cette fonction prend un mot de passe en clair et un mot de passe haché, et vérifie si le mot de passe en clair correspond au hachage. Elle retourne True si les mots de passe correspondent, sinon elle retourne False. Cela est utilisé lors de la connexion d'un utilisateur pour vérifier que le mot de passe qu'il a entré correspond au mot de passe stocké dans la base de données (qui est haché).
    return pwd_context.verify(plain_password, hashed_password)