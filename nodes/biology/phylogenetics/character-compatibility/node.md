---
tag: 26135H
kind: problem
slug: character-compatibility
name: Character compatibility
aliases:
- compatibility problem
area: biology/phylogenetics
level: advanced
summary: Find a largest set of characters that fit one tree without homoplasy. For binary characters this is a maximum clique in the pairwise compatibility graph and is NP-hard.
prereqs: [perfect-phylogeny, four-gamete-condition, maximum-clique]
see_also: [gusfield-perfect-phylogeny, splits-of-a-tree, maximum-parsimony, clique-problem, np-hard, phylogenetic-tree, parsimony-informative-site]
sources:
  - paper: doi:10.2307/2412604
    title: Walter J. Le Quesne, A method of selection of characters in numerical taxonomy, Systematic Zoology 18(2), 1969
    locator: pp. 201 to 205, the test of uniquely derived characters and the selection of a largest consistent set
  - paper: doi:10.1016/0025-5564(76)90035-3
    title: George F. Estabrook, C. S. Johnson Jr. and F. R. McMorris, A mathematical foundation for the analysis of cladistic character compatibility, Mathematical Biosciences 29(1-2), 1976
    locator: pp. 181 to 187, pairwise compatibility of binary characters implies joint compatibility
  - paper: "George F. Estabrook and F. R. McMorris, When are two qualitative taxonomic characters compatible?, Journal of Mathematical Biology 4(2), 1977"
    title: George F. Estabrook and F. R. McMorris, When are two qualitative taxonomic characters compatible?, 1977
    locator: pp. 195 to 200, the pairwise test for multistate characters
  - paper: "William H. E. Day and David Sankoff, Computational complexity of inferring phylogenies by compatibility, Systematic Zoology 35(2), 1986"
    title: William H. E. Day and David Sankoff, Computational complexity of inferring phylogenies by compatibility, 1986
    locator: pp. 224 to 229, NP-completeness of the largest compatible set
  - book: isbn:9780198509424
    title: Charles Semple and Mike Steel, Phylogenetics, Oxford University Press, 2003
    locator: Chapter 4, compatibility of characters
  - book: isbn:9780878931774
    title: Joseph Felsenstein, Inferring Phylogenies, Sinauer Associates, 2004
    locator: Chapter 8, compatibility (the compatibility graph, cliques and the multistate case)
---

The character compatibility problem asks for a largest subset of the characters of a matrix that fit one tree with no homoplasy, so that the subset has a [perfect phylogeny](/perfect-phylogeny/). The other characters are treated as noise. For binary characters the problem reduces to a [maximum clique](/maximum-clique/) in a graph on the characters, because a set of binary characters fits one tree if and only if each pair fits. This reduction is exact, and the problem is [NP-hard](/np-hard/) in general. For characters with three or more states, pairs no longer decide the question. The [four-gamete condition](/four-gamete-condition/) is the pairwise test that the binary case is built on.

## In plain words

Each column of the table is a trait, and each trait suggests how the species are grouped. Some traits agree with each other, and some contradict each other. The compatibility method keeps the largest group of traits that all agree, builds the tree that they support, and ignores the rest.

For yes or no traits there is a simple rule: a group of traits agrees as a whole exactly when every two of them agree. So you draw a network with one dot for each trait and a line between two traits that agree. The best group of traits is the largest set of dots that are all joined to each other. Finding that set is hard in general, but it is easy for small tables.

## Definition

**Input.** A set $X$ of $n$ taxa and a set $C$ of $m$ characters, each a function $c : X \to \{0, \ldots, r-1\}$. Optionally, a weight $w(c) > 0$ for each character.

**Compatibility.** A set $S \subseteq C$ is *compatible* if there is a tree $T$ on $X$ on which every character of $S$ is *convex*: for each $c \in S$ and each state $s$, the taxa with state $s$ span subtrees that are vertex-disjoint for different states. Equivalently, the submatrix with the columns of $S$ has a [perfect phylogeny](/perfect-phylogeny/). Two characters are compatible if the set of the two is.

**The problem.** Find a compatible set $S \subseteq C$ of largest size, or of largest total weight.

**The compatibility graph.** Its vertices are the characters, and two characters are adjacent if they are compatible as a pair.

The model is the one of discrete unordered characters with no missing entries, on unrooted trees. For binary characters, $c$ and $d$ are compatible if and only if the columns do not show all four pairs 00, 01, 10 and 11.

## Variants

- **Binary characters.** Pairwise compatibility implies joint compatibility (Estabrook, Johnson and McMorris 1976). So a set is compatible if and only if it is a clique of the compatibility graph, and the problem is exactly maximum clique on that graph.
- **Multistate characters.** Two characters $c$ and $d$ are compatible if and only if their *partition intersection graph* has no cycle (Estabrook and McMorris 1977). This graph has one vertex for each state of $c$ and each state of $d$, and an edge between state $s$ of $c$ and state $t$ of $d$ when some taxon has both. Pairwise compatibility no longer implies joint compatibility, as the example below shows. So a clique of the compatibility graph is only a candidate, and testing it is itself the NP-complete perfect phylogeny problem when $r$ is unbounded.
- **Weighted compatibility.** With weights, the binary problem is a maximum weight clique.
- **Rooted or directed characters.** If the ancestral state of each binary character is known, two characters are compatible if and only if their sets of derived taxa are disjoint or nested. This is the cladistic setting of Le Quesne and of Estabrook, Johnson and McMorris.
- **Quality of the answer.** Some methods list all largest cliques, or all maximal cliques, and compare the trees they give, because several largest sets with different trees are common.

## Examples

**Binary characters.** Six taxa and five characters.

| taxon | $c_1$ | $c_2$ | $c_3$ | $c_4$ | $c_5$ |
|---|---|---|---|---|---|
| $t_1$ | 0 | 1 | 1 | 0 | 0 |
| $t_2$ | 0 | 1 | 0 | 0 | 1 |
| $t_3$ | 1 | 0 | 1 | 1 | 0 |
| $t_4$ | 1 | 0 | 1 | 0 | 0 |
| $t_5$ | 0 | 0 | 1 | 1 | 1 |
| $t_6$ | 1 | 1 | 0 | 0 | 0 |

The pairs that show four gametes are $c_1c_2$, $c_1c_3$, $c_1c_4$, $c_5c_2$, $c_5c_3$ and $c_5c_4$. For example, $c_1$ and $c_2$ show $01$ in $t_1$, $10$ in $t_3$, $00$ in $t_5$ and $11$ in $t_6$. So the compatibility graph has the four edges $c_1c_5$, $c_2c_3$, $c_2c_4$ and $c_3c_4$. Its largest clique is $\{c_2, c_3, c_4\}$, and it is the only clique of size 3. These three characters give the splits $\{t_1, t_2, t_6\} \mid \{t_3, t_4, t_5\}$, $\{t_2, t_6\} \mid \{t_1, t_3, t_4, t_5\}$ and $\{t_3, t_5\} \mid \{t_1, t_2, t_4, t_6\}$, which all fit the tree `((t2,t6),t1,(t4,(t3,t5)))`. The method drops $c_1$ and $c_5$.

**Multistate characters, pairwise compatible but not jointly compatible.** Five taxa and three characters.

| taxon | $c_1$ | $c_2$ | $c_3$ |
|---|---|---|---|
| A | 0 | 0 | 0 |
| B | 1 | 1 | 1 |
| C | 2 | 1 | 0 |
| D | 0 | 0 | 2 |
| E | 1 | 0 | 2 |

The state classes are $c_1$: $\{A, D\}, \{B, E\}, \{C\}$; $c_2$: $\{A, D, E\}, \{B, C\}$; and $c_3$: $\{A, C\}, \{B\}, \{D, E\}$. Each pair fits exactly one of the 15 unrooted binary trees on five taxa:

| pair | the tree |
|---|---|
| $c_1, c_2$ | `((B,C),E,(A,D))` |
| $c_2, c_3$ | `((B,C),A,(D,E))` |
| $c_1, c_3$ | `((A,C),D,(B,E))` |

So the compatibility graph is a triangle. But the three characters together fit no tree. The binary character $c_2$ forces the split $\{B, C\} \mid \{A, D, E\}$. A binary tree on five taxa with this split is `((B,C),x,(y,z))` with $x$ one of A, D and E. If $x = A$ or $x = D$, the path from B to E and the path from A to D share the middle node, so $c_1$ is not convex. If $x = E$, the path from C to A and the path from D to E share two internal nodes, so $c_3$ is not convex.

The pairwise test of Estabrook and McMorris agrees: for $c_1$ and $c_2$, the partition intersection graph has the edges $\{A,D\} - \{A,D,E\}$ (through A and D), $\{B,E\} - \{A,D,E\}$ (through E), $\{B,E\} - \{B,C\}$ (through B) and $\{C\} - \{B,C\}$ (through C). This is a path, with no cycle, so the pair is compatible.

## Known algorithms

- **Binary characters.** Build the compatibility graph with the four-gamete test in $O(nm^2)$ time. Then find a maximum clique with any exact clique algorithm, such as branch and bound or the Bron and Kerbosch enumeration of maximal cliques. This is exponential in $m$ in the worst case. The [clique problem](/clique-problem/) page lists the known exact bounds. The chosen set is then turned into a tree with [Gusfield's algorithm](/gusfield-perfect-phylogeny/) in $O(nm)$ time.
- **Le Quesne's method.** Le Quesne in 1969 proposed to test each pair of characters for a conflict and to prefer the characters that conflict with few others. Choosing by conflict counts is a heuristic: it does not always find a largest compatible set.
- **Multistate characters.** Test each pair in $O(n + r^2)$ time with the partition intersection graph, find large cliques, and test each candidate clique for joint compatibility with a perfect phylogeny algorithm. For a fixed number of states the joint test is polynomial (Kannan and Warnow 1997).
- **Small data sets.** For a few dozen characters, exhaustive search over cliques is practical. Felsenstein, Chapter 8, describes the programs used in systematics.

## Bounds

- **Binary characters.** Day and Sankoff proved in 1986 that the decision version, "is there a compatible set of at least $k$ characters", is NP-complete, by a reduction from clique. So no polynomial algorithm exists unless P = NP. Building the compatibility graph takes $\Theta(nm^2)$ time with the direct pair test.
- **Multistate characters.** Even deciding whether all $m$ characters are compatible is NP-complete when the number of states is unbounded (Bodlaender, Fellows and Warnow 1992; Steel 1992). So the optimization problem is NP-hard even when the answer is the whole set.
- **Pairwise versus joint.** For binary characters, a largest clique is a largest compatible set. For multistate characters, a largest clique is only an upper bound on the size of a largest compatible set, and the example above shows that the bound can be strict.

## Reductions

- **To maximum clique.** For binary characters, the compatible sets are exactly the cliques of the compatibility graph. So any exact or approximate clique algorithm applies directly, with the same ratio.
- **From clique.** Day and Sankoff reduced the clique problem to binary compatibility, which gives the NP-hardness.
- **To splits.** A binary character is a split of the taxa. Compatible characters are compatible splits, and a compatible set of splits defines a unique tree, by the splits-equivalence theorem. See [splits of a tree](/splits-of-a-tree/).
- **Relation to parsimony.** A compatible set of characters is a set whose parsimony score on its tree reaches the lower bound of one change per extra state. Compatibility maximizes the number of characters that reach this bound, while [maximum parsimony](/maximum-parsimony/) minimizes the total number of changes over all characters. The two criteria can choose different trees.

## Applications

- **Systematics.** Compatibility analysis was one of the main tree building methods for morphological data in the 1970s and 1980s. It treats the characters that conflict with a large compatible set as homoplastic.
- **Data quality.** The compatibility graph shows which characters conflict, and a character in many conflicts is a candidate for a coding error.
- **Population genetics.** For a set of sites, the pairs that fail the four-gamete test mark recombination. The largest compatible set of sites in an interval gives a region that may have a single tree. See [ancestral recombination graph inference](/ancestral-recombination-graph-inference/).
- **Historical linguistics.** Compatibility of multistate characters, with a weighted version that allows a few conflicts, has been used to build trees of language families.

## References
