import gradio as gr
from dotenv import set_key, load_dotenv
import os

load_dotenv(".env")

ENV_FILE = ".env"

def save_config_value(key, value):
    set_key(ENV_FILE, key, value)

def update_config(project_id, location, processor_id):
    save_config_value("PROJECT_ID", project_id)
    save_config_value("LOCATION", location)
    save_config_value("PROCESSOR_ID", processor_id)
    return f"Configuration updated: Project ID: {project_id}, Location: {location}, Processor ID: {processor_id}"

def get_config_value(key, default_value):
    return os.getenv(key, default_value)

def create_configuration_tab():
    with gr.Tab("Configuration"):
        gr.Markdown("Update the configuration for OCR processing.")
        project_id_input = gr.Textbox(label="Project ID", value=get_config_value("PROJECT_ID", "your_project_id"))
        location_input = gr.Textbox(label="Location", value=get_config_value("LOCATION", "your_location"))
        processor_id_input = gr.Textbox(label="Processor ID", value=get_config_value("PROCESSOR_ID", "your_processor_id"))
        
        config_output = gr.Textbox(label="Configuration Status", interactive=False)
        update_button = gr.Button("Update Configuration")
        update_button.click(
            fn=update_config,
            inputs=[project_id_input, location_input, processor_id_input],
            outputs=config_output
        )
