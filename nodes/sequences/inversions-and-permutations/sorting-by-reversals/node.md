---
tag: 1DK4Q7
kind: problem
slug: sorting-by-reversals
name: Sorting by reversals
aliases:
- reversal distance
area: sequences/inversions-and-permutations
level: advanced
summary: Minimum number of reversals to sort a permutation; polynomial for signed permutations, NP-hard for unsigned.
prereqs: [breakpoint-distance, permutation]
see_also: [sorting-by-transpositions, pancake-sorting, burnt-pancake-problem, breakpoint-distance, approximation-ratio, np-hard, phylogenetic-tree, sorting-by-adjacent-swaps]
sources:
  - paper: "John Kececioglu and David Sankoff, Exact and approximation algorithms for sorting by reversals, with application to genome rearrangement, Algorithmica 13(1-2) (1995) 180-210"
    locator: the breakpoint lower bound, the 2-approximation and exact branch and bound
  - paper: "Sridhar Hannenhalli and Pavel A. Pevzner, Transforming cabbage into turnip: polynomial algorithm for sorting signed permutations by reversals, Journal of the ACM 46(1) (1999) 1-27"
    locator: the breakpoint graph, hurdles and fortresses, and the exact formula for the signed reversal distance
  - paper: "Alberto Caprara, Sorting permutations by reversals and Eulerian cycle decompositions, SIAM Journal on Discrete Mathematics 12(1) (1999) 91-110"
    locator: NP-hardness of sorting unsigned permutations by reversals
  - paper: "Haim Kaplan, Ron Shamir and Robert E. Tarjan, A faster and simpler algorithm for sorting signed permutations by reversals, SIAM Journal on Computing 29(3) (1999) 880-892"
    locator: the O(n^2) algorithm that finds a shortest sequence of signed reversals
---

Sorting by reversals asks for the least number of reversals of contiguous segments that turn a [permutation](/permutation/) into the identity, its reversal distance. It models the evolution of gene orders, in which a segment of a chromosome is cut out and put back the other way round. For *signed* permutations, where every gene also has an orientation that a reversal flips, Hannenhalli and Pevzner found an exact formula in 1995 and a polynomial algorithm, and the distance itself is now computed in linear time. For *unsigned* permutations, Caprara proved the problem NP-hard, and the best known approximation ratio is $1.375$. The [breakpoint](/breakpoint-distance/) count gives the basic lower bound $b(\pi)/2$, since a reversal removes at most two breakpoints.

## In plain words

You have a row of numbered cards in a mixed-up order. In one step you may pick any stretch of neighboring cards and flip its order end to end. How few steps sort the row?

A useful count is the number of places where two neighbors are not consecutive numbers. Sorted rows have none, and one flip changes only the two places at the ends of the stretch, so it can fix at most two of them. This gives a quick lower bound. Finding the true minimum is hard in general.

In genetics each card also has a direction, like an arrow, and a flip turns every arrow in the stretch around. Surprisingly, adding the arrows makes the problem easier: there is an exact formula, and a fast method finds a shortest way.

## Definition

**Reversal.** For $1 \le i \le j \le n$, the reversal $\rho(i, j)$ turns $\pi_1 \cdots \pi_{i-1}\, \pi_i \pi_{i+1} \cdots \pi_j\, \pi_{j+1} \cdots \pi_n$ into $\pi_1 \cdots \pi_{i-1}\, \pi_j \cdots \pi_{i+1} \pi_i\, \pi_{j+1} \cdots \pi_n$.

**Signed reversal.** For a signed permutation, whose entries are $\pm 1, \ldots, \pm n$ with each absolute value once, $\rho(i, j)$ also changes the sign of every entry in the segment.

**Problem.** Given $\pi$, find the reversal distance $d(\pi)$, the least $t$ such that some $t$ reversals turn $\pi$ into $1\,2 \cdots n$, or $+1\,+2 \cdots +n$ in the signed case, and find such a sequence. Between two gene orders $a$ and $b$ the distance is $d(\operatorname{pos}_b \circ a)$.

## Variants

- **Signed versus unsigned.** The signed problem is polynomial and the unsigned one is NP-hard. The unsigned distance is the least signed distance over all $2^n$ ways of assigning signs.
- **Prefix reversals.** Only reversals with $i = 1$ are allowed: [pancake sorting](/pancake-sorting/), and its signed form, the [burnt pancake problem](/burnt-pancake-problem/).
- **Bounded length.** Only reversals of length 2 are allowed, which is [sorting by adjacent swaps](/sorting-by-adjacent-swaps/) and is solved exactly by counting inversions. Reversals of length at most 3 or of other bounded lengths give intermediate problems.
- **Weighted reversals.** The cost of a reversal grows with its length, which models the higher cost of long rearrangements.
- **Other operations.** Block [transpositions](/sorting-by-transpositions/), and the double-cut-and-join model, which includes reversals, translocations, fusions and fissions and has a simple exact formula.
- **Multiple genomes.** The reversal median problem asks for a gene order that minimizes the sum of reversal distances to three given ones. It is NP-hard already in the signed case.

## Examples

**An unsigned permutation.** $\pi = 3\,1\,4\,5\,2$ has 5 breakpoints, so $d(\pi) \ge 3$. Three reversals suffice: $3\,1 \to 1\,3$ gives $1\,3\,4\,5\,2$, then $3\,4\,5\,2 \to 2\,5\,4\,3$ gives $1\,2\,5\,4\,3$, then $5\,4\,3 \to 3\,4\,5$. So $d(\pi) = 3$.

**The same with signs.** As a signed permutation with all signs positive, $+3\,+1\,+4\,+5\,+2$ needs 5 reversals, more than its unsigned version, because each reversal flips signs that must be flipped back. The cycle bound below gives only 4 here; the difference is a hurdle.

**Reversed order.** The unsigned $n \cdots 2\,1$ is sorted by one reversal. The signed $-n \cdots -2\,-1$ also needs one, while $+n \cdots +2\,+1$ needs $n + 1$ for $n = 5$.

**Distances in $S_n$.** For unsigned permutations of $[5]$ the numbers at distance $0, 1, 2, 3, 4$ are $1, 10, 52, 55, 2$, and for $[8]$ the largest distance, $7$, is reached by just 2 permutations. In general the unsigned diameter is $n - 1$, and Bafna and Pevzner showed which two permutations reach it.

## Known algorithms

- **Breadth-first search.** Explore the Cayley graph with the $\binom{n}{2}$ unsigned or the $\binom{n}{2} + n$ signed reversals as moves. Exact but feasible only for small $n$, since there are $n!$ or $2^n n!$ states.
- **Greedy breakpoint removal, unsigned.** Kececioglu and Sankoff remove breakpoints greedily, preferring reversals that remove two and keeping a decreasing strip available, which never uses more than $b(\pi)$ reversals and so is a 2-approximation.
- **Better approximations, unsigned.** Bafna and Pevzner gave a ratio of $7/4$, Christie $3/2$, and Berman, Hannenhalli and Karpinski $1.375$, all using the breakpoint graph and its decomposition into alternating cycles.
- **Signed, exact.** Hannenhalli and Pevzner's formula
$$d(\pi) = n + 1 - c(\pi) + h(\pi) + f(\pi)$$
where $c$ is the number of alternating cycles of the breakpoint graph, $h$ the number of hurdles, special unoriented components of that graph, and $f \in \{0, 1\}$ indicates a fortress. Their algorithm finds an optimal sequence in polynomial time.
- **Signed, faster.** Kaplan, Shamir and Tarjan find an optimal sequence in $O(n^2)$ time; Bader, Moret and Yan compute the distance alone in $O(n)$ time; Tannier, Bergeron and Sagot find a sequence in $O(n^{3/2}\sqrt{\log n})$ time.

## Bounds

- **Lower bounds.** $d(\pi) \ge \lceil b(\pi)/2 \rceil$ for unsigned permutations, and $d(\pi) \ge n + 1 - c(\pi)$ for signed ones. Each signed reversal changes the number of cycles by at most one.
- **Upper bound.** $d(\pi) \le b(\pi)$ for unsigned permutations, and $d(\pi) \le n - 1$; the reversals that bring $i$ to position $i$ for $i = 1, \ldots, n-1$ give the last bound.
- **Hardness.** The unsigned problem is NP-hard (Caprara 1997, journal version 1999) and APX-hard (Berman and Karpinski), so it has no polynomial-time approximation scheme unless P = NP.
- **Signed.** Linear time for the distance, so the signed problem is as easy as reading the input.
- **Random permutations.** The expected number of breakpoints of a random unsigned permutation is $n - 1$, so the breakpoint bound is about $n/2$ on average. Counting gives the same order: at most $\binom{n}{2}^t + \cdots + 1$ permutations lie within $t$ reversals, so almost every permutation needs at least $(1 - o(1))\, n/2$ of them.

## Reductions

- **Unsigned to signed.** Try all signings and take the least signed distance. This is exponential, but heuristics that choose signs for the strips of consecutive values work well in practice.
- **Signed to unsigned.** Replace each $+x$ by $2x-1,\ 2x$ and each $-x$ by $2x,\ 2x-1$. Every signed reversal of $\pi$ becomes an unsigned reversal of this permutation of $[2n]$ that does not split a pair, so its unsigned distance is at most the signed distance of $\pi$. It can be smaller, since unsigned reversals may split pairs: $+2\,+1$ has signed distance 3, while its image $3\,4\,1\,2$ is sorted by 2 unsigned reversals. The breakpoint graph of $\pi$ is drawn on this image.
- **From an NP-hard problem.** Caprara's proof uses the decomposition of a breakpoint graph into the most alternating cycles, which he showed NP-hard through a reduction from Eulerian cycle decomposition.

## Applications

- **Genome rearrangement.** Estimating the number of inversion events between the gene orders of two species, such as the chloroplast genomes of related plants or the X chromosomes of human and mouse, and building [phylogenetic trees](/phylogenetic-tree/) from these distances.
- **Comparative genomics.** Identifying conserved segments and the most parsimonious rearrangement scenarios that explain two gene orders.
- **Interconnection networks.** The Cayley graph of $S_n$ generated by reversals, and its prefix variant, the pancake graph, are studied as network topologies with small diameter.

## References
