import PyPDF2
import sys

def split_pdf(input_pdf_path, pages_per_file=100):
    """
    Splits a PDF into multiple smaller PDFs, each up to 'pages_per_file' pages.
    """
    try:
        # Open the original PDF
        pdf_reader = PyPDF2.PdfReader(input_pdf_path)
        total_pages = len(pdf_reader.pages)
        
        print(f"Splitting '{input_pdf_path}' which has {total_pages} pages...")

        # Calculate the start page of each chunk
        for start_page in range(0, total_pages, pages_per_file):
            # Create a writer object for each chunk
            pdf_writer = PyPDF2.PdfWriter()
            
            end_page = min(start_page + pages_per_file, total_pages)
            
            # Add pages to the chunk's PDF
            for page_num in range(start_page, end_page):
                pdf_writer.add_page(pdf_reader.pages[page_num])
            
            output_filename = f"jfk_part_{start_page+1}_to_{end_page}.pdf"
            with open(output_filename, 'wb') as out_file:
                pdf_writer.write(out_file)
            
            print(f"Created: {output_filename}")

    except Exception as e:
        print(f"Error splitting PDF: {e}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python pdf_splitter.py <input_pdf_path> [pages_per_file]")
        sys.exit(1)

    input_pdf = sys.argv[1]
    # default 100 pages if user doesn't specify
    pages_chunk_size = int(sys.argv[2]) if len(sys.argv) > 2 else 100

    split_pdf(input_pdf, pages_chunk_size)

if __name__ == "__main__":
    main()
