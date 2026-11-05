---
tag: GSNJXJ
kind: definition
slug: labeled-graph
name: Labeled graph
aliases:
- Labeled vs unlabeled graphs
area: graphs/graph-representation
level: intro
summary: A graph in which each vertex or edge carries a distinct name or label that identifies it.
prereqs: [graph, vertex, graph-isomorphism-definition]
see_also: [graph-isomorphism-problem, canonical-labeling, graph-automorphism, prufer-sequence, cayley-formula, symbol-graph, isomorphism-invariant]
sources:
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition, Prentice Hall, 2001
    locator: Section 1.1, isomorphism, isomorphism classes and the count of graphs with a fixed vertex set; Section 2.2, the count of labeled trees
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer, 2017
    locator: Chapter 1, Section 1.1 (Graphs), isomorphism, and the convention of identifying isomorphic graphs
  - book: Frank Harary and Edgar M. Palmer, Graphical Enumeration, Academic Press, 1973
    locator: Chapter 1 (Labeled enumeration) and Chapter 4 (Graphs), the number of labeled and of unlabeled graphs
---

A labeled graph is a [graph](/graph/) whose [vertices](/vertex/) have distinct names, usually $1, \ldots, n$, so that two graphs count as different when they have different edges between the same names, even if they have the same shape. An unlabeled graph is the shape alone: an isomorphism class of graphs. The distinction decides what is counted: on 4 vertices there are 64 labeled graphs but only 11 unlabeled ones. Every graph that a program stores is labeled, because the vertices are array indices; questions about unlabeled graphs are questions about [isomorphism](/graph-isomorphism-definition/).

## Definition

**Labeled graph.** A labeled graph on the label set $[n] = \{1, \ldots, n\}$ is a graph $G = (V, E)$ with $V = [n]$. Two labeled graphs $G = ([n], E)$ and $G' = ([n], E')$ are equal if and only if $E = E'$. More generally, a vertex labeling of a graph $G$ is a bijection $\lambda : V \to L$ onto a set $L$ of labels, and the pair $(G, \lambda)$ is a labeled graph. An edge labeling is a bijection from $E$ to a label set, which names the edges of a [multigraph](/multigraph/).

**Unlabeled graph.** Graphs $G$ and $H$ are isomorphic, $G \cong H$, if there is a bijection $f : V(G) \to V(H)$ with $\{u, v\} \in E(G) \iff \{f(u), f(v)\} \in E(H)$ (for directed graphs, with ordered pairs). An unlabeled graph on $n$ vertices is an isomorphism class of graphs on $n$ vertices.

**Counting.** For simple undirected graphs:

- The number of labeled graphs on $[n]$ is $2^{\binom{n}{2}}$, one for each subset of the $\binom{n}{2}$ possible edges. For directed graphs with self-loops allowed it is $2^{n^2}$.
- The labeled graphs in the class of an unlabeled graph $G$ are its relabelings $\pi(G)$ for the $n!$ permutations $\pi$ of $[n]$. Two permutations give the same labeled graph exactly when they differ by an [automorphism](/graph-automorphism/) of $G$, so the class has $n! / |\text{Aut}(G)|$ labeled members, where $\text{Aut}(G)$ is the [automorphism group](/graph-automorphism-group/). This is the orbit-stabilizer theorem.
- Hence the number $g_n$ of unlabeled graphs satisfies $g_n \ge 2^{\binom{n}{2}} / n!$. Since $\lg n! = O(n \log n)$, this gives $\lg g_n = \binom{n}{2} - O(n \log n)$. Almost all graphs have only the trivial automorphism ([almost all graphs are asymmetric](/almost-all-graphs-asymmetric/)), and $g_n \sim 2^{\binom{n}{2}} / n!$.

**Words.** "Labeled" here is about identity. The same word is also used for graphs whose vertices or edges carry data that need not be distinct, such as colors, types or weights; that data is better called an *attribute* or a *weight* (see [weighted graph](/weighted-graph/)). A *graph labeling* in the sense of graceful labelings is a third, unrelated use: an assignment of numbers with a condition on the edges.

## Examples and non-examples

**The three vertices.** On $\{1, 2, 3\}$ there are $2^3 = 8$ labeled graphs and 4 unlabeled ones:

| unlabeled graph | $\lvert \text{Aut} \rvert$ | labeled copies $3!/\lvert \text{Aut} \rvert$ |
|---|---|---|
| no edges | 6 | 1 |
| one edge | 2 | 3 |
| path $P_3$, two edges | 2 | 3 |
| triangle $K_3$ | 6 | 1 |

The labeled copies sum to $1 + 3 + 3 + 1 = 8$. The three labeled paths are $1\text{-}2\text{-}3$, $2\text{-}1\text{-}3$ and $1\text{-}3\text{-}2$, named by their middle vertex 2, 1 or 3.

**Small counts.**

| $n$ | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| labeled graphs $2^{\binom n2}$ | 1 | 2 | 8 | 64 | 1024 |
| unlabeled graphs $g_n$ | 1 | 2 | 4 | 11 | 34 |
| labeled trees $n^{n-2}$ | 1 | 1 | 3 | 16 | 125 |
| unlabeled trees | 1 | 1 | 1 | 2 | 3 |

The labeled trees are counted by [Cayley's formula](/cayley-formula/), with the bijection of the [Prüfer sequence](/prufer-sequence/). No closed formula like this is known for the unlabeled trees.

**Non-example.** A drawing of a graph with no names on its dots is not a labeled graph. Two drawings of the path on three dots are the same unlabeled graph however they are placed, but you cannot ask whether "vertex 1" is an end until you choose names.

**In a program.** An [adjacency matrix](/adjacency-matrix/) or an [adjacency list](/adjacency-list/) indexes the vertices by $0, \ldots, n - 1$, so it stores a labeled graph. Two different arrays can store isomorphic graphs. A [symbol graph](/symbol-graph/) uses strings as the labels and a table to map them to indices.

## Related definitions

- **Isomorphism.** The relation that forgets the labels. Deciding it is the [graph isomorphism problem](/graph-isomorphism-problem/).
- **Canonical labeling.** A [canonical labeling](/canonical-labeling/) picks one labeled graph from each isomorphism class, so that two graphs are isomorphic if and only if their canonical forms are equal. Tools such as [nauty](/nauty/) compute it.
- **Invariant.** A function of labeled graphs that does not change under relabeling, such as the degree sequence, is an [isomorphism invariant](/isomorphism-invariant/). It is a function of the unlabeled graph.
- **Automorphism.** A relabeling that maps a graph to itself. See [graph automorphism](/graph-automorphism/).

## References
