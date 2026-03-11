from ldap3 import Server, Connection, ALL, SIMPLE


# APRÈS - valeurs cachées dans .env ✅
import os
from dotenv import load_dotenv

load_dotenv(".secrets/.env")

LDAP_SERVER = os.getenv("LDAP_SERVER")
DOMAIN = os.getenv("DOMAIN")

def authenticate_ldap(username: str, password: str) -> bool:
    try:
        server = Server(LDAP_SERVER, get_info=ALL)
        
        # Format du login : DOMAIN\username
        user = f"{username}@{DOMAIN}"  # → username@isen.fr
        
        conn = Connection(
            server,
            user=user,
            password=password,
            authentication=SIMPLE
        )
        
        if conn.bind():
            print(f"✅ Authentification réussie pour {username}")
            return True
        else:
            print(f"❌ Échec authentification pour {username}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur LDAP : {e}")
        return False


if __name__ == "__main__":
    # Test avec bon mot de passe
    authenticate_ldap("patrice.cognet", os.getenv("LDAP_PASSWORD"))
    
    # # Test avec mauvais mot de passe
    # print("=== Test mauvais mot de passe ===")
    # authenticate_ldap("votre_username", "mauvais_mot_de_passe")