from flask import Flask, render_template, request
from deep_translator import GoogleTranslator
from langdetect import detect
from nltk.corpus import wordnet
import nltk

# Download WordNet data
nltk.download('wordnet')

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    translated_text = ""
    text_in_english = ""
    synonyms = []
    text = ""

    if request.method == "POST":
        text = request.form.get("text", "").strip()
        target_lang = request.form.get("language", "en")

        if text:
            try:
                # Translate to user-selected target language
                translated_text = GoogleTranslator(source='auto', target=target_lang).translate(text)

                # Translate to English for synonym lookup
                detected_lang=detect(text)
                if detected_lang != 'en':
                    text_in_english = GoogleTranslator(source='auto', target='en').translate(text)
                else:
                    text_in_english = text

                # Fetch English synonyms
                for syn in wordnet.synsets(text_in_english, lang='eng'):
                    for lemma in syn.lemmas():
                        if lemma.name() not in synonyms:
                            synonyms.append(lemma.name())

                if not synonyms:
                    synonyms = ["No synonyms found in English"]

            except Exception as e:
                translated_text = f"Error: {e}"
                synonyms = ["Error fetching synonyms"]

    return render_template(
        "index.html",
        text=text,
        translated_text=translated_text,
        synonyms=synonyms
    )

