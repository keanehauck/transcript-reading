import pdfplumber
import os

# Function to extract tables from PDF using pdfplumber
def extract_tables_from_pdf(pdf_path, search_string):
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            tables = page.extract_tables()
            if tables:
                for table in tables:
                    for row in table:
                        # Convert row to a single string and search for the target string
                        row_str = ' '.join([str(cell) for cell in row if cell])  # Skip empty cells
                        if search_string.lower() in row_str.lower():
                            print(f"String found in row: {row}")
                            return row  # Exit when string is found in the row
            else:
                print(f"No tables found on page {page_num + 1} of {pdf_path}")

# Function to iterate through all PDFs in a directory
def search_string_in_pdfs(directory_path, search_string):
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.pdf'):
                pdf_path = os.path.join(root, file)
                print(f"Searching in: {pdf_path}")
                result = extract_tables_from_pdf(pdf_path, search_string)
                if result:
                    print(f"Search string found in: {pdf_path}")
                    print(f"Row where string is found: {result}")
                else:
                    print(f"String not found in: {pdf_path}")

# Example usage
directory_path = 'C:/Users/635at/Documents/_K Files/_Research/First-Year Retention/TranscriptScraping/Transcripts'
search_string = 'ALG'
search_string_in_pdfs(directory_path, search_string)
