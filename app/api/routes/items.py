from fastapi import APIRouter, Depends
from app.api.deps import get_current_user

router = APIRouter(prefix="/items", tags=["items"]) # création d'un routeur FastAPI pour les routes liées aux items. Le préfixe "/items" signifie que toutes les routes définies dans ce routeur commenceront par "/items". Par exemple, la route définie ci-dessous sera accessible à l'URL "/items/". Les tags=["items"] sont utilisés pour organiser et documenter les routes dans la documentation interactive de FastAPI (Swagger UI). Cela permet de regrouper les routes liées aux items sous une même catégorie "items" dans la documentation, ce qui facilite la navigation et la compréhension de l'API.

@router.get("/")
def list_items(current_user: str = Depends(get_current_user)): # depends signifie que la fonction list_items dépend de la fonction get_current_user pour obtenir l'utilisateur actuel à partir du token d'accès JWT fourni dans la requête. 
    #Lorsque cette route est appelée, FastAPI exécutera d'abord get_current_user pour extraire et vérifier le token, puis passera le résultat (le nom d'utilisateur) à la variable current_user dans list_items. Si le token est valide, nous pouvons utiliser current_user pour personnaliser la réponse ou effectuer des actions spécifiques à l'utilisateur. 
    # Si le token est invalide ou expiré, l'accès à cette route sera refusé avec une erreur 401 Unauthorized.
    return {"user": current_user, "items": ["item1", "item2"]}

    # cette page sert à créer une route protégée qui nécessite une authentification pour accéder à la liste des items. 
    # En utilisant Depends(get_current_user), nous injectons automatiquement l'utilisateur actuel (extrait du token d'accès JWT) dans la fonction list_items. 
    # Si le token est valide, nous retournons une réponse contenant le nom de l'utilisateur et une liste d'items fictifs. Si le token est invalide ou expiré, l'accès à cette route sera refusé avec une erreur 401 Unauthorized.