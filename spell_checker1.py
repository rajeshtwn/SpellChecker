from symspellpy import SymSpell, Verbosity
from difflib import SequenceMatcher
import os
import re
import Levenshtein

# ----------- 1. SETUP SYMSPELL -----------
sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)

# Load dictionary (make sure this is a large one)
dictionary_path = "corpus/frequency_dictionary_en_82_765.txt"
if not os.path.exists(dictionary_path):
    raise FileNotFoundError("Dictionary file not found.")

medical_dictionary_path = os.path.join("corpus/medical_dictionary.txt")
if not os.path.exists(medical_dictionary_path):
    raise FileNotFoundError("Medical dictionary file not found.")

sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1)
sym_spell.load_dictionary(medical_dictionary_path, term_index=0, count_index=1)


# ----------- 2. UTILITIES -----------
def normalize_text(text):
    return re.sub(r'\s+', ' ', text).strip().lower()


def correct_text(text):
    words = text.split()
    corrected_words = []
    for word in words:
        suggestions = sym_spell.lookup(word, Verbosity.CLOSEST, max_edit_distance=2)
        corrected_words.append(suggestions[0].term if suggestions else word)
    return " ".join(corrected_words)


def word_error_rate(reference, hypothesis):
    ref_words = reference.split()
    hyp_words = hypothesis.split()
    matcher = SequenceMatcher(None, ref_words, hyp_words)
    edit_ops = matcher.get_opcodes()
    total_edits = sum(1 for tag, _, _, _, _ in edit_ops if tag != 'equal')
    return total_edits / len(ref_words) if ref_words else 1.0

# Compute Character Error Rate
def character_error_rate(reference: str, hypothesis: str) -> float:
    return Levenshtein.distance(reference, hypothesis) / len(reference) if len(reference) > 0 else 1.0


# ----------- 3. INPUT EXAMPLES -----------
# Replace these with your real data
ocr_text = """
Patint sufers from hypertensoin and dibetes. He was admited to the hosptal with chets pain.
"""

reference_text = """
Patient suffers from hypertension and diabetes. He was admitted to the hospital with chest pain.
"""

ocr_text = normalize_text(ocr_text)
reference_text = normalize_text(reference_text)
corrected_text = correct_text(ocr_text)


# ----------- 4. RESULTS -----------
original_wer = word_error_rate(reference_text, ocr_text)
corrected_wer = word_error_rate(reference_text, corrected_text)
# Compute CERs
original_cer = character_error_rate(reference_text, ocr_text)
corrected_cer = character_error_rate(reference_text, corrected_text)

print(f"📝 OCR Text:\n{ocr_text}")
print(f"\n✅ Corrected Text:\n{corrected_text}")
print(f"\n🎯 Reference Text:\n{reference_text}")

print(f"\n🔍 Word Error Rate (Before Correction): {original_wer:.2%}")
print(f"🔧 Word Error Rate (After Correction):  {corrected_wer:.2%}")
print(f"\n📉 Character Error Rate (Before Correction): {original_cer:.2%}")
print(f"🔧 Character Error Rate (After Correction):  {corrected_cer:.2%}")
