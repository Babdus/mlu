import sys
import re
import pandas as pd


def subsplit(mask, pattern, n_delimiter_groups=1):
    new_mask = []
    for group, status in mask:
        split = re.split(pattern, group)
        submask = [(subgroup, status and i%(n_delimiter_groups+1)==0) for i, subgroup in enumerate(split)]
        new_mask += submask
    return new_mask


def split_line_into_transliterable_and_not(line):
    split = re.split(r'(<)([a-z\'\s@\[\]:]*)(>\[[a-zA-Z0-9\'_\s]*\])', line)
    mask = [(group, i%2==0) for i, group in enumerate(split)]

    mask = subsplit(mask, pattern=r'(@[a-z\'])([^a-z\']|$)', n_delimiter_groups=2)
    mask = subsplit(mask, pattern=r'(^|\s)(\&.*[a-z\']+)([^a-z\']|$)', n_delimiter_groups=3)
    mask = subsplit(mask, pattern=r'(xxx|www)')
    mask = subsplit(mask, pattern=r'([^a-z\'])')

    mask = [group for group in mask if len(group[0]) > 0]

    new_mask = []
    for group, status in mask:
        if len(new_mask) > 0 and new_mask[-1][1] == status:
            new_mask[-1] = (new_mask[-1][0] + group, status)
        else:
            new_mask.append((group, status))
    
    return new_mask


def transliterate_line(line: str) -> str:
    try:
        key, value = line.split(':\t')
        if key.startswith('*'):
            part_tuples = split_line_into_transliterable_and_not(value)
            
            new_parts = [transliterate(part_tuple[0]) if part_tuple[1] else part_tuple[0] for part_tuple in part_tuples]
            line += f'\n%kat:\t{"".join(new_parts)}'
    except ValueError:
        pass
    return line


def transliterate_chat_file(text: str) -> None:
    
    text = text.replace('\n\t', ' ')
    text_lines = text.split('\n')
    new_lines = [transliterate_line(line) for line in text_lines]
    new_text = '\n'.join(new_lines)
     
    return new_text


def transliterate(utterance):
    rules_path = 'transliteration_rules.csv'
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
    with open(sys.argv[1], 'r') as f:
        text = f.read()
    new_text = transliterate_chat_file(text)
    with open('kat_'+sys.argv[1], 'w') as f:
        f.write(new_text)