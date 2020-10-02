from google.cloud import secretmanager
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-oas', '--oauth2-client-secret', required=True)
parser.add_argument('-sus', '--sqlalchemy-url-secret', required=True)
parser.add_argument('-p', '--project-id', required=True)
parser.add_argument('-f', '--file-path', required=True)
args = parser.parse_args()
env_file_path = args.file_path
project_id = args.project_id
client_secret_secret_id = args.oauth2_client_secret
sqlalchemy_url_secret_id = args.sqlalchemy_url_secret

client = secretmanager.SecretManagerServiceClient()
client_secret_name = f"projects/{project_id}/secrets/{client_secret_secret_id}/versions/latest"
sqlalchemy_url_secret_name = f"projects/{project_id}/secrets/{sqlalchemy_url_secret_id}/versions/latest"
client_secret_key_response = client.access_secret_version(request={"name": client_secret_name})
sqlalchemy_url_key_response = client.access_secret_version(request={"name": sqlalchemy_url_secret_name})
client_secret_string = f"CKAN_OAUTH2_CLIENT_SECRET={client_secret_key_response}"
sqlalchemy_url_string = f"CKAN_SQLALCHEMY_URL={sqlalchemy_url_key_response}"
with open(env_file_path, "a") as env_file:
    env_file.write(client_secret_string)
    env_file.write(sqlalchemy_url_string)
