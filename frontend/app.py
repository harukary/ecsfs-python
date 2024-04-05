import gradio as gr
import requests, os

BACKEND = os.getenv("BACKEND", 'ecsfs-backend.local')

def fetch_backend_greeting():
    print(f"http://{BACKEND}:5000")
    response = requests.get(f"http://{BACKEND}:5000")
    return response.text

def fetch_opensearch_info():
    response = requests.get(f"http://{BACKEND}:5000/opensearch_info")
    if response.status_code == 200:
        return response.json()
    else:
        return f"OpenSearch information could not be retrieved. {response.json()}"

def fetch_documentdb_info():
    response = requests.get(f"http://{BACKEND}:5000/documentdb_info")
    if response.status_code == 200:
        return response.json()
    else:
        return f"DocumentDB information could not be retrieved. {response.json()}"

app = gr.Blocks()

with app:
    gr.Markdown("### Frontend Greeting")
    greet_button = gr.Button("Greet from Backend")
    greet_res = gr.Textbox(label="Backend Greeting")
    greet_button.click(fn=fetch_backend_greeting, inputs=[], outputs=[greet_res])
    
    gr.Markdown("### OpenSearch Information")
    opensearch_button = gr.Button("Fetch OpenSearch Info")
    opensearch_res = gr.Textbox(label="OpenSearch Info")
    opensearch_button.click(fn=fetch_opensearch_info, inputs=[], outputs=[opensearch_res])

    gr.Markdown("### DocumentDB Information")
    documentdb_button = gr.Button("Fetch DocumentDB Info")
    documentdb_res = gr.Textbox(label="DocumentDB Info")
    documentdb_button.click(fn=fetch_documentdb_info, inputs=[], outputs=[documentdb_res])

if __name__ == "__main__":
    app.launch(server_name="0.0.0.0", server_port=3000)
