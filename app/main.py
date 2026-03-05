from fastapi import FastAPI
from app.api.routes import auth, items, users
from app.core.database import create_tables

app = FastAPI(title="MY_API")
app.include_router(auth.router) # on inclut le routeur d'authentification dans notre application FastAPI. Cela signifie que toutes les routes définies dans auth.router seront accessibles à partir de notre application principale. Par exemple, si auth.router définit une route "/token", elle sera accessible à l'URL "/auth/token" dans notre application, car nous avons défini le préfixe "/auth" pour ce routeur.
app.include_router(items.router)
app.include_router(users.router) # on inclut également le routeur des users dans notre application FastAPI. Cela signifie que toutes les routes définies dans users.router seront accessibles à partir de notre application principale. Par exemple, si users.router définit une route "/users/", elle sera accessible à l'URL "/users/" dans notre application, car nous avons défini le préfixe "/users" pour ce routeur. En incluant ces routeurs, nous organisons notre code de manière modulaire et maintenable, en séparant les différentes fonctionnalités de notre API (authentification et gestion des users) dans des fichiers distincts.

@app.get("/health")
def health():
    return {"status": "ok"}


@app.on_event("startup")
def startup():
    create_tables()  # crée les tables au démarrage