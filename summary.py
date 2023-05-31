from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

def summarize(input_text,count):
    parser = PlaintextParser.from_string(input_text, Tokenizer("english"))

    summarizer = LsaSummarizer()

    summary_word_count = count

    summary_sentences = []
    word_count = 0
    for sentence in summarizer(parser.document, sentences_count=summary_word_count):
        summary_sentences.append(sentence)
        word_count += len(sentence.words)
        if word_count >= summary_word_count:
            break

    summary = " ".join(str(sentence) for sentence in summary_sentences)

    return summary
