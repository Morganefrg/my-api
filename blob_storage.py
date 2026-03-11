from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
from datetime import datetime, timedelta, timezone


# Votre chaîne de connexion
import os
from dotenv import load_dotenv

load_dotenv(".secrets/.env")

CONNECTION_STRING = os.getenv("BLOB_CONNECTION_STRING")

# Connexion au Blob Storage
blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
container_client = blob_service_client.get_container_client(CONTAINER_NAME)

def upload_file(file_path: str, blob_name: str):
    with open(file_path, "rb") as data:
        container_client.upload_blob(name=blob_name, data=data, overwrite=True)
    print(f"✅ Fichier '{blob_name}' envoyé avec succès !")
    # def upload_file sert à envoyer un fichier local vers Azure Blob Storage. Elle prend en paramètre le chemin du fichier local (file_path) et le nom que le fichier aura dans le conteneur Azure (blob_name). La fonction ouvre le fichier en mode binaire, puis utilise la méthode upload_blob du client de conteneur pour télécharger le fichier vers Azure Blob Storage. L'option overwrite=True permet de remplacer un fichier existant avec le même nom. Après l'upload, un message de confirmation est affiché dans la console.

def list_files():
    blobs = container_client.list_blobs()
    print("📁 Fichiers dans le conteneur :")
    for blob in blobs:
        print(f"  - {blob.name}")
        # list_files sert à lister tous les fichiers présents dans le conteneur Azure Blob Storage. Elle utilise la méthode list_blobs du client de conteneur pour récupérer une liste de tous les blobs (fichiers) dans le conteneur, puis affiche leurs noms dans la console.

def download_file(blob_name: str, download_path: str):
    blob_client = container_client.get_blob_client(blob_name)
    with open(download_path, "wb") as f:
        f.write(blob_client.download_blob().readall())
    print(f"✅ Fichier '{blob_name}' téléchargé !")
    # download_file sert à télécharger un fichier depuis Azure Blob Storage vers un chemin local. Elle prend en paramètre le nom du blob à télécharger (blob_name) et le chemin local où le fichier doit être enregistré (download_path). La fonction crée un client de blob pour le fichier spécifié, puis utilise la méthode download_blob pour récupérer le contenu du blob et l'écrire dans un fichier local en mode binaire. Après le téléchargement, un message de confirmation est affiché dans la console.

def delete_file(blob_name: str): 
    container_client.delete_blob(blob_name)
    print(f"🗑️ Fichier '{blob_name}' supprimé !")
    # delete_file sert à supprimer un fichier du conteneur Azure Blob Storage. Elle prend en paramètre le nom du blob à supprimer (blob_name) et utilise la méthode delete_blob du client de conteneur pour supprimer le fichier spécifié. Après la suppression, un message de confirmation est affiché dans la console.


def generate_download_link(blob_name: str, expiry_minutes: int = 3) -> str:
    # Extraire le nom du compte et la clé depuis la connection string
    account_name = blob_service_client.account_name
    account_key = blob_service_client.credential.account_key

    sas_token = generate_blob_sas(
        account_name=account_name,
        container_name=CONTAINER_NAME,
        blob_name=blob_name,
        account_key=account_key,
        permission=BlobSasPermissions(read=True),
        expiry=datetime.now(timezone.utc) + timedelta(minutes=expiry_minutes)
    )

    url = f"https://{account_name}.blob.core.windows.net/{CONTAINER_NAME}/{blob_name}?{sas_token}"
    print(f"🔗 Lien de téléchargement ({expiry_minutes} min) : {url}")
    return url


if __name__ == "__main__":
    with open("test.txt", "w") as f:
        f.write("Bonjour depuis mon API !")
        # ce bloc de code est exécuté lorsque le script est lancé directement. Il crée un fichier local nommé "test.txt" et y écrit une ligne de texte. Ensuite, il appelle la fonction upload_file pour envoyer ce fichier vers Azure Blob Storage, puis appelle list_files pour afficher la liste des fichiers présents dans le conteneur. Cela permet de tester les fonctionnalités d'upload et de listing des fichiers dans Azure Blob Storage.
    # Envoyer une image et générer un lien
    upload_file("test.txt", "test.txt")
    generate_download_link("test.txt", expiry_minutes=3)
    upload_file("test.txt", "test.txt")
    list_files()
    # ces deux dernieres fonctions sont appelées pour tester les fonctionnalités d'upload et de listing des fichiers dans Azure Blob Storage. upload_file("test.txt", "test.txt") envoie le fichier local "test.txt" vers Azure Blob Storage avec le même nom, tandis que list_files() affiche la liste des fichiers présents dans le conteneur, ce qui permet de vérifier que le fichier a été correctement téléchargé.