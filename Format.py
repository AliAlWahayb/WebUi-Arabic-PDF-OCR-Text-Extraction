import os
import re

from Display_Arabic_In_Termanal import display_arabic

def clean_arabic_text(text):
    """
    Cleans and formats Arabic text.
    """

    # Normalize Arabic text (remove tashkeel, etc.) using regex for efficiency
    text = re.sub(r"[\u064B-\u0652\u06D0]", "", text)  # Remove tashkeel
    text = re.sub(r"[\u0600-\u0605\u0610-\u061A\u06DD\u06DE]", "", text) #Remove misc Arabic chars
    text = text.replace("ـ", "") #Remove Tatweel

    corrections = [
        # Numbers (Arabic to English)
        ("١", "1"), ("٢", "2"), ("٣", "3"), ("٤", "4"), ("٥", "5"),
        ("٦", "6"), ("٧", "7"), ("٨", "8"), ("٩", "9"), ("٠", "0"),

        # Punctuation (Arabic to English)
        ("«", '"'), ("»", '"'), ("))", '"'), ("((", '"'),

        # Common spelling errors
        ("اخطىء", "اخطئ"), ("يبدىء", "يبدأ"), ("يقرىء", "يقرأ"),
        ("نبدىء", "نبدأ"), ("يخطىء", "يخطئ"), ("ينشىء", "ينشئ"),
        ("يرجىء", "يرجئ"), ("بدأىء", "بدأ"), ("قرىء", "قرأ"),
        ("يتدفىء", "يتدفأ"), ("ملجىء", "ملجأ"), ("يفترىء", "يفتري"),
        ("يخشىء", "يخشى"), ("مبدىء", "مبدأ"), ("مأوىء", "مأوى"),
        ("يجزىء", "يجزي"), ("ينهىء", "ينهي"), ("يخلىء", "يخلي"),
        ("يبنىء", "يبني"), ("ترجىء", "ترجئ"), ("ينبئء", "ينبئ"),
        ("يعطىء", "يعطي"), ("يزدرىء", "يزدري"), ("يستدلىء", "يستدل"),
        ("مجلىء", "مجلى"), ("يسعىء", "يسعى"), ("يجلىء", "يجلي"),
        ("تبدىء", "تبدأ"), ("يرضىء", "يرضى"), ("يقتضىء", "يقتضي"),
        ("يطمأنَىء", "يطمئن"), ("يستعلىء", "يستعلي"), ("يقترىء", "يقترى"),

        # Remove extra spaces and newlines and other characters
        # ("\n", " "), ("  ", " "), ("   ", " "), ("•", ""), ("\u200f", ""), ("\u200e", ""),("ـ",""),
    ]

    for wrong, correct in corrections:
        text = text.replace(wrong, correct)

    # text = re.sub(r"\s+", " ", text).strip()  # Remove multiple spaces and trim
    return text

def Format_Text(input_folder, output_folder):
    """
    Processes all .txt files in the input folder, cleans them, and saves
    the cleaned output directly to the output folder.
    """

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith(".txt"):
            input_file_path = os.path.join(input_folder, filename)
            output_file_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.txt") # Correct output path

            try:
                with open(input_file_path, 'r', encoding='utf-8') as infile:
                    text = infile.read()
                cleaned_text = clean_arabic_text(text)
                with open(output_file_path, 'w', encoding='utf-8') as outfile:
                    outfile.write(cleaned_text)
                print(f"Processed and saved: {display_arabic(filename)} to {display_arabic(output_folder)}")

            except FileNotFoundError:
                print(f"Error: Input file not found: {display_arabic(input_file_path)}")
            except Exception as e:
                print(f"Error processing {display_arabic(filename)}: {display_arabic(e)}")
    print("Finished processing all files.")


# Example usage (if you want to run it as a standalone script)
if __name__ == "__main__":
    input_folder = "output\التحول5"  # Replace with your input folder
    output_folder = f"{input_folder}/cleaned" # Replace with your desired output folder

    Format_Text(input_folder, output_folder)