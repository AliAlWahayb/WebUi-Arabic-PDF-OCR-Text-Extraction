import gradio as gr
import os
import asyncio
from dotenv import load_dotenv, set_key
from Combine import combine_text_files
from Format import Format_Text
from Harakat import Harakat
from OCR_google import process_pdfs_async
from PDF_Spliter import split_pdf

# Load .env file
ENV_FILE = ".env"
load_dotenv(ENV_FILE)

# Load configuration values
def get_config_value(key, default_value):
    return os.getenv(key, default_value)

def save_config_value(key, value):
    set_key(ENV_FILE, key, value)

def process_pdf_with_options(pdf_file, split, ocr, format_text, harakat, combine):
    output = ""
    try:
        # Ensure directories exist
        base_dir = os.path.splitext(os.path.basename(pdf_file.name))[0]
        os.makedirs(base_dir, exist_ok=True)
        
        pdf_path = pdf_file.name  # Directly use the temporary file path provided by Gradio

        # Split PDF
        if split:
            split_output = os.path.join(base_dir, "PDFs")
            split_pdf(pdf_path, split_output)
            output += "PDF split completed.\n"

        # OCR
        if ocr:
            ocr_output = os.path.join(base_dir, "OCR")
            asyncio.run(process_pdfs_async(
                project_id=get_config_value("PROJECT_ID", "your_project_id"),
                location=get_config_value("LOCATION", "your_location"),
                processor_id=get_config_value("PROCESSOR_ID", "your_processor_id"),
                input_folder=split_output if split else pdf_path,
                output_folder=ocr_output
            ))
            output += "OCR processing completed.\n"

        # Format Text
        if format_text:
            format_output = os.path.join(base_dir, "Formatted")
            Format_Text(ocr_output if ocr else split_output, format_output)
            output += "Text formatting completed.\n"

        # Harakat
        if harakat:
            harakat_output = os.path.join(base_dir, "Harakat")
            Harakat(format_output if format_text else ocr_output, harakat_output)
            output += "Text diacritization completed.\n"

        # Combine
        if combine:
            combine_output = os.path.join(base_dir, "Combine")
            combine_text_files(harakat_output if harakat else format_output, combine_output)
            output += f"Text combining completed. Combined file is saved in {combine_output}.\n"

    except Exception as e:
        output += f"An error occurred: {str(e)}"
    
    return output

def update_config(project_id, location, processor_id):
    save_config_value("PROJECT_ID", project_id)
    save_config_value("LOCATION", location)
    save_config_value("PROCESSOR_ID", processor_id)
    return f"Configuration updated: Project ID: {project_id}, Location: {location}, Processor ID: {processor_id}"

# Gradio Interface
with gr.Blocks() as demo:
    gr.Markdown("# Arabic PDF Processor")
    
    with gr.Tabs():
        # Tab 1: Process PDF
        with gr.Tab("Process PDF"):
            gr.Markdown("Upload an Arabic PDF and choose which steps to apply.")
            
            with gr.Row():
                pdf_file = gr.File(label="Upload PDF", file_types=[".pdf"])
                with gr.Column():
                    split_checkbox = gr.Checkbox(label="Split PDF", value=True)
                    ocr_checkbox = gr.Checkbox(label="OCR (Extract Text)", value=True)
                    format_checkbox = gr.Checkbox(label="Format Text", value=True)
                    harakat_checkbox = gr.Checkbox(label="Diacritize Text (Harakat)", value=False)
                    combine_checkbox = gr.Checkbox(label="Combine Text Files", value=True)
            
            output_text = gr.Textbox(label="Process Output", lines=10, interactive=False)
            process_button = gr.Button("Process PDF")
            process_button.click(
                fn=process_pdf_with_options,
                inputs=[pdf_file, split_checkbox, ocr_checkbox, format_checkbox, harakat_checkbox, combine_checkbox],
                outputs=output_text
            )

        # Tab 2: Configuration
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

if __name__ == "__main__":
    # Ensure .env file exists
    if not os.path.exists(ENV_FILE):
        with open(ENV_FILE, "w") as f:
            f.write("# Environment Variables\n")
    demo.launch()
