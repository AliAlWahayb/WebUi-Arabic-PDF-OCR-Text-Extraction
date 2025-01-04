# Arabic-PDF-OCR-Text-Extraction

This project provides a Python-based solution to extract Arabic text from PDF documents using Google Document AI. It processes PDFs to generate formatted `.txt` files containing the extracted text.

## Features

- **High-Accuracy OCR**: Employs Google Cloud Document AI for robust and scalable Optical Character Recognition of Arabic text in PDFs.
- **Comprehensive Text Processing**: Includes functions for:
- Normalizing Arabic text (removing tashkeel, etc.).
- Correcting common spelling errors.
- Removing unwanted characters and whitespace.
- Improving overall text readability.
- **Optional Diacritization**: Integrates Farasa for adding diacritics (tashkeel) to the extracted text, enhancing linguistic accuracy.
- **Asynchronous Processing**: Utilizes asyncio and concurrent.futures to process multiple files concurrently, significantly improving performance for large datasets.

## Requirements

Ensure the following dependencies are installed:

- `google-cloud-documentai`
- `PyPDF2`
- `python-dotenv`
- `arabic_reshaper`
- `python-bidi`
- `tqdm`

Install these dependencies using the provided `requirements.txt` file:

```bash
pip install -r requirements.txt
```

*Note*: Ensure that you have access to Google Document AI and have set up the necessary authentication credentials.

## Usage

1. **Set Up Google Document AI Credentials**: Follow the [Google Cloud documentation](https://cloud.google.com/document-ai/docs/setup) to set up authentication and obtain your credentials.

2. **Create .env File**:
   - Create .env file and add 
   - project_id=
   - location=
   - processor_id=

3. **Configure the Scripts**:
   - Specify the path to your input PDF file in `main.py`.

4. **Run the Scripts**:
   - Use `main.py` to extract text from PDF files. The extracted and formatted text will be saved as `.txt` files in the output directory.



## Output

- **Text Files**: `.txt` files containing the extracted Arabic text, formatted for readability and ease of use.

## Example

Here's how to set the input PDF path in the scripts:

```python
# Set the path to the input PDF file in main.py
pdf_file_path = '/path/to/your/input.pdf'

# Run main.py 
```

After running the scripts, the extracted and processed text files will be saved in the output directory with the same name as the pdf file.

## License
- This project is licensed under the MIT License.

## Notes

- Ensure that your Google Cloud credentials are correctly set up and that you have the necessary permissions to use Document AI.
- The script is designed to handle PDFs containing Arabic text. For other languages, adjust the Document AI settings accordingly.

For more details and updates, visit the [GitHub repository](https://github.com/AliAlWahayb/Arabic-PDF-OCR-Text-Extraction).
