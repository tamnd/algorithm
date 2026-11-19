---
tag: 4W6YMS
kind: definition
slug: dependency-tree
name: Dependency tree
aliases:
- dependency structure
- dependency graph of a sentence
area: natural-language-and-speech/natural-language-parsing
level: intro
summary: A rooted tree over the words of a sentence with a labeled arc from each head word to each of its dependents.
prereqs: [rooted-tree]
see_also: [projective-dependency-tree, dependency-parsing, attachment-score, arborescence, head-rules, treebank, cayley-formula, parse-tree]
sources:
  - book: isbn:9781598295962
    title: "Sandra Kübler, Ryan McDonald and Joakim Nivre, Dependency Parsing, Synthesis Lectures on Human Language Technologies, Morgan and Claypool, 2009"
    locator: "Chapter 2, Dependency Parsing (dependency graphs, the artificial root, well-formed dependency trees and projectivity)"
  - paper: doi:10.1162/coli.07-056-R1-07-027
    title: "Joakim Nivre, Algorithms for deterministic incremental dependency parsing, Computational Linguistics 34(4), 513-553, 2008"
    locator: the definitions of dependency graphs and dependency trees at the start of the article
  - url: https://universaldependencies.org/
    title: "Universal Dependencies, the annotation guidelines"
    locator: the basic dependency tree with one root word and the list of universal relations
---

A dependency tree describes the syntax of a sentence by links between its words. Each word has exactly one head, the word that it modifies or completes, and the link from the head to the word carries a label, the grammatical relation, such as subject or determiner. An artificial root word 0 is the head of the main word of the sentence. The links form a tree rooted at 0, so every word reaches the root by following heads. Dependency trees are the output of [dependency parsing](/dependency-parsing/), the unit of the dependency [treebanks](/treebank/), and the structure that [attachment scores](/attachment-score/) compare.

## Definition

A sentence is a sequence of words $w_1 \cdots w_n$. We add an artificial root $w_0$ at the left edge. Let $R$ be a finite set of relation labels.

A **dependency tree** of the sentence is a set $A$ of labeled arcs $(h, d, r)$ with head $h \in \{0, \ldots, n\}$, dependent $d \in \{1, \ldots, n\}$ and label $r \in R$, such that:

1. **Single head.** Each word $d \in \{1, \ldots, n\}$ is the dependent of exactly one arc. No arc enters the root 0.
2. **Connected to the root.** For each word $d$, the chain $d, h(d), h(h(d)), \ldots$ reaches 0, where $h(d)$ is the head of $d$.

The two conditions say that the arcs form a spanning [arborescence](/arborescence/) rooted at 0 of the complete directed graph on $\{0, \ldots, n\}$: there are exactly $n$ arcs, there is no cycle, and there is exactly one directed path from 0 to each word. Without the labels, the tree is its head function $h$, and the code on these pages stores it as a list `heads` of length $n + 1$ with `heads[0] = -1` and `heads[d]` $= h(d)$.

The words $d$ with $h(d) = k$ are the **dependents** of $k$. The **subtree** of $k$ is $k$ and all the words whose chain of heads passes through $k$; its set of positions is the **yield** of $k$. A word $k$ **dominates** a word $d$ when $d$ is in the subtree of $k$.

**The children of the root.** In the definition above the root may have more than one child. The Universal Dependencies treebanks require exactly one child of the root, the word with the relation `root`; many parsers allow several. Each page of this group says which convention it uses.

**Counting.** Over $n$ words there are $(n + 1)^{n - 1}$ dependency trees without labels: they are the spanning trees of the complete graph on the $n + 1$ nodes $\{0, \ldots, n\}$, each directed away from 0, and [Cayley's formula](/cayley-formula/) counts those. This gives 1, 3, 16, 125, 1296 for $n = 1$ to 5. With exactly one child of the root there are $n^{n - 1}$ trees (1, 2, 9, 64, 625): by the degree form of Cayley's formula, the trees on $N$ labeled nodes in which a fixed node has degree 1 number $(N - 1)^{N - 2}$, and here $N = n + 1$. With $|R|$ labels each count is multiplied by $|R|^n$, or by $|R|^{n - 1}$ when the single root arc must carry the label `root`.

## Examples and non-examples

**A small tree.** For *the cat sat on the mat*, in the style of Universal Dependencies:

| $d$ | word | $h(d)$ | label |
|---|---|---|---|
| 1 | the | 2 | det |
| 2 | cat | 3 | nsubj |
| 3 | sat | 0 | root |
| 4 | on | 6 | case |
| 5 | the | 6 | det |
| 6 | mat | 3 | obl |

The head list is `[-1, 2, 3, 0, 6, 6, 3]`. The root has one child, *sat*. The subtree of *mat* is *on the mat*, positions 4 to 6. Other annotation schemes make the preposition *on* the head of *mat*. The definition allows either choice, and the treebank fixes it.

**All trees over two words.** With $n = 2$ the head lists are $(h(1), h(2)) = (0, 0)$, $(0, 1)$ and $(2, 0)$, three trees as $(n + 1)^{n - 1} = 3$ says. The first one gives the root two children, so only two of them satisfy the one-child rule, as $n^{n - 1} = 2$ says. The pair $(2, 1)$ is not a tree: the two words head each other and neither reaches the root.

**A tree with crossing arcs.** In *A hearing is scheduled on the issue today*, with the head list `[-1, 2, 3, 0, 3, 2, 7, 5, 4]`, the phrase *on the issue* modifies *hearing* and *today* modifies *scheduled*. The arc from *hearing* (2) to *on* (5) passes over *is* (3) and *scheduled* (4), which *hearing* does not dominate. The set of arcs is still a dependency tree. It is not a [projective tree](/projective-dependency-tree/).

**Non-examples.**

- A word with two heads. Enhanced representations, for example the enhanced graphs of Universal Dependencies, add arcs so that a word can have several heads. The result is a directed graph, not a dependency tree.
- A set of arcs in which some word has no head. That is a forest, a partial analysis; the transition parsers of this group pass through such forests before they finish.
- A cycle such as $h(1) = 2$, $h(2) = 1$: each word has one head, but neither is connected to the root.
- A [parse tree](/parse-tree/) of a constituency grammar. It has phrase nodes above the words. [Head rules](/head-rules/) turn it into a dependency tree by choosing a head child in each phrase.

## Related definitions

- [Projective dependency tree](/projective-dependency-tree/): a dependency tree in which no two arcs cross when they are drawn above the sentence.
- [Arborescence](/arborescence/): the graph form of the definition. The [maximum spanning arborescence](/mst-dependency-parsing/) of a weighted complete graph is the best tree under arc scores.
- [Attachment score](/attachment-score/): the fraction of words whose head (and label) in a predicted tree is the same as in the gold tree.
- [Dependency parsing](/dependency-parsing/): the problem of finding the dependency tree of a sentence.
- [Rooted tree](/rooted-tree/): a dependency tree is a rooted tree on the positions $0, \ldots, n$ whose nodes also have a linear order, the word order.
- [Dependency model with valence](/dependency-model-with-valence/): a probability model over dependency trees, used for learning them without a treebank.

## References
