#Extraire le token depuis la requête, le vérifier, puis récupérer qui est l’utilisateur (souvent username ou user_id) pour le donner à la route protégée.
# C’est ce que fait la fonction get_current_user() dans app.api.deps.py, qui est une dépendance FastAPI que nous allons utiliser dans les routes protégées pour obtenir l’utilisateur actuel à partir du token d’accès JWT fourni dans la requête.

from fastapi import Depends, HTTPException, status # importation de plusieurs classes et fonctions depuis le module fastapi :
# Depends : permet de déclarer des dépendances pour les routes de l'API. Par exemple, nous allons l'utiliser pour injecter automatiquement le token d'authentification dans les routes protégées.
# HTTPException : permet de lever des exceptions HTTP avec un code de statut et un message détail. Nous l'utiliserons pour gérer les erreurs d'authentification et d'autorisation.
from fastapi.security import OAuth2PasswordBearer # importation de la classe OAuth2PasswordBearer depuis fastapi.security. Cette classe est utilisée pour gérer les données de formulaire d'authentification dans les requêtes POST. Elle attend des champs comme "username" et "password" dans le corps de la requête, ce qui est standard pour les flux d'authentification OAuth2 avec mot de passe.
from jose import jwt, JWTError # importation de la bibliothèque jose, qui est utilisée pour créer et vérifier les tokens JWT (JSON Web Tokens). jwt est le module principal de jose qui contient les fonctions pour encoder et décoder les tokens, tandis que JWTError est une classe d'exception qui est levée lorsque le décodage d'un token échoue (par exemple, si le token est invalide ou expiré).

from app.core.security import SECRET_KEY, ALGORITHM # importation de la clé secrète et de l'algorithme de signature depuis le module app.core.security. Ces constantes sont utilisées pour signer et vérifier les tokens JWT. SECRET_KEY est la clé secrète utilisée pour signer les tokens, tandis que ALGORITHM est l'algorithme de signature utilisé (par exemple, HS256). Ces valeurs doivent être cohérentes avec celles utilisées lors de la création des tokens dans app.core.security.create_access_token.

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token") # création d'une instance de OAuth2PasswordBearer, qui est une classe de FastAPI utilisée pour gérer l'authentification basée sur les tokens JWT. Le paramètre tokenUrl="/auth/token" indique l'URL où les clients peuvent obtenir un token d'accès en envoyant leurs identifiants (nom d'utilisateur et mot de passe). Cette URL doit correspondre à la route que nous avons définie dans app.api.routes.auth.login_for_access_token, qui est responsable de l'authentification et de la génération des tokens JWT. En utilisant cette instance oauth2_scheme, nous pouvons facilement extraire le token d'accès des requêtes entrantes dans les routes protégées en utilisant Depends(oauth2_scheme).

def get_current_user(token: str = Depends(oauth2_scheme)) -> str: # cette fonction est une dépendance FastAPI qui permet d'extraire et de vérifier le token d'accès JWT à partir des requêtes entrantes. Elle prend en paramètre un token de type string, qui est automatiquement extrait de la requête grâce à Depends(oauth2_scheme). Cette fonction va décoder le token JWT, vérifier sa validité et son expiration, et retourner le nom d'utilisateur (ou une autre information pertinente) si le token est valide. Si le token est invalide ou expiré, elle lèvera une HTTPException avec un code de statut 401 (Unauthorized) pour indiquer que l'accès est refusé.
    try: # nous allons essayer de décoder le token JWT en utilisant la fonction jwt.decode() de la bibliothèque jose. Nous passons le token, la clé secrète et l'algorithme de signature pour vérifier que le token est valide et n'a pas été altéré. Si le décodage réussit, nous obtenons le payload du token, qui est un dictionnaire contenant les informations que nous avons incluses lors de la création du token (comme "sub", "iat", "exp", etc.).
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token invalide (sub manquant)",
                headers={"WWW-Authenticate": "Bearer"},
            ) 
        return username # si le token est valide et contient un champ "sub" (subject) qui représente le nom d'utilisateur, nous retournons ce nom d'utilisateur. Cela permet aux routes protégées qui utilisent cette dépendance de savoir quel utilisateur est actuellement authentifié à partir du token d'accès JWT fourni dans la requête.

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide ou expiré",
            headers={"WWW-Authenticate": "Bearer"},
        ) # si le décodage du token échoue (par exemple, si le token est invalide ou expiré), une JWTError sera levée. Dans ce cas, nous attrapons cette exception et levons une HTTPException avec un code de statut 401 (Unauthorized) pour indiquer que l'accès est refusé en raison d'un token invalide ou expiré. Le message de détail "Token invalide ou expiré" informe le client de la raison de l'échec de l'authentification.

