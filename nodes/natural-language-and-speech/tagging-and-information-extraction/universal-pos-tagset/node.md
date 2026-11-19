---
tag: QFGHXN
kind: definition
slug: universal-pos-tagset
name: Universal part-of-speech tagset
aliases:
- universal POS tags
- UPOS
area: natural-language-and-speech/tagging-and-information-extraction
level: core
summary: "A coarse part-of-speech tagset shared across languages: 12 tags in Petrov, Das and McDonald (2012), and 17 UPOS tags in Universal Dependencies, with mappings from treebank tagsets."
prereqs: [part-of-speech-tagging]
see_also: [hmm-part-of-speech-tagger, treebank, dependency-parsing, sequence-labeling, morphological-analysis, lemmatization, brill-tagger, bayesian-hmm-tagging]
sources:
  - paper: "Slav Petrov, Dipanjan Das and Ryan McDonald, A universal part-of-speech tagset, Proceedings of the Eighth International Conference on Language Resources and Evaluation (LREC 2012), pages 2089 to 2096"
    title: "Petrov, Das and McDonald 2012"
    locator: "the twelve universal tags, and the mappings from 25 treebank tagsets for 22 languages"
  - paper: "Joakim Nivre, Marie-Catherine de Marneffe, Filip Ginter, Yoav Goldberg, Jan Hajič, Christopher D. Manning, Ryan McDonald, Slav Petrov, Sampo Pyysalo, Natalia Silveira, Reut Tsarfaty and Daniel Zeman, Universal Dependencies v1: a multilingual treebank collection, Proceedings of LREC 2016, pages 1659 to 1666"
    title: Nivre et al. 2016
    locator: the universal part-of-speech tags (17 tags) and the morphological features of Universal Dependencies version 1
---

A universal part-of-speech tagset is a small set of coarse word classes that can be used for every language, together with a mapping from the detailed tagset of each treebank to it. Petrov, Das and McDonald (2012) proposed 12 tags with mappings for 25 tagsets of 22 languages. Universal Dependencies (Nivre et al. 2016) extended it to 17 tags, the UPOS tags, and moved the finer distinctions into separate morphological features. This page defines the tags and the mapping. The task of choosing the tags is [part-of-speech tagging](/part-of-speech-tagging/); this page is only about the label set.

## Definition

A universal tagset is a set $U$ of coarse tags with a definition of each tag that does not depend on one language. For a language-specific tagset $T$, a mapping is a function $\mu : T \to U$. A treebank tagged with $T$ becomes a treebank tagged with $U$ by replacing each tag $t$ with $\mu(t)$. The mapping must be a function: every fine tag goes to exactly one coarse tag, so it can lose information but never needs context. A tagger trained on $T$ thus also gives tags in $U$.

The 12 tags of Petrov, Das and McDonald (2012) are:

| tag | class |
|---|---|
| NOUN | nouns, with proper nouns |
| VERB | verbs, with auxiliaries and modals |
| ADJ | adjectives |
| ADV | adverbs |
| PRON | pronouns |
| DET | determiners and articles |
| ADP | adpositions (prepositions and postpositions) |
| NUM | numerals |
| CONJ | conjunctions |
| PRT | particles and other function words |
| . | punctuation |
| X | other: foreign words, typos, abbreviations |

The 17 UPOS tags of Universal Dependencies are ADJ, ADP, ADV, AUX, CONJ, DET, INTJ, NOUN, NUM, PART, PRON, PROPN, PUNCT, SCONJ, SYM, VERB and X. Compared with the 12 tags, UPOS splits proper nouns (PROPN) from NOUN, auxiliaries (AUX) from VERB, and subordinating conjunctions (SCONJ) from the other conjunctions, and adds interjections (INTJ) and symbols (SYM). PRT becomes PART, and "." becomes PUNCT. In Universal Dependencies version 2, CONJ was renamed CCONJ, so the count stays 17. Features such as Number, Tense, Case and VerbForm carry the finer distinctions that a tagset such as that of the Penn Treebank puts into the tag itself.

## Examples and non-examples

A part of the mapping from the Penn Treebank tagset to the 12 tags:

| Penn Treebank tags | 12 tags | UPOS |
|---|---|---|
| NN, NNS | NOUN | NOUN |
| NNP, NNPS | NOUN | PROPN |
| VB, VBD, VBG, VBN, VBP, VBZ | VERB | VERB or AUX |
| JJ, JJR, JJS | ADJ | ADJ |
| DT | DET | DET |
| IN | ADP | ADP or SCONJ |
| CD | NUM | NUM |

The table shows why the UPOS column is not a pure function of the Penn tag: a Penn VBZ is AUX in "she is singing" and VERB in "she sings", and IN is ADP in "in the house" and SCONJ in "because it rained". Mapping to UPOS needs the word or the syntax, while mapping to the 12 tags of Petrov et al. needs only the tag.

The sentence "The dog barks ." gets DET NOUN VERB . in the 12 tags and DET NOUN VERB PUNCT in UPOS. "Mary has left" gets NOUN VERB VERB in the 12 tags and PROPN AUX VERB in UPOS.

Non-examples:

- The Penn Treebank tagset itself is not universal: tags such as VBZ and NNS encode English verb and noun forms.
- A set of word clusters, such as the classes found by [Bayesian HMM tagging](/bayesian-hmm-tagging/), is not a tagset in this sense, since its classes have no definition outside the data. Such clusters are scored by mapping them to universal tags.
- A mapping that sends one fine tag to two coarse tags, depending on the word, is not a mapping in the sense above; UPOS conversion from the Penn tags is of that kind for AUX and SCONJ.

## Related definitions

- [Part-of-speech tagging](/part-of-speech-tagging/): the task, for any tagset.
- [Treebank](/treebank/): the annotated corpora that the mappings are defined for.
- Universal Dependencies: the project that uses UPOS together with universal morphological features and universal dependency relations for [dependency parsing](/dependency-parsing/).
- [Morphological analysis](/morphological-analysis/): the features that UPOS moves out of the tag.
- Coarse tags are used to compare taggers across languages, to train taggers for languages without a treebank by projecting tags across parallel text, and to score unsupervised taggers with the many-to-one mapping.

## References
