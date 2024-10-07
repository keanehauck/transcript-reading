import os
import PyPDF2
import pytesseract
from pdf2image import convert_from_path
from PyPDF2 import PdfReader
from io import StringIO
import re
import pdfkit

#So, I used tesseract for python. Tesseract is
#an OCR (Optical Character Recognition) library that 
#has the ability to perform a character search using a neural network.

#Problems I encountered: Pdfs were not formatted correctly. 
# Pdfs needed to be rotated.
#       Found a functionality in tesseract that estimates the direction a PDF should be rotated
# Basic search function for pdfs seemed inaccurate
#       for example, Some PDFs have text embedded only in the margins. So, we need to use OCR for these.
# PDFs with text embedded had inaccurate text
#       Need to use OCR for these
#Overall, using OCR for every pdf seemed to be generally more accurate
#Cons: takes a lot of time. 



custom_config = r'--oem 1 --psm 4'  #custom config telling tesseract to use a neural network engine and assume that there may be 
                                    #multiple tables per page of the pdf
# Path to Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'




def is_pdf_searchable(pdf_path):
    """
    Checks if the PDF is searchable by trying to extract text.
    """
    reader = PdfReader(pdf_path)
    text = ''
    for page in reader.pages:
        text += page.extract_text() or ''
    return bool(text.strip())  # Returns False if no text was extracted

def rotate_image_if_needed(image):
    """
    Detects if an image (PDF page) is rotated, and rotates it to correct orientation if necessary.
    """
    osd = pytesseract.image_to_osd(image)
    rotation_angle = int(re.search(r'(?<=Rotate: )\d+', osd).group(0))

    # Rotate image based on the detected angle
    if rotation_angle == 90:
        print("Rotation needed.")
        return image.rotate(-90, expand=True)
    elif rotation_angle == 180:
        print("Rotation needed.")
        return image.rotate(-180, expand=True)
    elif rotation_angle == 270:
        print("Rotation needed.")
        return image.rotate(-270, expand=True)
    else:
        print("No rotation needed.")
        return image  # No rotation needed

def ocr_pdf(pdf_path):
    """
    Convert non-searchable PDF to text using OCR.
    Handles page rotation before OCR.
    """
    pages = convert_from_path(pdf_path)
    text = ''
    for page in pages:
        # Correct the orientation of the page before running OCR
        corrected_page = rotate_image_if_needed(page)
        text += pytesseract.image_to_string(corrected_page, config=custom_config)
    return text


def extract_lines(text, search_string):
    lines = text.splitlines()
    matching_lines = [line for line in lines if search_string.lower() in line.lower()]
    return matching_lines

def search_string_in_pdf(pdf_path, search_string):
    """
    Search for a string in a PDF file (searchable or non-searchable),
    and return the full line containing the string.
    """
    if (0): #is_pdf_searchable(pdf_path):         # replace (0) with this text to return to traditional search technique
        reader = PdfReader(pdf_path)
        for page_num, page in enumerate(reader.pages):
            text = page.extract_text() or ''
            # print(f"Extracted text from page {page_num + 1}:")
            print(text[:500])  # Print first 500 characters for debugging. Currently set to 0 for brevity.


            text = page.extract_text() or ''
            line = extract_lines(text, search_string)
            if line:
                print(f"Found '{search_string}' on page {page_num + 1} of {pdf_path}")
                print(f"Full line: {line}\n")
                return True
    else:
        print(f"PDF is not searchable. Running OCR on {pdf_path}...")
        ocr_text = ocr_pdf(pdf_path)
        # print(f"OCR extracted text:")
        print(ocr_text[:500])  # Print first 500 characters for debugging. Currently set to 0 for brevity.

        line = extract_lines(ocr_text, search_string)
        if line:
            print(f"Found '{search_string}' after OCR in {pdf_path}")
            print(f"Full line: {line}\n")
            return True
    return False

def process_pdfs_in_directory(directory_path, search_string):
    """
    Process all PDFs in a directory, checking if each contains the search string.
    """
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".pdf"):
                pdf_path = os.path.join(root, file)
                if search_string_in_pdf(pdf_path, search_string):
                    print(f"Search string found in {pdf_path}")
                    print("")
                    print("")
                else:
                    print(f"Search string not found in {pdf_path}")
                    print("")
                    print("")



# Example usage:
directory_path = 'C:/Users/635at/Documents/_K Files/_Research/First-Year Retention/TranscriptScraping/Transcripts'
search_string = 'ALG'
process_pdfs_in_directory(directory_path, search_string)


#Found 'ALG': 21
#Missed 'ALG': 1

#Full line interpreted correctly: 12
#Missed partial data(such as missing a II in Algebra II or misspelling word): 10
