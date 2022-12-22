import gradio as gr
from predictLSTM import predictText_LSTM
from predictANN import predictText_ANN
import pandas as pd

def predict(text):
    result_ANN = predictText_ANN(text)
    result_LSTM = predictText_LSTM(text)
    d = {'text': [text], 'result_ANN': [result_ANN], 'result_LSTM': [result_LSTM]}
    df = pd.DataFrame(data=d)
    return df

text_input = gr.Textbox(label="text")

gradio_ui = gr.Interface(
    fn=predict,
    title="Predict Text Sentiment",
    inputs=[text_input],
    outputs=[gr.components.Dataframe(label="Result")]
)

gradio_ui.launch() 