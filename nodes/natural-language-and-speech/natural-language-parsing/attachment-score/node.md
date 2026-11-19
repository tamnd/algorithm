---
tag: AZPM01
kind: definition
slug: attachment-score
name: Attachment score
aliases:
- labeled attachment score
- unlabeled attachment score
area: natural-language-and-speech/natural-language-parsing
level: intro
summary: The fraction of words whose predicted head is correct (unlabeled) or whose head and relation label are both correct (labeled).
prereqs: [dependency-tree]
see_also: [dependency-parsing, parseval-measures, hamming-distance, precision-and-recall, treebank, eisner-algorithm, mst-dependency-parsing, arc-standard-parsing]
sources:
  - book: isbn:9781598295962
    title: "Sandra Kübler, Ryan McDonald and Joakim Nivre, Dependency Parsing, Synthesis Lectures on Human Language Technologies, Morgan and Claypool, 2009"
    locator: "Chapter 6, Evaluation (attachment scores, exact match and the treatment of punctuation)"
  - paper: doi:10.1162/coli.07-056-R1-07-027
    title: "Joakim Nivre, Algorithms for deterministic incremental dependency parsing, Computational Linguistics 34(4), 513-553, 2008"
    locator: "the experimental section, which reports labeled and unlabeled attachment scores and exact match"
---

The attachment score of a predicted [dependency tree](/dependency-tree/) is the fraction of its words that got the right head. The **unlabeled attachment score** (UAS) checks the head only. The **labeled attachment score** (LAS) checks the head and the relation label together. They are the standard scores of [dependency parsing](/dependency-parsing/). Because both trees give every word exactly one head, a word is either right or wrong, and precision, recall and F1 all equal the same number. Two choices change the value and must be reported with it: whether punctuation tokens are counted, and whether the corpus score is the total over all words or an average over sentences.

## Definition

Let a sentence have the words $1, \ldots, n$, a gold tree with head $h^\ast(d)$ and label $r^\ast(d)$ for each word $d$, and a predicted tree with $h(d)$ and $r(d)$. Let $D \subseteq \{1, \ldots, n\}$ be the set of scored words: all words, or all words except punctuation. Then

$$\mathrm{UAS} = \frac{|\{d \in D : h(d) = h^\ast(d)\}|}{|D|}, \qquad \mathrm{LAS} = \frac{|\{d \in D : h(d) = h^\ast(d) \text{ and } r(d) = r^\ast(d)\}|}{|D|}.$$

The **label accuracy** is $|\{d \in D : r(d) = r^\ast(d)\}| / |D|$. Always $\mathrm{LAS} \le \mathrm{UAS}$ and $\mathrm{LAS} \le$ label accuracy.

**Corpus score.** For a test corpus, the usual score is the micro average: add the correct words over all sentences and divide by the total number of scored words. This is not the mean of the sentence scores, which gives short sentences more weight. The **exact match** score is the fraction of sentences whose scored words are all correct.

**Precision and recall.** A gold tree and a predicted tree over the same words both have exactly one arc per word. So the number of predicted arcs equals the number of gold arcs, [precision and recall](/precision-and-recall/) of the arcs are equal, and both equal UAS (or LAS for labeled arcs). This is the difference from the [PARSEVAL measures](/parseval-measures/), where the two trees can have different numbers of constituents. If a parser may leave a word without a head, or if the system and the gold standard tokenize the text differently, the counts differ, and evaluations then report precision, recall and F1 over the aligned words.

**Relation to the Hamming distance.** Write the head lists as strings of length $n$. Then $1 - \mathrm{UAS}$, with all words scored, is the [Hamming distance](/hamming-distance/) between the two strings divided by $n$. Minimizing this loss is the target of the [dynamic oracle](/dynamic-oracle/), whose cost counts the gold arcs that can no longer be built.

The definition does not depend on whether the root may have one child or several; the root arc of each word is scored like any other arc.

## Examples and non-examples

**One sentence.** Gold tree of *the cat sat on the mat .*, with the final full stop attached to *sat*:

| $d$ | word | gold head, label | predicted head, label | head right | both right |
|---|---|---|---|---|---|
| 1 | the | 2 det | 2 det | yes | yes |
| 2 | cat | 3 nsubj | 3 obj | yes | no |
| 3 | sat | 0 root | 0 root | yes | yes |
| 4 | on | 6 case | 3 obl | no | no |
| 5 | the | 6 det | 6 det | yes | yes |
| 6 | mat | 3 obl | 4 nmod | no | no |
| 7 | . | 3 punct | 6 punct | no | no |

Counting the full stop, $\mathrm{UAS} = 4/7$ and $\mathrm{LAS} = 3/7$. Leaving out punctuation, $\mathrm{UAS} = 4/6 = 2/3$ and $\mathrm{LAS} = 3/6 = 1/2$. The label accuracy over all seven words is $4/7$. The same parser output thus has two different scores, and a paper must say which convention it uses.

**Micro and macro averages.** Add a second sentence of two words, both with wrong heads. Over all eight non-punctuation words, $\mathrm{UAS} = (4 + 0) / (6 + 2) = 1/2$. The mean of the two sentence scores is $(2/3 + 0) / 2 = 1/3$. The standard corpus score is $1/2$. The exact match score is 0, since neither sentence is fully right.

**Non-examples.**

- The fraction of correct arcs among the predicted arcs when the predicted structure is a forest that leaves some words without a head. That is a precision, and it is not equal to the recall.
- The PARSEVAL F1 of a constituency tree converted from the dependency tree. It scores spans, not heads, and a single wrong head can change many spans.
- A score that checks only the label of each word. That is the label accuracy; it can be high while many heads are wrong.

## Related definitions

- [Dependency tree](/dependency-tree/) and [dependency parsing](/dependency-parsing/): the objects scored and the task.
- [PARSEVAL measures](/parseval-measures/): the bracket precision, recall and F1 used for constituency parsers.
- [Hamming distance](/hamming-distance/): $n (1 - \mathrm{UAS})$ is the Hamming distance between the gold and the predicted head lists.
- [Dynamic oracle](/dynamic-oracle/): trains a transition parser to keep the attachment loss as small as possible from any configuration.
- [Treebank](/treebank/): the source of the gold trees, and of the split into training, development and test sentences on which scores are reported.

## References
