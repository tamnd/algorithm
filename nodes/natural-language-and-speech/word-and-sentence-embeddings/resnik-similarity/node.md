---
tag: QP71HQ
kind: definition
slug: resnik-similarity
name: Resnik similarity
aliases:
- information content similarity
area: natural-language-and-speech/word-and-sentence-embeddings
level: core
summary: The similarity of two concepts in a taxonomy as the information content -log P(c) of their most informative common subsumer.
prereqs: [self-information]
see_also: [lowest-common-ancestor, directed-acyclic-graph, tree, word-sense-disambiguation, hearst-patterns, pointwise-mutual-information, spearman-rank-correlation, distributional-hypothesis]
sources:
  - paper: "Philip Resnik, Using information content to evaluate semantic similarity in a taxonomy, Proceedings of the 14th International Joint Conference on Artificial Intelligence (IJCAI-95), 1995"
    title: Resnik 1995
    locator: the definition of similarity as the information content of the most informative common subsumer, the class frequencies from noun counts in the Brown corpus over WordNet, the maximum over senses for words, and the correlations with human ratings
  - url: https://web.stanford.edu/~jurafsky/slp3/
    title: Daniel Jurafsky and James H. Martin, Speech and Language Processing, third edition draft
    locator: Appendix Word Senses and WordNet, the section on word similarity in a thesaurus
---

Resnik similarity measures how similar two concepts of a taxonomy are by the information content of the most specific concept that subsumes both. A taxonomy such as the noun hierarchy of WordNet puts "cat" and "dog" under "mammal", and "cat" and "car" only under the root, "entity". Resnik 1995 gives each concept a probability from corpus counts and scores a pair by the [self-information](/self-information/) $-\log P(c)$ of their common subsumer with the largest value. A rare, specific subsumer such as "bird" means a high similarity, and the root, with probability 1, means similarity 0. Unlike counting the edges of the path between two concepts, the measure does not assume that all links of the taxonomy have the same length. That it agrees with human ratings better than edge counting is a measurement.

## Definition

Let a taxonomy be a [directed acyclic graph](/directed-acyclic-graph/) of concepts with one root, in which an edge from $c$ to $c'$ says that $c$ is a kind of $c'$. Concept $c'$ **subsumes** $c$ if $c' = c$ or $c'$ is an ancestor of $c$. Each word $n$ is attached to the concepts that are its senses, and $\operatorname{words}(c)$ is the set of words attached to $c$ or to a concept that $c$ subsumes. From a corpus with the count $\operatorname{count}(n)$ of each word,

$$ \operatorname{freq}(c) = \sum_{n \in \operatorname{words}(c)} \operatorname{count}(n), \qquad P(c) = \frac{\operatorname{freq}(c)}{N}, \qquad \operatorname{IC}(c) = -\log P(c), $$

where $N$ is the frequency of the root. The **Resnik similarity** of two concepts is

$$ \operatorname{sim}(c_1, c_2) = \max_{c \in S(c_1, c_2)} \operatorname{IC}(c), $$

where $S(c_1, c_2)$ is the set of concepts that subsume both. For two words, Resnik takes the largest similarity over their senses: $\operatorname{wsim}(w_1, w_2) = \max \operatorname{sim}(c_1, c_2)$ over the senses $c_1$ of $w_1$ and $c_2$ of $w_2$. The base of the logarithm sets the unit; the examples below use base 2, so the values are in bits.

These facts follow from the definition.

- **Monotone.** If $c'$ subsumes $c$, then $\operatorname{words}(c) \subseteq \operatorname{words}(c')$, so $P(c) \le P(c')$ and $\operatorname{IC}(c) \ge \operatorname{IC}(c')$. The information content does not grow toward the root, and the root has $\operatorname{IC} = 0$.
- **Trees.** In a tree, $S(c_1, c_2)$ is the path from the [lowest common ancestor](/lowest-common-ancestor/) to the root, so by monotonicity the most informative common subsumer is the lowest common ancestor. In a DAG there can be several lowest common subsumers, and the maximum chooses among them.
- **Range.** $0 \le \operatorname{sim}(c_1, c_2) \le \min(\operatorname{IC}(c_1), \operatorname{IC}(c_2))$. The root is a common subsumer, which gives the lower bound, and every common subsumer subsumes $c_1$ and $c_2$, so by monotonicity its information content is at most theirs. $\operatorname{sim}$ is symmetric.
- **Not a normalized score.** $\operatorname{sim}(c, c) = \operatorname{IC}(c)$, which differs from concept to concept, so the similarity of a concept with itself is not a constant.
- **Ambiguous words.** Resnik 1995 adds the count of an ambiguous word to every concept of each of its senses. A common variant divides the count among the senses.

## Examples and non-examples

**A small taxonomy.** The tree and the counts below are written for this page, with $N = 100$ noun tokens.

| concept | parent | freq | P | IC (bits) |
| --- | --- | --- | --- | --- |
| entity | (root) | 100 | 1 | 0 |
| animal | entity | 58 | 0.58 | 0.7859 |
| mammal | animal | 50 | 0.50 | 1.0000 |
| cat | mammal | 20 | 0.20 | 2.3219 |
| dog | mammal | 30 | 0.30 | 1.7370 |
| bird | animal | 8 | 0.08 | 3.6439 |
| sparrow | bird | 5 | 0.05 | 4.3219 |
| eagle | bird | 3 | 0.03 | 5.0589 |
| artifact | entity | 42 | 0.42 | 1.2515 |
| vehicle | artifact | 35 | 0.35 | 1.5146 |
| car | vehicle | 25 | 0.25 | 2.0000 |
| bicycle | vehicle | 10 | 0.10 | 3.3219 |
| tool | artifact | 7 | 0.07 | 3.8365 |
| hammer | tool | 7 | 0.07 | 3.8365 |

Only the leaves have counts. The frequency of an inner concept is the sum over the leaves below it.

| pair | most informative subsumer | sim (bits) |
| --- | --- | --- |
| sparrow, eagle | bird | 3.6439 |
| car, bicycle | vehicle | 1.5146 |
| car, hammer | artifact | 1.2515 |
| cat, dog | mammal | 1.0000 |
| cat, sparrow | animal | 0.7859 |
| cat, car | entity | 0 |

Sparrow and eagle come out more similar than cat and dog, because "bird" is rarer in this corpus than "mammal". The measure rewards a specific common class, and here specific means rare. Car and hammer, whose common class is "artifact", also come out more similar than cat and dog, although their path in the tree has 4 edges and the path from cat to dog has 2. The counts decide, not the shape of the tree.

**Self-similarity.** $\operatorname{sim}(\text{cat}, \text{cat}) = 2.3219$ and $\operatorname{sim}(\text{dog}, \text{dog}) = 1.7370$, which is less than $\operatorname{sim}(\text{sparrow}, \text{eagle})$. So a dog is less similar to itself than a sparrow is to an eagle. This is a known weakness that the normalized measures below fix.

**The measurement.** Resnik 1995 took the frequencies from the nouns of the Brown corpus over WordNet and compared the measure with the human ratings of 30 noun pairs from Miller and Charles. The correlation was $r = 0.7911$ for information content, against $0.6645$ for edge counting and $0.6671$ for the probability of the subsumer alone. A replication of the ratings with new subjects gave correlations near 0.9 with the original ratings (Resnik reports 0.9015, and 0.8848 as the average per subject), which serves as an upper bound.

**Not: a distance.** The value grows with similarity and has no fixed maximum, and $\operatorname{sim}(c, c)$ is not a constant, so it cannot be turned into a distance that is 0 exactly for equal concepts by subtracting it from a constant.

**Not: distributional similarity.** The counts only give the weights of the concepts. Whether two concepts share a subsumer comes from the hand-built taxonomy, not from the contexts of the words as in the [distributional hypothesis](/distributional-hypothesis/). Two words that never occur near each other can be very similar.

## Related definitions

- **Self-information.** $\operatorname{IC}(c)$ is the [self-information](/self-information/) of the event that a random noun token falls under $c$.
- **Lin similarity.** $\frac{2 \operatorname{IC}(\operatorname{lcs})}{\operatorname{IC}(c_1) + \operatorname{IC}(c_2)}$, with lcs the most informative common subsumer, is in $[0, 1]$ and gives 1 for a concept with itself. In the table, cat and dog get $2 / (2.3219 + 1.7370) = 0.4927$, and sparrow and eagle $0.7769$.
- **Jiang and Conrath distance.** $\operatorname{IC}(c_1) + \operatorname{IC}(c_2) - 2 \operatorname{IC}(\operatorname{lcs})$ is 0 for a concept with itself. In the table, cat and dog get $2.0589$ and cat and car $4.3219$.
- **Path length.** The number of edges between the two concepts, through the lowest common subsumer. Resnik's argument against it is that the links of a taxonomy do not all stand for the same distance in meaning.
- **Uses.** The similarity of the senses of nearby words is a knowledge source for [word sense disambiguation](/word-sense-disambiguation/), and taxonomies can be extended with pairs from [Hearst patterns](/hearst-patterns/). Rank correlation, such as [Spearman's](/spearman-rank-correlation/), is the usual way to compare a measure with human ratings.

## References
