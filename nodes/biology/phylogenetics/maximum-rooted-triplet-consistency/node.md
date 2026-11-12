---
tag: JRWKR0
kind: problem
slug: maximum-rooted-triplet-consistency
name: Maximum rooted triplet consistency
aliases:
- MaxRTC
area: biology/phylogenetics
level: advanced
summary: Given rooted triplets, find a rooted tree that displays as many as possible. NP-hard; a tree that displays one third of them always exists.
prereqs: [rooted-triplet, np-hard]
see_also: [supertree, maximum-quartet-consistency, method-of-conditional-expectations, approximation-ratio, consensus-tree, species-tree-estimation, phylogenetic-network-inference, adams-consensus]
sources:
  - paper: "David Bryant, Building trees, hunting for trees, and comparing trees: theory and methods in phylogenetic analysis, PhD thesis, University of Canterbury, 1997"
    title: David Bryant, Building trees, hunting for trees, and comparing trees, PhD thesis, 1997
    locator: the proof that the maximum rooted triplet consistency problem is NP-hard
  - paper: "Jesper Jansson, On the complexity of inferring rooted evolutionary trees, Proceedings of GRACO 2001, Electronic Notes in Discrete Mathematics 7, 2001"
    title: Jesper Jansson, On the complexity of inferring rooted evolutionary trees
    locator: NP-hardness of the maximum and minimum versions of rooted triplet consistency
  - paper: doi:10.1023/A:1009833626004
    title: Leszek Gąsieniec, Jesper Jansson, Andrzej Lingas and Anna Östlin, On the complexity of constructing evolutionary trees, Journal of Combinatorial Optimization 3(2/3), 1999, pages 183 to 197
    locator: a polynomial algorithm for a tree consistent with at least one third of the triplets, and the optimality of one third for the set of all triplets
  - paper: "Jaroslaw Byrka, Sylvain Guillemot and Jesper Jansson, New results on optimizing rooted triplets consistency, ISAAC 2008, LNCS 5369, 2008"
    title: Jaroslaw Byrka, Sylvain Guillemot and Jesper Jansson, New results on optimizing rooted triplets consistency
    locator: NP-hardness for dense inputs, with one triplet for each set of three taxa, and approximation results
  - paper: doi:10.1137/0210030
    title: Alfred V. Aho, Yehoshua Sagiv, Thomas G. Szymanski and Jeffrey D. Ullman, Inferring a tree from lowest common ancestors with an application to the optimization of relational expressions, SIAM Journal on Computing 10(3), 1981, pages 405 to 421
    locator: the BUILD algorithm, which solves the case where all triplets are consistent
  - book: isbn:9780198509424
    title: Charles Semple and Mike Steel, Phylogenetics, Oxford University Press, 2003
    locator: Chapter 6, Subtrees and supertrees
---

Maximum rooted triplet consistency (MaxRTC) asks for a rooted [phylogenetic tree](/phylogenetic-tree/) that displays as many triplets as possible from a given set of [rooted triplets](/rooted-triplet/). When some tree displays all of them, the BUILD algorithm of Aho, Sagiv, Szymanski and Ullman (1981) finds it in polynomial time. In general the problem is [NP-hard](/np-hard/) (Bryant 1997, Jansson 2001), but a tree that displays at least one third of the triplets always exists and can be found in polynomial time (Gąsieniec, Jansson, Lingas and Östlin 1999). It is the rooted form of the [supertree](/supertree/) problem.

## In plain words

A rooted triplet is the smallest statement about a family tree: of the three species a, b and c, the two species a and b are more closely related to each other than to c. Different experiments give you many such statements, and some of them disagree. You want one tree for all the species that agrees with as many statements as you can.

If no statements disagree, a classic method builds the tree fast. When they do disagree, finding the best tree is hard, and nobody knows a fast method that is always right. But a tree that agrees with one third of the statements is easy to get: put the species in a random order on a ladder-shaped tree, and each statement holds with chance one third.

## Definition

**Triplets.** For distinct taxa $a, b, c$, the rooted triplet $ab|c$ is the rooted tree `((a,b),c);`. A rooted tree $T$ *displays* $ab|c$ if $T$ has a cluster that contains $a$ and $b$ but not $c$, which means that the lowest common ancestor of $a$ and $b$ is a proper descendant of the lowest common ancestor of all three.

**Input.** A finite set $X$ of $n$ taxa and a set $R$ of $m$ rooted triplets on taxa of $X$. In the weighted version, each triplet has a weight $w(t) \ge 0$.

**Output.** A rooted tree $T$ with leaf set $X$ that maximizes the number (or total weight) of triplets in $R$ that $T$ displays.

An optimal tree can always be taken to be binary: refining a node keeps every cluster, so it keeps every displayed triplet. A binary tree displays exactly one of the three triplets $ab|c$, $ac|b$ and $bc|a$ on each set of three taxa.

## Variants

- **Consistency (decision).** Is there a tree that displays all of $R$? BUILD answers this in polynomial time and returns such a tree. The [rooted triplet](/rooted-triplet/) page gives the algorithm.
- **Minimum rooted triplet inconsistency.** Minimize the number of triplets that the tree does not display. It has the same optimal trees, but the approximation question is different, because the optimum can be 0.
- **Dense input.** $R$ has exactly one triplet for each set of three taxa. Byrka, Guillemot and Jansson (2008) showed that MaxRTC stays NP-hard in this case.
- **Weighted triplets.** Triplets come with weights, for example the number of gene trees that show them.
- **Networks.** Find a level-1 [phylogenetic network](/phylogenetic-network/) that is consistent with the triplets, which allows a tree to explain conflicting triplets by reticulation. See [phylogenetic network inference](/phylogenetic-network-inference/).
- **Unrooted analog.** For unrooted trees and quartets, the problem is [maximum quartet consistency](/maximum-quartet-consistency/).

## Examples

**Seven triplets on five taxa.** Let $X = \{a, b, c, d, e\}$ and
$$R = \{ab|c,\ bc|d,\ cd|a,\ da|b,\ ae|b,\ ce|d,\ be|d\}.$$
The first four triplets alone are not consistent: the BUILD graph on $abcd$ has the edges ab, bc, cd and da, which is one connected component. A brute force over all 105 rooted binary trees on five taxa finds that the best tree displays 5 of the 7 triplets, and that only one binary tree does:

`((((a,e),b),c),d);`

Its clusters are ae, abe and abce. It displays $ab|c$, $bc|d$, $ae|b$, $ce|d$ and $be|d$, and it misses $cd|a$ and $da|b$.

**The one third bound on this input.** Place the taxa in a random order $x_1, \ldots, x_5$ on the caterpillar `((((x1,x2),x3),x4),x5);`. A triplet $ab|c$ is displayed exactly when $c$ comes after both $a$ and $b$, which has probability $1/3$. The average over all 120 orders is $7/3$ displayed triplets, as the script checks.

**All triplets.** On four taxa, the set of all $3 \binom{4}{3} = 12$ triplets has the best value 4, which is one third. A binary tree displays exactly one triplet of each set of three taxa, so no tree can do better.

## Known algorithms

- **BUILD.** If $R$ is consistent, BUILD returns a tree that displays all of $R$ in $O(n(n + m))$ time, as the [rooted triplet](/rooted-triplet/) page shows. If $R$ is not consistent, BUILD reports this but gives no tree.
- **One third of the triplets.** A random caterpillar displays $m/3$ triplets in expectation. The [method of conditional expectations](/method-of-conditional-expectations/) turns this into a deterministic algorithm: choose the order of the taxa one position at a time, each time keeping the expected count of the rest of the random order at least $m/3$. Gąsieniec, Jansson, Lingas and Östlin (1999) give a polynomial algorithm with this guarantee. This gives an [approximation ratio](/approximation-ratio/) of 3.
- **Exact dynamic program.** For each subset $S$ of taxa, let $f(S)$ be the best number of triplets with all three taxa in $S$ that a binary tree on $S$ displays. Then $f(S) = \max \{ f(S_1) + f(S_2) + g(S_1, S_2) \}$ over the splits of $S$ into two nonempty parts, where $g$ counts the triplets $ab|c$ with $a, b$ in one part and $c$ in the other. There are $O(3^n)$ pairs $(S, S_1)$, so the time is $O(3^n)$ times the cost of $g$. On the example, this gives 5.
- **Heuristics.** Greedy merging of clusters by triplet support, and local search over trees.

## Bounds

- **Lower bound for every input.** Some tree displays at least $\lceil m/3 \rceil$ triplets, by the caterpillar argument.
- **Upper bound for the full set.** If $R$ holds all three triplets of every set of three taxa, every tree displays at most $m/3$ of them. So the constant $1/3$ cannot be improved as a guarantee in terms of $m$.
- **Hardness.** MaxRTC is NP-hard (Bryant 1997, Jansson 2001), and so is its weighted version. It stays NP-hard for dense inputs (Byrka, Guillemot and Jansson 2008).

## Reductions

- **From rooted trees.** A rooted tree is the same as the set of all its triplets. So a [supertree](/supertree/) problem for rooted input trees becomes a MaxRTC instance with one triplet for each triplet of each input tree.
- **From gene trees.** Count, for each set of three taxa, the triplets of a set of gene trees, and use the counts as weights. A tree with the largest total weight is a triplet based estimate of the species tree. This is the rooted analog of the quartet method [ASTRAL](/astral/).
- **To networks.** When no tree fits the triplets well, a level-1 network can display more of them. This leads to [phylogenetic network inference](/phylogenetic-network-inference/) from triplets.

## Applications

- **Supertrees.** Combining rooted trees on overlapping taxon sets.
- **Species trees.** Summarizing many rooted gene trees, which disagree because of [incomplete lineage sorting](/incomplete-lineage-sorting/) and other causes, into one species tree.
- **Triplet data from experiments.** Some data give relations of three taxa directly, for example comparisons of three sequences against an outgroup.

## References
