import sys
import click
import deepl
import os
import dotenv

# All supported target languages
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


def attempt_login_to_env(key):
    """
    Attempts to write login to .env
    :param key: Deepl API key
    :return: True if successfully wrote a key to .env; False if .env not writable
    """
    with open(os.path.join(os.path.dirname(__file__), '.env'), "w") as environment:
        if environment.writable():
            return environment.write(f'APIKEY={key}')
        else:
            return False


def enter_login_details():
    """
    Interactive way of entering Deepl API key to environment. Allows entering the key string or
    providing a path to a file with key
    :return: Does not return anything. If unable to write key to environment - does sys.exit()
    """
    file_or_manual = input('Do you want to enter a key file or enter key manually? Type "e" to exit. [F/M]?: ')
    if file_or_manual.upper().startswith('F'):
        filepath = input('Please, enter a filepath: ')
        if os.path.isfile(filepath):
            with open(filepath, 'r') as keyfile:
                key = keyfile.read()
                if attempt_login_to_env(key):
                    click.secho('Successful login', fg='green')
                else:
                    click.secho('Login Unsuccessful', fg='red')
                    sys.exit()
        else:
            click.secho(f'File {filepath} does not exist or is a directory', fg='red')
            enter_login_details()

    elif file_or_manual.upper().startswith('M'):
        key = input('Please, enter deepl API key: ')
        if attempt_login_to_env(key):
            click.secho('Successful login', fg='green')
        else:
            click.secho('Login Unsuccessful', fg='red')
            sys.exit()

    elif file_or_manual.upper().startswith('E'):
        sys.exit()
    else:
        enter_login_details()


def is_logged_in():
    """
    Checks if APIKEY is in .env
    :return: True if APIKEY in .env ; False if APIKEY is not in .env
    """
    if os.getenv('APIKEY'):
        return True
    else:
        return False


def init_translator(key):
    """
    Initiates a deepl translator instance
    :param key: deepl API key
    :return: deepl.Translator instance
    """
    return deepl.Translator(key)


def overwrite_check(path):
    """
    Checks if file already exists. If file exists - prompts user if they want to overwrite it.
    If user does not want to overwrite the file - sys.exit()
    :param path: System path to a file
    """
    if os.path.exists(path):
        cmd = input(f'File {path} already exists. Overwrite? [y/n] -> ').upper()
        if not cmd.startswith('Y'):
            sys.exit()


def verify_target_language(target_lang):
    """
    Verifies that the target language is supported. If it is not supported then execution of the program ends.
    If target language is unsupported, user is presented with a dictionary of supported languages.
    :param target_lang: Code of language (i.e. EN-GB for British English, RU for Russian)
    """
    if target_lang.upper() not in TARGET_LANGUAGES:
        click.secho(f'Target language {target_lang} is not recognised.', fg='red')
        click.secho(f'Please, use one of the following: {TARGET_LANGUAGES}', fg='blue')
        sys.exit()


def translate_text(target_lang, text, key):
    """
    Attempts to translate provided string of text. If authentication fails or key is empty program execution ends.
    :param target_lang: target language code
    :param text: string of text
    :param key: deepl API key
    :return: if successful - returns a string of translated text or a list of translated strings
    """
    translator = init_translator(key)
    verify_target_language(target_lang)
    try:
        return translator.translate_text(text=text, target_lang=target_lang.upper())
    except deepl.exceptions.AuthorizationException:
        click.secho('Authentication Failure. Check API key', fg='red')
        sys.exit()
    except ValueError:
        click.secho('Key must not be empty', fg='red')
        sys.exit()


def translate_file(target_lang, key, input_file_path, output_file_path):
    """
    Attempts to translate a file input_file_path and save it as output_file_path.
    :param target_lang: target language code
    :param key: deepl API key
    :param input_file_path: path of an input file with text to be translated
    :param output_file_path: path of an output file with translated text
    :return:
    """
    translator = init_translator(key)
    verify_target_language(target_lang)
    overwrite_check(output_file_path)
    try:
        translator.translate_document_from_filepath(
            input_file_path,
            output_file_path,
            target_lang=target_lang.upper()
        )
        return True
    except deepl.exceptions.AuthorizationException:
        click.secho('Authentication Failure. Check API key', fg='red')
        sys.exit()


@click.group()
@click.option('-k', '--key', type=str, help='DeepL API key. [Optional. API key should be passed to login command]')
@click.option('-kf', '--keyfile', type=click.types.File(mode='r'),
              help='File containing DeepL API key. [Optional. API key should be passed to login command]')
@click.pass_context
def init(ctx, key, keyfile):
    """DeepLCMD is a simple command line application for text and document translation with Deepl Translator API.
    https://www.deepl.com/en/pro-api"""
    dotenv.load_dotenv()
    ctx.ensure_object(dict)
    if key:
        ctx.obj['KEY'] = key
    elif keyfile:
        ctx.obj['KEY'] = keyfile.read()
    elif is_logged_in():
        ctx.obj['KEY'] = os.getenv('APIKEY')
    else:
        ctx.obj['KEY'] = None


@init.command(help='Persistently store an API key.')
@click.option('-k', '--key', type=str, help='Your DeepL API key')
@click.option('-kf', '--keyfile', type=click.types.File(mode='r'),
              help='File containing DeepL API key (should contain ONLY key')
def login(key, keyfile):
    if key:
        if attempt_login_to_env(key):
            click.secho('Successful login', fg='green')
        else:
            click.secho('Login Unsuccessful', fg='red')
            sys.exit()

    elif keyfile:
        if attempt_login_to_env(keyfile.read()):
            click.secho('Successful login', fg='green')
        else:
            click.secho('Login Unsuccessful', fg='red')
            sys.exit()
    else:
        enter_login_details()


@init.command(help='Translate a string of text.')
@click.option('-tl', '--target-language', required=True, prompt='Language of translation',
              help='Language of translation')
@click.argument('text')
@click.pass_context
def text(ctx, target_language, text):
    key = ctx.obj['KEY']
    if not key:
        click.secho('Key was not provided', fg='red')
        sys.exit()
    click.echo(translate_text(target_language, text, key))


@init.command(help='Translate a file.')
@click.option('-tl', '--target-language', required=True, prompt='Language of translation',
              help='Language of translation')
@click.argument('input_file_path', type=click.types.Path(exists=True, dir_okay=False))
@click.argument('output_file_path', type=click.types.Path(dir_okay=False, writable=True))
@click.pass_context
def file(ctx, target_language, input_file_path, output_file_path):
    key = ctx.obj['KEY']
    if not key:
        click.secho('Key was not provided', fg='red')
        sys.exit()
    if translate_file(target_language, key, input_file_path, output_file_path):
        click.echo(click.style('File ', fg='green') + click.style(input_file_path, fg='blue') +
                   click.style(' has been successfully translated and saved as ', fg='green') +
                   click.style(output_file_path, fg='blue'))


if __name__ == '__main__':
    init()
