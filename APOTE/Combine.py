# -*- coding: utf-8 -*-
import os

from APOTE.Display_Arabic_In_Termanal import display_arabic

def combine_text_files(input_folder, output_folder, output_filename="Combined_text.txt"):
    """
    Combines all .txt files in the input folder into a single text file.

    Args:
        input_folder: Path to the folder containing the .txt files.
        output_folder: Path to the folder where the combined file will be saved.
        output_filename: Name of the combined output file (default: "combined_text.txt").
    """

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    output_path = os.path.join(output_folder, output_filename) # Use output_filename here

    try:
        with open(output_path, 'w', encoding='utf-8') as outfile:
            for filename in os.listdir(input_folder):
                if filename.endswith(".txt"):
                    input_file_path = os.path.join(input_folder, filename)
                    try:
                        with open(input_file_path, 'r', encoding='utf-8') as infile:
                            outfile.write(infile.read())
                            outfile.write("\n")  # Add a newline between files
                            outfile.write("\n")  # Add a newline between files
                        print(f"Added {display_arabic(filename)} to combined file.")
                    except UnicodeDecodeError:
                        print(f"UnicodeDecodeError: Skipping file {display_arabic(filename)}. Try a different encoding if needed.")
                    except Exception as inner_e:
                        print(f"Error reading file {display_arabic(filename)}: {display_arabic(inner_e)}")
        print(f"Combined text saved to: {display_arabic(output_path)}")

    except Exception as e:
        print(f"An error occurred during combining: {display_arabic(e)}")


# Example usage (if running as a standalone script):
if __name__ == "__main__":
    input_folder = "output\التحول5\Harakat"  # Replace with your input folder path
    output_folder = "output\التحول5\combine" # Replace with your output folder path


    combine_text_files(input_folder, output_folder, output_filename="التحول5.txt")

