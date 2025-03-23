import PyPDF2
import openai
import sys
import os

openai.api_key = "YOUR_OPENAI_API_KEY_HERE"  # Replace with your real key

def extract_text_from_pdf(pdf_path):
    """
    Extracts all text from a PDF file and returns it as a string.
    """
    text_content = []
    with open(pdf_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text_content.append(page_text)
    return "\n".join(text_content)

def analyze_text_with_gpt(text, chunk_name="unknown_chunk"):
    """
    Sends the text to GPT and returns the summarized insights.
    """
    # Truncate text if it's too long (just to avoid GPT-4 token limit issues)
    max_chars = 12000  # adjust as needed
    text_chunk = text[:max_chars]

    prompt = (
        f"You are an expert historian analyzing newly released JFK documents. "
        f"Your goal is to identify significant details, names, connections, dates, events, or anomalies. "
        f"Provide a concise bullet-point summary of the content, focusing on unique or surprising findings. "
        f"\n\nText from {chunk_name}:\n\n{text_chunk}"
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # or 'gpt-3.5-turbo' if GPT-4 is not accessible
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1500,
            temperature=0.3,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error interacting with OpenAI API: {e}"

def main():
    if len(sys.argv) < 2:
        print("Usage: python ai_analyzer.py <pdf_file_or_folder>")
        sys.exit(1)

    path_input = sys.argv[1]

    if os.path.isfile(path_input) and path_input.lower().endswith(".pdf"):
        # Single PDF file scenario
        text = extract_text_from_pdf(path_input)
        summary = analyze_text_with_gpt(text, chunk_name=os.path.basename(path_input))
        print(f"\nSummary for {path_input}:\n")
        print(summary)
    elif os.path.isdir(path_input):
        # If it's a folder, analyze each PDF in that folder
        for item in os.listdir(path_input):
            full_path = os.path.join(path_input, item)
            if os.path.isfile(full_path) and item.lower().endswith(".pdf"):
                text = extract_text_from_pdf(full_path)
                summary = analyze_text_with_gpt(text, chunk_name=item)
                print(f"\nSummary for {item}:\n")
                print(summary)
                print("\n" + "="*50 + "\n")
    else:
        print("The provided path is neither a PDF file nor a directory containing PDFs.")
        sys.exit(1)

if __name__ == "__main__":
    main()
