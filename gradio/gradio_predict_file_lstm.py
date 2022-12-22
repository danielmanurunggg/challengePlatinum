import gradio as gr
import pandas as pd
from predictLSTM import predictText_LSTM, predictFile_LSTM


def _data_cleaning(csv_file):
    print(csv_file.name)
    dataframe = pd.read_csv(csv_file.name, names=['text'], encoding=('ISO-8859-1'))
    dataframe['result'] = predictFile_LSTM(dataframe)
    row_10 = dataframe.head(5)
    dataframe.to_csv('output.csv', index=False)
    output_csv = "output.csv"
    return row_10, dataframe.head(5), output_csv

gradio_ui = gr.Interface(
    fn=_data_cleaning,
    title="Simple Interface",
    inputs=[gr.components.File(label="CSV File")],
    outputs=[gr.components.Dataframe(label="Result"),gr.components.Dataframe(label="All Data"),gr.components.File(label="Output CSV")]
)

gradio_ui.launch()