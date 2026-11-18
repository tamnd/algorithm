---
tag: FGZ5H1
kind: problem
slug: sentence-boundary-detection
name: Sentence boundary detection
aliases:
- sentence segmentation
- sentence splitting
area: natural-language-and-speech/tokenization-and-text-normalization
level: intro
summary: Decide which periods, question marks and other candidate marks in a text end a sentence, despite abbreviations, numbers and ellipses.
prereqs: [text-tokenization]
see_also: [penn-treebank-tokenization, unicode-text-segmentation, logistic-regression, sequence-labeling, truecasing, likelihood-ratio-test, precision-and-recall, tts-text-normalization]
sources:
  - url: https://aclanthology.org/J06-4003/
    title: Tibor Kiss and Jan Strunk, Unsupervised multilingual sentence boundary detection, Computational Linguistics 32(4), 2006
    locator: pages 485 to 525; Section 1 (the ambiguity of the period), Section 6 (evaluation on eleven languages), Section 7 (comparison with other systems)
  - url: https://aclanthology.org/J97-2002/
    title: David D. Palmer and Marti A. Hearst, Adaptive multilingual sentence boundary disambiguation, Computational Linguistics 23(2), 1997
    locator: pages 241 to 267
  - url: https://aclanthology.org/A97-1004/
    title: Jeffrey C. Reynar and Adwait Ratnaparkhi, A maximum entropy approach to identifying sentence boundaries, ANLP 1997
    locator: pages 16 to 19
  - url: https://www.unicode.org/reports/tr29/
    title: Unicode Standard Annex 29, Unicode Text Segmentation
    locator: Section 5 (sentence boundaries)
---

Sentence boundary detection is the problem of splitting a text into sentences, which comes down to deciding for each candidate mark, mostly the period, whether it ends a sentence. A question mark or an exclamation mark nearly always ends one, but a period can also end an abbreviation ("Dr."), an initial ("J."), an ordinal number in German ("12."), or be part of an ellipsis, and an abbreviation at the end of a sentence carries both meanings at once. The [Punkt sentence tokenizer](/punkt-sentence-tokenizer/) is an unsupervised algorithm for this problem; supervised classifiers and hand-written rules are the other main approaches. Many later stages expect one sentence per line, for example [Penn Treebank tokenization](/penn-treebank-tokenization/).

## In plain words

A period usually ends a sentence, but not always. In "Dr. Brown came at 5 p.m. He left early." the first period does not end a sentence, the period after "p.m." does, and it also marks a short form. A program must decide for each period. It looks at the word before it (is it a short form?) and at the word after it (is it capitalized, and is it a word that often starts sentences?). It can get this knowledge from a list, from labeled examples, or by counting in the text itself.

## Definition

**Input:** a text, split into tokens, and the set of candidate positions: the tokens that end in a period, a question mark, an exclamation mark or an ellipsis, possibly followed by closing quotes or brackets.

**Output:** for each candidate, a label "boundary" or "no boundary". Equivalently, a split of the token sequence into sentences.

**Quality** is measured on a labeled text, either as the error rate over all candidates or as [precision and recall](/precision-and-recall/) of the boundaries. Because most periods are easy, the error rate of the baseline "every period ends a sentence" is already low on news text, and the differences between systems are a few tenths of a percent. This is a measurement and depends on the corpus.

The problem has no answer independent of a convention: whether a colon, a semicolon or a line break ends a sentence, and where a quote after a period belongs, is fixed by the annotation guidelines of a corpus.

## Variants

- **Periods only.** Many papers treat ? and ! as sure boundaries and study only the period.
- **Abbreviation detection.** The joint task of finding which tokens are abbreviations; Punkt solves both, and its paper reports both error rates.
- **Text without case information.** In text that is all upper case or all lower case, capitalization gives no evidence, and the task interacts with [truecasing](/truecasing/).
- **Text without punctuation.** Speech recognizer output and some chat text have no periods at all. Then the task is to insert boundaries, a [sequence labeling](/sequence-labeling/) task with prosody or word features, often done together with punctuation restoration.
- **Other scripts.** Chinese and Japanese use a full stop that is rarely ambiguous, while Thai marks sentences with spaces, so the hard cases differ by language.
- **Rule-based default.** The [Unicode sentence boundary rules](/unicode-text-segmentation/) give a language-independent default, which does not break after a period when the next word starts in lower case, and breaks in most other cases.

## Examples

Take "Dr. Brown came at 5 p.m. He left early. Was it Mr. Lee's car? Yes."

| candidate | next token | boundary | why |
|---|---|---|---|
| Dr. | Brown | no | a title before a name |
| p.m. | He | yes | an abbreviation that also ends the sentence |
| early. | Was | yes | an ordinary word with a period |
| Mr. | Lee's | no | a title before a name |
| car? | Yes | yes | a question mark |
| Yes. | (end) | yes | the end of the text |

There is no period after "5" here, but in "came at 5. The" a period after a number would be another hard case. In German, "am 12. Juni" has an ordinal number with a period inside a sentence.

## Known algorithms

- **Rules and abbreviation lists.** Split at every period unless the token is in a list of abbreviations, with extra rules for initials and numbers. Simple, but the list must fit the language and the domain.
- **Decision trees.** Riley (1989) used regression trees over features of the words around a period.
- **Satz.** Palmer and Hearst (1997) feed the part-of-speech probabilities of the words around a candidate to a neural network or a decision tree, and adapt it to several languages.
- **Maximum entropy.** Reynar and Ratnaparkhi (1997) train a [logistic regression](/logistic-regression/) classifier (the system MxTerminator) on features of the token before and after a candidate.
- **[Punkt](/punkt-sentence-tokenizer/).** Kiss and Strunk (2006) learn abbreviations, initials, collocations and frequent sentence starters from the raw text with likelihood ratios, with no labeled data.
- **Neural sequence taggers.** Label each token or character as the end of a sentence or not; these are the standard when labeled data exist.

## Bounds

Every method that decides each candidate from a window of a fixed number of tokens runs in $O(n)$ time for a text of $n$ characters, given hash tables for the counts or the lists. Unsupervised methods such as Punkt first count over the whole text, which is also $O(n)$ expected time but needs all of the text before the first decision. On newspaper text in eleven languages, Kiss and Strunk measured error rates from 0.35% to 2.12% for Punkt, with a mean of 1.26%, and a mean of 1.77% for MxTerminator trained on the same corpora; these are measurements.

## Reductions

- **To binary classification.** Each candidate is one example with features from its context, so any classifier applies, for example [logistic regression](/logistic-regression/) or the [naive Bayes classifier](/naive-bayes-classifier/).
- **To sequence labeling.** Tag every token as "ends a sentence" or not; this also covers text without punctuation.
- **From abbreviation detection.** If the abbreviations are known, the remaining hard cases are abbreviations at the end of a sentence, initials and numbers; Punkt decides these with the word that follows.

## Applications

- **Tokenizers and parsers** that work one sentence at a time, such as [Penn Treebank tokenization](/penn-treebank-tokenization/).
- **Machine translation**, where parallel texts are aligned sentence by sentence.
- **Text to speech**, where a sentence end changes the intonation and the pause, see [TTS text normalization](/tts-text-normalization/).
- **Summarization and information extraction**, which select or label whole sentences.

## References
