import sys
import deepl
import argparse
import os
from pathvalidate.argparse import validate_filepath_arg

TARGET_LANGUAGES = {
    "AR": "Arabic",
    "BG": "Bulgarian",
    "CS": "Czech",
    "DA": "Danish",
    "DE": "German",
    "EL": "Greek",
    "EN-GB": "English (British)",
    "EN-US": "English (American)",
    "ES": "Spanish",
    "ET": "Estonian",
    "FI": "Finnish",
    "FR": "French",
    "HU": "Hungarian",
    "ID": "Indonesian",
    "IT": "Italian",
    "JA": "Japanese",
    "KO": "Korean",
    "LT": "Lithuanian",
    "LV": "Latvian",
    "NB": "Norwegian Bokmål",
    "NL": "Dutch",
    "PL": "Polish",
    "PT": "Portuguese (unspecified variant for backward compatibility; please select PT-BR or PT-PT instead)",
    "PT-BR": "Portuguese (Brazilian)",
    "PT-PT": "Portuguese (all Portuguese varieties excluding Brazilian Portuguese)",
    "RO": "Romanian",
    "RU": "Russian",
    "SK": "Slovak",
    "SL": "Slovenian",
    "SV": "Swedish",
    "TR": "Turkish",
    "UK": "Ukrainian",
    "ZH": "Chinese (simplified)"
}

parser = argparse.ArgumentParser(prog='python deeplcmd.py', description=r'CLI app that can translate texts or files '
                                                                        'to different languages using deepl API '
                                                                        'https://www.deepl.com/en/pro-api')

group1 = parser.add_mutually_exclusive_group(required=True)
group1.add_argument('-t', '--text', type=str, help='Text to be translated')
group1.add_argument('-f', '--file', type=validate_filepath_arg, nargs=2, help='input file, output file')
parser.add_argument('-tl', '--targetlanguage', required=True, help='language of translation (language code. i.e. RU '
                                                                   'for Russian)')
group2 = parser.add_mutually_exclusive_group(required=True)
group2.add_argument('-kf', '--keyfile', type=validate_filepath_arg, help='file containing deepl API key')
group2.add_argument('-k', '--key', type=str, help='your deepl API key')
args = parser.parse_args()

if args.targetlanguage.upper() not in TARGET_LANGUAGES:
    print(f'Target language {args.targetlanguage} is not recognised.')
    print('Please, use one of the following:', TARGET_LANGUAGES)
    sys.exit()

if args.key:
    translator = deepl.Translator(args.key)
elif args.keyfile:
    if os.path.exists(args.keyfile):
        with open(args.keyfile, 'r') as file:
            key = file.read()
            translator = deepl.Translator(key)
    else:
        print(f'Key file {args.keyfile} does not exists')
        sys.exit()

if args.text and args.targetlanguage:
    try:
        print(translator.translate_text(text=args.text, target_lang=args.targetlanguage))
    except deepl.exceptions.AuthorizationException:
        print('Authentication Failure. Check API key')
        sys.exit()

if args.file and args.targetlanguage:
    input_path, output_path = tuple(args.file)
    if os.path.exists(input_path):
        if os.path.exists(output_path):
            cmd = input(f'File {output_path} already exists. Rewrite? [y/n] -> ').upper()
            if not cmd.startswith('Y'):
                sys.exit()
        try:
            translator.translate_document_from_filepath(
                input_path,
                output_path,
                target_lang=args.targetlanguage.upper()
            )
        except deepl.exceptions.AuthorizationException:
            print('Authentication Failure. Check API key')
            sys.exit()

        print(f'Output has been saved in {output_path}')

    else:
        print(f'File {input_path} does not exist')
