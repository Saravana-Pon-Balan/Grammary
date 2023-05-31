from textblob import TextBlob

def spellcheck(text):
    blob = TextBlob(text)

    misspelled = []
    for word in blob.words:
        corrected_word = word.correct()
        if word != corrected_word:
            misspelled.append(word)

    misspelled_count = len(misspelled)

    corrected = blob.correct()
    corrected_text = ' '.join(corrected)

    print(corrected)
    print(misspelled)
    return corrected,misspelled_count,misspelled

