---
tag: 7F24HG
kind: definition
slug: breakpoint-distance
name: Breakpoint distance
aliases:
- breakpoints
area: sequences/inversions-and-permutations
level: advanced
summary: Adjacent pairs that are not consecutive in the target order; a lower bound on reversal distance.
prereqs: [permutation, descents]
see_also: [sorting-by-reversals, sorting-by-transpositions, pancake-sorting, burnt-pancake-problem, phylogenetic-tree, presortedness, kendall-tau-distance, ulam-distance]
sources:
  - paper: "John Kececioglu and David Sankoff, Exact and approximation algorithms for sorting by reversals, with application to genome rearrangement, Algorithmica 13(1-2) (1995) 180-210"
    locator: breakpoints as a lower bound on the reversal distance, and the 2-approximation by removing breakpoints
  - paper: "Vineet Bafna and Pavel A. Pevzner, Sorting by transpositions, SIAM Journal on Discrete Mathematics 11(2) (1998) 224-240"
    locator: the bound of three breakpoints removed per transposition and the cycle graph
  - paper: "David Sankoff and Mathieu Blanchette, Multiple genome rearrangement and breakpoint phylogeny, Journal of Computational Biology 5(3) (1998) 555-570"
    locator: the breakpoint distance between genomes and the breakpoint median problem
---

A breakpoint of a [permutation](/permutation/) $\pi$, framed by $\pi_0 = 0$ and $\pi_{n+1} = n + 1$, is a pair of neighbors $\pi_i, \pi_{i+1}$ that are not consecutive integers. The number of breakpoints $b(\pi)$ is zero only for the identity, and it is the breakpoint distance from $\pi$ to the identity. Between two rankings or two genomes, the breakpoint distance counts the neighboring pairs of one that are not neighbors in the other. A single reversal of a segment changes $b$ by at most 2 and a block transposition by at most 3, so $b/2$ and $b/3$ are lower bounds for [sorting by reversals](/sorting-by-reversals/) and [sorting by transpositions](/sorting-by-transpositions/), and the first approximation algorithms for both problems remove breakpoints greedily.

## Definition

**Framing.** For $\pi \in S_n$ write $\pi_0 = 0$ and $\pi_{n+1} = n + 1$. The $n + 1$ pairs $(\pi_i, \pi_{i+1})$ for $0 \le i \le n$ are its *gaps*.

**Unsigned breakpoints.** The gap $(\pi_i, \pi_{i+1})$ is an *adjacency* if $|\pi_{i+1} - \pi_i| = 1$ and a *breakpoint* otherwise. This version fits reversals, which can turn $5\,4$ into $4\,5$.

**Directed breakpoints.** The gap is an adjacency if $\pi_{i+1} = \pi_i + 1$ and a breakpoint otherwise. This version fits transpositions and other operations that never reverse a segment.

**Signed breakpoints.** For a signed permutation, in which each item carries an orientation $+$ or $-$, the gap is an adjacency if $\pi_{i+1} - \pi_i = 1$ with the signs included, so $-5\,-4$ is an adjacency and $+5\,+4$ is not.

**Breakpoint distance.** $b(\pi)$ is the number of breakpoints. For two rankings $a$ and $b$ of the same items, framed by the same two end markers, $d_{BP}(a, b)$ is the number of neighboring pairs of $a$ that are not neighboring pairs of $b$, unordered in the unsigned version. It equals $b(w)$ for $w = \operatorname{pos}_b \circ a$, the usual relabeling.

**Facts.**

- **Zero only at the identity.** If every gap is an adjacency in the directed sense, then $\pi_i = i$ for all $i$. In the unsigned sense the same holds: starting at $\pi_0 = 0$, the only neighbor value allowed is $1$, then $2$, and so on.
- **Not 1.** In both versions $b(\pi) = 1$ is impossible: if all gaps but one are adjacencies, the items split into at most two increasing runs of consecutive values joined at the breakpoint, and the framing forces them to be one run.
- **A metric.** $d_{BP}$ is symmetric and satisfies the triangle inequality, since it counts the pairs in the symmetric difference of two sets of adjacencies, divided by two. It is zero only for equal rankings, given the framing.
- **Mean.** For a uniform random $\pi \in S_n$ the expected number of unsigned breakpoints is $n - 1$, since each of the $n - 1$ inner gaps is an adjacency with probability $2/n$ and each of the two end gaps with probability $1/n$. The expected number of directed breakpoints is $(n^2 - 1)/n$.
- **Effect of one operation.** A reversal of $\pi_i \cdots \pi_j$ changes only the two gaps at its ends, so it removes at most 2 breakpoints. A transposition, which exchanges two adjacent blocks, changes three gaps and removes at most 3 directed breakpoints. A prefix reversal, the move of [pancake sorting](/pancake-sorting/), changes the front gap $(0, \pi_1)$ and one other gap, so it removes at most 1 breakpoint among the gaps that do not involve the front marker.
- **Computing it.** One pass in $\Theta(n)$ time, after relabeling by the positions in the target in $\Theta(n)$ time.

## Examples and non-examples

**One permutation.** $\pi = 3\,1\,4\,5\,2$, framed as $0\,3\,1\,4\,5\,2\,6$. Its gaps are $(0,3)$, $(3,1)$, $(1,4)$, $(4,5)$, $(5,2)$, $(2,6)$, and only $(4,5)$ is an adjacency, so $b(\pi) = 5$ in both the unsigned and the directed sense. The bounds give at least $\lceil 5/2 \rceil = 3$ reversals and at least $\lceil 5/3 \rceil = 2$ transpositions, and both are exact: three reversals $3\,1 \to 1\,3$, then $3\,4\,5\,2 \to 2\,5\,4\,3$, then $5\,4\,3 \to 3\,4\,5$ sort it, and so do two transpositions, exchanging the blocks $3$ and $1$ and then the blocks $3\,4\,5$ and $2$.

**Unsigned versus directed.** $\pi = 2\,1$ framed as $0\,2\,1\,3$ has the unsigned adjacency $(2, 1)$ and so 2 unsigned breakpoints, but 3 directed ones. The reversal $n \cdots 2\,1$ has only the two end gaps as unsigned breakpoints, and one reversal sorts it, while it has $n + 1$ directed breakpoints.

**Distribution.** For $n = 5$, the numbers of permutations with $0, 2, 3, 4, 5, 6$ unsigned breakpoints are $1, 10, 28, 39, 32, 10$.

**Genomes.** Two gene orders $a = (A, B, C, D, E)$ and $b = (B, E, A, C, D)$ with the end markers give $w = 3\,1\,4\,5\,2$ and $d_{BP}(a, b) = 5$: among the neighbor pairs of $a$, framed as $\triangleleft A\,B\,C\,D\,E \triangleright$, only $C\,D$ is also a neighbor pair of $b$, framed as $\triangleleft B\,E\,A\,C\,D \triangleright$.

**Non-example: breakpoints are not descents.** A [descent](/descents/) is a gap with $\pi_i > \pi_{i+1}$. The permutation $1\,3\,5\,2\,4$ has one descent but 5 directed breakpoints, and $2\,1$ has one descent and 3 directed breakpoints.

## Related definitions

- **[Sorting by reversals](/sorting-by-reversals/).** The reversal distance $d_R$ satisfies $b(\pi)/2 \le d_R(\pi) \le b(\pi)$, and Kececioglu and Sankoff's greedy removal of breakpoints is a 2-approximation.
- **[Sorting by transpositions](/sorting-by-transpositions/).** The transposition distance satisfies $d_T(\pi) \ge b(\pi)/3$ for directed breakpoints, and Bafna and Pevzner sharpened this with the cycles of a breakpoint graph.
- **[Pancake sorting](/pancake-sorting/).** A prefix reversal changes only one gap that does not involve the front marker, so the number of unsigned breakpoints among $(\pi_1, \pi_2), \ldots, (\pi_n, n + 1)$ is a lower bound on the number of flips.
- **Breakpoint graph.** The graph on the framed values with the gaps of $\pi$ as one color of edges and the adjacencies of the identity as the other color. Its alternating cycles give the exact formula of Hannenhalli and Pevzner for signed reversals.
- **Breakpoint median and phylogeny.** Given three or more genomes, find one that minimizes the sum of breakpoint distances to them. Sankoff and Blanchette used it to build [phylogenetic trees](/phylogenetic-tree/); it is NP-hard and reduces to an instance of the [traveling salesman problem](/traveling-salesman-problem/).

## References
