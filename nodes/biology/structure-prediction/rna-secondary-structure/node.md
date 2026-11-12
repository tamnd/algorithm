---
tag: B1DFYM
kind: definition
slug: rna-secondary-structure
name: RNA secondary structure
aliases:
- Nested base pairs
- RNA base-pair structure
- Dot-bracket structure
- Pseudoknot-free structure
area: biology/structure-prediction
level: intro
summary: A set of base pairs of an RNA sequence with allowed pair types, at least three bases in each hairpin, no shared bases and no crossing pairs.
prereqs: []
see_also: [rna-secondary-structure-prediction, nussinov-algorithm, zuker-algorithm, pseudoknot, nearest-neighbor-model, dyck-word, catalan-numbers, outerplanar-graph]
sources:
  - paper: doi:10.1016/0012-365X(79)90033-5
    title: Paul R. Stein and Michael S. Waterman, On some new sequences generalizing the Catalan and Motzkin numbers, Discrete Mathematics 26(3), 1979, pages 261 to 272
    locator: the number of secondary structures of a sequence of length n with a minimum hairpin size, and its recurrence
  - paper: "Michael S. Waterman, Secondary structure of single-stranded nucleic acids, Studies in Foundations and Combinatorics, Advances in Mathematics Supplementary Studies 1, 1978, pages 167 to 212"
    title: Secondary structure of single-stranded nucleic acids
    locator: the combinatorial definition of secondary structure as a set of non-crossing pairs
  - paper: doi:10.1016/S0166-218X(98)00073-0
    title: Ivo L. Hofacker, Peter Schuster and Peter F. Stadler, Combinatorics of RNA secondary structures, Discrete Applied Mathematics 88, 1998, pages 207 to 237
    locator: generating functions and the growth rates of the numbers of secondary structures
  - book: isbn:9780521629713
    title: Richard Durbin, Sean R. Eddy, Anders Krogh and Graeme Mitchison, Biological Sequence Analysis, Cambridge University Press, 1998
    locator: Chapter 10, RNA structure analysis, Section 10.2, the terms of RNA secondary structure (stems, loops and pseudoknots)
---

An RNA secondary structure is the set of base pairs that an RNA strand forms when it folds back on itself, in the form that ignores the shape in space. The pairs must be of allowed types, each base pairs at most once, the loop at the tip of a hairpin must have some minimum size, and two pairs must not cross. Without crossings, the pairs nest like brackets, so a structure can be written as a string of dots and brackets. This nesting is what makes interval dynamic programs such as the [Nussinov algorithm](/nussinov-algorithm/) and the [Zuker algorithm](/zuker-algorithm/) possible. Pairs that cross form a [pseudoknot](/pseudoknot/), which is not a secondary structure in this sense.

## Definition

Let $s = s_1 s_2 \cdots s_n$ be a sequence over the alphabet $\{A, C, G, U\}$. Let $\mathcal{B}$ be the set of allowed pairs, usually the Watson-Crick pairs AU and GC and the wobble pair GU, in both orders:

$$\mathcal{B} = \{AU, UA, GC, CG, GU, UG\}.$$

Let $\theta \ge 0$ be the hairpin minimum, usually $\theta = 3$. A **secondary structure** of $s$ is a set $P$ of pairs $(i, j)$ with $1 \le i < j \le n$ such that:

1. **Allowed pairs.** $s_i s_j \in \mathcal{B}$ for each $(i, j) \in P$.
2. **Hairpin minimum.** $j - i - 1 \ge \theta$ for each $(i, j) \in P$: at least $\theta$ bases lie between the two ends of a pair.
3. **No shared bases.** Each position $1, \ldots, n$ is an end of at most one pair of $P$.
4. **No crossing.** There are no two pairs $(i, j)$ and $(k, l)$ in $P$ with $i < k < j < l$.

Rule 4 means that any two pairs are nested, $i < k < l < j$, or side by side, $i < j < k < l$. Rules 1 and 2 depend on the model: some papers allow any two bases to pair, or use $\theta = 0$. Each page in this area states its model.

**Dot-bracket notation.** Write a string $w_1 \cdots w_n$ with $w_i = ($ if $i$ is the left end of a pair, $w_j = )$ if $j$ is the right end, and $w_x = .$ if $x$ is unpaired. Because of rule 4, the brackets are balanced, and each closing bracket matches the nearest open bracket that is not yet closed. So the map from structures to dot-bracket strings is a bijection between the sets of pairs that satisfy rules 3 and 4 and the strings over $\{(, ), .\}$ whose brackets are balanced. Rules 1 and 2 then restrict which strings are allowed for a given $s$.

**Loops.** Each pair $(i, j)$ closes one loop: the bases inside $(i, j)$ that are not inside a pair that is itself inside $(i, j)$. The loop is a hairpin, a stack, a bulge, an interior loop or a multiloop, by the number and the place of the pairs directly inside it. The bases outside all pairs form the exterior loop. A run of stacked pairs is a helix, or stem. The energy models of the [nearest-neighbor model](/nearest-neighbor-model/) give an energy to each loop.

**The number of structures.** Let $S_\theta(n)$ be the number of sets of pairs on $n$ positions that satisfy rules 2 to 4, when any two bases can pair. Base $n$ is unpaired, or it pairs with some $k \le n - \theta - 1$, and then the pairs split into a structure of the $k - 1$ positions before $k$ and one of the $n - k - 1$ positions inside. So

$$S_\theta(n) = S_\theta(n - 1) + \sum_{k = 1}^{n - \theta - 1} S_\theta(k - 1)\, S_\theta(n - k - 1), \qquad S_\theta(n) = 1 \text{ for } n \le \theta + 1.$$

For $\theta = 0$ these are the Motzkin numbers $1, 1, 2, 4, 9, 21, 51, \ldots$. For $\theta = 3$ the sequence starts $1, 1, 1, 1, 1, 2, 4, 8, 16, 32, 65$ for $n = 0, \ldots, 10$, and $S_3(30) = 240{,}944{,}076$. Stein and Waterman (1979) studied these numbers. They grow exponentially: for $\theta = 3$ the ratio $S_3(n + 1) / S_3(n)$ tends to about $2.2888$, and Hofacker, Schuster and Stadler (1998) give the asymptotic forms $c\, n^{-3/2} \alpha^n$ from the [generating function](/generating-functions/). So the structures cannot be listed one by one, and prediction needs [interval dynamic programming](/interval-dp/).

## Examples and non-examples

In these examples $\theta = 3$ and $\mathcal{B}$ is AU, GC and GU.

- **A hairpin.** The sequence GGGAAAUCC has the structure (((...))), with the pairs $(1, 9)$, $(2, 8)$ and $(3, 7)$. Each pair is allowed (GC, GC and GU), and the hairpin has 3 unpaired bases.
- **Two hairpins side by side.** GCAAAGCAAAGC has the structure ((...)(...)), with the pairs $(1, 12)$, $(2, 6)$ and $(7, 11)$. The pairs $(2, 6)$ and $(7, 11)$ are side by side, and both are nested in $(1, 12)$. The pair $(1, 12)$ closes a multiloop with two inner branches.
- **The empty structure.** The empty set is a secondary structure of every sequence. Its dot-bracket string has only dots.
- **Not a structure: a short hairpin.** In GGAACC, the set $\{(1, 6), (2, 5)\}$ breaks rule 2, because the pair $(2, 5)$ has only 2 bases inside. The string ((..)) is balanced, but it is not allowed for $\theta = 3$.
- **Not a structure: a pair that is not allowed.** In AAAAAAC, the set $\{(1, 7)\}$ breaks rule 1, because A does not pair with C.
- **Not a structure: a shared base.** In GAAACAC, the set $\{(1, 5), (1, 7)\}$ breaks rule 3, because base 1 is in two pairs. Real RNAs have base triples, but they are tertiary contacts, outside the model.
- **Not a structure: crossing pairs.** In GAAGAAACAAAC, the pairs $(1, 8)$ and $(4, 12)$ are both GC pairs with enough bases inside, but $1 < 4 < 8 < 12$, which breaks rule 4. This is a [pseudoknot](/pseudoknot/). It cannot be written with one kind of bracket; the extended notation uses a second kind, as in (..[...)...].

## Related definitions

- **Arc diagram and outerplanar graph.** Draw the bases on a line and each pair as an arc above it. Rule 4 says that no two arcs cross. With the backbone as a path, a secondary structure is a graph whose vertices lie on one face, an [outerplanar graph](/outerplanar-graph/).
- **Dyck words and trees.** A structure in which every base is paired, with $\theta = 0$, is a [Dyck word](/dyck-word/), so these are counted by the [Catalan numbers](/catalan-numbers/). A general structure is a [rooted tree](/rooted-tree/) of loops: the exterior loop is the root, and the loop closed by each pair is a child of the loop that contains the pair.
- **Matching.** A structure is a matching in the graph whose edges are the allowed pairs, with the extra rules 2 and 4. Without rule 4, the largest set of pairs is a [maximum matching](/maximum-matching/) problem.
- **Pseudoknot.** A set of pairs that satisfies rules 1 to 3 but not rule 4. See [pseudoknot](/pseudoknot/).
- **Secondary structure prediction.** The task of finding the structure of a given sequence. See [RNA secondary structure prediction](/rna-secondary-structure-prediction/).

## References
