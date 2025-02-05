
# WebUi-Arabic-PDF-OCR-Text-Extraction

This project provides an interactive Web User Interface (WebUI) for extracting Arabic text from PDF documents using Google Document AI, with additional features for text processing and formatting.

## Features

### 1. **Web-Based Interface**:
- Easily upload PDFs and apply OCR processing through a user-friendly Gradio-powered WebUI.
- Multi-tab interface for streamlined operations:
  - **Process PDF**: Extract text from PDFs and apply advanced processing options.
  - **Configuration**: Update project configurations for Google Document AI.
  - **Custom Formatting**: Apply custom formatting options to text files.

### 2. **High-Accuracy OCR**:
- Utilizes Google Document AI for robust and scalable Optical Character Recognition (OCR) for Arabic text.

### 3. **Comprehensive Text Processing**:
- Options for splitting PDFs into pages.
- Text formatting, including removing unwanted characters and improving readability.
- Optional diacritization (tashkeel) for linguistic accuracy.
- Combining processed text files into a single document.

### 4. **Custom Text Formatting**:
- Remove page numbers, watermarks, or extra lines.
- Combine lines into paragraphs for enhanced readability.

### 5. **Configuration Management**:
- Easily configure Project ID, Location, and Processor ID for Google Document AI using the WebUI.

## Screenshots

<div style="display: flex; justify-content: space-around;">
    <img src="https://i.imgur.com/vbG34YW.png"  width="300">
    <img src="https://i.imgur.com/7htc5Hx.png"  width="300">
    <img src="https://i.imgur.com/klTVXZB.png"  width="300">
</div>

## Requirements

Ensure the following dependencies are installed:

- `gradio`
- `google-cloud-documentai`
- `PyPDF2`
- `python-dotenv`
- `arabic_reshaper`
- `python-bidi`
- `tqdm`
- `tkinter`

Install these dependencies using the provided `requirements.txt`:

```bash
pip install -r requirements.txt
```

**Note**: Ensure access to Google Document AI and the proper setup of authentication credentials.

## Usage

### 1. **Set Up Google Document AI Credentials**:
Follow the [Google Cloud documentation](https://cloud.google.com/document-ai/docs/setup) to configure authentication and obtain your credentials.

### 2. **Configuration**:
- Add the following values to the Configuration tab:
  ```
  PROJECT_ID=your_project_id
  LOCATION=your_location
  PROCESSOR_ID=your_processor_id
  ```

### 3. **Run the WebUI**:
Launch the Gradio interface with the following command:

```bash
python main.py
```

### 4. **Process PDFs**:
- Navigate to the **Process PDF** tab to upload a file and apply desired operations such as OCR, formatting, and diacritization.
- Use the **Configuration** tab to update settings for Google Document AI.
- Use the **Custom Formatting** tab to apply advanced formatting to text files.

## Output

- **Formatted Text Files**: Extracted and processed `.txt` files are saved in organized output directories.
- **Logs**: Detailed processing logs are displayed in the WebUI.

## Example

After uploading a PDF in the **Process PDF** tab and selecting the desired options (e.g., OCR, text formatting, etc.), click "Process PDF." The processed files will be saved in the output directory.

## License

This project is licensed under the MIT License.

## Notes

- Ensure Google Cloud credentials are correctly set up with sufficient permissions.
- The tool is designed primarily for Arabic PDFs but can be adapted for other languages with adjustments to Google Document AI settings.

For more details and updates, visit the [GitHub repository](https://github.com/AliAlWahayb/Arabic-PDF-OCR-Text-Extraction).
