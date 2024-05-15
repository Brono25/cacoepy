import textgrid
import re
import os
import glob
import json 
from cacoepy.core.utils import pretty_sequences

substition_pattern = re.compile(r"^\s*[a-zA-Z]+\s*,\s*[a-zA-Z]+\s*,\s*s\s*$")
addition_pattern = re.compile(r"^\s*[a-zA-Z]+\s*,\s*[a-zA-Z]+\s*,\s*a\s*$")
deletion_pattern = re.compile(r"^\s*[a-zA-Z]+\s*,\s*[a-zA-Z]+\s*,\s*d\s*$")
correct_pattern = re.compile(r"^[A-Za-z]+$")


def save_dict_to_json(data, filename):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)


def load_tiers_from_textgrid(file_path):
    try:
        tg = textgrid.TextGrid.fromFile(file_path)
        words_tier = tg.getFirst("words")
        phones_tier = tg.getFirst("phones")
        return words_tier, phones_tier
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None

def process_file(file_path):

    words_tier, phones_tier = load_tiers_from_textgrid(file_path)

    target = []
    perceived = []
    for interval in phones_tier:
        phone = re.sub(r"\d+", "", interval.mark).lower()
        phone = phone.replace("*", "").replace(" ", "")
        if not phone:
            continue
        if phone == "sil" or phone == "sp":
            pass
            target.append("sil")
            perceived.append("-")

        elif correct_pattern.match(phone):
            target.append(phone)
            perceived.append(phone)

        elif substition_pattern.match(phone):
            cpl, ppl, _ = phone.split(",")
            target.append(cpl)
            if ppl == "err":
                perceived.append(cpl)
            else:
                perceived.append(ppl)

        elif addition_pattern.match(phone):
            cpl, ppl, _ = phone.split(",")
            target.append("-")
            perceived.append(ppl)

        else:
            cpl, ppl, c = phone.split(",")

            assert c == "d"
            target.append(cpl)
            perceived.append("-")
    words = []
    for interval in words_tier:
        word = interval.mark 
        if word:
            words.append(word)
    return (" ").join(words), (" ").join(target), (" ").join(perceived)


def process_textgrid_files(directory):

    file_pattern = os.path.join(directory, "*.TextGrid")
    textgrid_files = glob.glob(file_pattern)
    data = {}
    for file_path in textgrid_files:
        filename = os.path.basename(file_path)

        words, target_phonemes, perceived_phonemes = process_file(file_path)
        data[filename] = {
            "words": words,
            "target_phonemes": target_phonemes,
            "perceived_phonemes": perceived_phonemes
        }
        print(file_path)

        pretty_sequences(target_phonemes.split(" "), perceived_phonemes.split(" "))

    #save_dict_to_json(data, "data/L2Arctic_annotations.json")


directory = "/Users/brono/Downloads/L2Arctic/ABA/annotation"
process_textgrid_files(directory)
