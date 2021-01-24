import re
import io
import pathlib
from text.soros import compile

filepath = pathlib.Path(__file__).parent.absolute()
with io.open(f"{filepath}/ca.sor", 'r', encoding="utf-8") as prg:
    num2text = compile(prg.read(), 'ca')

_separador_milers_re = re.compile(r'([0-9][0-9\.]+[0-9]{3})')
_decimal_re = re.compile(r'([0-9]+\,[0-9]+)')
_ordinal_ms_re = re.compile(r'([0-9]+)(r|er|n|on|t|rt|è|e|ne|nè)+(\b)')
_ordinal_mp_re = re.compile(r'([0-9]+)(rs|ns|ts|ns)+(\b)')
_ordinal_fs_re = re.compile(r'([0-9]+)(a|ra|na|ta)+(\b)')
_ordinal_fp_re = re.compile(r'([0-9]+)(es)+(\b)')
_cardinal_re = re.compile(r'[0-9]+')
_fraccions_re = re.compile(r'(\b)([0-9]+\/[0-9]+)(\b)')
_hores_re = re.compile(r'(\b)([0-9]{1,2}):([0-9]{2})(\b)')

def _esborra_separador_milers(m):
  return m.group(1).replace('.', '')

def _num2text(m):
  return num2text.run(m.group(0))

def _ordinal_ms(m):
  return num2text.run(f"ordinal {m.group(1)}") + m.group(3)

def _ordinal_mp(m):
  return num2text.run(f"ordinal-masculine-plural {m.group(1)}") + m.group(3)

def _ordinal_fs(m):
  return num2text.run(f"ordinal-feminine {m.group(1)}") + m.group(3)

def _ordinal_fp(m):
  return num2text.run(f"ordinal-feminine-plural {m.group(1)}") + m.group(3)

def _fraccions(m):
  return m.group(1) + num2text.run(f"fraction {m.group(2)}") + m.group(3)

def _hores(m):
  return m.group(1) + num2text.run(m.group(2)) + " i " + num2text.run(m.group(3))  + m.group(4)

def normalize_numbers_ca(text):
  text = re.sub(_separador_milers_re, _esborra_separador_milers, text)
  text = re.sub(_decimal_re, _num2text, text)
  text = re.sub(_ordinal_ms_re, _ordinal_ms, text)
  text = re.sub(_ordinal_mp_re, _ordinal_mp, text)
  text = re.sub(_ordinal_fs_re, _ordinal_fs, text)
  text = re.sub(_ordinal_fp_re, _ordinal_fp, text)
  text = re.sub(_fraccions_re, _fraccions, text)
  text = re.sub(_hores_re, _hores, text)
  text = re.sub(_cardinal_re, _num2text, text)
  return text
