import requests
import gradio as gr

def predict(text):
    data_payload = {
        "text":text,
    }
    url = "http://127.0.0.1:1234/api/v1/lstm/text"
    response = requests.post(url,json=data_payload)
    result = response.json()
    result = result['result']
    return result

text_input = gr.Textbox(label="text")

gradio_ui = gr.Interface(
    fn=predict,
    title="Predict Sentiment",
    inputs=[text_input],
    outputs=[gr.Textbox(label="Sentiment Predict Result")]
)

gradio_ui.launch() 