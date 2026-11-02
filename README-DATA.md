# Vocab MASter EV 1.2.0: word data in the handoff schema

For the enrichment pipeline in the earlier handoff package (`data/schema.json`, `scripts/validate_entries.py`).

| File | What it is |
|---|---|
| `entries-ev.json` | All 6,488 full entries in the handoff schema: `word`, `pos`, `ipa`, `respelling`, `definition`, `extra_senses`, `strong_synonyms`, `weak_synonyms`, `antonyms` (strongest then weak), `related`, `examples` (5), `collocations`, `word_family`, `lists`, plus `no_natural_antonym` / `no_close_synonym` flags where they apply. New in 1.2: `example_usage` (a usage label for each of the 5 examples, such as "Past tense" or "Gerund · -ing form as a noun"), `forms` (the word-forms table) and `form_sentences` (one extra labelled sentence for each form of the word: 14,661 in all). |
| `validate_entries.py` | The handoff validator, version 2. |
| `validation-report.txt` | Results for all entries and for IBA + Barron's, with the original validator shown for comparison, plus the check of the EV 1.2 form sentences. |

## Why the validator was updated
The original checked that each sentence contains the first letters of the headword. That rejects correct English:
- irregular forms: *wrote* (write), *shone* (shine), *upheld* (uphold), *broke* (break)
- phrasal verbs in the past tense or split: *worked out*, *broke down*, *turned the offer down*
- concrete nouns with fewer than 3 true synonyms (*ankle*, *squirrel*), which the schema had no way to mark

Version 2 accepts irregular and phrasal-verb forms and adds a `no_close_synonym` flag that works like the existing `no_natural_antonym`. Every other check is unchanged. All 320 sentence "errors" under version 1 are these false positives, and the 144 synonym "errors" are flagged concrete nouns.

Run it with: `python3 validate_entries.py entries-ev.json`
