from pydantic import BaseModel # Pydantic est une bibliothèque de validation de données qui permet de définir des modèles de données avec des types et des contraintes. Nous allons utiliser Pydantic pour définir les schémas de données que notre API va utiliser pour les requêtes et les réponses.

class UserCreate(BaseModel):
    username: str
    password: str # ce modèle représente les données nécessaires pour créer un nouvel utilisateur. Il contient deux champs : username (le nom d'utilisateur) et password (le mot de passe en clair). Ce modèle sera utilisé pour valider les données envoyées par le client lors de la création d'un nouvel utilisateur.

class UserResponse(BaseModel):
    username: str
    message: str
    # données que l'API renvoie après l'inscription d'un utilisateur. Il contient le nom d'utilisateur et un message de confirmation. Ce modèle sera utilisé pour formater la réponse de l'API après la création d'un nouvel utilisateur.


class Token(BaseModel): # cette classe représente le schéma d'un token d'accès JWT que notre API va retourner lors de l'authentification. Elle hérite de BaseModel, ce qui lui permet de bénéficier des fonctionnalités de validation et de sérialisation de Pydantic.
    access_token: str # le champ access_token est une chaîne de caractères qui contiendra le token JWT généré par notre API. Ce token sera utilisé par les clients pour s'authentifier lors de leurs requêtes. est le JWT que ton API renvoie au client après authentification.
# C’est la “clé d’accès” que le client utilisera ensuite pour appeler les routes protégées.
    token_type: str = "bearer" # le champ token_type est une chaîne de caractères qui indique le type de token. Par convention, pour les tokens d'accès JWT, on utilise "bearer".