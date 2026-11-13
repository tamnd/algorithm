---
tag: A1T1QQ
kind: problem
slug: maximum-quartet-consistency
name: Maximum quartet consistency
aliases:
- MaxQC
area: biology/phylogenetics
level: advanced
summary: Given quartets, find an unrooted tree that displays as many as possible. NP-hard; a PTAS exists when every four taxa have a quartet.
prereqs: [quartet, np-hard]
see_also: [quartet-max-cut, astral, maximum-rooted-triplet-consistency, supertree, ptas, approximation-ratio, species-tree-estimation, method-of-conditional-expectations]
sources:
  - paper: doi:10.1007/BF02618470
    title: Mike Steel, The complexity of reconstructing trees from qualitative characters and subtrees, Journal of Classification 9(1), 1992, pages 91 to 116
    locator: NP-completeness of quartet compatibility, which makes the optimization problem NP-hard
  - paper: "Tao Jiang, Paul Kearney and Ming Li, A polynomial time approximation scheme for inferring evolutionary trees from quartet topologies and its application, SIAM Journal on Computing 30(6), 2001, pages 1942 to 1961"
    title: Tao Jiang, Paul Kearney and Ming Li, A polynomial time approximation scheme for inferring evolutionary trees from quartet topologies and its application
    locator: a PTAS for the complete case, with one quartet for every set of four taxa
  - paper: doi:10.1109/TCBB.2008.133
    title: Sagi Snir and Satish Rao, Quartets MaxCut, a divide and conquer quartets algorithm, IEEE/ACM Transactions on Computational Biology and Bioinformatics 7(4), 2010, pages 704 to 718
    locator: the max-cut heuristic for quartet amalgamation
  - book: isbn:9780198509424
    title: Charles Semple and Mike Steel, Phylogenetics, Oxford University Press, 2003
    locator: Chapter 6, Subtrees and supertrees
  - book: isbn:9781107184718
    title: Tandy Warnow, Computational Phylogenetics, 2017
    locator: Chapter 7, Supertrees
---

Maximum quartet consistency (MQC) asks for an unrooted binary [phylogenetic tree](/phylogenetic-tree/) that displays as many [quartets](/quartet/) as possible from a given set. A quartet $ab|cd$ is the smallest unrooted statement about a tree: the path between $a$ and $b$ does not meet the path between $c$ and $d$. Deciding whether one tree displays all the quartets is already NP-complete (Steel 1992), so MQC is [NP-hard](/np-hard/). When the input has one quartet for every set of four taxa, Jiang, Kearney and Li (2001) give a [PTAS](/ptas/). In practice, heuristics such as [Quartet MaxCut](/quartet-max-cut/) and the constrained exact search of [ASTRAL](/astral/) are used.

## In plain words

A quartet is a statement about four species: a and b are on one side of the tree, and c and d are on the other side. Many such statements come from small analyses, from gene trees, or from comparing four sequences at a time. They often disagree. You want one tree for all the species that agrees with as many statements as you can.

For rooted statements on three species, there is a fast test for whether all of them fit one tree. For quartets there is none, unless P equals NP: even the yes or no question is hard. So the methods either give up on a perfect answer and settle for a good tree, or search only a limited set of trees.

## Definition

**Quartets.** For four distinct taxa, the quartet $ab|cd$ is the unrooted binary tree with the cherries $\{a, b\}$ and $\{c, d\}$. An unrooted tree $T$ *displays* $ab|cd$ if $T$ has an edge whose removal puts $a$ and $b$ on one side and $c$ and $d$ on the other. Equivalently, $ab \mid cd$ is a restriction of a [split](/splits-of-a-tree/) of $T$.

**Input.** A finite set $X$ of $n$ taxa and a set $Q$ of $m$ quartets on taxa of $X$. In the weighted version, each quartet has a weight $w(q) \ge 0$.

**Output.** An unrooted binary tree $T$ with leaf set $X$ that maximizes the number (or total weight) of quartets in $Q$ that $T$ displays.

A binary tree displays exactly one of the three quartets $ab|cd$, $ac|bd$ and $ad|bc$ on each set of four taxa. A tree with a multifurcation can display none of them, so a binary tree is always among the optimal trees.

## Variants

- **Quartet compatibility (decision).** Does some tree display all of $Q$? NP-complete in general (Steel 1992). For a complete set, with one quartet for every set of four taxa, it can be decided in polynomial time, because the tree must then be the one tree that the quartets determine.
- **Complete or dense input.** $Q$ has exactly one quartet for each set of four taxa. This is the case of the PTAS of Jiang, Kearney and Li (2001).
- **Weighted quartets.** Each quartet has a weight, for example the number of gene trees that display it. Maximizing the total weight over all trees is the optimization behind [ASTRAL](/astral/), which solves it exactly inside a restricted set of allowed splits.
- **Minimum quartet inconsistency.** Minimize the number of quartets that are not displayed. It has the same optimal trees.
- **Rooted analog.** For rooted trees and rooted triplets, the problem is [maximum rooted triplet consistency](/maximum-rooted-triplet-consistency/). There, the decision version is polynomial.

## Examples

**Six quartets on five taxa.** Let $X = \{a, b, c, d, e\}$ and
$$Q = \{ab|cd,\ ac|be,\ ad|ce,\ bc|de,\ ab|de,\ ae|cd\}.$$
A brute force over all 15 unrooted binary trees on five taxa finds that the best tree displays 3 of the 6 quartets, and five trees reach this value. Two of them, written by their nontrivial splits, are:

| tree | splits | displayed quartets |
|---|---|---|
| `((a,b),c,(d,e));` | $ab \mid cde$, $abc \mid de$ | $ab|cd$, $bc|de$, $ab|de$ |
| `((b,e),a,(c,d));` | $be \mid acd$, $abe \mid cd$ | $ab|cd$, $ac|be$, $ae|cd$ |

No tree displays four, so $Q$ is not compatible. One conflict is direct: the set $\{a, c, d, e\}$ carries two different quartets, $ad|ce$ and $ae|cd$, and a tree displays at most one of them. The other conflicts involve several sets of four taxa at once, and only the brute force shows that three quartets must be lost.

**The one third bound on this input.** Place the taxa in a random order on a caterpillar. A quartet on four taxa is displayed exactly when its two pairs are the first two and the last two of the four in that order, which has probability $2 / \binom{4}{2} = 1/3$. So a random caterpillar displays $6/3 = 2$ quartets on average, and the optimum is 3.

**All quartets.** On five taxa, the set of all $3 \binom{5}{4} = 15$ quartets has the best value 5. Each binary tree displays exactly one quartet of each set of four taxa, so the value is one third, and no tree does better.

## Known algorithms

| method | type | guarantee |
|---|---|---|
| brute force over all $(2n-5)!!$ binary trees | exact | optimal, exponential time |
| random caterpillar, derandomized by [conditional expectations](/method-of-conditional-expectations/) | approximation | at least $m/3$ quartets |
| Jiang, Kearney and Li (2001) | PTAS for complete input | $(1 - \epsilon)$ of the optimum in polynomial time for each fixed $\epsilon$ |
| [ASTRAL](/astral/) | exact on a restricted set of splits | optimal among trees whose splits come from a given set |
| [Quartet MaxCut](/quartet-max-cut/) (Snir and Rao) | divide and conquer heuristic | no worst-case guarantee |
| quartet puzzling | randomized heuristic | no worst-case guarantee |

## Bounds

- **Lower bound for every input.** Some tree displays at least $\lceil m/3 \rceil$ quartets, by the caterpillar argument. So the simple algorithm has [approximation ratio](/approximation-ratio/) 3.
- **Upper bound for the full set.** If $Q$ holds all three quartets of every set of four taxa, every tree displays exactly $m/3$ of them, so the constant $1/3$ cannot be improved as a guarantee in terms of $m$.
- **Hardness.** Quartet compatibility is NP-complete (Steel 1992). So MQC is NP-hard, because a tree with value $m$ exists exactly when $Q$ is compatible.
- **Complete input.** For complete input, the optimum is at least $\binom{n}{4}/3$, and the PTAS of Jiang, Kearney and Li reaches any constant factor close to 1.

## Reductions

- **From unrooted supertrees.** An unrooted tree displays an input tree exactly when it displays all quartets of that tree. So an unrooted [supertree](/supertree/) problem becomes an MQC instance with all quartets of all input trees.
- **From gene trees.** Weighting each quartet by the number of gene trees that display it gives the weighted problem that [ASTRAL](/astral/) solves for [species tree estimation](/species-tree-estimation/). Under the [multispecies coalescent](/multispecies-coalescent/), the most frequent quartet on each set of four taxa is the species tree quartet, so the optimal tree is a consistent estimate.
- **To max-cut.** [Quartet MaxCut](/quartet-max-cut/) splits the taxa into two sides with a [maximum cut](/maximum-cut/) of a graph built from the quartets, so that many quartets have their two pairs on opposite sides.
- **Rooting.** Adding a new taxon $r$ to all trees maps a rooted triplet $ab|c$ to the quartet $ab|cr$. This shows that rooted triplet problems are special cases of quartet problems.

## Applications

- **Species trees from gene trees.** Quartet based methods are statistically consistent under [incomplete lineage sorting](/incomplete-lineage-sorting/), which makes weighted MQC the core of widely used species tree methods.
- **Supertrees.** Combining unrooted trees on overlapping taxon sets.
- **Large trees.** Quartet methods can build trees from many small analyses of four taxa each, which are fast and accurate.

## References
