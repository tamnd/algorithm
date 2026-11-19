---
tag: E5FZ0M
kind: problem
slug: text-chunking
name: Text chunking
aliases:
- shallow parsing
area: natural-language-and-speech/tagging-and-information-extraction
level: core
summary: "Split a sentence into non-overlapping, non-nested phrases such as noun and verb groups, usually as BIO sequence labeling."
prereqs: [sequence-labeling, bio-encoding, part-of-speech-tagging]
see_also: [named-entity-recognition, constituency-parsing, semi-markov-crf, brill-tagger, structured-perceptron, conditional-random-field, weighted-interval-scheduling, precision-and-recall]
sources:
  - paper: "Erik F. Tjong Kim Sang and Sabine Buchholz, Introduction to the CoNLL-2000 shared task: chunking, Proceedings of CoNLL-2000 and LLL-2000, pages 127 to 132"
    title: Tjong Kim Sang and Buchholz 2000
    locator: "Section 2 (task and example sentence), Section 3 (the chunk types), Section 4 and Table 1 (data, B-X, I-X and O tags, the repair of I-X after O, precision, recall and F), Table 2 (results)"
  - paper: "Steven P. Abney, Parsing by chunks, in Robert C. Berwick, Steven P. Abney and Carol Tenny (editors), Principle-Based Parsing, Kluwer, 1991, pages 257 to 278"
    url: "https://doi.org/10.1007/978-94-011-3474-3_10"
    title: Abney 1991
    locator: "chunks as the first stage of a parser, and their relation to full constituents"
  - paper: "Lance A. Ramshaw and Mitchell P. Marcus, Text chunking using transformation-based learning, Proceedings of the Third Workshop on Very Large Corpora, 1995, pages 82 to 94"
    title: Ramshaw and Marcus 1995
    locator: "Section 4.1 (chunking as tagging with I, O and B tags), the abstract (about 92% recall and precision for baseNP chunks, about 88% for partitioning chunks)"
  - paper: "Michael Collins, Discriminative training methods for hidden Markov models: theory and experiments with perceptron algorithms, Proceedings of EMNLP 2002, pages 1 to 8"
    title: Collins 2002
    locator: "Section 4.1 (NP chunking as tagging with B, I and O), Section 4.3 (test F 93.63 for the perceptron and 93.29 for the maximum entropy tagger)"
---

Text chunking splits a sentence into flat, non-overlapping phrases, called chunks, and gives each one a type such as NP (noun phrase) or VP (verb group). A chunk holds the head of a phrase and the words before it, but no phrases inside it, so chunks never nest. Compared with [constituency parsing](/constituency-parsing/), which builds a full tree, chunking finds only the lowest layer, and it is much faster and more robust. Compared with [named entity recognition](/named-entity-recognition/), which finds spans of the same flat form, chunking marks syntactic phrases, not names. Both are usually solved as [sequence labeling](/sequence-labeling/) with [BIO encoding](/bio-encoding/).

## In plain words

Draw brackets around the small phrases of a sentence: "[the current account deficit] [will narrow] [to] [only 1.8 billion]". Each bracket gets a label, such as noun phrase or verb group. Brackets never go inside each other, and some words, such as most punctuation, are outside all brackets. A chunk stops at the main word of its phrase, so a noun phrase does not include the prepositional phrase after it. To solve it with a tagger, put a tag on each word: "begin a noun phrase", "inside a noun phrase", or "outside". Then the brackets can be read back from the tags.

## Definition

**Input.** A sentence $x_1 \ldots x_n$ of tokens, usually with their part-of-speech tags, and a set $C$ of chunk types.

**Output.** A set of labeled spans $(i, j, c)$ with $0 \le i < j \le n$ and $c \in C$, where the span $(i, j)$ covers tokens $i + 1$ to $j$, and no two spans share a token. Tokens covered by no span are outside.

**What a chunk is.** In the CoNLL-2000 data, a chunk contains everything to the left of and including the syntactic head of the constituent of the same name, with premodifiers but without postmodifiers or arguments (Tjong Kim Sang and Buchholz 2000, Section 3). So a PP chunk is usually only the preposition, and the NP after it is a chunk of its own.

**Score.** Chunk precision $P$ (the fraction of predicted chunks that are right), chunk recall $R$ (the fraction of gold chunks that were found), and $F_{\beta=1} = 2 P R / (P + R)$. A chunk is right only if both of its ends and its type are right ([precision and recall](/precision-and-recall/)). Tag accuracy is not used, since one wrong tag can break two chunks.

## Variants

- NP chunking (base noun phrases): one chunk type, the non-recursive noun phrases. This is the task of Ramshaw and Marcus (1995), and it is the most studied form.
- Full chunking: all chunk types. The CoNLL-2000 shared task has 11 types: NP, VP, PP, ADVP, SBAR, ADJP, PRT, CONJP, INTJ, LST and UCP.
- Partitioning chunks: Ramshaw and Marcus (1995) also split the whole sentence into N-type and V-type chunks, a coarser division with two types.
- Chunking with gold or predicted part-of-speech tags. CoNLL-2000 used tags from the Brill tagger, not the Treebank tags, so that the scores are realistic for new text (Section 4).
- Cascades. Abney (1991) uses chunks as the first stage of a parser: a later stage attaches the chunks to each other to give a full parse.

## Examples

The CoNLL-2000 example sentence (Section 2):

[NP He] [VP reckons] [NP the current account deficit] [VP will narrow] [PP to] [NP only £ 1.8 billion] [PP in] [NP September] .

In BIO tags (Section 4): He/B-NP reckons/B-VP the/B-NP current/I-NP account/I-NP deficit/I-NP will/B-VP narrow/I-VP to/B-PP only/B-NP £/I-NP 1.8/I-NP billion/I-NP in/B-PP September/B-NP ./O. The full stop is outside every chunk.

More cases from the CoNLL-2000 guidelines (Section 3):

- A verb group can span words that the Treebank puts into four nested VPs: [NP Mr. Icahn] [VP may not want to sell].
- An adjective phrase inside a noun phrase joins the NP chunk: [NP the most volatile form].
- An adverb phrase that contains an NP gives two chunks: [NP a year] [ADVP earlier].

## Known algorithms

- BIO tagging with any [sequence labeling](/sequence-labeling/) method, with $k = 2|C| + 1$ tags. The tags of a first-order tagger are decoded by the [Viterbi algorithm](/viterbi-algorithm/) and turned back into chunks; see [BIO encoding](/bio-encoding/).
- Transformation-based learning: Ramshaw and Marcus (1995) applied the method of the [Brill tagger](/brill-tagger/) to chunk tags, with about 92% recall and precision for base NPs.
- Classifiers and their combinations in the CoNLL-2000 shared task (Table 2): the best F was 93.48, by Kudoh and Matsumoto with support vector machines, against a baseline of 77.07 that gives each part-of-speech tag its most frequent chunk tag. The single statistical systems, with maximum entropy models, HMMs and memory-based learning, scored between 90.14 and 92.12.
- Discriminative sequence models: the [structured perceptron](/structured-perceptron/) reached F 93.63 on NP chunking in Collins (2002, Section 4.3), against 93.29 for a maximum entropy tagger with the same features. The [conditional random field](/conditional-random-field/) and the [BiLSTM-CRF](/bilstm-crf/) are also used.
- Span models: a [semi-Markov CRF](/semi-markov-crf/) labels whole chunks, so it can use features of the full span.
- Rules and finite-state cascades over part-of-speech tags, as in Abney (1991) and in the rule-based CoNLL-2000 systems.

## Bounds

- With $k = 2|C| + 1$ BIO tags, Viterbi decoding of a first-order model takes $O(n k^2) = O(n |C|^2)$ time and $O(n k)$ space (a theorem). The forbidden pairs such as O followed by I-X get the score $-\infty$, so the output is always a valid chunking.
- A span model with chunks of length at most $L$ is decoded in $O(n L |C|^2)$ time by a segment Viterbi (see [semi-Markov CRF](/semi-markov-crf/)).
- The number of chunkings grows exponentially: with one chunk type there are $a_n$ chunkings of $n$ tokens, where $a_n = 3 a_{n-1} - a_{n-2}$, giving 1, 2, 5, 13, 34, 89 for $n = 0$ to 5 (see [BIO encoding](/bio-encoding/)). So decoding must use dynamic programming, not enumeration.
- Accuracy is measured: F of about 93 to 94 on the CoNLL-2000 test data for the systems of that time (Table 2).

## Reductions

- Chunking to sequence labeling: BIO encoding is a bijection between chunkings and valid tag sequences, so a tagger with a constraint on adjacent tags solves chunking exactly. A tagger without the constraint can produce I-X after O; CoNLL-2000 repairs this by reading such an I-X as the start of a new chunk (Section 4).
- Chunking with span scores and no interaction between chunks to [weighted interval scheduling](/weighted-interval-scheduling/): each candidate span is an interval with a weight, and the best chunking is a set of disjoint intervals of maximum weight, found by [DAG dynamic programming](/dag-dynamic-programming/) over the positions $0, \ldots, n$.
- Parsing to chunking: the chunks of CoNLL-2000 were extracted from the parse trees of the Penn Treebank by a script (Section 3), so any full parser also gives a chunker.

## Applications

Chunks are cheap phrase boundaries for later steps: features for [named entity recognition](/named-entity-recognition/) and [semantic role labeling](/semantic-role-labeling/), candidate arguments for [relation extraction](/relation-extraction/), noun phrases for indexing and term extraction in information retrieval, and the first stage of a cascaded parser. Chunking was also a standard benchmark for sequence models, together with part-of-speech tagging and entity recognition.

## References
