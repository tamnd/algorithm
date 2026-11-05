---
tag: WDJSX1
kind: problem
slug: sorting-by-transpositions
name: Sorting by transpositions
aliases:
- transposition distance problem
area: sequences/inversions-and-permutations
level: advanced
summary: Sort a permutation using block transpositions, a genome-rearrangement model.
prereqs: [breakpoint-distance, permutation]
see_also: [sorting-by-reversals, breakpoint-distance, pancake-sorting, cayley-distance, ulam-distance, approximation-ratio, np-hard, phylogenetic-tree]
sources:
  - paper: "Vineet Bafna and Pavel A. Pevzner, Sorting by transpositions, SIAM Journal on Discrete Mathematics 11(2) (1998) 224-240"
    locator: the cycle graph, the lower bound from odd cycles and the 3/2-approximation
  - paper: "Isaac Elias and Tzvika Hartman, A 1.375-approximation algorithm for sorting by transpositions, IEEE/ACM Transactions on Computational Biology and Bioinformatics 3(4) (2006) 369-379"
    locator: the 1.375-approximation and the diameter computations
  - paper: "Laurent Bulteau, Guillaume Fertin and Irena Rusu, Sorting by transpositions is difficult, SIAM Journal on Discrete Mathematics 26(3) (2012) 1148-1180"
    locator: NP-hardness of computing the transposition distance
  - paper: "David A. Christie, Sorting permutations by block-interchanges, Information Processing Letters 60(4) (1996) 165-169"
    locator: the exact formula and polynomial algorithm for block interchanges
---

Sorting by transpositions asks for the least number of block transpositions that sort a [permutation](/permutation/), where a transposition cuts out a contiguous block and pastes it elsewhere, which is the same as exchanging two adjacent blocks. It models the genome rearrangement in which a segment of DNA moves to another place without changing its orientation. Each transposition removes at most three directed [breakpoints](/breakpoint-distance/), which gives the lower bound $b(\pi)/3$, and Bafna and Pevzner sharpened it with the odd cycles of a cycle graph and gave a $3/2$-approximation in 1995. The problem was open for many years and was shown NP-hard by Bulteau, Fertin and Rusu in 2012; the best known approximation ratio is $1.375$.

## In plain words

You have a row of numbered cards out of order. In one step you may pick up a run of neighboring cards, keep them in the same order, and slide them in somewhere else in the row. How few steps sort it?

Look at the places where a card is not followed by the next number. A sorted row has none. One step cuts the row in two places and joins it in one more, so it touches only three such places and can fix at most three. That gives a lower bound. Finding the exact minimum turned out to be a hard problem, but there are methods that are guaranteed to be within a small factor of it.

## Definition

**Transposition.** For $1 \le i < j < k \le n + 1$, the transposition $\tau(i, j, k)$ exchanges the adjacent blocks $\pi_i \cdots \pi_{j-1}$ and $\pi_j \cdots \pi_{k-1}$:
$$\pi_1 \cdots \pi_{i-1}\ \underline{\pi_i \cdots \pi_{j-1}}\ \underline{\pi_j \cdots \pi_{k-1}}\ \pi_k \cdots \pi_n \;\mapsto\; \pi_1 \cdots \pi_{i-1}\ \pi_j \cdots \pi_{k-1}\ \pi_i \cdots \pi_{j-1}\ \pi_k \cdots \pi_n.$$
There are $\binom{n+1}{3}$ of them. Moving a single item is the special case of a block of length 1, so every move of the [Ulam distance](/ulam-distance/) is a transposition.

**Problem.** Given $\pi \in S_n$, find the transposition distance $d_T(\pi)$, the least number of transpositions that turn $\pi$ into $1\,2 \cdots n$, and find such a sequence. Between two gene orders $a$ and $b$, the distance is $d_T(\operatorname{pos}_b \circ a)$.

**Cycle graph.** Frame $\pi$ as $\pi_0 = 0$, $\pi_{n+1} = n + 1$, and replace each value $x$ by the two points $2x - 1, 2x$, giving a sequence of $2n + 2$ points that starts with $0$ and ends with $2n + 1$. Black edges join the points $2i$ and $2i + 1$ of this sequence, one for each gap of $\pi$; gray edges join the values $2k$ and $2k + 1$, one for each gap of the identity. Every vertex has one edge of each color, so the graph splits into alternating cycles. A cycle is *odd* if it has an odd number of black edges, and $c_{\mathrm{odd}}(\pi)$ is the number of odd cycles.

## Variants

- **Block interchanges.** Exchange two blocks that need not be adjacent. Christie showed that the distance is exactly $(n + 1 - c(\pi))/2$, where $c$ counts all alternating cycles, and gave a polynomial algorithm.
- **Prefix transpositions.** The first block must start at position 1. This is another genome model and, like [pancake sorting](/pancake-sorting/), a sorting puzzle with prefix moves.
- **Transreversals.** A transposition that also reverses one of the blocks, combined with reversals in the signed model.
- **Short transpositions.** Blocks of total length at most 3, a model of local moves with polynomial approximation and exact results for some classes.
- **Swaps of two items.** Exchanging any two single items gives the [Cayley distance](/cayley-distance/), $n$ minus the number of cycles, which is easy.

## Examples

**A small permutation.** $\pi = 3\,1\,4\,5\,2$ has 5 directed breakpoints, so $d_T(\pi) \ge \lceil 5/3 \rceil = 2$. Two transpositions suffice: exchange the blocks $3$ and $1$ to get $1\,3\,4\,5\,2$, then the blocks $3\,4\,5$ and $2$. So $d_T(\pi) = 2$. Its cycle graph has 2 alternating cycles, both odd, and the odd-cycle bound $(n + 1 - c_{\mathrm{odd}})/2 = (6 - 2)/2 = 2$ is also exact.

**The reversed order.** $n \cdots 2\,1$ has $n + 1$ directed breakpoints, and it needs exactly $\lfloor n/2 \rfloor + 1$ transpositions for $n \ge 3$, a result of Meidanis, Walter and Dias.

**Distances in $S_n$.** For $n = 5$, the numbers of permutations at transposition distance $0, 1, 2, 3$ are $1, 20, 68, 31$. For $n = 8$ they are $1, 84, 1932, 13467, 22000, 2836$, and the largest distance for $n = 3, \ldots, 8$ is $2, 3, 3, 4, 4, 5$, which is $\lfloor n/2 \rfloor + 1$, the value at the reversed order.

**When the bounds differ.** The odd-cycle bound is exact for 6 of the 6 permutations of $[3]$, for 113 of the 120 of $[5]$, and for 4460 of the 5040 of $[7]$, so it is a good but not exact estimate.

## Known algorithms

- **Breadth-first search.** Exact over the $n!$ states with $\binom{n+1}{3}$ moves each, feasible only for small $n$.
- **Breakpoint greedy.** Removing breakpoints greedily guarantees a ratio of 3, since at least one breakpoint can always be removed and at most three can be.
- **Bafna and Pevzner.** A transposition changes $c_{\mathrm{odd}}$ by $-2$, $0$ or $+2$, which gives $d_T(\pi) \ge (n + 1 - c_{\mathrm{odd}}(\pi))/2$. They showed how to find, in polynomial time, a sequence of transpositions of which enough are "2-moves" that increase $c_{\mathrm{odd}}$ by 2, giving a $3/2$-approximation in $O(n^2)$ time.
- **Better ratios.** Elias and Hartman gave a $1.375$-approximation by a computer-assisted case analysis of small configurations, with later implementations running in $O(n \log n)$ time.
- **Exact methods.** Branch and bound with the cycle bound, and integer programming, solve instances of moderate size.

## Bounds

- **Lower bounds.** $d_T(\pi) \ge \lceil b(\pi)/3 \rceil$ for directed breakpoints, and $d_T(\pi) \ge (n + 1 - c_{\mathrm{odd}}(\pi))/2$, which is never weaker.
- **Upper bounds.** $d_T(\pi) \le n - \operatorname{LIS}(\pi)$, by moving the items outside a longest increasing subsequence one at a time, and $d_T(\pi) \le b(\pi)$. The diameter of $S_n$ under transpositions is at most $\lfloor (2n - 2)/3 \rfloor$ for $n \ge 9$, by Eriksson and others, and at least $\lfloor n/2 \rfloor + 1$.
- **Hardness.** NP-hard by a reduction from 3-satisfiability (Bulteau, Fertin and Rusu).

## Reductions

- **From 3-satisfiability.** Bulteau, Fertin and Rusu build a permutation whose transposition distance meets the lower bound $b(\pi)/3$ exactly when the formula is satisfiable, using gadgets in which every transposition must remove three breakpoints.
- **To the cycle graph.** All the approximation algorithms work on the cycle graph, whose cycles of length 1, 2 and 3 have explicit optimal treatments; a permutation with only short cycles is reduced to a set of small configurations.
- **Block interchanges as a relaxation.** Allowing non-adjacent blocks gives Christie's exact formula, a lower bound of half the cycle deficit that is achieved in polynomial time.

## Applications

- **Genome rearrangement.** Transpositions model segments that move without inversion, as in some mitochondrial and bacterial genomes, and the distance estimates the number of such events between two species.
- **Phylogeny.** Transposition and combined rearrangement distances are used to build [phylogenetic trees](/phylogenetic-tree/) from gene orders.
- **Text editing.** Cut and paste of blocks is the basic operation of text editors, and the transposition distance measures the least editing effort to reorder the paragraphs of a document.

## References
