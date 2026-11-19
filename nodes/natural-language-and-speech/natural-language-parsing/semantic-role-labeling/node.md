---
tag: 45T8RK
kind: problem
slug: semantic-role-labeling
name: Semantic role labeling
aliases:
- SRL
- shallow semantic parsing
area: natural-language-and-speech/natural-language-parsing
level: core
summary: Find the predicates of a sentence and label the spans that fill their roles, such as agent, patient and instrument.
prereqs: [sequence-labeling, constituency-parsing]
see_also: [bio-encoding, span-f1-score, semi-markov-crf, bilstm-crf, weighted-interval-scheduling, binary-integer-programming, abstract-meaning-representation, semantic-parsing]
sources:
  - paper: doi:10.1162/089120102760275983
    title: "Daniel Gildea and Daniel Jurafsky, Automatic labeling of semantic roles, Computational Linguistics 28(3), 245-288, 2002"
    locator: "the task on FrameNet, the features (phrase type, grammatical function, position, voice, head word and parse tree path), and the results for labeling given constituents and for finding and labeling them together"
  - paper: "Martha Palmer, Daniel Gildea and Paul Kingsbury, The Proposition Bank: an annotated corpus of semantic roles, Computational Linguistics 31(1), 71-106, 2005"
    title: "Martha Palmer, Daniel Gildea and Paul Kingsbury, The Proposition Bank"
    locator: "the framesets, the numbered arguments ARG0 to ARG5 and the modifier roles ARGM"
  - paper: doi:10.1162/coli.2008.34.2.257
    title: "Vasin Punyakanok, Dan Roth and Wen-tau Yih, The importance of syntactic parsing and inference in semantic role labeling, Computational Linguistics 34(2), 257-287, 2008"
    locator: "the pruning, identification and classification stages, and the inference with integer linear programming under linguistic and structural constraints"
---

Semantic role labeling (SRL) finds the predicates of a sentence, usually verbs, and for each predicate marks the spans of words that fill its roles, such as who acted, what was acted on, and when and where it happened. The roles stay the same when the syntax changes: in "John broke the window" and "The window broke", the window is the thing broken in both. SRL is called shallow semantic parsing because, unlike [semantic parsing](/semantic-parsing/) into logical forms or [abstract meaning representation](/abstract-meaning-representation/) graphs, it labels spans of the sentence and leaves out quantifiers, entity types and the links between predicates.

## In plain words

Take the sentence "Mary sold the book to John yesterday". The verb is "sold". A selling has a seller, a thing sold and a buyer, and it can have a time. SRL marks "Mary" as the seller, "the book" as the thing sold, "to John" as the buyer, and "yesterday" as the time.

The same roles can appear in different places. In "The book was sold to John by Mary", the seller comes last. A role labeler must see through these changes, which is why it needs more than word order.

A system usually works one verb at a time. For each verb, it decides which groups of words are its arguments and which role each one has.

## Definition

**Input.** A sentence $w = w_1 \cdots w_n$ of $n$ words, often with its part-of-speech tags and a predicted [constituency](/constituency-parsing/) or dependency parse.

**Output.** A set of predicates, each a word position $p$ with a sense such as the PropBank frameset `sell.01`, and for each predicate a set of labeled arguments $(i, j, \ell)$. Spans are fenceposts: $(i, j)$ covers the words $w_{i+1}, \ldots, w_j$. The arguments of one predicate do not overlap, and the label $\ell$ comes from a role inventory of $L$ labels.

**Role inventories.**

- **PropBank** (Palmer, Gildea and Kingsbury 2005) uses numbered core arguments `ARG0` to `ARG5`, whose meaning is defined by each frameset, and shared modifier roles such as `ARGM-TMP` for time, `ARGM-LOC` for place and `ARGM-NEG` for negation. `ARG0` is usually the agent and `ARG1` the patient or theme.
- **FrameNet** groups predicates into frames, such as Commerce_sell, each with its own frame elements, such as Seller, Goods and Buyer.

**Subtasks.** Predicate identification, predicate sense disambiguation, argument identification (which spans are arguments) and argument classification (which role each one has). The usual measure is the [span F1 score](/span-f1-score/) over labeled arguments: an argument is correct if its span and label both match.

## Variants

- **Span-based SRL** labels full argument spans, as in PropBank over constituency trees.
- **Dependency-based SRL** labels only the head word of each argument, so the output is a set of labeled arcs from predicates to words.
- **Given predicates or not.** Many systems take the predicates as given and only label arguments; end-to-end systems also find the predicates.
- **Nominal and other predicates.** Nouns such as "sale" and adjectives also take roles, with their own resources.
- **FrameNet parsing** also chooses the frame of each predicate, from a much larger inventory.

## Examples

With the PropBank frameset `sell.01` (seller `ARG0`, thing sold `ARG1`, buyer `ARG2`), the sentence "Mary sold the book to John yesterday", words 1 to 7, has the arguments

| span | words | label |
|---|---|---|
| $(0, 1)$ | Mary | `ARG0` |
| $(2, 4)$ | the book | `ARG1` |
| $(4, 6)$ | to John | `ARG2` |
| $(6, 7)$ | yesterday | `ARGM-TMP` |

and the predicate "sold" at position 2. In "The book was sold to John by Mary" the labels are the same, though `ARG0` is now the last phrase.

In BIO form for the predicate "sold" the tags are `B-ARG0 B-V B-ARG1 I-ARG1 B-ARG2 I-ARG2 B-ARGM-TMP`, where `V` marks the predicate.

For `break.01`, "John broke the window" has `ARG0` John and `ARG1` the window, while "The window broke" has only `ARG1` the window, in subject position.

## Known algorithms

- **Feature-based classification over a parse.** Gildea and Jurafsky (2002) took the constituents of a parse tree as candidate arguments and labeled them with a probabilistic model over features such as the phrase type, the grammatical function, the position before or after the predicate, the voice, the head word and the path in the tree from the constituent to the predicate. On about 50,000 FrameNet sentences, they labeled given constituents with 82% accuracy, and found and labeled them together with 65% precision and 61% recall (measurement).
- **Pipelines with global inference.** Punyakanok, Roth and Yih (2008) pruned the candidates with syntactic rules, classified them, and then chose the final set by [integer linear programming](/binary-integer-programming/) under constraints: arguments do not overlap, each core argument appears at most once, a reference argument needs the argument it refers to, and a continuation argument needs an earlier part. They also showed that the quality of the syntactic parse matters most at the pruning stage (measurement).
- **Sequence labeling.** For each predicate, tag the words with [BIO tags](/bio-encoding/) of the roles, with a feature that marks the predicate, using a [conditional random field](/conditional-random-field/), a [BiLSTM-CRF](/bilstm-crf/) or a pretrained transformer encoder. Viterbi decoding takes $O(n\,T^2)$ time for $T = 2L + 1$ tags (theorem). Deep neural taggers of this kind do well without any syntactic parse (measurement).
- **Span-based models.** Score every span $(i, j)$ for every role, and decode the best set of non-overlapping spans by dynamic programming, as in a [semi-Markov CRF](/semi-markov-crf/).

## Bounds

- **Decoding non-overlapping spans (theorem).** For one predicate, let $s(i, j, \ell)$ be the score of labeling the span $(i, j)$ with $\ell$, and let the score of an output be the sum over its arguments. The best set of non-overlapping arguments satisfies $B(0) = 0$ and $B(j) = \max\big(B(j - 1),\ \max_{i < j,\ \ell} B(i) + s(i, j, \ell)\big)$, which is [weighted interval scheduling](/weighted-interval-scheduling/) on the span positions. It takes $O(n^2 L)$ time, or $O(n\,d\,L)$ if arguments are at most $d$ words long. The proof is that the best output either leaves word $j$ out of every argument, or has an argument $(i, j)$ ending at $j$, and the rest is an optimal output for the prefix of length $i$.
- **Unique core roles (theorem).** Adding the constraint that each of $c$ core roles appears at most once makes the dynamic program track the set of core roles used so far, which takes $O(n^2 L\,2^c)$ time. With $c \le 6$ in PropBank this is a constant factor.
- **General constraints.** With arbitrary linear constraints, the decoding is an integer linear program, NP-hard in general. In practice the programs for one sentence are small and solved quickly (measurement in Punyakanok and others).

## Reductions

- **To sequence labeling.** Per predicate, non-overlapping labeled spans are in bijection with BIO tag sequences, so SRL reduces to [sequence labeling](/sequence-labeling/) once per predicate.
- **To weighted interval scheduling.** As in the bounds above, decoding with additive span scores is a weighted interval scheduling problem.
- **To integer linear programming.** Decoding with global constraints is a [binary integer program](/binary-integer-programming/) with one variable for each candidate span and label.
- **As part of other problems.** The predicate-argument structure that SRL finds is the core of an [AMR](/abstract-meaning-representation/) graph, which adds the rest of the meaning.

## Applications

- Information extraction, where roles give the slots of events.
- Question answering, by matching the roles of a question with the roles of a candidate answer.
- Machine translation and its evaluation, to keep who did what to whom across languages.
- Features or auxiliary tasks for [semantic parsing](/semantic-parsing/) and [natural language inference](/natural-language-inference/).

## References
