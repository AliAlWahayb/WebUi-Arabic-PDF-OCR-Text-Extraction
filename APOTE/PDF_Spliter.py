import os
import PyPDF2

from APOTE.Display_Arabic_In_Termanal import display_arabic

def split_pdf(pdf_path, output_folder="output_pages"):
    """يقسم ملف PDF ويسمي الملفات بالصيغة bookNamePageNumber.pdf بدون إضافة نص."""
    try:
        book_name = os.path.splitext(os.path.basename(pdf_path))[0]

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        with open(pdf_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            num_pages = len(pdf_reader.pages)

            for page_num in range(num_pages):
                pdf_writer = PyPDF2.PdfWriter()
                page = pdf_reader.pages[page_num]
                pdf_writer.add_page(page)

                output_filename = os.path.join(output_folder, f"{book_name}-{page_num + 1}.pdf")
                with open(output_filename, 'wb') as output_file:
                    pdf_writer.write(output_file)

        print(display_arabic(f"تم تقسيم الملف '{pdf_path}' إلى {num_pages} صفحة بالصيغة المطلوبة في المجلد '{output_folder}'."))

    except FileNotFoundError:
        print(display_arabic(f"خطأ: الملف '{pdf_path}' غير موجود."))
    except PyPDF2.errors.PdfReadError:
        print(display_arabic(f"خطأ: لا يمكن قراءة الملف '{pdf_path}'. قد يكون تالفًا أو مشفرًا."))
    except Exception as e:
        print(display_arabic(f"حدث خطأ غير متوقع: {e}"))

# مثال للاستخدام:
if __name__ == "__main__":
    pdf_file_path = "PDF/التحول5.pdf"
    output_directory = "التحول5"



    split_pdf(pdf_file_path, output_directory)