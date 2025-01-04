# -*- coding: utf-8 -*-
import os
import multiprocessing
from Display_Arabic_In_Termanal import display_arabic
from farasa.diacratizer import FarasaDiacritizer
import time

def diacritize_text(text):
    """تشكيل نص باستخدام Farasa."""
    diacritizer = FarasaDiacritizer()
    return diacritizer.diacritize(text)

def process_file(input_path, output_path):
    """قراءة ملف، تشكيله، وكتابته إلى ملف آخر."""
    try:
        with open(input_path, 'r', encoding='utf-8') as infile:
            text = infile.read()
            diacritized_text = diacritize_text(text)
        with open(output_path, 'w', encoding='utf-8') as outfile:
            outfile.write(diacritized_text)
        print(display_arabic(f"تم تشكيل الملف: {input_path}"))
    except Exception as e:
        print(display_arabic(f"حدث خطأ أثناء معالجة الملف {input_path}: {e}"))

def Harakat(input_folder, output_folder, num_processes=None, chunksize=1):
    """معالجة جميع الملفات في مجلد باستخدام التوازي مع تحسين استخدام الموارد."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    files = [os.path.join(input_folder, f) for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f))]
    num_files = len(files)

    if num_processes is None:
        num_processes = max(1, multiprocessing.cpu_count() // 4)  # استخدام ربع عدد الأنوية على الأكثر
    
    print(f"Using {num_processes} processes")

    start_time = time.time()
    with multiprocessing.Pool(processes=num_processes) as pool: # Use a context manager
        tasks = [(file, os.path.join(output_folder, os.path.basename(file))) for file in files]
        pool.starmap(process_file, tasks, chunksize=chunksize)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Processing took {elapsed_time:.2f} seconds.")
    print(display_arabic("تم الانتهاء من معالجة المجلد."))

# مثال للاستخدام:
if __name__ == "__main__":
    input_folder = r"output\التحول5\cleaned"  # استبدل بمسار مجلد الإدخال
    output_folder = r"output\التحول5\Harakat"  # استبدل بمسار مجلد الإخراج
    
    Harakat(input_folder, output_folder, chunksize=1)