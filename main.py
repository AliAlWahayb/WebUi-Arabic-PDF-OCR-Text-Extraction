import gradio as gr
from process_pdf_tab import create_process_pdf_tab
from configuration_tab import create_configuration_tab
from custom_formatting_tab import create_custom_formatting_tab

# Gradio Interface
with gr.Blocks() as demo:
    gr.Markdown("# Arabic PDF Processor")
    
    with gr.Tabs():
        create_process_pdf_tab()
        create_configuration_tab()
        create_custom_formatting_tab()

if __name__ == "__main__":
    demo.launch()
