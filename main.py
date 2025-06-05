from fastapi import FastAPI, Form, File, UploadFile
from symspellpy import SymSpell, Verbosity
from PIL import Image
import pytesseract
from difflib import SequenceMatcher
import Levenshtein
import os
import io
import re
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],           # ✅ Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize SymSpell
sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
dictionary_path = os.path.join("corpus/frequency_dictionary_en_82_765.txt")
if not os.path.exists(dictionary_path):
    raise FileNotFoundError("Dictionary file not found.")

medical_dictionary_path = os.path.join("corpus/medical_dictionary.txt")
if not os.path.exists(medical_dictionary_path):
    raise FileNotFoundError("Medical dictionary file not found.")

sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1)
sym_spell.load_dictionary(medical_dictionary_path, term_index=0, count_index=1)

def normalize_text(text):
    return re.sub(r'\s+', ' ', text).strip().lower()


def correct_text(text):
    words = text.split()
    corrected_words = []
    for word in words:
        suggestions = sym_spell.lookup(word, Verbosity.CLOSEST, max_edit_distance=2)
        corrected_words.append(suggestions[0].term if suggestions else word)
    return " ".join(corrected_words)


def calculate_wer(reference, hypothesis):
    ref_words = reference.split()
    hyp_words = hypothesis.split()
    matcher = SequenceMatcher(None, ref_words, hyp_words)
    edit_ops = matcher.get_opcodes()
    total_edits = sum(1 for tag, _, _, _, _ in edit_ops if tag != 'equal')
    return total_edits / len(ref_words) if ref_words else 1.0

# Compute Character Error Rate
def calculate_cer(reference: str, hypothesis: str) -> float:
    return Levenshtein.distance(reference, hypothesis) / len(reference) if len(reference) > 0 else 1.0

@app.post("/spell-correct/")
async def spell_correct(text: str = Form(...)):
    words = text.split()
    corrected = []
    for word in words:
        suggestions = sym_spell.lookup(word, Verbosity.CLOSEST, max_edit_distance=2)
        corrected.append(suggestions[0].term if suggestions else word)
    corrected_text = ' '.join(corrected)
    return {
        "original_text": text,
        "corrected_text": corrected_text
    }

@app.post("/ocr-correct/")
async def ocr_and_correct(file: UploadFile = File(...)):
    # Load and OCR image
    image = Image.open(io.BytesIO(await file.read()))
    raw_text = pytesseract.image_to_string(image)

    # Spelling correction
    corrected_words = []
    for word in raw_text.split():
        suggestions = sym_spell.lookup(word, Verbosity.CLOSEST, max_edit_distance=2)
        corrected_words.append(suggestions[0].term if suggestions else word)

    corrected_text = ' '.join(corrected_words)

    return {
        "original_text": raw_text,
        "corrected_text": corrected_text
    }

@app.post("/word-error-rate/")
async def word_error_rate(reference: str, hypothesis: str):
    """
    :param reference: ground truth text
    :param hypothesis: corrected text (e.g., from SymSpell)
    :return: calculates a rough word error rate (WER).
    """
    ref_words = re.sub(r'\s+', ' ', reference).strip().lower().split()
    hyp_words = re.sub(r'\s+', ' ', hypothesis).strip().lower().split()
    matcher = SequenceMatcher(None, ref_words, hyp_words)
    edit_distance = sum(tag != 'equal' for tag, _, _, _, _ in matcher.get_opcodes())
    return edit_distance / len(ref_words)

@app.post("/character-error-rate/")
async def character_error_rate(reference: str, hypothesis: str):
    """
    :param reference: ground truth text
    :param hypothesis: corrected text (e.g., from SymSpell)
    :return: calculates a rough character error rate (CER).
    """
    ref_words = re.sub(r'\s+', ' ', reference).strip().lower()
    hyp_words = re.sub(r'\s+', ' ', hypothesis).strip().lower()
    return Levenshtein.distance(ref_words, hyp_words) / len(ref_words) if len(ref_words) > 0 else 1.0

@app.post("/wer/")
async def wer(reference: str = Form(...), original: str = Form(...), hypothesis: str = Form(...)):
    """
        :param reference: ground truth text
        :param original: original OCR extracted text
        :param hypothesis: corrected text (e.g., from SymSpell)
        :return: calculates a rough word error rate (WER) before and after correction.
    """
    ocr_text = normalize_text(original)
    reference_text = normalize_text(reference)
    corrected_text = normalize_text(hypothesis)

    original_wer = calculate_wer(reference_text, ocr_text)
    corrected_wer = calculate_wer(reference_text, corrected_text)

    return {
        "WER (Before Correction": f'{original_wer:.2%}',
        "WER (After Correction": f'{corrected_wer:.2%}'
    }

@app.post("/cer/")
async def cer(reference: str = Form(...), original: str = Form(...), hypothesis: str = Form(...)):
    """
        :param reference: ground truth text
        :param original: original OCR extracted text
        :param hypothesis: corrected text (e.g., from SymSpell)
        :return: calculates a rough character error rate (CER) before and after correction.
    """
    ocr_text = normalize_text(original)
    reference_text = normalize_text(reference)
    corrected_text = normalize_text(hypothesis)

    original_cer = calculate_cer(reference_text, ocr_text)
    corrected_cer = calculate_cer(reference_text, corrected_text)

    return {
        "CER (Before Correction": f'{original_cer:.2%}',
        "CER (After Correction": f'{corrected_cer:.2%}'
    }


# from fastapi import FastAPI, Query
# from symspellpy.symspellpy import SymSpell, Verbosity
# from typing import List
# import os
#
# app = FastAPI()
#
# # Initialize SymSpell
# sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
#
# # Load dictionary
# dictionary_path = "corpus/frequency_dictionary_en_82_765.txt"
# if not os.path.exists(dictionary_path):
#     raise FileNotFoundError("Dictionary file not found.")
#
# sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1)
#
# @app.get("/spell-correct")
# def correct_spelling(text: str = Query(..., description="Text to correct")):
#     suggestions = sym_spell.lookup_compound(text, max_edit_distance=2)
#     if suggestions:
#         return {"original": text, "corrected": suggestions[0].term}
#     return {"original": text, "corrected": text}
