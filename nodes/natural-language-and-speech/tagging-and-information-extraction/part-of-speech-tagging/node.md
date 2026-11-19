---
tag: GPAJQS
kind: problem
slug: part-of-speech-tagging
name: Part-of-speech tagging
aliases:
- POS tagging
- word-category disambiguation
area: natural-language-and-speech/tagging-and-information-extraction
level: intro
summary: "Label each word of a sentence with its part of speech, such as noun, verb or adjective, resolving ambiguity from context."
prereqs: [sequence-labeling]
see_also: [universal-pos-tagset, hmm-part-of-speech-tagger, brill-tagger, structured-perceptron, maximum-entropy-markov-model, bayesian-hmm-tagging, out-of-vocabulary-word, treebank]
sources:
  - paper: "Thorsten Brants, TnT: a statistical part-of-speech tagger, Proceedings of the Sixth Conference on Applied Natural Language Processing (ANLP 2000), pages 224 to 231"
    title: Brants 2000
    locator: "Tables 2 and 5 (accuracy on known and unknown words on NEGRA and the Penn Treebank)"
  - paper: "Eric Brill, Transformation-based error-driven learning and natural language processing: a case study in part-of-speech tagging, Computational Linguistics 21(4), 1995, pages 543 to 565"
    title: Brill 1995
    locator: "Section 4 (tagging as a learning task; the lexicon of a word lists the tags it had in training, such as the seven tags of half), Section 4.3 (the accuracy of the initial annotator and of the full tagger on unknown words)"
  - paper: "Slav Petrov, Dipanjan Das and Ryan McDonald, A universal part-of-speech tagset, Proceedings of LREC 2012, pages 2089 to 2096"
    title: "Petrov, Das and McDonald 2012"
    locator: the twelve universal tags and the mappings from 25 treebank tagsets for 22 languages
  - book: isbn:9780262133609
    title: "Christopher D. Manning and Hinrich Schütze, Foundations of Statistical Natural Language Processing, MIT Press, 1999"
    locator: Chapter 10 (part-of-speech tagging)
---

Part-of-speech tagging labels each word of a sentence with its word class, such as noun, verb, adjective or determiner, from a fixed tagset. Many frequent words have more than one possible tag, so the task is to choose the right one from the context: "book" is a noun in "the book" and a verb in "book a flight". It is the classic instance of [sequence labeling](/sequence-labeling/), and it is usually the first step before parsing, chunking and entity recognition. The tagset itself is a separate choice; the [universal POS tagset](/universal-pos-tagset/) is one shared across languages.

## In plain words

Every word gets a label that says what kind of word it is: a noun names a thing, a verb names an action, and so on. Most word types have only one possible label, but the words that appear most often in text often have several, and an unknown word can have any label. The tagger must look at the neighbours: after "the" a noun or adjective is likely, after "to" a verb. A good tagger gets about 97 words out of 100 right on newspaper English, but even the simple rule "give each word its most common label" gets more than 90 right.

## Definition

**Input.** A sentence $x_1 \ldots x_n$ of tokens, already split into words, and a tagset $Y$ with $k$ tags. A tagged training corpus is usually available.

**Output.** A tag $y_i \in Y$ for each token, so that the tags agree with the annotation guidelines of the tagset.

**Score.** Token accuracy: the fraction of tokens whose tag equals the gold tag. It is often reported separately for known words (seen in training) and unknown words.

**Ambiguity.** For each word $w$, the lexicon is the set of tags that $w$ had in training. Brill (1995, Section 4.1) shows the entry of "half" in the Penn Treebank with seven tags. Tagging is easy for words with one tag in the lexicon, and the hard cases are the frequent ambiguous words and the unknown words.

## Variants

- Tagsets. The Penn Treebank tagset for English has about 45 tags, with tags for verb forms such as VBD (past tense) and VBZ (third person singular present). Coarse tagsets such as the 12 tags of Petrov, Das and McDonald (2012) and the 17 universal tags of Universal Dependencies are used across languages; see the [universal POS tagset](/universal-pos-tagset/).
- Morphological tagging. In languages with rich inflection, each tag also holds features such as case, number and gender, so the tagset has hundreds or thousands of tags.
- Closed and open vocabulary. Tests that put the test words into the lexicon (closed vocabulary) give higher numbers than tests with real unknown words.
- Unsupervised tagging. With no tagged data, the task is to induce word classes, and the result is scored by mapping the classes to gold tags; see [Bayesian HMM tagging](/bayesian-hmm-tagging/).
- Joint tasks. Tagging can be done together with [word segmentation](/word-segmentation/), [morphological analysis](/morphological-analysis/) or parsing.

## Examples

- "Time flies like an arrow": the usual reading is Time/N flies/V like/P an/D arrow/N, but "flies" can be a noun and "like" a verb (Time/N flies/N like/V ...), as in "fruit flies like a banana". A tagger picks one reading from the statistics of the context.
- "can": "I can swim" (modal), "a can of beans" (noun), "they can fish" (verb, to put into cans). Brill's example "The/determiner can/modal rusted/verb" has the wrong tag modal for "can", which the rule "change modal to noun if the previous word is a determiner" fixes (Brill 1995, Section 2).
- "that" can be a determiner, a pronoun, a complementizer or a relative pronoun, and the Penn Treebank tags these uses differently.

## Known algorithms

- Most frequent tag: give each word its most frequent training tag and unknown words a default. Brill reports 92.4% for this initial state on the Penn Treebank Wall Street Journal corpus with real unknown words (Section 4.3); the exact number depends on the lexicon.
- [HMM taggers](/hmm-part-of-speech-tagger/): a bigram or trigram model of tags with word emissions, decoded by Viterbi. TnT reports 96.7% on the Penn Treebank (Brants 2000, Table 5).
- [Brill tagger](/brill-tagger/): an ordered list of learned rewrite rules. Brill reports 96.6% with unknown words (Section 4.3).
- Discriminative models with rich word features: the [maximum entropy Markov model](/maximum-entropy-markov-model/), the [structured perceptron](/structured-perceptron/) (2.89% error in Collins 2002), and the [conditional random field](/conditional-random-field/).
- Neural taggers: a [BiLSTM-CRF](/bilstm-crf/) or a token classifier on a pretrained encoder such as [BERT](/bert/).
- Unsupervised: [Bayesian HMM tagging](/bayesian-hmm-tagging/) and the [Baum-Welch algorithm](/baum-welch-algorithm/) with a tag dictionary.

## Bounds

- Decoding a first-order tagger with $k$ tags takes $O(n k^2)$ time with the [Viterbi algorithm](/viterbi-algorithm/), and a second-order tagger $O(n k^3)$. Restricting each known word to the tags of its lexicon entry makes this much smaller in practice.
- Accuracy is measured, not proved. On the Wall Street Journal part of the Penn Treebank, the methods above range from about 96.5% to a little over 97% in the papers cited here. The remaining errors include errors and inconsistencies of the gold annotation, so 100% is not a realistic target.
- Unknown words are much harder: TnT reports 85.5% on unknown words against 97.0% on known words (Brants 2000, Table 5), and Brill 82.2% on unknown words (Section 4.3).

## Reductions

- POS tagging is [sequence labeling](/sequence-labeling/) with one tag per token and the tagset as label set.
- Unknown-word tagging reduces to classification of the word form by its suffixes, prefixes, capitalization and digits, as in the suffix model of TnT and the unknown-word rules of Brill; see [out-of-vocabulary word](/out-of-vocabulary-word/).
- Mapping fine tags to coarse tags is a function on the tagset, so a fine tagger also gives a coarse tagger, as in the mappings of Petrov, Das and McDonald (2012).

## Applications

Tags are features for parsing ([constituency parsing](/constituency-parsing/) and [dependency parsing](/dependency-parsing/)), [text chunking](/text-chunking/), [named entity recognition](/named-entity-recognition/) and [lemmatization](/lemmatization/). They are used in text-to-speech to choose the pronunciation of words such as "record" (noun or verb), in information retrieval to find noun phrases, and in corpus linguistics to search for grammatical patterns.

## References
