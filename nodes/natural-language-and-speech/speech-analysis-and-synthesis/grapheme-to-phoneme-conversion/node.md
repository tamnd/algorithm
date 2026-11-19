---
tag: ZS6V26
kind: problem
slug: grapheme-to-phoneme-conversion
name: Grapheme-to-phoneme conversion
aliases:
- G2P
- letter-to-sound conversion
area: natural-language-and-speech/speech-analysis-and-synthesis
level: core
summary: "Predict the sequence of phonemes that spells the pronunciation of a written word, including words not in the lexicon."
prereqs: [text-to-speech, pronunciation-lexicon]
see_also: [joint-sequence-g2p, tts-text-normalization, edit-distance, word-error-rate, decision-tree, finite-state-transducer, encoder-decoder-model, automatic-speech-recognition]
sources:
  - paper: doi:10.1016/j.specom.2008.01.002
    title: "Maximilian Bisani and Hermann Ney, Joint-sequence models for grapheme-to-phoneme conversion, Speech Communication 50(5), 2008, pages 434 to 451"
    locator: "the introduction and the overview of earlier approaches, and the section on evaluation measures"
  - book: isbn:9780521899277
    title: "Paul Taylor, Text-to-Speech Synthesis, Cambridge University Press, 2009"
    locator: "Chapter 8 (Pronunciation), with the lexicon and the letter-to-sound methods"
  - url: https://web.stanford.edu/~jurafsky/slp3/
    title: "Daniel Jurafsky and James H. Martin, Speech and Language Processing, 3rd edition draft, August 24, 2025"
    locator: "the chapter Text-to-Speech"
---

Grapheme-to-phoneme conversion (G2P) maps the spelling of a word, a string of letters (graphemes), to its pronunciation, a string of phonemes. It is a step of the front end of [text-to-speech](/text-to-speech/), after [text normalization](/tts-text-normalization/), and it also builds the lexicons of [automatic speech recognition](/automatic-speech-recognition/). Systems first look a word up in a [pronunciation lexicon](/pronunciation-lexicon/). G2P is needed for the words that are not there: new names, places, brands, loan words and new coinages, which no fixed lexicon can list. The problem is hard in languages such as English, where the same letters are read in different ways ("ough" in "though", "through", "tough" and "cough") and the lengths of the two strings differ ("phone" has five letters and three phonemes). The classic solutions are hand-written rules and [decision trees](/decision-tree/); the main statistical one is the [joint-sequence model](/joint-sequence-g2p/); current systems use neural sequence models.

## In plain words

When a reading machine meets a word, it must know how to say it. For common words it can look in a dictionary that lists the sounds of each word. But new names and new words appear all the time, and no dictionary has them all.

So the machine needs a way to guess the sounds from the letters. This is easy in some languages, where each letter almost always has one sound. In English it is hard. The same letters can sound different in different words, two letters can make one sound, and some letters make no sound at all.

Good systems learn the patterns from a large dictionary. They then use those patterns to guess words they have never seen. A few words, such as "read" or "lead", have two pronunciations, and only the sentence shows which one is right.

## Definition

**Input.** A word $g = g_1 \cdots g_n$ over an alphabet of graphemes, sometimes with its context in a sentence or its part of speech.

**Output.** A pronunciation $\varphi = \varphi_1 \cdots \varphi_m$ over a phoneme set, such as ARPAbet for American English, often with stress marks and syllable boundaries. The lengths $n$ and $m$ need not be equal.

**Learning setting.** The training data is a lexicon, a list of pairs $(g, \varphi)$, with no alignment between letters and phonemes. The model is judged on held-out words, which models the words that a system meets but that are not in its lexicon.

**Evaluation.** Two measures are standard, as in Bisani and Ney (2008):

- **Phoneme error rate (PER):** the [edit distance](/edit-distance/) between the output and the reference pronunciation, summed over the test words and divided by the total number of reference phonemes.
- **Word error rate (WER):** the fraction of test words whose output is not exactly correct. This is a different measure from the [word error rate](/word-error-rate/) of speech recognition, which counts edits over words in a sentence.

If a word has more than one correct pronunciation in the lexicon, the usual rule is to count the output as correct if it matches any of them.

## Variants

- **Isolated words or words in context.** Out of context, a homograph such as "read" (/r iy d/ or /r eh d/) cannot be resolved. In context, the tense, the part of speech or the meaning decides, so G2P for running text needs [part-of-speech tagging](/part-of-speech-tagging/) or [word sense disambiguation](/word-sense-disambiguation/).
- **Phoneme to grapheme.** The inverse map, from sounds to spelling, used for spelling correction and in some speech recognizers.
- **Many languages.** One model for many languages, or a model for a language with very little data.
- **Names.** Proper names follow the rules of their language of origin, so a model may first guess the origin, a form of [language identification](/language-identification/).
- **Stress and syllables.** Predict lexical stress and syllable boundaries with the phonemes; in English, a wrong stress can make a word hard to recognize.

## Examples

- **Different lengths.** "phone" is F OW N in ARPAbet. One alignment pairs "ph" with F, "o" with OW, "n" with N, and the final "e" with nothing. The letters "ph" form one sound and the "e" has no sound, so a model must allow units of more than one letter and units with no phoneme.
- **Scoring.** Suppose a system outputs F AA N for "phone". The edit distance to F OW N is 1 (one substitution), so the PER for this word is $1/3 \approx 33\%$ and the word is wrong. If the system also outputs K AE T for "cat" (correct), the totals are 1 error over 6 reference phonemes, a PER of $1/6 \approx 17\%$, and 1 wrong word out of 2, a WER of 50%.
- **Same letters, different sounds.** "though" (DH OW), "through" (TH R UW), "tough" (T AH F) and "cough" (K AO F) show four readings of "ough". No rule on those four letters alone can be right for all of them; the model must use the letters around them, and even then some words are exceptions.

## Known algorithms

- **Hand-written rules.** Ordered rules that rewrite a letter in a context of letters. Good for languages with regular spelling; for English they need many rules and many exceptions.
- **[Decision trees](/decision-tree/).** First align letters to phonemes (with a null phoneme where a letter is silent), then train one classifier for each letter that predicts its phoneme from a window of letters around it.
- **[Joint-sequence models](/joint-sequence-g2p/).** Bisani and Ney (2008) model the pair as a sequence of graphones, units that join a few letters with a few phonemes, with an [n-gram model](/n-gram-language-model/) over the graphones. Training uses [expectation maximization](/expectation-maximization/) over all segmentations, and decoding finds the best pronunciation.
- **Weighted finite-state transducers.** A joint n-gram model compiled into a [finite-state transducer](/finite-state-transducer/), so that G2P becomes composition and a best path search.
- **Neural sequence models.** An [encoder-decoder model](/encoder-decoder-model/) with attention, or a [transformer](/transformer/), reads the letters and writes the phonemes, usually with [beam search](/beam-search/).

## Bounds

- **Homographs.** For a word with two correct pronunciations that depend on context, any method that sees only the word is wrong on one of the two uses. So on running text, G2P from the word alone has an error rate at least as large as the share of the less common reading of each homograph (a theorem about any function of the word alone).
- **Lexicon noise.** The reference lexicons have errors and inconsistent choices, so a test score near zero is not possible on real lexicons (an observation).
- **Time.** Lookup in a lexicon stored as a trie takes time linear in the length of the word. For a joint-sequence model with graphones of at most $L$ letters and a fixed n-gram order, decoding with a pruned search is about linear in $n$; exact search over all phoneme strings is harder, and practical decoders use a beam.

## Reductions

- **To alignment.** Many methods first align letters to phonemes, with null symbols or multi-letter units, as an [edit distance](/edit-distance/) style alignment.
- **To classification.** After a one-to-one alignment, G2P is the prediction of one phoneme (or null) for each letter, a [sequence labeling](/sequence-labeling/) problem.
- **To transduction.** With joint-sequence models compiled to transducers, G2P is composition with a [weighted automaton](/weighted-automaton/) and a best path search.
- **To translation.** A neural model treats G2P as translation from one alphabet to another.
- **From [text-to-speech](/text-to-speech/).** The front end of TTS uses lexicon lookup, then G2P for the words that are missing.

## Applications

Front ends of text-to-speech systems; building and extending pronunciation lexicons for speech recognition, so that new words can be recognized; pronunciation aids in language learning; search by sound, such as finding a name that a user spoke; and transliteration between writing systems.
