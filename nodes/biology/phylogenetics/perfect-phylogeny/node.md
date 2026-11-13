---
tag: Y9D3XV
kind: problem
slug: perfect-phylogeny
name: Perfect phylogeny
aliases:
- perfect phylogeny problem
area: biology/phylogenetics
level: advanced
summary: Decide whether a character matrix fits a tree on which every state of every character forms one connected part, so each change happens once. Linear for binary data, NP-complete in general.
prereqs: [phylogenetic-tree, rooted-and-unrooted-trees, splits-of-a-tree]
see_also: [four-gamete-condition, gusfield-perfect-phylogeny, character-compatibility, maximum-parsimony, camin-sokal-parsimony, dollo-parsimony, ancestral-recombination-graph-inference, np-complete]
sources:
  - book: isbn:9780198509424
    title: Charles Semple and Mike Steel, Phylogenetics, Oxford University Press, 2003
    locator: Chapter 4, compatibility of characters (binary characters, the partition intersection graph and the triangulation view)
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: Chapter 17, the section on the perfect phylogeny problem
  - paper: doi:10.1002/net.3230210104
    title: Dan Gusfield, Efficient algorithms for inferring evolutionary trees, Networks 21(1), 1991
    locator: pp. 19 to 28, the O(nm) algorithm for binary characters
  - paper: "Hans L. Bodlaender, Michael R. Fellows and Tandy J. Warnow, Two strikes against perfect phylogeny, Proceedings of ICALP 1992, Lecture Notes in Computer Science 623, Springer, 1992"
    title: Hans L. Bodlaender, Michael R. Fellows and Tandy J. Warnow, Two strikes against perfect phylogeny, 1992
    locator: pp. 273 to 283, NP-completeness of perfect phylogeny for multistate characters
  - paper: "Mike Steel, The complexity of reconstructing trees from qualitative characters and subtrees, Journal of Classification 9(1), 1992"
    title: Mike Steel, The complexity of reconstructing trees from qualitative characters and subtrees, 1992
    locator: pp. 91 to 116, NP-completeness of the compatibility of multistate characters
  - paper: "Richa Agarwala and David Fernández-Baca, A polynomial-time algorithm for the perfect phylogeny problem when the number of character states is fixed, SIAM Journal on Computing 23(6), 1994"
    title: Richa Agarwala and David Fernández-Baca, A polynomial-time algorithm for the perfect phylogeny problem when the number of character states is fixed, 1994
    locator: pp. 1216 to 1224, the O(2^(3r)(nm^3 + m^4)) algorithm
  - paper: doi:10.1137/S0097539794279067
    title: Sampath Kannan and Tandy Warnow, A fast algorithm for the computation and enumeration of perfect phylogenies, SIAM Journal on Computing 26(6), 1997
    locator: pp. 1749 to 1763, the O(2^(2r) n m^2) algorithm
  - book: isbn:9780878931774
    title: Joseph Felsenstein, Inferring Phylogenies, Sinauer Associates, 2004
    locator: Chapter 8, compatibility
---

The perfect phylogeny problem asks whether a matrix of characters fits a tree on which no character state ever arises twice. Each taxon is a row, each character is a column, and the tree must place the taxa so that, for every character, the taxa with the same state form one connected part of the tree. For binary characters the answer is given by the pairwise [four-gamete condition](/four-gamete-condition/), and [Gusfield's algorithm](/gusfield-perfect-phylogeny/) builds the tree in $O(nm)$ time. For characters with many states the problem is [NP-complete](/np-complete/), but it is polynomial when the number of states is fixed. This page is about the yes or no question and its known answers. The problem of keeping a largest subset of characters that fits is [character compatibility](/character-compatibility/).

## In plain words

You have a table. Each row is a species, and each column is a trait, such as "has feathers" or the base at one position of a gene. You want a family tree for the species in which each trait value appeared one time only. A trait may change from one value to another, but it never comes back to a value it had before, and two branches never invent the same value on their own.

If such a tree exists, it is called a perfect phylogeny. It explains the table with the fewest possible changes, one change for each new trait value. Real data are rarely this clean, but the question matters because some kinds of data, such as rare mutations in a short piece of DNA, are expected to behave this way.

## Definition

**Input.** A set $X$ of $n$ taxa and $m$ characters. Character $c$ is a function $c : X \to \{0, 1, \ldots, r - 1\}$ that gives each taxon one of at most $r$ states. The data form an $n \times m$ matrix $M$ with $M[x][c] = c(x)$. A character is *binary* if $r = 2$.

**A perfect phylogeny** for $M$ is a tree $T$ whose nodes carry vectors in $\{0, \ldots, r-1\}^m$, with these two properties.

1. Every row of $M$ is the vector of some node of $T$.
2. For every character $c$ and every state $s$, the nodes whose vector has value $s$ at $c$ form a connected subtree of $T$ (possibly empty).

Property 2 is called *convexity*. It says that each state of each character arises on one edge only and is never lost and regained. A row may sit at an internal node; attaching a leaf with the same vector gives an equivalent tree with the taxa at the leaves. For a binary character, property 2 says that the character changes on at most one edge.

**The question.** Does $M$ have a perfect phylogeny? If so, output one.

**The rooted binary version.** Here $r = 2$ and an ancestor vector is given, usually all zero. The tree must contain a node with this vector, and each character changes from its ancestral state to the other state at most one time, on the way down from the root. Each nonzero column then labels exactly one edge, and the path from the root to the leaf of row $x$ crosses exactly the columns where row $x$ holds a 1.

The model is the one of discrete characters: $n$ taxa, $m$ characters, at most $r$ states per character, unordered states, and no missing entries. The tree need not be binary. Time is counted on the [word RAM](/word-ram/), with the matrix as input.

## Variants

- **Binary, rooted.** The ancestor is all zero. A tree exists if and only if the sets $O_c = \{\, x : M[x][c] = 1 \,\}$ are pairwise disjoint or nested, so if and only if no two columns show all three of 01, 10 and 11.
- **Binary, unrooted.** No ancestor is given. A tree exists if and only if no two columns show all four of 00, 01, 10 and 11. Complementing each column where row 1 holds a 1 turns it into the rooted version.
- **Multistate with $r$ states.** The convexity condition is now about each state class. It is not pairwise any more, and the problem is NP-complete when $r$ is part of the input.
- **Fixed number of characters.** McMorris, Warnow and Wimer showed in 1994 that the problem is polynomial when $m$ is fixed.
- **Directed multistate characters.** A character may come with a character state tree that fixes the allowed order of changes. This is the cladistic setting of Estabrook and McMorris.
- **Missing entries.** Some entries are unknown, and the question is whether they can be filled so that a perfect phylogeny exists. The pairwise test no longer works, even for binary data, as the [four-gamete condition](/four-gamete-condition/) page shows.
- **Haplotypes.** In perfect phylogeny haplotyping, each input row is a genotype with entries 0, 1 and 2, where 2 means that the two copies differ. The question is whether the genotypes can be split into pairs of haplotypes that have a binary perfect phylogeny. Gusfield introduced the problem in 2002 and solved it in almost linear time; later algorithms take linear time.
- **Optimization versions.** When no perfect phylogeny exists, one can keep the largest set of characters that fits, which is [character compatibility](/character-compatibility/), or remove the fewest taxa, or allow a few extra changes. A model with recombination replaces the tree by an [ancestral recombination graph](/ancestral-recombination-graph/).

## Examples

**A binary yes instance.** Five taxa A to E and five binary characters, with the all-zero ancestor.

| row | $c_0$ | $c_1$ | $c_2$ | $c_3$ | $c_4$ |
|---|---|---|---|---|---|
| A | 1 | 1 | 0 | 0 | 0 |
| B | 0 | 0 | 1 | 0 | 0 |
| C | 1 | 1 | 0 | 0 | 1 |
| D | 0 | 0 | 1 | 1 | 0 |
| E | 0 | 1 | 0 | 0 | 0 |

The sets are $O_{c_1} = \{A, C, E\}$, $O_{c_0} = \{A, C\}$, $O_{c_4} = \{C\}$, $O_{c_2} = \{B, D\}$ and $O_{c_3} = \{D\}$. They nest, so a rooted perfect phylogeny exists: `((E,(A,(C)c4)c0)c1,(B,(D)c3)c2)`, where each label is the character that changes on the edge above that node. The [Gusfield page](/gusfield-perfect-phylogeny/) traces the algorithm on this matrix.

**A binary no instance.** The four rows $00$, $01$, $10$ and $11$ have no perfect phylogeny, rooted or unrooted. Any tree for them must put the 1s of column 1 on one side of an edge and the 1s of column 2 on one side of another edge, and these two edges cut the tree into three parts, which can hold only three of the four pairs.

**Rooted no, unrooted yes.** The rows $01$, $10$ and $11$ fit the unrooted path $01 - 11 - 10$. There is no rooted tree with the all-zero ancestor, because column 1 holds 1 in rows 2 and 3, column 2 in rows 1 and 3, and these two sets overlap without nesting.

**A multistate no instance in which every pair fits.** Five taxa and three characters, with states 0, 1 and 2.

| taxon | $c_1$ | $c_2$ | $c_3$ |
|---|---|---|---|
| A | 0 | 0 | 0 |
| B | 1 | 1 | 1 |
| C | 2 | 1 | 0 |
| D | 0 | 0 | 2 |
| E | 1 | 0 | 2 |

Each pair of characters has a perfect phylogeny, and on 5 taxa it is unique among the 15 unrooted binary trees. All three characters together have none. The [character compatibility](/character-compatibility/) page gives the trees and the reason.

## Known algorithms

| case | method | time | source |
|---|---|---|---|
| binary, rooted or unrooted | pairwise four-gamete test, no tree | $O(nm^2)$ | Estabrook, Johnson and McMorris 1976 |
| binary, rooted or unrooted | [Gusfield's algorithm](/gusfield-perfect-phylogeny/), with the tree | $O(nm)$ | Gusfield 1991 |
| $r = 3$ | convex realizations of partitions | polynomial | Dress and Steel 1992 |
| fixed $r$ | dynamic programming over subsets of characters | $O(2^{3r}(nm^3 + m^4))$ | Agarwala and Fernández-Baca 1994 |
| fixed $r$ | improved dynamic programming, also lists all minimal trees | $O(2^{2r} n m^2)$ | Kannan and Warnow 1997 |
| fixed $m$ | triangulation of the partition intersection graph | polynomial in $n$ and $r$ | McMorris, Warnow and Wimer 1994 |
| general $r$ | none known in polynomial time | NP-complete | Bodlaender, Fellows and Warnow 1992; Steel 1992 |

For binary data the $O(nm)$ bound is linear in the size of the matrix.

## Bounds

- **Binary data.** The problem is solvable in $O(nm)$ time, which is linear in the input size. When the answer is yes, a tree exists with at most $m + 1$ internal nodes, one for each distinct nonzero column and one for the root.
- **Multistate data.** The decision problem is NP-complete when the number of states is part of the input. Bodlaender, Fellows and Warnow and, independently, Steel proved this in 1992. So no polynomial algorithm is known, and none exists unless P = NP.
- **Fixed parameters.** For a fixed number of states $r$, the time is polynomial in $n$ and $m$, with a factor $2^{O(r)}$. For a fixed number of characters $m$, it is polynomial in $n$ and $r$.
- **Change count.** A perfect phylogeny of character $c$ with $r_c$ observed states has exactly $r_c - 1$ changes of $c$, which is the minimum on any tree. So a perfect phylogeny exists if and only if the [maximum parsimony](/maximum-parsimony/) score of $M$ equals $\sum_c (r_c - 1)$.

## Reductions

- **Unrooted to rooted, binary.** Complement each column in which the first row holds a 1. A column and its complement change on the same edge, so the two problems have the same trees. This takes $O(nm)$ time.
- **To parsimony.** As in the change count above, the matrix has a perfect phylogeny if and only if some tree has parsimony score $\sum_c (r_c - 1)$. Every tree has at least this score. So perfect phylogeny is the special case of [maximum parsimony](/maximum-parsimony/) in which the lower bound is reached. For binary characters with the all-zero ancestor, a perfect phylogeny is also a tree in which each character changes from 0 to 1 once and never back, which is the irreversible model of [Camin-Sokal parsimony](/camin-sokal-parsimony/) with exactly one change per character.
- **To splits.** A binary character is a split of the taxa. A binary matrix has an unrooted perfect phylogeny if and only if its splits are pairwise compatible, which is the splits-equivalence theorem on the [splits of a tree](/splits-of-a-tree/) page.
- **To graph triangulation.** Build the *partition intersection graph*: one vertex for each pair (character, state), and an edge between two vertices when some taxon has both. Color each vertex by its character. A perfect phylogeny exists if and only if this graph has a chordal supergraph in which no edge joins two vertices of the same color. Buneman found this link, and it is the base of the fixed-parameter algorithms. See Semple and Steel, Chapter 4.

## Applications

- **Population genetics.** Under the infinite sites model with no recombination, each site mutates at most one time, so the haplotypes of a sample have a binary perfect phylogeny. A no answer is evidence of recombination or repeated mutation, and the pairs of sites that fail locate it. See [ancestral recombination graph inference](/ancestral-recombination-graph-inference/).
- **Tumor evolution.** Many methods for cancer phylogenies assume that each somatic mutation arose once and was never lost, which is the rooted binary perfect phylogeny with the normal cell as the all-zero ancestor.
- **Haplotype inference.** Perfect phylogeny haplotyping recovers the haplotypes of a sample from unphased genotypes under the same no recombination model.
- **Historical linguistics.** Ringe, Warnow and Taylor used multistate perfect phylogeny methods on lexical, phonological and morphological characters of the Indo-European languages.
- **Character analysis in systematics.** Compatibility methods, which keep the characters that fit one tree without conflict, are built on the perfect phylogeny question.

## References
