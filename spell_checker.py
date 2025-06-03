from symspellpy import SymSpell, Verbosity
import os, re

def normalize_text(text):
    return re.sub(r'\s+', ' ', text).strip().lower()

def spell_correct():
    # Initialize SymSpell object
    sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)

    # Load a frequency dictionary
    dictionary_path = os.path.join("corpus/frequency_dictionary_en_82_765.txt")
    sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1)

    # OCR output example
    ocr_text = """Ths is a smple txt extrcted frm OCR.
    Hi there"""

    # Word-level correction
    corrected_words = []
    for word in ocr_text.split():
        print(word)
        suggestions = sym_spell.lookup(word, Verbosity.CLOSEST, max_edit_distance=2)
        corrected_words.append(suggestions[0].term if suggestions else word)

    corrected_text = ' '.join(corrected_words)
    return corrected_text


def word_error_rate(reference: str, hypothesis: str):
    """
    :param reference: ground truth text
    :param hypothesis: corrected text (e.g., from SymSpell)
    :return: calculates a rough word error rate (WER).
    """
    from difflib import SequenceMatcher
    ref_words = reference.split()
    hyp_words = hypothesis.split()
    matcher = SequenceMatcher(None, ref_words, hyp_words)
    edit_distance = sum(tag != 'equal' for tag, _, _, _, _ in matcher.get_opcodes())
    return edit_distance / len(ref_words)

print(spell_correct())
print(word_error_rate('''This is a simple text extracted from OCR.
Hi there''', '''chs is a simple text extracted from OCR. i there'''))
