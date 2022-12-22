import gradio as gr
import pandas as pd
from predictLSTM import predictFile_LSTM
from predictANN import predictFile_ANN

def predict(csv_file):
    print(csv_file.name)
    dataframe = pd.read_csv(csv_file.name, names=['text'], encoding=('ISO-8859-1'))
    dataframe['result_ANN'] = predictFile_ANN(dataframe)
    dataframe['result_LSTM'] = predictFile_LSTM(dataframe)
    row_10 = dataframe.head(5)
    dataframe.to_csv('output.csv', index=False)
    output_csv = "output.csv"
    return row_10, dataframe.head(5), output_csv

gradio_ui = gr.Interface(
    fn=predict,
    title="Predict File Sentiment",
    inputs=[gr.components.File(label="CSV File")],
    outputs=[gr.components.Dataframe(label="Input Data"),gr.components.Dataframe(label="top 5 data"),gr.components.File(label="Output CSV")]
)

gradio_ui.launch()