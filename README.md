# Summarize-Al
Text Summarization Using NLP
This project is a Text Summarization Tool that extracts key information from text documents, PDFs, and Wikipedia articles using Natural Language Processing (NLP) techniques.

Features
✅ Supports text input from:

Direct user input
.txt file
.pdf file
Wikipedia article URL
✅ Implements TF-IDF (Term Frequency - Inverse Document Frequency) for text ranking.
✅ Uses SpaCy and NLTK for text processing, tokenization, and lemmatization.
✅ Extracts key sentences based on computed scores.
✅ Outputs a summarized version of the input text.

Technologies Used
Python
NLTK
SpaCy
BeautifulSoup4 (for web scraping)
PyPDF2 (for PDF parsing)
How to Run the Project
Install dependencies:
bash
Copy
Edit
pip install spacy nltk beautifulsoup4 PyPDF2
Download necessary NLP models:
bash
Copy
Edit
python -m spacy download en_core_web_sm
nltk.download('wordnet')
Run the Python script:
bash
Copy
Edit
python summarizer.py
Usage
When you run the script, you can select from different input methods and get a summarized version of the text.
