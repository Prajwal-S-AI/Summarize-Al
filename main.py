pip install spacy nltk beautifulsoup4 PyPDF2

import sys
import math
import bs4 as bs
import urllib.request
import re
import PyPDF2
import nltk
from nltk.stem import WordNetLemmatizer
import spacy

nltk.download('wordnet')

nlp = spacy.load('en_core_web_sm')
lemmatizer = WordNetLemmatizer()

def file_text(filepath):
    with open(filepath) as f:
        text = f.read().replace("\n", '')
        return text

def pdfReader(pdf_path):

    with open(pdf_path, 'rb') as pdfFileObject:
        pdfReader = PyPDF2.PdfFileReader(pdfFileObject)
        count = pdfReader.numPages
        print("\nTotal Pages in pdf = ", count)

        c = 'Y'
        start_page = 0
        end_page = count-1
        c = input("Do you want to read entire pdf ?[Y]/N  :  ")
        if c == 'N' or c == 'n' :
            start_page  = int(input("Enter start page number (Indexing start from 0) :  "))
            end_page = int(input(f"Enter end page number (Less than {count}) : "))

            if start_page <0 or start_page >= count:
                print("\nInvalid Start page given")
                sys.exit()

            if end_page <0 or end_page >= count:
                print("\nInvalid End page given")
                sys.exit()

        for i in range(start_page,end_page+1):
            page = pdfReader.getPage(i)

        return page.extractText()

def wiki_text(url):
    scrap_data = urllib.request.urlopen(url)
    article = scrap_data.read()
    parsed_article = bs.BeautifulSoup(article,'lxml')

    paragraphs = parsed_article.find_all('p')
    article_text = ""

    for p in paragraphs:
        article_text += p.text

    article_text = re.sub(r'\[[0-9]*\]', '', article_text)
    return article_text

input_text_type = int(input("Select one way of inputting your text  \
: \n1. Type your Text(or Copy-Paste)\n2. Load from .txt file\n3. Load from .pdf file\n4. From Wikipedia Page URL\n\n"))

if input_text_type == 1:
    text = input(u"Enter your text : \n\n")

elif input_text_type == 2:
    txt_path = input("Enter file path :  ")
    text = file_text(txt_path)


elif input_text_type == 3:
    file_path = input("Enter file path :  ")
    text = pdfReader(file_path)

elif input_text_type == 4:
    wiki_url = input("Enter Wikipedia URL to load Article : ")
    text = wiki_text(wiki_url)

else:
    print("Sorry! Wrong Input, Try Again.")

def frequency_matrix(sentences):
    freq_matrix = {}
    stopWords = nlp.Defaults.stop_words

    for sent in sentences:
        freq_table = {}


        words = [word.text.lower() for word in sent  if word.text.isalnum()]

        for word in words:
            word = lemmatizer.lemmatize(word)
            if word not in stopWords:
                if word in freq_table:
                    freq_table[word] += 1
                else:
                    freq_table[word] = 1

        freq_matrix[sent[:15]] = freq_table

    return freq_matrix

def tf_matrix(freq_matrix):
    tf_matrix = {}

    for sent, freq_table in freq_matrix.items():
        tf_table = {}

        total_words_in_sentence = len(freq_table)
        for word, count in freq_table.items():
            tf_table[word] = count / total_words_in_sentence

        tf_matrix[sent] = tf_table

    return tf_matrix

def sentences_per_words(freq_matrix):
    sent_per_words = {}

    for sent, f_table in freq_matrix.items():
        for word, count in f_table.items():
            if word in sent_per_words:
                sent_per_words[word] += 1
            else:
                sent_per_words[word] = 1

    return sent_per_words

def idf_matrix(freq_matrix, sent_per_words, total_sentences):
    idf_matrix = {}

    for sent, f_table in freq_matrix.items():
        idf_table = {}

        for word in f_table.keys():
            idf_table[word] = math.log10(total_sentences / float(sent_per_words[word]))

        idf_matrix[sent] = idf_table

    return idf_matrix

def tf_idf_matrix(tf_matrix, idf_matrix):
    tf_idf_matrix = {}

    for (sent1, f_table1), (sent2, f_table2) in zip(tf_matrix.items(), idf_matrix.items()):

        tf_idf_table = {}


        for (word1, tf_value), (word2, idf_value) in zip(f_table1.items(),
                                                    f_table2.items()):
            tf_idf_table[word1] = float(tf_value * idf_value)

        tf_idf_matrix[sent1] = tf_idf_table

    return tf_idf_matrix

def score_sentences(tf_idf_matrix):

    sentenceScore = {}

    for sent, f_table in tf_idf_matrix.items():
        total_tfidf_score_per_sentence = 0

        total_words_in_sentence = len(f_table)
        for word, tf_idf_score in f_table.items():
            total_tfidf_score_per_sentence += tf_idf_score

        if total_words_in_sentence != 0:
            sentenceScore[sent] = total_tfidf_score_per_sentence / total_words_in_sentence

    return sentenceScore

def average_score(sentence_score):

    total_score = 0
    for sent in sentence_score:
        total_score += sentence_score[sent]

    average_sent_score = (total_score / len(sentence_score))

    return average_sent_score

def create_summary(sentences, sentence_score, threshold):
    summary = ''

    for sentence in sentences:
        if sentence[:15] in sentence_score and sentence_score[sentence[:15]] >= (threshold):
            summary += " " + sentence.text

    return summary

original_words = text.split()
original_words = [w for w in original_words if w.isalnum()]
num_words_in_original_text = len(original_words)

text = nlp(text)


sentences = list(text.sents)
total_sentences = len(sentences)


freq_matrix = frequency_matrix(sentences)


tf_matrix = tf_matrix(freq_matrix)


num_sent_per_words = sentences_per_words(freq_matrix)


idf_matrix = idf_matrix(freq_matrix, num_sent_per_words, total_sentences)


tf_idf_matrix = tf_idf_matrix(tf_matrix, idf_matrix)



sentence_scores = score_sentences(tf_idf_matrix)


threshold = average_score(sentence_scores)


summary = create_summary(sentences, sentence_scores, 1.3 * threshold)
print("\n\n")
print("*"*20,"Summary","*"*20)
print("\n")
print(summary)
print("\n\n")
print("Total words in original article = ", num_words_in_original_text)
print("Total words in summarized article = ", len(summary.split()))
