import asyncio
import concurrent.futures
from typing import Optional
from dotenv import load_dotenv
from google.api_core.client_options import ClientOptions
from google.cloud import documentai  # type: ignore
import os

from APOTE.Display_Arabic_In_Termanal import display_arabic

def process_document_sync(
    project_id: str,
    location: str,
    processor_id: str,
    file_path: str,
    mime_type: str,
    field_mask: Optional[str] = None,
    processor_version_id: Optional[str] = None,
) -> str:
    """Processes a single document using Document AI (synchronous)."""
    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    if processor_version_id:
        name = client.processor_version_path(project_id, location, processor_id, processor_version_id)
    else:
        name = client.processor_path(project_id, location, processor_id)

    try:
        with open(file_path, "rb") as image:
            image_content = image.read()
    except FileNotFoundError:
        print(f"Error: File not found: {display_arabic(file_path)}")
        return ""
    except Exception as e:
        print(f"Error reading file {display_arabic(file_path)}: {e}")
        return ""

    raw_document = documentai.RawDocument(content=image_content, mime_type=mime_type)
    process_options = documentai.ProcessOptions()

    request = documentai.ProcessRequest(
        name=name,
        raw_document=raw_document,
        field_mask=field_mask,
        process_options=process_options,
    )

    try:
        result = client.process_document(request=request)
        document = result.document
        return document.text
    except Exception as e:
        print(f"Error processing with Document AI: {display_arabic(e)}")
        return ""

async def process_pdf_async(
    project_id: str,
    location: str,
    processor_id: str,
    input_file_path: str,
    output_folder: str,
    mime_type: str,
    field_mask: Optional[str],
    processor_version_id: Optional[str],
    executor: concurrent.futures.ThreadPoolExecutor,
    semaphore: asyncio.Semaphore, # Add semaphore here
) -> None:
    """Processes a single PDF asynchronously with semaphore."""
    book_name = os.path.splitext(os.path.basename(input_file_path))[0]
    output_file_path = os.path.join(output_folder, f"{book_name}.txt")

    async with semaphore: # Acquire semaphore
        try:
            loop = asyncio.get_running_loop()
            text = await loop.run_in_executor(
                executor,
                process_document_sync,
                project_id,
                location,
                processor_id,
                input_file_path,
                mime_type,
                field_mask,
                processor_version_id,
            )

            if text:
                with open(output_file_path, "w", encoding="utf-8") as file:
                    file.write(text)
                print(f"Processed and saved text for: {display_arabic(os.path.basename(input_file_path))}")
            else:
                print(f"No text extracted or error occurred for {display_arabic(os.path.basename(input_file_path))}")
        except Exception as e:
            print(f"A general error occurred processing {display_arabic(os.path.basename(input_file_path))}: {e}")


async def process_pdfs_async(
    project_id: str,
    location: str,
    processor_id: str,
    input_folder: str,
    output_folder: str,
    mime_type: str = "application/pdf",
    field_mask: Optional[str] = None,
    processor_version_id: Optional[str] = None,
    concurrency_limit: int = 10,  # Add concurrency limit
) -> None:
    """Processes PDFs in a folder asynchronously with concurrency limit."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    semaphore = asyncio.Semaphore(concurrency_limit) # Create semaphore
    with concurrent.futures.ThreadPoolExecutor() as executor:
        tasks = []
        for filename in os.listdir(input_folder):
            if filename.lower().endswith((".pdf", ".jpg", ".jpeg", ".png", ".tif", ".tiff")):
                input_file_path = os.path.join(input_folder, filename)
                task = asyncio.create_task(process_pdf_async(
                    project_id, location, processor_id, input_file_path,
                    output_folder, mime_type, field_mask, processor_version_id, executor, semaphore # Pass semaphore
                ))
                tasks.append(task)
        await asyncio.gather(*tasks)
    print("Finished processing all files.")

# Example usage:
if __name__ == "__main__":
    load_dotenv()
    project_id = os.getenv('PROJECT_ID')
    location = os.getenv('LOCATION')
    processor_id = os.getenv('PROCESSOR_ID')
    input_folder = "التحول5"
    output_folder = f"output/{input_folder}"
    concurrency_limit = 5 # Set your desired concurrency limit

    
    asyncio.run(process_pdfs_async(project_id, location, processor_id, input_folder, output_folder, concurrency_limit=concurrency_limit)) # Pass the concurrency limit