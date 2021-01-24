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
_fraccions_mig_s_re = re.compile(r'(\b)1\/2(\b)')
_fraccions_mig_p_re = re.compile(r'(\b)([0,2-9]+)\/2(\b)')
_fraccions_terc_s_re = re.compile(r'(\b)1\/3(\b)')
_fraccions_terc_p_re = re.compile(r'(\b)([0,2-9]+)\/3(\b)')
_fraccions_generic_s_re = re.compile(r'(\b)1\/([0-9]+)(\b)')
_fraccions_generic_p_re = re.compile(r'(\b)([0,2-9]+)\/([0-9]+)(\b)')

def _esborra_separador_milers(m):
  return m.group(1).replace('.', '')

def _num2text(m):
  return num2text.run(m.group(0))

def _num2text_ordinal_ms(m):
  return num2text.run(f"ordinal {m.group(1)}") + m.group(3)

def _num2text_ordinal_mp(m):
  return num2text.run(f"ordinal-masculine-plural {m.group(1)}") + m.group(3)

def _num2text_ordinal_f(m):
  return num2text.run(f"ordinal-feminine {m.group(1)}") + m.group(3)
  
def _fraccions_mig_s(m):
  return m.group(1) + "mig" + m.group(2)

def _fraccions_mig_p(m):
  return m.group(1) + num2text.run(f"masculine {m.group(2)}") + " mitjos" + m.group(3)

def _fraccions_terc_s(m):
  return m.group(1) + "un terç" + m.group(2)

def _fraccions_terc_p(m):
  return m.group(1) + num2text.run(f"masculine {m.group(2)}") + " terços" + m.group(3)
  
def _fraccions_generic_s(m):
  return m.group(1) + "un " + num2text.run(f"ordinal {m.group(2)}") + m.group(3)
  
def _fraccions_generic_p(m):
  return m.group(1) + num2text.run(f"masculine {m.group(2)}") + " " + num2text.run(f"ordinal-masculine-plural {m.group(3)}") + m.group(4)

def normalize_numbers_ca(text):
  text = re.sub(_separador_milers_re, _esborra_separador_milers, text)
  text = re.sub(_decimal_re, _num2text, text)
  text = re.sub(_ordinal_ms_re, _num2text_ordinal_ms, text)
  text = re.sub(_ordinal_mp_re, _num2text_ordinal_mp, text)
  text = re.sub(_ordinal_fs_re, _num2text_ordinal_f, text)
  text = re.sub(_fraccions_mig_s_re, _fraccions_mig_s, text)
  text = re.sub(_fraccions_mig_p_re, _fraccions_mig_p, text)
  text = re.sub(_fraccions_terc_s_re, _fraccions_terc_s, text)
  text = re.sub(_fraccions_terc_p_re, _fraccions_terc_p, text)
  text = re.sub(_fraccions_generic_s_re, _fraccions_generic_s, text)
  text = re.sub(_fraccions_generic_p_re, _fraccions_generic_p, text)
  text = re.sub(_cardinal_re, _num2text, text)
  return text
