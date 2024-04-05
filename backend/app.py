import time, random, os
from fastapi import FastAPI, HTTPException
from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import boto3
from pymongo import MongoClient, errors

app = FastAPI()

# 環境変数から接続情報を読み込む
OPENSEARCH_HOST = os.getenv("OPENSEARCH_HOST", 'localhost')
OPENSEARCH_PORT = os.getenv("OPENSEARCH_PORT", 443)
OPENSEARCH_USERNAME = os.getenv("OPENSEARCH_USERNAME", 'admin')
OPENSEARCH_PASSWORD = os.getenv("OPENSEARCH_PASSWORD", 'admin')
# OPENSEARCH_COLLECTION_NAME = os.getenv("OPENSEARCH_COLLECTION_NAME", 'my_collection')

DOCUMENTDB_HOST = os.getenv("DOCUMENTDB_HOST", 'localhost')
DOCUMENTDB_USERNAME = os.getenv("DOCUMENTDB_USERNAME", 'admin')
DOCUMENTDB_PASSWORD = os.getenv("DOCUMENTDB_PASSWORD", 'admin')

    
# OpenSearchクライアントの初期化
try:
    session = boto3.Session()
    credentials = session.get_credentials()
    awsauth = AWS4Auth(
        credentials.access_key,
        credentials.secret_key,
        session.region_name,
        'es',
        session_token=credentials.token
    )
    opensearch_client = OpenSearch(
        hosts=[{'host': OPENSEARCH_HOST, 'port': OPENSEARCH_PORT}],
        http_auth=awsauth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection
    )
except Exception as e:
    print(e)
    opensearch_client = None

# DocumentDBクライアントの初期化
try:
    # global-bundle.pemがカレントディレクトリに存在するか確認するコード
    if os.path.exists('global-bundle.pem'):
        print('`global-bundle.pem` found.')
    else:
        raise FileNotFoundError('`global-bundle.pem` not found.')
    mongo_client = MongoClient(
        host=DOCUMENTDB_HOST,
        port=27017,
        username=DOCUMENTDB_USERNAME,
        password=DOCUMENTDB_PASSWORD,
        tls=True,
        tlsCAFile='global-bundle.pem',
        replicaSet='rs0',
        readPreference='secondaryPreferred',
        retryWrites=False
    )
except Exception as e:
    mongo_client = None

@app.get("/opensearch_info")
def get_opensearch_info():
    if not opensearch_client:
        raise HTTPException(status_code=503, detail="OpenSearch is not configured or unavailable")
    try:
        info = opensearch_client.info()
        return {"opensearch_info": str(info)}
    except Exception as e:
        print(f"Failed to get OpenSearch info: {str(e)}")
        raise HTTPException(status_code=503, detail="Failed to get OpenSearch info")

@app.get("/documentdb_info")
def get_documentdb_info():
    if not mongo_client:
        raise HTTPException(status_code=503, detail="DocumentDB is not configured or unavailable")
    try:
        db = mongo_client.test_database
        collection = db.test_collection
        collection.insert_one({"message": "Hello, DocumentDB!"})
        document = collection.find_one({"message": "Hello, DocumentDB!"})
        return {"documentdb_info": str(document)}
    except Exception as e:
        print(f"Failed to get DocumentDB info: {str(e)}")
        raise HTTPException(status_code=503, detail="Failed to get DocumentDB info")

@app.get("/")
def read_root():
    interval = time.time() + 1

    # Simulates some CPU load.
    while time.time() < interval:
        x = 435344
        x * x
        x = x + random.randint(-12314, 10010)

    return {"message": f"Hello from the backend. Backend computed {x}"}