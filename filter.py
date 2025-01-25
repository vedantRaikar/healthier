#this file is to filter out the unnecessary non english words
import re
from spellchecker import SpellChecker
import nltk
nltk.download('words')
from nltk.corpus import words

spell = SpellChecker()
english_words = set(words.words())

#function to normalize and correct text

def filter_english_words(text):
    
    words_list = text.split()
    
    normalized_words = [re.sub(r"[^a-zA-Z]","", word).lower() for word in words_list]
    
    # Correct spelling errors
    corrected_words = []
    for word in normalized_words:
        if word in english_words:
            corrected_words.append(word)  # Keep valid English words
        else:
            corrected_word = spell.correction(word)  # Correct misspelled words
            if corrected_word:
                corrected_words.append(corrected_word)

    return " ".join(corrected_words)
