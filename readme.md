# deeplcmd

A command line application that uses the [DeepL Translator API](https://www.deepl.com/en/pro-api) to translate text or documents into one of the supported languages. The DeepL API has a free plan that allows for up to 500,000 characters to be translated.

## Usage

You can use this application to translate a string of text directly or to translate a document.

The syntax for translating text is as follows:

## Installation
```commandline
git clone https://github.com/ilya-smut/deeplcmd
cd deeplcmd
pip install -e .
```
Please, note. You may want to create a virtual environment for the installation of the script
```commandline
python -m venv .venv
.venv/bin/activate
```
read more about virtual environments here https://docs.python.org/3/library/venv.html

```commandline
deeplcmd -t "text to be translated" -tl "target language code" -k "your deepl API key"

```

```commandline
deeplcmd -t "text to be translated" -tl "target language code" -kf "file containing deepl API key"
```

The syntax for translating a document is as follows:

```commandline
deeplcmd -f "input file" "output file" -tl "target language" -kf "file containing deepl API key"

```

### Options

- `t`, `-text`: The text to be translated
- `-file`: The input file and output file for the document to be translated
- `tl`, `-targetlanguage`: The language of translation. This is required.
- `-keyfile`, `kf`: The file containing the DeepL API key
- `k`, `-key`: Your DeepL API key

### Supported Languages

The supported languages are as follows:

- Arabic
- Bulgarian
- Czech
- Danish
- German
- Greek
- English (British)
- English (American)
- Spanish
- Estonian
- Finnish
- French
- Hungarian
- Indonesian
- Italian
- Japanese
- Korean
- Lithuanian
- Latvian
- Norwegian Bokmål
- Dutch
- Polish
- Portuguese (unspecified variant for backward compatibility; please select PT-BR or PT-PT instead)
- Portuguese (Brazilian)
- Portuguese (all Portuguese varieties excluding Brazilian Portuguese)
- Romanian
- Russian
- Slovak
- Slovenian
- Swedish
- Turkish
- Ukrainian
- Chinese (simplified)

Please note that you need to have a DeepL API key to use this application. You can obtain a key by signing up for a free or paid plan on the [DeepL API Pro page](https://www.deepl.com/en/pro-api).