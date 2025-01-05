# -*- coding: utf-8 -*-
import asyncio
import os
import shutil
from dotenv import load_dotenv
from Combine import combine_text_files
from APOTE.Display_Arabic_In_Termanal import display_arabic
from Format import Format_Text
from Harakat import Harakat
from OCR_google import process_pdfs_async
from PDF_Spliter import split_pdf


if __name__ == "__main__":
    pdf_file_path = "PDF\التحول5.pdf" # replace with your PDF file path
    
    filename = os.path.splitext(os.path.basename(pdf_file_path))[0] # Get the filename without extension

    output_directory = filename 

    print("book name:",display_arabic(filename))

    PDFs_Path = f"{output_directory}/PDFs"
    split_pdf(pdf_file_path, PDFs_Path) # Split the PDF

    # Load environment variables from .env
    load_dotenv()
    # Access variables
    project_id = os.getenv('PROJECT_ID') # replace with your project id
    location = os.getenv('LOCATION') # replace with your location
    processor_id = os.getenv('PROCESSOR_ID') # replace with your processor id

    OCR_Path = f"{output_directory}/OCR"
    # Process PDFs
    asyncio.run(process_pdfs_async(project_id, location, processor_id, PDFs_Path, OCR_Path))

    Format_Path = f"{output_directory}/Formated"
    # Format Text
    Format_Text(OCR_Path, Format_Path)

    Harakat_Path = f"{output_directory}/Harakat"
    # Harakat
    Harakat(Format_Path, Harakat_Path)

    combine_Path = f"{output_directory}/Combine"
    # Combine
    combine_text_files(Harakat_Path, combine_Path, output_filename=f"{filename}.txt")#

    # Delete the PDFs folder
    shutil.rmtree(PDFs_Path)

    print(display_arabic("تم الانتهاء من التنفيذ"))