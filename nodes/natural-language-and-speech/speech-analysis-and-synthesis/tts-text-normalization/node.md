---
tag: VSXFZB
kind: problem
slug: tts-text-normalization
name: Text normalization for speech
aliases:
- verbalization of non-standard words
area: natural-language-and-speech/speech-analysis-and-synthesis
level: core
summary: "Rewrite numbers, dates, abbreviations and symbols in a text as the words a speaker would say, such as 1999 as nineteen ninety-nine."
prereqs: [text-to-speech, finite-state-transducer]
see_also: [grapheme-to-phoneme-conversion, text-tokenization, sentence-boundary-detection, sequence-labeling, word-sense-disambiguation, weighted-automaton, regular-expression, truecasing]
sources:
  - paper: doi:10.1006/csla.2001.0169
    title: "Richard Sproat, Alan W. Black, Stanley Chen, Shankar Kumar, Mari Ostendorf and Christopher Richards, Normalization of non-standard words, Computer Speech and Language 15(3), 2001, pages 287 to 333"
    locator: "Table 1 (the taxonomy of non-standard words) and the sections on tagging and expansion"
  - paper: doi:10.1017/S1351324914000175
    title: "Peter Ebden and Richard Sproat, The Kestrel TTS text normalization system, Natural Language Engineering 21(3), 2015, pages 333 to 353"
    locator: "the description of the classification and verbalization stages"
  - book: isbn:9780521899277
    title: "Paul Taylor, Text-to-Speech Synthesis, Cambridge University Press, 2009"
    locator: "Chapter 4 (Text segmentation and organisation) and Chapter 5 (Text decoding: finding the words from the text)"
---

Text normalization for speech is the first step of [text-to-speech](/text-to-speech/). It rewrites the parts of a text that are not ordinary words, such as numbers, dates, times, money, measures, abbreviations, acronyms and symbols, as the words that a speaker would say. Sproat and his coauthors call these tokens non-standard words. The task is hard because the same written form can have different readings. "1999" is "nineteen ninety-nine" as a year and "one thousand nine hundred ninety-nine" as a count. "St." is "saint" or "street". "Dr." is "doctor" or "drive". The context decides. A wrong reading is a bad error, because the listener hears a different fact (a wrong number, a wrong date) and cannot see the original text.

## In plain words

Text is full of things that we do not read letter by letter. We see "$3.50" and say "three dollars and fifty cents". We see "Dr." and say "doctor". We see "NATO" and say it as a word, but we spell out "CIA" letter by letter.

A text-to-speech system must do the same before it can make any sound. It must first find these special pieces of text, then decide what kind each one is, and then write out the words.

The hard part is that one piece of text can be read in more than one way. A number can be a year or a count. "St." can be a saint or a street. The system must look at the words around it to choose. A mistake here changes the meaning, not only the sound.

## Definition

**Input.** A text, as a sequence of characters, usually split into tokens by [text tokenization](/text-tokenization/) and into sentences by [sentence boundary detection](/sentence-boundary-detection/).

**Output.** A sequence of spoken-form words, one verbalization for each input token. Ordinary words are copied. A non-standard word may become zero words (punctuation that is not read), one word or several words, and the words may be in a different order than the symbols: "$3.50" becomes "three dollars and fifty cents", with "dollars" after the number.

**Structure.** Most systems split the task into three steps, as Sproat et al. (2001) and the Kestrel system of Ebden and Sproat (2015) do:

1. **Detection and splitting.** Find the non-standard tokens, and split mixed tokens such as "3am" or "WinNT".
2. **Classification.** Give each token a class. The taxonomy of Sproat et al. (2001, Table 1) has letter classes, among them EXPN (expand an abbreviation, as "mph"), LSEQ (read as letters, as "CIA"), ASWD (read as a word, as "NATO") and MSPL (a misspelling), and number classes, among them NUM (a cardinal), NYER (a year), MONEY, ordinals and digit strings. Kestrel uses a similar set of semiotic classes, such as cardinal, date, time, money and measure.
3. **Verbalization.** Write out the words for the class, by rules for each language: number names, date formats, unit names, and the agreement of case and gender in languages that need it.

**Evaluation.** The usual score is the token error rate or the sentence error rate against a human reading. Because some errors change meaning and others do not, systems are also judged by the number of "unacceptable" errors, such as a wrong digit.

## Variants

- **Normalization for speech recognition.** The inverse task: turn spoken-form words from a recognizer back into written form ("twelve thirty p m" to "12:30 p.m."). It is called inverse text normalization.
- **Normalization of social media text.** Map "cul8r" or "sooooo" to standard words. The goal is reading or analysis, not speech, but many methods are shared.
- **Many languages.** Number names and agreement differ a lot across languages. In Russian, for example, the form of a number word depends on the case and gender of the noun after it.
- **Rule-based or learned.** Hand-written grammars, learned classifiers with hand-written verbalizers, or neural sequence models that learn the whole mapping.

## Examples

- **Year or count.** A year rule splits a four-digit number into two pairs when the second pair is not "00": 1999 becomes "nineteen" plus "ninety-nine". A count rule reads thousands, hundreds and the rest: 1999 is 1 thousand, 9 hundreds and 99, so "one thousand nine hundred ninety-nine". For 1905, the year rule gives "nineteen oh five". For 2005, the usual English reading is "two thousand five" (an observation about usage), so the rule needs an exception for the years 2000 to 2009.
- **Money.** "$3.50" has the class MONEY. The number before the point is the dollar part and the two digits after it are the cents: "three dollars and fifty cents". "$3.5 billion" is not "three dollars and fifty cents billion" but "three point five billion dollars", so the verbalizer must look past the number.
- **Abbreviations in context.** In "Dr. Smith lives on Elm Dr.", the first "Dr." comes before a name and is "doctor", the second comes after a street name and is "drive". A classifier can learn this from the neighboring words, or a grammar can encode the two patterns.

## Known algorithms

- **Hand-written rules and lexicons.** Patterns, often [regular expressions](/regular-expression/), detect the tokens, and code or tables verbalize them. Simple, but hard to maintain across languages.
- **Weighted finite-state grammars.** Classification and verbalization are written as weighted grammars and compiled into [finite-state transducers](/finite-state-transducer/). The input is composed with the transducer, and the best path gives the output. Kestrel is built this way.
- **Classifiers for ambiguous tokens.** Sproat et al. (2001) use a classifier over features of the token and its context to choose the class, and language models over the possible expansions of an abbreviation. This is a form of [word sense disambiguation](/word-sense-disambiguation/) for tokens.
- **Neural sequence models.** An encoder-decoder model reads the characters around a token and writes the spoken form. Such models are accurate on common cases but can make unacceptable errors such as a changed digit, so they are often combined with finite-state grammars that limit the output to valid readings.

## Bounds

- **Time.** For a fixed grammar compiled into a transducer, normalization of a text of $n$ characters is linear in $n$: the composition of the input with the transducer has $O(n)$ states for a fixed transducer, and its best path in this acyclic result takes linear time (a theorem about composition and acyclic shortest paths).
- **Ambiguity.** Some tokens cannot be resolved from the text at all. "St." with no name around it, or a four-digit number with no context, can have two correct readings. Any method has a nonzero error rate on such cases (an observation).
- **Coverage.** A rule system reads only the patterns that its authors wrote; a learned system reads only what its data covers. Both fail on new formats, such as new kinds of identifiers.

## Reductions

- **To [sequence labeling](/sequence-labeling/).** Classification gives each token a class label, so the second step is a tagging problem.
- **To transducer composition and shortest path.** With weighted grammars, normalization is composition with a [weighted automaton](/weighted-automaton/) followed by a best path search.
- **To sequence-to-sequence learning.** A neural model treats the whole task as translation from written form to spoken form.
- **From [text-to-speech](/text-to-speech/).** Text normalization is the first stage of the front end, before [grapheme-to-phoneme conversion](/grapheme-to-phoneme-conversion/). Every TTS system needs it, including end-to-end neural ones.

## Applications

The front end of every text-to-speech system; the inverse task in speech recognition, to write numbers and dates in the usual written form; preparation of training text for speech and language models; and screen readers, where text from web pages has many symbols, addresses and codes.
