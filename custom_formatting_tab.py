import shutil
import gradio as gr
import os
from tkinter import Tk, filedialog


def on_browse(data_type):
    """
    Open a file or folder dialog based on the selected data type.
    """
    root = Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    if data_type == "Folder":
        filename = filedialog.askdirectory()
        root.destroy()
        return filename if filename else "No folder selected"
    return "Invalid selection"

def combine_lines_to_paragraphs(lines):
    """
    Combine lines into a single paragraph while maintaining proper spacing and punctuation.
    """
    paragraph = ""
    for line in lines:
        stripped_line = line.strip()
        if not stripped_line:  # Skip empty lines
            continue

        if paragraph:  # Add a space before appending the next line
            paragraph += " "

        paragraph += stripped_line

    return paragraph


def custom_format_folder(folder_path, remove_page_numbers, remove_extra_newlines, watermarks):
    """
    Apply formatting to all `.txt` files in the selected folder.
    Save the formatted files in a new folder inside the parent directory.
    """
    if not os.path.exists(folder_path):
        return "The selected folder does not exist."

    # Get folder name and parent directory
    folder_name = os.path.basename(folder_path.rstrip(os.sep))
    parent_dir = os.path.dirname(folder_path)

    # Create the new folder for formatted files
    new_folder_name = f"{folder_name}-Custom Formatting"
    new_folder_path = os.path.join(parent_dir, new_folder_name)

    if os.path.exists(new_folder_path):
        shutil.rmtree(new_folder_path)  # Deletes the existing folder

    os.makedirs(new_folder_path, exist_ok=True)

    formatted_files = []
    watermarks_list = [w.strip().lower() for w in watermarks.split(",")] if watermarks else []

    # Process all `.txt` files in the folder
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".txt"):
                input_file_path = os.path.join(root, file)
                output_file_path = os.path.join(new_folder_path, f"formatted_{file}")

                with open(input_file_path, "r", encoding="utf-8") as infile:
                    content = infile.read()

                # Apply formatting
                lines = content.splitlines()
                formatted_lines = []

                for line in lines:
                    stripped_line = line.strip()

                    # Remove page numbers
                    if remove_page_numbers and stripped_line.isdigit():
                        continue

                    # Remove watermarks
                    if any(watermark in stripped_line.lower() for watermark in watermarks_list):
                        continue


                    formatted_lines.append(line)


                    # Combine lines into paragraphs if remove_extra_newlines is True
                    if remove_extra_newlines:
                        formatted_content = combine_lines_to_paragraphs(formatted_lines)
                    else:
                        formatted_content = "\n".join(formatted_lines)


                with open(output_file_path, "w", encoding="utf-8") as outfile:
                    outfile.write(formatted_content)

                formatted_files.append(output_file_path)

    return (
        f"Formatted {len(formatted_files)} files in the folder. "
        f"New folder created at: {new_folder_path}"
    )


def create_custom_formatting_tab():
    """
    Create a Gradio tab for browsing and applying custom formatting to a folder.
    """
    with gr.Tab("Custom Formatting"):
        gr.Markdown("## Custom Folder Formatting\nUse the **Browse** button to select a folder containing `.txt` files.")

        # Hidden component to store the data type
        data_type = gr.Textbox(value="Folder", visible=False)

        # Folder browsing and selection
        folder_path = gr.Textbox(label="Selected Folder Path", interactive=True)
        browse_button = gr.Button("Browse Folder")
        browse_button.click(fn=on_browse, inputs=[data_type], outputs=folder_path)

        # Formatting options
        remove_page_numbers = gr.Checkbox(label="Remove Page Numbers", value=True)
        remove_extra_newlines = gr.Checkbox(label="Remove Extra Newlines", value=True)
        watermarks = gr.Textbox(
            label="Watermarks (Comma, Separated)",
            placeholder="Enter watermarks to remove, e.g., watermark1, watermark2"
        )

        # Apply formatting
        format_button = gr.Button("Apply Formatting")
        output_message = gr.Textbox(label="Output Message", lines=10, interactive=False)

        format_button.click(
            fn=custom_format_folder,
            inputs=[folder_path, remove_page_numbers, remove_extra_newlines, watermarks],
            outputs=output_message
        )
