import sys
import pandas as pd
from typing import List, Union


def transliterate_word(filtered_word: List[List[Union[str, bool]]]) -> str:
    new_word = ''
    for part, is_transliterable in filtered_word:
        new_word += transliterate(part) if is_transliterable else part
    return new_word


def filter_word(word: str) -> List[List[Union[str, bool]]]:
    is_transliterable = True
    i = 0
    parts = [['', True]]
    while is_transliterable and i < len(word):
        if word[i] in {'@', '&'}:
            is_transliterable = False
            parts.append([word[i:], False])
        else:
            parts[0][0] += word[i]
        i += 1
    return parts


def transliterate_line(line: str) -> str:
    try:
        key, value = line.split(':\t')
        if key.startswith('*'):
            words = value.split(' ')
            new_words = [transliterate_word(filter_word(word)) for word in words]
            value = ' '.join(new_words)
        new_line = f'{key}:\t{value}'
    except ValueError:
        new_line = line
    return new_line


def transliterate_chat_file(file_path: str) -> None:
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    text = text.replace('\n\t', ' ')
    text_lines = text.split('\n')
    new_lines = [transliterate_line(line) for line in text_lines]
    new_text = '\n'.join(new_lines)
     
    with open('test.cha', 'w', encoding='utf-8') as f:
        f.write(new_text)


def transliterate(utterance):
    rules_path = sys.argv[2]
    df = pd.read_csv(rules_path, index_col='latin')
    dictionary = df.georgian.to_dict()
    longest_symbol = max(dictionary.keys(), key=len)
    
    ka_text = ''

    i = 0
    while i < len(utterance):
        for symbol_length in reversed(range(1,len(longest_symbol)+1)):
            if i + symbol_length > len(utterance):
                continue

            latin_symbol = utterance[i:i+symbol_length]
            if symbol_length > 1 and latin_symbol not in dictionary:
                continue
            elif latin_symbol not in dictionary:
                ka_text += latin_symbol
                i += symbol_length
                continue
            ka_text += dictionary[latin_symbol]
            i += symbol_length
            break

    return ka_text


if __name__ == '__main__':
    transliterate_chat_file(sys.argv[1])