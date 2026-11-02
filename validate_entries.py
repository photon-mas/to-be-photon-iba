#!/usr/bin/env python3
"""Quality gate for enriched Vocab MASter entries (v2, Vocab MASter EV 1.0).

Changes from v1: sentences may use irregular forms (wrote, broke, shone) and
inflected or split phrasal verbs (broke down, turned the offer down); an entry may
set "no_close_synonym": true when the word has fewer than 3 true synonyms
(concrete nouns such as ankle or carrot), which turns that error into a warning.

Usage:
  python3 validate_entries.py batch.json
  python3 validate_entries.py ../data/words-master.json --only-status full

Input: a JSON array of entries (or {"entries": [...]}) using the field names in data/schema.json.
ERROR  = entry must be fixed before it is merged.
WARN   = below the gold standard but usable.
Exit code 1 if any ERROR is found.
"""
import json
import re
import sys
from collections import Counter

POS = {"noun", "verb", "adjective", "adverb", "preposition", "conjunction",
       "pronoun", "interjection", "phrase", "word"}


IRR = {'arise':'arose arisen','awake':'awoke awoken','be':'was were been','bear':'bore borne born','beat':'beaten','become':'became','begin':'began begun','bend':'bent','bid':'bade','bind':'bound','bite':'bit bitten','bleed':'bled','blow':'blew blown','break':'broke broken','breed':'bred','bring':'brought','build':'built','burn':'burnt','buy':'bought','catch':'caught','choose':'chose chosen','cling':'clung','come':'came','creep':'crept','deal':'dealt','dig':'dug','do':'did done does','draw':'drew drawn','dream':'dreamt','drink':'drank drunk','drive':'drove driven','eat':'ate eaten','fall':'fell fallen','feed':'fed','feel':'felt','fight':'fought','find':'found','flee':'fled','fling':'flung','fly':'flew flown flies','forbid':'forbade forbidden','forget':'forgot forgotten','forgive':'forgave forgiven','forswear':'forswore forsworn','freeze':'froze frozen','get':'got gotten','give':'gave given','go':'went gone goes','grind':'ground','grow':'grew grown','hang':'hung','have':'had has','hear':'heard','hide':'hid hidden','hold':'held','keep':'kept','kneel':'knelt','know':'knew known','lay':'laid','lead':'led','leap':'leapt','leave':'left','lend':'lent','lie':'lay lain lying','light':'lit','lose':'lost','make':'made','mean':'meant','meet':'met','mislead':'misled','overcome':'overcame','overtake':'overtook overtaken','partake':'partook partaken','pay':'paid','ride':'rode ridden','ring':'rang rung','rise':'rose risen','run':'ran','say':'said','see':'saw seen','seek':'sought','sell':'sold','send':'sent','shake':'shook shaken','shine':'shone','shoot':'shot','show':'shown','shrink':'shrank shrunk','sing':'sang sung','sink':'sank sunk','sit':'sat','sleep':'slept','slide':'slid','speak':'spoke spoken','speed':'sped','spend':'spent','spin':'spun','spring':'sprang sprung','stand':'stood','steal':'stole stolen','stick':'stuck','sting':'stung','stride':'strode','strike':'struck stricken','strive':'strove striven','swear':'swore sworn','sweep':'swept','swim':'swam swum','swing':'swung','take':'took taken','teach':'taught','tear':'tore torn','tell':'told','think':'thought','throw':'threw thrown','tread':'trod trodden','understand':'understood','undertake':'undertook undertaken','undergo':'underwent undergone','undo':'undid undone','uphold':'upheld','wake':'woke woken','wear':'wore worn','weave':'wove woven','weep':'wept','win':'won','wind':'wound','withdraw':'withdrew withdrawn','withhold':'withheld','withstand':'withstood','write':'wrote written','foresee':'foresaw foreseen','forgo':'forwent forgone','forsake':'forsook forsaken','beget':'begot begotten','slay':'slew slain','child':'children','man':'men','woman':'women','person':'people','foot':'feet','tooth':'teeth','mouse':'mice','criterion':'criteria','phenomenon':'phenomena','medium':'media','thesis':'theses','analysis':'analyses','crisis':'crises','hypothesis':'hypotheses','life':'lives','knife':'knives','wife':'wives','leaf':'leaves','half':'halves','shelf':'shelves','thief':'thieves','good':'better best','bad':'worse worst','far':'further farther furthest farthest','little':'less least'}


def forms(w):
    w = w.lower()
    f = {w, w+'s', w+'es', w+'ed', w+'d', w+'ing', w+'er', w+'est', w+'ly', w+"'s"}
    if w.endswith('e'): f |= {w[:-1]+'ing', w[:-1]+'ed'}
    if w.endswith('y'): f |= {w[:-1]+'ies', w[:-1]+'ied', w[:-1]+'ier', w[:-1]+'iest', w[:-1]+'ily'}
    if w.endswith('ie'): f |= {w[:-2]+'ying'}
    if len(w) > 2 and w[-1] not in 'aeiouwxy' and w[-2] in 'aeiou': f |= {w+w[-1]+'ed', w+w[-1]+'ing', w+w[-1]+'er'}
    if w.endswith('c'): f |= {w+'ked', w+'king'}
    f |= set(IRR.get(w, '').split())
    return f


def uses_word(sentence, word):
    """True if the sentence contains the headword or a form of it (handles irregular and phrasal verbs)."""
    s = sentence.lower().replace("\u2019", "'")
    toks = re.findall(r"[a-z][a-z'\-]*", s)
    parts = word.lower().split()
    if len(parts) == 1:
        if '-' in word: return word.lower() in s or word.lower().replace('-', ' ') in s
        F = forms(word)
        pre = re.compile(r"\b" + re.escape(prefix(word)) + r"\w*", re.I)
        return bool(pre.search(sentence)) or any(t in F or t.strip("'") in F for t in toks) or any(t.endswith('-' + word.lower()) or t.startswith(word.lower() + '-') for t in toks)
    skip = {'sth', 'sb', 'oneself', "one's", 'someone', 'something'}
    return all(any(t in forms(x) for t in toks) for x in parts if x not in skip)


def prefix(word):
    w = word.lower()
    if len(w) >= 6:
        return w[:len(w) - 2]
    if w.endswith(("e", "y")):
        return w[:-1]
    return w


def check(e):
    errs, warns = [], []
    w = (e.get("word") or "").strip().lower()
    if not w:
        return ["missing word"], warns
    d = (e.get("definition") or "").strip()
    if not d:
        errs.append("missing definition")
    elif len(d.split()) > 30:
        warns.append("definition longer than 30 words")
    pos = e.get("pos")
    pos_list = pos if isinstance(pos, list) else ([pos] if pos else [])
    if not pos_list:
        warns.append("missing pos")
    elif any(p not in POS for p in pos_list):
        errs.append(f"unknown pos {pos_list}")
    if not (e.get("ipa") or e.get("respelling") or e.get("ipa_or_respelling")):
        warns.append("missing pronunciation")

    strong, weak = e.get("strong_synonyms") or [], e.get("weak_synonyms") or []
    ants, rel = e.get("antonyms") or [], e.get("related") or []
    if len(strong) < 3 and e.get("no_close_synonym"):
        warns.append(f"strong_synonyms {len(strong)} < 3 (flagged no_close_synonym)")
    elif len(strong) < 3:
        errs.append(f"strong_synonyms {len(strong)} < 3")
    elif len(strong) < 5:
        warns.append(f"strong_synonyms {len(strong)} < 5")
    if len(weak) < 5:
        warns.append(f"weak_synonyms {len(weak)} < 5")
    if not ants and not e.get("no_natural_antonym"):
        errs.append("no antonyms (set no_natural_antonym:true if none exist)")
    elif 0 < len(ants) < 2:
        warns.append("antonyms < 2")
    if len(rel) < 5:
        warns.append(f"related {len(rel)} < 5")
    if w in {s.lower() for s in strong + weak + ants}:
        errs.append("word listed as its own synonym/antonym")
    if {s.lower() for s in strong + weak} & {a.lower() for a in ants}:
        errs.append("a word is both synonym and antonym")
    if {s.lower() for s in strong} & {s.lower() for s in weak}:
        warns.append("strong and weak synonym lists overlap")

    ex = [x.strip() for x in (e.get("examples") or []) if x and x.strip()]
    if len(ex) < 5:
        errs.append(f"examples {len(ex)} < 5")
    if len({x.lower() for x in ex}) < len(ex):
        errs.append("duplicate example sentences")
    using = sum(1 for x in ex if uses_word(x, w))
    if ex and using < min(5, len(ex)):
        errs.append(f"only {using} sentences contain the word or an inflection")
    for x in ex:
        n = len(x.split())
        if n < 5 or n > 30:
            warns.append(f"sentence length {n} words: {x[:40]}...")
            break
    return errs, warns


def main():
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    data = json.load(open(sys.argv[1], encoding="utf8"))
    entries = data["entries"] if isinstance(data, dict) else data
    if "--only-status" in sys.argv:
        want = sys.argv[sys.argv.index("--only-status") + 1]
        entries = [e for e in entries if e.get("status") == want]
    bad = clean = 0
    issues = Counter()
    for e in entries:
        errs, warns = check(e)
        for m in errs:
            issues["ERROR " + re.sub(r"\d+", "N", m)] += 1
        for m in warns:
            issues["WARN  " + re.sub(r"\d+", "N", m.split(":")[0])] += 1
        if errs:
            bad += 1
            print(f"[ERROR] {e.get('word')}: " + "; ".join(errs))
        elif not warns:
            clean += 1
    print(f"\nentries: {len(entries)} | with errors: {bad} | fully clean: {clean}")
    for k, v in issues.most_common():
        print(f"  {v:5d}  {k}")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
