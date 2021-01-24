import re
import io
import pathlib
from text.soros import compile

filepath = pathlib.Path(__file__).parent.absolute()
with io.open(f"{filepath}/ca.sor", 'r', encoding="utf-8") as prg:
    num2text = compile(prg.read(), 'ca')

_separador_milers_re = re.compile(r'([0-9][0-9\.]+[0-9]{3})')
_decimal_re = re.compile(r'([0-9]+\,[0-9]+)')
_ordinal_re = re.compile(r'[0-9]+(st|nd|rd|th)')
_cardinal_re = re.compile(r'[0-9]+')

def _esborra_separador_milers(m):
  return m.group(1).replace('.', '')

def _expand_ordinal(m):
  return _inflect.number_to_words(m.group(0))

def _num2text(m):
  return num2text.run(m.group(0))

def _num2text_ordinal(m):
  return num2text.run(f"ordinal {m.group(0)}")

def normalize_numbers_ca(text):
  text = re.sub(_separador_milers_re, _esborra_separador_milers, text)
  text = re.sub(_decimal_re, _num2text, text)
  text = re.sub(_ordinal_re, _num2text_ordinal, text)
  text = re.sub(_cardinal_re, _num2text, text)
  return text
