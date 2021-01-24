""" from https://github.com/keithito/tacotron """

'''
Cleaners are transformations that run over the input text at both training and eval time.

Cleaners can be selected by passing a comma-delimited list of cleaner names as the "cleaners"
hyperparameter. Some cleaners are English-specific. You'll typically want to use:
  1. "english_cleaners" for English text
  2. "transliteration_cleaners" for non-English text that can be transliterated to ASCII using
     the Unidecode library (https://pypi.python.org/pypi/Unidecode)
  3. "basic_cleaners" if you do not want to transliterate (in this case, you should also update
     the symbols in symbols.py to match your data).
'''

import re
from unidecode import unidecode
from text.numbers import normalize_numbers
from text.numbers_ca import normalize_numbers_ca
from text.symbols import symbols

# Regular expression matching whitespace:
_whitespace_re = re.compile(r'\s+')

# List of (regular expression, replacement) pairs for abbreviations:
_abbreviations_en = [(re.compile('\\b%s\\.' % x[0], re.IGNORECASE), x[1]) for x in [
  ('mrs', 'misess'),
  ('mr', 'mister'),
  ('dr', 'doctor'),
  ('st', 'saint'),
  ('co', 'company'),
  ('jr', 'junior'),
  ('maj', 'major'),
  ('gen', 'general'),
  ('drs', 'doctors'),
  ('rev', 'reverend'),
  ('lt', 'lieutenant'),
  ('hon', 'honorable'),
  ('sgt', 'sergeant'),
  ('capt', 'captain'),
  ('esq', 'esquire'),
  ('ltd', 'limited'),
  ('col', 'colonel'),
  ('ft', 'fort'),
]]

# List of (regular expression, replacement) pairs for catalan abbreviations:
_abbreviations_ca = [(re.compile('\\b%s\\b' % x[0], re.IGNORECASE), x[1]) for x in [
  ('tv3', 't v tres'),
  ('8tv', 'vuit t v'),
  ('pp', 'p p'),
  ('psoe', 'p soe'),
  ('sr.?', 'senyor'),
  ('sra.?', 'senyora'),
  ('srta.?', 'senyoreta')
]]

_replacements_ca = [(re.compile('%s' % x[0], re.IGNORECASE), x[1]) for x in [
  (';', ','),
  (':', '\.'),
  ('\.\.\.,', ','),
  ('\.\.\.', '…'),
  ('ñ','ny')
]]


def expand_abbreviations(text, lang='ca'):
  if lang == 'en':
    _abbreviations = _abbreviations_en
  elif lang == 'ca':
    _abbreviations = _abbreviations_ca
  else:
    raise ValueError('no %s language for abbreviations'%lang)
  for regex, replacement in _abbreviations:
    text = re.sub(regex, replacement, text)
  return text


def convert_characters(text, lang='ca'):
  if lang == 'ca':
    _replacements = _replacements_ca
  else:
    raise ValueError('no %s language for punctuation conversion'%lang)
  for regex, replacement in _replacements_ca:
    text = re.sub(regex, replacement, text)
  return text


def expand_numbers(text, lang="ca"):
  if lang == 'ca':
    return normalize_numbers_ca(text)
  else:
    return normalize_numbers(text)


def lowercase(text):
  return text.lower()


def collapse_whitespace(text):
  return re.sub(_whitespace_re, ' ', text)


def convert_to_ascii(text, lang="ca"):
  if lang == 'en':
    return unidecode(text)
  elif lang == 'ca':
    char_replace = []
    for t in set(list(text)):
      if t not in symbols:
        char_replace.append([t, unidecode(t)])
    for target, replace in char_replace:
      text = text.replace(target, replace)
    return text
  else:
    raise ValueError('no %s language for punctuation conversion'%lang)


def basic_cleaners(text):
  '''Basic pipeline that lowercases and collapses whitespace without transliteration.'''
  text = lowercase(text)
  text = collapse_whitespace(text)
  return text


def transliteration_cleaners(text):
  '''Pipeline for non-English text that transliterates to ASCII.'''
  text = convert_to_ascii(text)
  text = lowercase(text)
  text = collapse_whitespace(text)
  return text


def english_cleaners(text):
  '''Pipeline for English text, including number and abbreviation expansion.'''
  text = convert_to_ascii(text)
  text = lowercase(text)
  text = expand_numbers(text, lang='en')
  text = expand_abbreviations(text, lang='en')
  text = collapse_whitespace(text)
  return text


def catalan_cleaners(text):
  text = lowercase(text)
  text = expand_numbers(text, lang="ca")
  text = convert_characters(text, lang="ca")
  text = convert_to_ascii(text, lang="ca")
  text = expand_abbreviations(text, lang="ca")
  text = collapse_whitespace(text)
  return text
