import sys
import pandas as pd


def transliterate_file(file_path, rules_path):
    df = pd.read_csv(rules_path, index_col='latin')
    dictionary = df.georgian.to_dict()
    longest_symbol = max(dictionary.keys(), key=len)

    with open(file_path, 'r', encoding='utf-8') as f:
        latin_text = f.read()
    
    georgian_text = ''

    i = 0
    while i < len(latin_text):
        for symbol_length in reversed(range(1,len(longest_symbol)+1)):
            if i + symbol_length > len(latin_text):
                continue

            latin_symbol = latin_text[i:i+symbol_length]
            if symbol_length > 1 and latin_symbol not in dictionary:
                continue
            elif latin_symbol not in dictionary:
                georgian_text += latin_symbol
                i += symbol_length
                continue
            georgian_text += dictionary[latin_symbol]
            i += symbol_length
            break

    with open(f'{".".join(file_path.split(".")[:-1])}_ka.txt', 'w', encoding='utf-8') as f:
        f.write(georgian_text)


if __name__ == '__main__':
    transliterate_file(sys.argv[1], sys.argv[2])