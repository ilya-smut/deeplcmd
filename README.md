# DeepLCMD

DeepLCMD is a Python-based command line tool that utilizes the DeepL API to translate text and documents into a variety of languages.

## Features

- Translate text directly from the command line
- Translate documents from a given file path
- Supports a variety of target languages

## Installation
```bash
pip install deeplcmd
```
Please, note. You may want to create a virtual environment for the installation of the script
```bash
python -m venv .venv
.venv/bin/activate
```
read more about virtual environments here https://docs.python.org/3/library/venv.html

## Usage

Before using DeepLCMD, you need to login with your DeepL API key. You can do this directly on the command line using the `-k` option or by supplying a file containing the key using the `-kf` option. If no key is provided, you will be prompted to enter it.

```bash
deeplcmd login -k YOUR_API_KEY

```

OR

```bash
deeplcmd login -kf PATH_TO_YOUR_KEYFILE

```

OR

Open an interactive login. Will prompt you for either a filepath or a key
```bash
deeplcmd login
```

You can translate text using the `text` command:

```bash
deeplcmd text -tl TARGET_LANGUAGE "Your text here"

```

You can also translate documents using the `file` command:

```bash
deeplcmd file -tl TARGET_LANGUAGE INPUT_FILE OUTPUT_FILE

```

In both cases, replace `TARGET_LANGUAGE` with the language you want to translate to. 

Please note that the use of the DeepL API you will need to obtain API key from https://www.deepl.com/pro-api?cta=header-pro-api
