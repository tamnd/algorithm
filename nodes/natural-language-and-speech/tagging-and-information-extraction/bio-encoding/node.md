---
tag: ANKPZQ
kind: definition
slug: bio-encoding
name: BIO encoding
aliases:
- IOB tagging
- BIOES encoding
area: natural-language-and-speech/tagging-and-information-extraction
level: intro
summary: "Encode spans as token tags B for the first token, I for the next ones and O outside, so span finding becomes sequence labeling."
prereqs: [sequence-labeling]
see_also: [text-chunking, named-entity-recognition, semi-markov-crf, bilstm-crf, conditional-random-field, brill-tagger, structured-perceptron, part-of-speech-tagging]
sources:
  - paper: "Lance A. Ramshaw and Mitchell P. Marcus, Text chunking using transformation-based learning, Proceedings of the Third Workshop on Very Large Corpora, 1995, pages 82 to 94"
    title: Ramshaw and Marcus 1995
    locator: "Section 4.1 (the chunk tags I, O and B, with B only on the first word of a baseNP that directly follows another baseNP, and the local repair of a B after an O), the abstract (about 92% recall and precision for baseNP chunks)"
  - paper: "Erik F. Tjong Kim Sang and Jorn Veenstra, Representing text chunks, Proceedings of the Ninth Conference of the European Chapter of the Association for Computational Linguistics (EACL 1999), pages 173 to 179"
    title: Tjong Kim Sang and Veenstra 1999
    locator: "Section 2.1 and Table 1 (the formats IOB1, IOB2, IOE1, IOE2, IO and the bracket formats, on one example sentence), Table 2 (the results of each format)"
  - paper: "Erik F. Tjong Kim Sang and Sabine Buchholz, Introduction to the CoNLL-2000 shared task: chunking, Proceedings of CoNLL-2000 and LLL-2000, pages 127 to 132"
    title: Tjong Kim Sang and Buchholz 2000
    locator: "page 130 (the chunk tags of the shared task, and the rule that an I-X tag after O or after a tag of another type starts a new chunk)"
---

BIO encoding turns a set of labeled, non-overlapping spans of a sentence into one tag per token: B-X on the first token of a span with label X, I-X on the other tokens of the span, and O on the tokens outside every span. With it, finding spans such as noun phrase chunks or named entities becomes [sequence labeling](/sequence-labeling/), and any tagger can do it. This page defines the encoding, its variants IOB1, IOB2 and BIOES, which tag sequences are valid, and how to repair invalid ones. The tasks that use it are on the pages for [text chunking](/text-chunking/) and [named entity recognition](/named-entity-recognition/). A [semi-Markov CRF](/semi-markov-crf/) works on the spans directly and does not need the encoding.

## Definition

Spans. A sentence has tokens $1, \ldots, n$. A span is a triple $(i, j, X)$ with $0 \le i < j \le n$ and a label $X$ from a set of $L$ labels. It uses fencepost indices: $(i, j, X)$ covers the tokens $i + 1, \ldots, j$. A span set is a set of spans that do not overlap. Spans may touch: $(0, 2, X)$ and $(2, 3, X)$ are two spans, not one.

IOB2 (also called BIO). The tag of token $p$ is B-X if $p$ is the first token of a span with label $X$, I-X if $p$ is another token of such a span, and O if no span covers $p$. A tag sequence is valid when every I-X directly follows a B-X or an I-X.

IOB1. Ramshaw and Marcus (1995, Section 4.1) introduced chunk tags with I on every token inside a chunk, O outside, and B only to mark the first token of a chunk that directly follows another chunk. With labels, the tag is B-X on the first token of a span with label $X$ that starts right where another span with label $X$ ends, and I-X on every other covered token. A sequence is valid when every B-X directly follows a B-X or an I-X. Tjong Kim Sang and Veenstra (1999) gave the names IOB1 and IOB2, and also defined IOE1 and IOE2, which mark the last token of a span with E instead of the first token with B.

BIOES (also written IOBES, or BILOU with L for last and U for unit). S-X marks a span of one token. A longer span gets B-X on its first token, E-X on its last and I-X in between. A sequence is valid when the tags of each span appear in the order B I ... I E or as one S, with the same label, and O appears only outside spans.

The encoding and the decoding are both one pass from left to right:

```pseudo id=main
ENCODE(spans, n, scheme)
L1  tags ← O at every position
L2  for each span (i, j, X) in order of i do
L3      tags[i+1 .. j] ← I-X
L4      IOB2: tags[i+1] ← B-X
L5      IOB1: if the previous span ends at i and has label X then tags[i+1] ← B-X
L6      BIOES: if j = i+1 then tags[j] ← S-X else tags[i+1] ← B-X; tags[j] ← E-X
L7  return tags
REPAIR(tags)                                        ▷ any sequence of O, B-X, I-X becomes valid IOB2
L8  for p ← 1 to n do
L9      if tags[p] = I-X and (p = 1 or tags[p-1] = O or the label of tags[p-1] is not X) then
L10         tags[p] ← B-X                           ▷ the CoNLL-2000 rule: this I-X starts a chunk
L11 return tags
```

Bijection (a theorem). For each scheme, ENCODE is a bijection from the span sets on $n$ tokens to the valid tag sequences of length $n$, and the decoder is its inverse. In IOB2, a span starts exactly at a B tag and continues over the I tags that follow it with the same label, so the spans can be read back, and a valid sequence has a span at each B. IOB1 keeps the boundaries because B appears exactly where two spans with the same label touch; at any other start of a span the change from O or from another label shows the boundary. BIOES marks both ends. The number of span sets satisfies $a_0 = 1$, $a_1 = L + 1$ and $a_n = (L + 2) a_{n-1} - a_{n-2}$: either token $n$ is outside every span ($a_{n-1}$ ways), or it ends a span that starts at one of the $n$ positions with one of $L$ labels, which gives $a_n = a_{n-1} + L (a_0 + \cdots + a_{n-1})$, and the difference of two such lines gives the recurrence. For $L = 1$ the numbers 1, 2, 5, 13, 34, 89 are every other Fibonacci number. The test file checks the bijection and these counts by enumerating all tag sequences for $n \le 4$ with two labels, and the round trip for $n \le 5$.

Repair. A tagger that predicts each tag alone can output an invalid IOB2 sequence, such as O I-X. The CoNLL-2000 evaluation reads an I-X that follows O, the sentence start, or a tag with another label as the start of a new chunk (Tjong Kim Sang and Buchholz 2000, page 130). REPAIR rewrites such an I-X as B-X. The result is always valid, a valid sequence does not change, and the only changes are I-X to B-X. Ramshaw and Marcus used the same kind of local repair for their tags: a B right after an O is read as an I (Section 4.1).

## Examples and non-examples

The CoNLL-2000 style sentence "He reckons the current account deficit" has the spans $(0, 1, \mathrm{NP})$, $(1, 2, \mathrm{VP})$ and $(2, 6, \mathrm{NP})$:

| token | He | reckons | the | current | account | deficit |
|---|---|---|---|---|---|---|
| IOB2 | B-NP | B-VP | B-NP | I-NP | I-NP | I-NP |
| IOB1 | I-NP | I-VP | I-NP | I-NP | I-NP | I-NP |
| BIOES | S-NP | S-VP | B-NP | I-NP | I-NP | E-NP |

Touching spans with the same label, $(0, 2, \mathrm{NP})$ and $(2, 3, \mathrm{NP})$ on four tokens, give B-NP I-NP B-NP O in IOB2, I-NP I-NP B-NP O in IOB1, and B-NP E-NP S-NP O in BIOES. Without the B, the plain I-NP I-NP I-NP O would read as one span of three tokens: this is why the B tag exists.

Non-examples:

- O I-X is not valid IOB2, since I-X does not follow a tag with label X. It is valid IOB1. Repair turns it into O B-X.
- B-X I-Y is not valid IOB2. Repair gives B-X B-Y: two spans of one token.
- O B-X is not valid IOB1, because IOB1 uses B only right after a span with the same label.
- B-X alone and B-X O are not valid BIOES, since the span has no E-X.
- Nested or overlapping spans, such as an entity inside another entity, cannot be encoded at all: each token gets one tag. Use a different method for nested spans.

## Related definitions

- [Sequence labeling](/sequence-labeling/): the general problem that the encoding reduces span finding to.
- [Text chunking](/text-chunking/) and [named entity recognition](/named-entity-recognition/): the two main tasks that use BIO tags.
- Constrained decoding: a first-order tagger such as a [conditional random field](/conditional-random-field/) or the [BiLSTM-CRF](/bilstm-crf/) can forbid the invalid transitions (O to I-X, and B-X or I-X to I-Y with $Y \ne X$) by giving them a score of $-\infty$, so the [Viterbi algorithm](/viterbi-algorithm/) returns only valid sequences.
- Choice of scheme (a measurement): Tjong Kim Sang and Veenstra (1999, Table 2) found that the choice among IOB1, IOB2, IOE1 and IOE2 changed the F score of their noun phrase chunker by less than one point (88.67 to 89.17 in their first series). BIOES makes both ends of each span explicit, at the cost of twice as many tags per label.
- [Semi-Markov CRF](/semi-markov-crf/): labels whole spans and needs no token tags.

## References
