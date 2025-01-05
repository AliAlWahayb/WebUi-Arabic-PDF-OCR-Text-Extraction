import gradio as gr
import asyncio
import os
from APOTE.Combine import combine_text_files
from APOTE.Format import Format_Text
from APOTE.Harakat import Harakat
from APOTE.OCR_google import process_pdfs_async
from APOTE.PDF_Spliter import split_pdf
from dotenv import load_dotenv

load_dotenv(".env")


def get_config_value(key, default_value):
    return os.getenv(key, default_value)


def process_pdf_with_options(pdf_file, split, ocr, format_text, harakat, combine):
    output = ""
    try:
        base_dir = os.path.splitext(os.path.basename(pdf_file.name))[0]
        os.makedirs(base_dir, exist_ok=True)
        pdf_path = pdf_file.name

        if split:
            split_output = os.path.join(base_dir, "PDFs")
            split_pdf(pdf_path, split_output)
            output += "PDF split completed.\n"

        if ocr:
            ocr_output = os.path.join(base_dir, "OCR")
            asyncio.run(process_pdfs_async(
                project_id=get_config_value("PROJECT_ID", "your_project_id"),
                location=get_config_value("LOCATION", "your_location"),
                processor_id=get_config_value(
                    "PROCESSOR_ID", "your_processor_id"),
                input_folder=split_output if split else pdf_path,
                output_folder=ocr_output
            ))
            output += "OCR processing completed.\n"

        if format_text:
            format_output = os.path.join(base_dir, "Formatted")
            Format_Text(ocr_output if ocr else split_output, format_output)
            output += "Text formatting completed.\n"

        if harakat:
            harakat_output = os.path.join(base_dir, "Harakat")
            Harakat(format_output if format_text else ocr_output, harakat_output)
            output += "Text diacritization completed.\n"

        if combine:
            combine_output = os.path.join(base_dir, "Combine")
            combine_text_files(
                harakat_output if harakat else format_output, combine_output)
            output += f"Text combining completed. Combined file is saved in {combine_output}.\n"

    except Exception as e:
        output += f"An error occurred: {str(e)}"

    return output


def create_process_pdf_tab():
    with gr.Tab("Process PDF"):
        gr.Markdown("Upload an Arabic PDF and choose which steps to apply.")
        pdf_file = gr.File(label="Upload PDF", file_types=[".pdf"])
        split_checkbox = gr.Checkbox(label="Split PDF", value=True)
        ocr_checkbox = gr.Checkbox(label="OCR (Extract Text)", value=True)
        format_checkbox = gr.Checkbox(label="Format Text", value=True)
        harakat_checkbox = gr.Checkbox(
            label="Diacritize Text (Harakat)", value=False)
        combine_checkbox = gr.Checkbox(label="Combine Text Files", value=True)

        output_text = gr.Textbox(
            label="Process Output", lines=10, interactive=False)
        process_button = gr.Button("Process PDF")
        process_button.click(
            fn=process_pdf_with_options,
            inputs=[pdf_file, split_checkbox, ocr_checkbox,
                    format_checkbox, harakat_checkbox, combine_checkbox],
            outputs=output_text
        )
