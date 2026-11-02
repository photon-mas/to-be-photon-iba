# Changelog

## EV 1.2.0 (2 November 2026): play, test and every form

### New
- **Timed Test** (`#vm-test`) with four time controls, as in chess: **Bullet** 10 s, **Blitz** 20 s, **Rapid** 30 s (the 30-second thumb rule, the default) and **Classical** 60 s per question. Choose 10, 20, 30 or 50 questions, the word source (any list, Saved words or the Mistakes deck) and the question types: meaning, word from meaning, synonym, antonym, fill in the blank and **word form**. A countdown ring, keys 1–4, a combo multiplier (×1.5 from 3 in a row, ×2 from 6, ×3 from 10), points with a time bonus and ticks in the last seconds.
- **Ratings:** each time control has an Elo-style rating (start 1200). Every question is rated by how hard the word is (its lists and length), so beating hard words moves your rating more. The first five tests in a control count double. Results show accuracy, average time, best combo, the rating change, personal bests and a full review; missed words go to the **Mistakes deck**.
- **Daily Challenge** (`#vm-daily`): seven questions, the same for everyone each day (Dhaka time), 30 s each, one scored attempt, a Wordle-style result grid to copy or share, and a daily streak.
- **Context Detective** (`#vm-detective`): name a hidden word from sentences with the word blanked. Each wrong guess or extra clue reveals more (a sentence, the part of speech and first letter, the definition); 5 points down to 1.
- **Form Forge** (`#vm-forge`): pick the exact form a sentence needs (abate, abates, abated, abating) and see the grammar label that explains it.
- **Levels, XP and badges:** earn XP for new words, reviews, games, tests and streaks, and climb ten chess levels from Pawn to Grandmaster. 24 badges, a header chip with your level and streak, and a **Profile** page (`#vm-profile`) with ratings and sparklines, a 26-week activity heatmap, badges and records. Sound effects can be turned off.
- **Exam countdown:** set your exam date and list; the planner shows the days left and how many words a day you need, with today's progress.
- **Every sentence labelled:** each example sentence shows how the word is used (noun, past tense, past participle in the passive, gerund, adjective before a noun, and so on). Entries also show a **word-forms table** (5,579 entries) and, where written, one more sentence for each form of the word (14,661 every-form sentences; 47,101 sentences in all).

### Changed
- New look: pure white pages and cards (no off-white or grey), Photon orange for strongest and strong synonyms, **light green for weak synonyms** and **red for antonyms**, with a key above the synonym list. The synonym map, quiz feedback and the dark theme use the same colours.
- The bottom tab bar on phones is Home, Lists, **Test**, Games and About. Flashcards stay in Games and in each list.
- The data files are now split into more parts because of the new sentences; `sw.js` lists them all.

## EV 1.1.0 (30 October 2026)
- **Thesaurus.com-style intro:** each word page opens with the word, its pronunciation, then a part-of-speech and sense card (for example NOUN · spying), then the synonyms.
- **Three tiers:** synonyms and antonyms are now grouped as Strongest, Strong and Weak.
- **Pronunciation variants** in dictionary style, for example tomato [tuh-**mey**-toh, -**mah**-toh] and record [ruh-**kawrd**, **rek**-erd, ri-**kawrd**], with matching IPA.
- **New: Word of the Day player.** An animated, spoken card that plays the word, its syllables, meaning, an example and synonyms. It appears on every word page, on the home page and on the Word of the Day page.
- **New: Spell It.** Hear the word, read its meaning and a gapped sentence, then type the spelling. It includes letter hints, a mistake highlighter and a score.
- **Photon IBA branding:** logo, cover banner, app icons and an orange, white and slate colour theme taken from the logo, with a matching dark theme. Antonyms use slate blue so they stand apart from the orange synonyms.
- **About:** adds MBA, Institute of Business Administration (IBA), University of Dhaka; links to github.com/photon-mas; and a Photon IBA section with a note that this is an independent student project.
- New entries: *espionage* and *senescent* (6,488 full entries).
- Now published from the `photon-mas` GitHub account: https://photon-mas.github.io/vocab-master-ev/

## EV 1.0.0 (30 October 2026): the completed English edition

This release finishes the work left open in the earlier Vocab MASter EV build (the single-file app and its handoff package). It is English only: there are no Bangla meanings in this edition.

### What was incomplete, and what EV 1.0.0 does

| Earlier EV build (measured in its handoff) | EV 1.0.0 |
|---|---|
| 2,964 words, but only **60** hand-written and **36** with five or more sentences | **6,486 full entries**, every one with **five** everyday example sentences (32,430 in total) |
| 295 words with a Barron's meaning only; 2,609 words with just the headword, which depended on an untested live lookup | Every entry is complete and stored offline; there is no live lookup |
| 34 of the 35 best entries had fewer than 5 weak synonyms, 24 had no related words | 99% have 5 or more weak synonyms and related words (see `verify.js`) |
| Synonyms as *Strongest* and *Weak* on a few words only | *Strongest / Weak* synonyms and *Strongest / Weak* antonyms on every entry, as on Thesaurus.com |
| No collocations or word family | 3–6 collocations on every entry, and the word family where one exists |
| Oxford, Gregmat, TOEFL and Everyday tags made up from memory | Real lists only: TOEFL = Coxhead's Academic Word List (570), Everyday = Oxford 3000 (3,488). Gregmat has no source file, so **Import a list** lets you add yours |
| 15 hand-written words wrongly tagged IBA; IBA list 1,071 tokens with inflections, typos and noise | IBA list rebuilt from the PDF: 1,053 base-form words, OCR typos fixed (*timidity*, *relinquish*), short words kept (*awe*, *cue*, *flu*, *fur*, *sly*, *wit*), with a filter by test year |
| GRE 500 decks 498 and 499 of 500 cards; Word Smart list with roots and non-words | 500 / 500 cards in each deck, and only real Word Smart headwords |
| Barron's meanings copied from the PDF | Own definitions; source books give headwords only |
| One 270 KB file with all data inline; list pages drew up to 1,666 cards at once; no typo tolerance | Data in 50 lazy-loaded files; list pages load as you scroll; search suggests the closest spellings |
| Pronunciation missing on most words | Respelling and IPA on every word |
| Service worker cache `vocab-mas-v3` deleted every other cache on the site | Cache cleanup is limited to this app's own caches |

**IBA comes first:** IBA Admission is the first list and the default list for flashcards, the quiz, Match and Spin the Wheel.

**References:** each entry links to the Oxford Learner's Dictionaries and the Cambridge Dictionary. There are no Thesaurus.com links and no ads.

### Quality checks run for this release
- `verify.js`: all 6,486 entries have a definition, part of speech and five sentences, and none contains Bangla text.
- The handoff's `validate_entries.py`, updated to accept irregular verb forms (*wrote*, *shone*) and split phrasal verbs (*broke down*): **0 errors** on all 6,486 entries, and 1,259 of the 1,306 IBA and Barron's words fully clean, with no warnings. The remaining warnings are concrete nouns with few true synonyms (*squirrel*, *measles*) or words with a single real antonym.
- Browser tests at 1,366 px and 390 px, in light and dark themes: every page loads with no console errors and no sideways scrolling, and the words still open offline.
