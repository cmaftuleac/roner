# ── 0.  Set-up ─────────────────────────────────────────────────────────
# pip  install  roner               # one-time install  :contentReference[oaicite:0]{index=0}
import copy
import roner

# ── 1.  Load the model ────────────────────────────────────────────────
ner = roner.NER()                   # downloads model weights on first call

# ── 2.  Run NER and keep an untouched copy ────────────────────────────
text = """
Andrei Popescu lucrează la Guvernul Republicii Moldova în Chișinău.
Datele lui de contact sunt urmatoarele:
Tel: 02 371 256 100
E-mail: andrei.popescu@gmail.com
Cod Personal: 1029384756478
Adresa: str. Bogdan Vilhetei, nr. 10, Chisinau.
"""
outputs = ner([text])               # list with one dict
orig    = copy.deepcopy(outputs)    # we’ll need this for de-anon

# ── 3.  Anonymise in-place ────────────────────────────────────────────
for word in outputs[0]['words']:
    if word['tag'] != "O":          # “O” = outside any entity
        # redact the surface form with its (BIO-2 collapsed) label
        word['text'] = f"<{word['tag']}>"

anon_text = ner.detokenize(outputs)[0]   # preserves white-space/diacritics
print("ANON :", anon_text)

# ── 4.  De-anonymise (simply detokenise pristine copy) ───────────────
deanon_text = ner.detokenize(orig)[0]
print("ORIG :", deanon_text)
