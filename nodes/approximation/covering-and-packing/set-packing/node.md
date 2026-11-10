---
tag: EV36V3
kind: problem
slug: set-packing
name: Set packing problem
aliases:
- maximum set packing
- set packing
- k-set packing
area: approximation/covering-and-packing
level: intro
summary: Choose the largest collection of pairwise disjoint sets.
prereqs: [np-complete, approximation-ratio, independent-set, greedy-algorithm]
see_also: [set-cover, independent-set, packing-integer-program, three-dimensional-matching, maximum-matching, karps-21-np-complete-problems, local-search, parameterized-set-packing]
sources:
  - paper: "R. M. Karp, Reducibility among combinatorial problems, in Complexity of Computer Computations, Plenum Press, 1972, pp. 85-103"
    title: Karp 1972
    locator: the list of 21 NP-complete problems, which includes set packing
  - paper: "C. A. J. Hurkens and A. Schrijver, On the size of systems of sets every t of which have an SDR, with an application to the worst-case ratio of heuristics for packing problems, SIAM Journal on Discrete Mathematics 2(1), 1989, pp. 68-72"
    title: Hurkens and Schrijver 1989
    locator: the local search ratio k/2 + epsilon for k-set packing
  - paper: "E. Hazan, S. Safra and O. Schwartz, On the complexity of approximating k-set packing, Computational Complexity 15(1), 2006, pp. 20-39"
    title: Hazan, Safra and Schwartz 2006
    locator: the hardness ratio Omega(k / log k)
  - paper: "M. Cygan, Improved approximation for 3-dimensional matching via bounded pathwidth local search, FOCS 2013, pp. 509-518"
    title: Cygan 2013
    locator: the ratio (k + 1 + epsilon) / 3 for k-set packing
  - paper: "P. Berman, A d/2 approximation for maximum weight independent set in d-claw free graphs, Nordic Journal of Computing 7(3), 2000, pp. 178-184"
    title: Berman 2000
    locator: the ratio (k + 1) / 2 for weighted k-set packing
---

The set packing problem gives a family of sets and asks for the largest number of sets that are pairwise disjoint. It is one of [Karp's 21 NP-complete problems](/karps-21-np-complete-problems/), and it is as hard to approximate as [independent set](/independent-set/): no polynomial-time algorithm has ratio $m^{1/2 - \varepsilon}$, where $m$ is the size of the universe, unless P = NP. The greedy rule that takes the smallest available set reaches ratio $\sqrt m$. When each set has at most $k$ elements, the problem is $k$-set packing; any maximal packing has ratio $k$, and local search reaches about $\frac{k+1}{3}$.

## In plain words

You have a list of groups, and each group is made of some people. You want to choose as many groups as possible, but no person may be in two chosen groups.

A simple rule takes a smallest group that does not share a person with the groups already chosen, and repeats. Small groups block few others, so this is a good choice, but it can still be far from the best answer. If every group is small, say at most three people, then any choice that cannot be extended is within a factor three of the best, and trying small swaps does even better.

## Definition

The input is a universe $U$ with $|U| = m$ and a family $\mathcal{S} = \{S_1, \ldots, S_n\}$ of nonempty subsets of $U$. A *packing* is a subfamily $\mathcal{P} \subseteq \mathcal{S}$ whose sets are pairwise disjoint. The goal is to make $|\mathcal{P}|$ as large as possible, and $\mathrm{OPT}$ is the largest size. In the weighted version each set has a weight $w(S) \ge 0$, and the goal is the largest total weight. In $k$-set packing each set has at most $k$ elements.

The decision version asks whether there is a packing with at least $t$ sets. It is NP-complete, already for $k = 3$, because [3-dimensional matching](/three-dimensional-matching/) is a special case.

*Ratio convention.* This is a maximization problem. An algorithm has ratio $\rho \ge 1$ if $\mathrm{ALG} \ge \mathrm{OPT} / \rho$ on every input. The proofs below bound $\mathrm{OPT}$ from above by counting: an optimal packing is a family of disjoint sets, so at most $|G|$ of its sets meet a given set $G$, and at most $m / s$ of its sets have $s$ or more elements.

## Variants

- **$k$-set packing.** Each set has at most $k$ elements. For $k = 2$ it is [maximum matching](/maximum-matching/) in a graph and is solvable in polynomial time; for $k \ge 3$ it is NP-hard.
- **Weighted set packing.** Sets have weights; this is the winner determination problem of combinatorial auctions.
- **Hypergraph matching.** The same problem in the words of [hypergraphs](/hypergraph/): find the largest set of pairwise disjoint edges.
- **Exact cover.** Ask for a packing that covers every element; see [exact cover](/exact-cover/).
- **Integer program.** Set packing is the [packing integer program](/packing-integer-program/) with a 0/1 matrix and right side 1.
- **Parameterized.** Decide whether $t$ disjoint sets exist, with $t$ as the parameter; see [parameterized set packing](/parameterized-set-packing/).

## Examples

Take $U = \{1, \ldots, 6\}$ and the sets $A = \{1, 2, 3\}$, $B = \{1, 4\}$, $C = \{2, 5\}$, $D = \{3, 6\}$, $E = \{4, 5, 6\}$.

| rule | chosen sets | size |
|---|---|---|
| largest available set first | $A$, then $E$; all others meet $A$ or $E$ | 2 |
| smallest available set first | $B$, $C$, $D$; then $A$ and $E$ are blocked | 3 |
| optimum | $B, C, D$ | 3 |

$\mathrm{OPT} = 3$, because each set has at least 2 elements and $m = 6$.

*A bad case for the smallest set rule.* Take a $q \times q$ grid of elements, so $m = q^2$, with the $q$ rows and one column as the sets. All sets have size $q$. If the tie is broken toward the column, the rule takes the column, and then each row meets it, so $\mathrm{ALG} = 1$ while the $q$ rows give $\mathrm{OPT} = q = \sqrt m$.

## Known algorithms

- **Any maximal packing for $k$-set packing.** Take sets in any order and keep each one that is disjoint from those kept. *Theorem.* The result has at least $\mathrm{OPT} / k$ sets. *Proof.* Each set $O$ of an optimal packing meets some kept set; otherwise $O$ would have been kept. A kept set $G$ has at most $k$ elements, and the optimal sets are disjoint, so at most $k$ of them meet $G$. So $\mathrm{OPT} \le k \cdot \mathrm{ALG}$. $\square$ For weighted $k$-set packing, taking the sets by decreasing weight gives ratio $k$ by the same charging.
- **Smallest set first.** Repeatedly take a smallest set that is disjoint from the sets already taken. Time $O(n \log n + \sum_i |S_i|)$ with sorting and a mark for each used element.
  *Theorem.* $\mathrm{OPT} \le \sqrt m \cdot \mathrm{ALG}$. *Proof.* Let $O$ be a set of an optimal packing $\mathcal{O}$. Some taken set meets $O$, or else the rule would have taken $O$ at the end; let $g(O)$ be the first taken set that meets $O$. When $g(O)$ was taken, $O$ was disjoint from all sets taken so far, so it was available, and the rule chose $g(O)$ as a smallest available set: $|g(O)| \le |O|$. Fix a taken set $G$ and let $\mathcal{O}_G = \{ O \in \mathcal{O} : g(O) = G \}$. Each set in $\mathcal{O}_G$ meets $G$ and they are disjoint, so $|\mathcal{O}_G| \le |G|$. Each set in $\mathcal{O}_G$ has at least $|G|$ elements and they are disjoint subsets of $U$, so $|\mathcal{O}_G| \le m / |G|$. So $|\mathcal{O}_G| \le \min(|G|, m/|G|) \le \sqrt m$, and summing over the taken sets gives $\mathrm{OPT} \le \sqrt m \cdot \mathrm{ALG}$. $\square$ The grid example shows that $\sqrt m$ is tight for this rule.
- **Local search for $k$-set packing.** Start with a maximal packing. While some $t$ sets of the packing can be replaced by $t + 1$ sets, for $t$ up to a constant, make the swap. Hurkens and Schrijver (1989) proved ratio $\frac k2 + \varepsilon$. Cygan (2013) and Fürer and Yu (2014) used swaps of bounded pathwidth and reached $\frac{k + 1 + \varepsilon}{3}$. See [local search](/local-search/).
- **Weighted $k$-set packing.** Berman (2000) gave ratio $\frac{k+1}{2}$ by a local search on the squares of the weights.
- **Exact algorithms.** Dynamic programming over the subsets of $U$ takes $O(2^m n)$ time; branching on sets works when $n$ is small.

## Bounds

| claim | statement | source |
|---|---|---|
| maximal packing, $k$-set packing | ratio $k$ | proved above |
| smallest set first | ratio $\sqrt m$, tight for the rule | proved above |
| hardness, general | no ratio $m^{1/2 - \varepsilon}$ and no ratio $n^{1 - \varepsilon}$, unless P = NP | from independent set, below |
| local search | $\frac k2 + \varepsilon$ | Hurkens and Schrijver 1989 |
| best for $k$-set packing | $\frac{k + 1 + \varepsilon}{3}$ | Cygan 2013; Fürer and Yu 2014 |
| hardness, $k$-set packing | no ratio $o(k / \log k)$ unless P = NP | Hazan, Safra and Schwartz 2006 |
| weighted $k$-set packing | $\frac{k+1}{2}$ | Berman 2000 |

## Reductions

- **From independent set.** For a graph with $n$ vertices and $m$ edges, let $U$ be the set of edges, and for each vertex $v$ let $S_v$ be the set of edges at $v$. Two sets $S_u$ and $S_v$ are disjoint exactly when $uv$ is not an edge, so packings are exactly independent sets. [Independent set](/independent-set/) has no polynomial-time ratio $n^{1 - \varepsilon}$ unless P = NP (Håstad 1999, Zuckerman 2007), so neither has set packing in terms of the number $n$ of sets. Since $m < n^2$, a ratio $m^{1/2 - \varepsilon}$ would give a ratio $n^{1 - 2\varepsilon}$, so that is ruled out too.
- **To independent set.** Conversely, the *conflict graph* has a vertex for each set and an edge between sets that meet; packings are its independent sets. In $k$-set packing this graph has no induced claw with $k + 1$ leaves, which is the structure that the local search methods use.
- **From 3-dimensional matching.** The triples are sets of size 3 over $X \cup Y \cup Z$, so 3-set packing is NP-hard.
- **Dual to set cover.** The LP relaxation of set packing, with the roles of sets and elements exchanged, is the dual of the LP relaxation of [set cover](/set-cover/).

## Applications

- **Combinatorial auctions.** Each bid asks for a bundle of items; accepting bids with disjoint bundles to make the most money is weighted set packing.
- **Scheduling.** Each job needs a fixed set of resources at the same time; running the most jobs at once is set packing.
- **Wireless and network design.** Choosing transmissions or paths that do not share a channel, a node or an edge.
- **Chemistry and biology.** Choosing non-overlapping fragments or binding sites in a molecule.

## References
