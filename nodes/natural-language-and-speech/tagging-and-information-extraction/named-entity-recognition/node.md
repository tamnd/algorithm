---
tag: 37YW7A
kind: problem
slug: named-entity-recognition
name: Named entity recognition
aliases:
- NER
- entity extraction
area: natural-language-and-speech/tagging-and-information-extraction
level: core
summary: "Find the spans of a text that name entities such as persons, organizations and places, and label each span with its type."
prereqs: [sequence-labeling, bio-encoding]
see_also: [span-f1-score, entity-linking, relation-extraction, coreference-resolution, text-chunking, bilstm-crf, semi-markov-crf, bert]
sources:
  - paper: "Ralph Grishman and Beth Sundheim, Message Understanding Conference-6: a brief history, Proceedings of COLING 1996"
    title: Grishman and Sundheim 1996
    locator: the named entity task of MUC-6 and its entity, time and number types
  - paper: "Erik F. Tjong Kim Sang and Fien De Meulder, Introduction to the CoNLL-2003 shared task: language-independent named entity recognition, Proceedings of CoNLL-2003, pages 142 to 147"
    title: Tjong Kim Sang and De Meulder 2003
    locator: the four entity types, the English and German data, the exact-match evaluation and the results of the participating systems
  - paper: doi:10.18653/v1/N16-1030
    title: "Guillaume Lample, Miguel Ballesteros, Sandeep Subramanian, Kazuya Kawakami and Chris Dyer, Neural architectures for named entity recognition, NAACL 2016"
    locator: the LSTM-CRF model with character-based word representations and its CoNLL-2003 results
  - paper: doi:10.18653/v1/N19-1423
    title: "Jacob Devlin, Ming-Wei Chang, Kenton Lee and Kristina Toutanova, BERT: pre-training of deep bidirectional transformers for language understanding, NAACL 2019"
    locator: the CoNLL-2003 named entity experiment
---

Named entity recognition (NER) finds the names in a text and says what each one names: a person, an organization, a place, or another type from a fixed list. It is the first step of most information extraction: [relation extraction](/relation-extraction/) needs the entities whose relations it finds, [entity linking](/entity-linking/) needs the mentions it links, and [coreference resolution](/coreference-resolution/) often starts from them. The task took its present form in the Message Understanding Conferences of the 1990s and in the CoNLL-2002 and CoNLL-2003 shared tasks. Since the names form flat spans, it is usually solved as [sequence labeling](/sequence-labeling/) with [BIO encoding](/bio-encoding/), and it is scored with the [span F1 score](/span-f1-score/).

## In plain words

Read a sentence such as "Ekeus met officials of the U.N. in Baghdad" and mark the names: "Ekeus" is a person, "U.N." is an organization and "Baghdad" is a place. A name can be several words long, such as "New York Stock Exchange", and then the whole group must be marked, not only part of it. The same word can be a different type in different places: "Washington" can be a person, a city or the government. A system decides from the word itself, its shape (capital letters, digits), and the words around it. It is right about a name only if it marks exactly the right words and gives the right type.

## Definition

**Input.** A sentence of tokens $x_1, \ldots, x_n$ and a set $T$ of entity types.

**Output.** A set of typed spans $(i, j, t)$ with $0 \le i < j \le n$ and $t \in T$. The span $(i, j)$ uses fencepost indices: it covers the tokens $i + 1, \ldots, j$. In the standard (flat) task, no two spans share a token.

**Types.** The CoNLL-2003 task uses four types: PER (persons), ORG (organizations), LOC (locations) and MISC (other names, such as nationalities and events). The MUC-6 task marked names of persons, organizations and locations, and also times, dates, money and percentages (Grishman and Sundheim 1996). Larger type sets exist, and domain tasks use their own, such as genes and proteins in biomedical text.

**Score.** Exact-match [span F1](/span-f1-score/): a predicted entity counts only if both its boundaries and its type are right, with precision and recall summed over the whole test set (Tjong Kim Sang and De Meulder 2003).

## Variants

- Flat NER: the spans do not overlap. This is the CoNLL form, and it reduces to tagging.
- Nested NER: entities can contain entities, as in "[[University of [California]] Press]". Nested data sets exist for news and for biomedical text. Tagging with one tag per token cannot express nesting.
- Discontinuous entities: in "left and right ventricle", "left ventricle" is an entity whose words are not adjacent. Some medical data sets mark them.
- Fine-grained typing: types from a large hierarchy, such as "politician" below "person".
- Cross-lingual and low-resource NER: train on one language, or on few labeled sentences, and tag another.
- Entity typing given the spans: classify each given mention into a type. It is a classification problem, not span finding.

## Examples

The CoNLL-2003 style sentence "U.N. official Ekeus heads for Baghdad ." has the entities $(0, 1, \mathrm{ORG})$ for "U.N.", $(2, 3, \mathrm{PER})$ for "Ekeus" and $(5, 6, \mathrm{LOC})$ for "Baghdad". In IOB2 tags: U.N./B-ORG official/O Ekeus/B-PER heads/O for/O Baghdad/B-LOC ./O.

Ambiguity of type: in "Jordan scored 40 points" Jordan is a person, in "Jordan signed the treaty" a country, and a system must decide from the context.

Ambiguity of boundaries: in "Bank of America Corp. said", the organization is "Bank of America Corp.", and a system that marks only "America" as a location makes one false positive and one false negative.

## Known algorithms

- Rules and gazetteers: hand-written patterns over capital letters, titles ("Mr.") and lists of known names. These were common in the MUC systems.
- Generative taggers: [hidden Markov models](/hidden-markov-model/) over BIO tags, decoded by the [Viterbi algorithm](/viterbi-algorithm/).
- Discriminative taggers: the [maximum entropy Markov model](/maximum-entropy-markov-model/), the [structured perceptron](/structured-perceptron/) and the [conditional random field](/conditional-random-field/), with features such as word shape, prefixes and suffixes, and gazetteer matches. Most CoNLL-2003 systems were of this kind; the best English test F1 was 88.76 (a measurement, Tjong Kim Sang and De Meulder 2003).
- Neural taggers: the [BiLSTM-CRF](/bilstm-crf/) of Lample et al. (2016) reached 90.94 F1 on the English CoNLL-2003 test set without gazetteers (a measurement).
- Pretrained encoders: fine-tune [BERT](/bert/) or another [transformer](/transformer/) encoder with a tag classifier on each token. Devlin et al. (2019) report 92.8 test F1 on English CoNLL-2003 for BERT-large (a measurement).
- Span models: score every span up to a length $L$ and pick a set of non-overlapping spans, as in the [semi-Markov CRF](/semi-markov-crf/); span classifiers can also handle nested entities.

## Bounds

- With $k = 2|T| + 1$ BIO tags, Viterbi decoding of a first-order tagger takes $O(n k^2) = O(n |T|^2)$ time and $O(n k)$ space (a theorem). Forbidden transitions such as O followed by I-X get score $-\infty$, so the output is always a valid span set.
- A semi-Markov model with spans of length at most $L$ decodes in $O(n L |T|^2)$ time (a theorem, see [semi-Markov CRF](/semi-markov-crf/)).
- Classifying each token independently takes $O(n k)$ after the encoder, but can give invalid tag sequences, which the span reader of the [span F1 score](/span-f1-score/) still turns into spans.
- Any system must read each token, so $\Omega(n)$ time is needed.

## Reductions

- Flat NER to sequence labeling: [BIO encoding](/bio-encoding/) is a bijection between span sets and valid tag sequences, so any tagger solves NER, and the spans are read back exactly.
- Flat NER to weighted interval selection: if each span has a score and the scores add, the best set of non-overlapping spans is a [weighted interval scheduling](/weighted-interval-scheduling/) problem, solved by dynamic programming.
- Nested NER to span classification: enumerate all $O(n L)$ spans and classify each as an entity type or none.
- NER is a part of [entity linking](/entity-linking/) and [relation extraction](/relation-extraction/): end-to-end systems for those tasks solve NER on the way.

## Applications

- Information extraction: entities are the slots of events and relations.
- Search and question answering: index documents by the entities they mention.
- Anonymization: find and remove names of persons in medical or legal records.
- Knowledge base building: with [entity linking](/entity-linking/), map mentions to entries and add new facts.

## References
