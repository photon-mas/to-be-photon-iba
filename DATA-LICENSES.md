# Data sources and licences

Vocab MASter EV's own code is MIT-licensed (see `LICENSE`). The word data combines original writing with open data:

| Part of the data | Source | Licence |
|---|---|---|
| Headword lists (which words are on which list) | Barron's GRE 333 high-frequency list; GRE 500 Essential and 500 Advanced flash cards; Word Smart I and II (with the GRE Hit Parade); DU IBA BBA/MBA vocabulary; Coxhead's Academic Word List; the Oxford 3000 (via the MIT-licensed `oxford_3000` package) | Only the headwords are used. No definitions, example sentences or other text from these books are included. |
| Learner's definitions, sense labels, strongest and weak synonyms, antonyms, related words, collocations, five example sentences per word | Written for Vocab MASter | MIT, with the app |
| Extra senses, extra weak synonyms and antonyms, related words, word families, thesaurus entries | WordNet 3.1, Princeton University (via the `wordnet-db` package) | WordNet licence, reproduced below |
| Pronunciation respellings and IPA | Generated from the CMU Pronouncing Dictionary (via `cmu-pronouncing-dictionary`) | BSD-2-Clause, Copyright (C) 1993-2015 Carnegie Mellon University |
| Word frequencies used to rank weak synonyms | SUBTLEX-US (via `subtlex-word-frequencies`) | ISC package; research data |
| Fonts: Barlow, Barlow Condensed, Newsreader | Google Fonts, via Fontsource | SIL Open Font License 1.1 (`OFL.txt`) |

## WordNet licence

WordNet Release 3.0

This software and database is being provided to you, the LICENSEE, by  
Princeton University under the following license.  By obtaining, using  
and/or copying this software and database, you agree that you have  
read, understood, and will comply with these terms and conditions.:  
  
Permission to use, copy, modify and distribute this software and  
database and its documentation for any purpose and without fee or  
royalty is hereby granted, provided that you agree to comply with  
the following copyright notice and statements, including the disclaimer,  
and that the same appear on ALL copies of the software, database and  
documentation, including modifications that you make for internal  
use or for distribution.  
  
WordNet 3.0 Copyright 2006 by Princeton University.  All rights reserved.  
  
THIS SOFTWARE AND DATABASE IS PROVIDED "AS IS" AND PRINCETON  
UNIVERSITY MAKES NO REPRESENTATIONS OR WARRANTIES, EXPRESS OR  
IMPLIED.  BY WAY OF EXAMPLE, BUT NOT LIMITATION, PRINCETON  
UNIVERSITY MAKES NO REPRESENTATIONS OR WARRANTIES OF MERCHANT-  
ABILITY OR FITNESS FOR ANY PARTICULAR PURPOSE OR THAT THE USE  
OF THE LICENSED SOFTWARE, DATABASE OR DOCUMENTATION WILL NOT  
INFRINGE ANY THIRD PARTY PATENTS, COPYRIGHTS, TRADEMARKS OR  
OTHER RIGHTS.  
  
The name of Princeton University or Princeton may not be used in  
advertising or publicity pertaining to distribution of the software  
and/or database.  Title to copyright in this software, database and  
any associated documentation shall at all times remain with  
Princeton University and LICENSEE agrees to preserve same.  
