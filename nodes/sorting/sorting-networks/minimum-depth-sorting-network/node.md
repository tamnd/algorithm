---
tag: VFVDV5
kind: problem
slug: minimum-depth-sorting-network
name: Minimum-depth sorting network
aliases:
- optimal-depth sorting network
area: sorting/sorting-networks
level: advanced
summary: Find a sorting network on n inputs with the smallest possible depth.
prereqs: [sorting-network, network-depth]
see_also: [minimum-size-sorting-network, sorting-network-depth-lower-bound, depth-size-tradeoff, zero-one-principle, sat, odd-even-merge-sort, aks-sorting-network]
sources:
  - paper: doi:10.1007/BF02090393
    title: Ian Parberry, A computer-assisted optimal depth lower bound for nine-input sorting networks, Mathematical Systems Theory 24 (1991)
    locator: pp. 101 to 116 (no network on 9 inputs has depth 6)
  - paper: doi:10.1007/978-3-319-04921-2_19
    title: Daniel Bundala and Jakub Závodný, Optimal sorting networks, LATA 2014, Lecture Notes in Computer Science 8370
    locator: pp. 236 to 247 (optimal depth for 11 to 16 inputs, by a SAT solver)
  - paper: doi:10.1016/j.jcss.2016.04.004
    title: M. Codish, L. Cruz-Filipe, T. Ehlers, M. Müller and P. Schneider-Kamp, Sorting networks, to the end and back again, Journal of Computer and System Sciences 104 (2019)
    locator: pp. 184 to 201 (a 17-input network with optimal depth)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.3.4, Networks for sorting (the fastest known networks for small n)
  - url: https://bertdobbelaere.github.io/sorting_networks.html
    title: Bert Dobbelaere, List of sorting networks
    locator: the summary table of the best known size and depth for n up to 64
  - paper: doi:10.1007/BF02579338
    title: M. Ajtai, J. Komlós and E. Szemerédi, Sorting in c log n parallel steps, Combinatorica 3(1) (1983)
    locator: pp. 1 to 19
---

The minimum-depth sorting network problem asks, for a given $n$, for a [sorting network](/sorting-network/) on $n$ wires with the fewest layers, and for the smallest such [depth](/network-depth/) $d(n)$. The depth is the parallel time of the network, so this is the question of how fast $n$ items can be sorted by comparators that work at the same time. The values of $d(n)$ are known for $n \le 17$, mostly through searches with [SAT](/sat/) solvers since 2014. Asymptotically $d(n) = \Theta(\log n)$ by the [AKS network](/aks-sorting-network/).

## In plain words

In one round, each item can take part in at most one comparison. The question is how few rounds are enough to sort $n$ items, when the plan of comparisons is fixed in advance.

For 4 items, 3 rounds are enough and 2 are not. For 16 items, 9 rounds are enough and 8 are not. These answers came from large computer searches, because a proof by hand is known only for very small numbers of items.

## Definition

**Input.** An integer $n \ge 1$.

**Output.** A sorting network on $n$ wires of the smallest depth $d(n)$: a sequence of $d(n)$ layers, each a set of [comparators](/comparator/) with disjoint wires, whose composition sorts each input.

The decision form asks, for given $n$ and $d$, whether some sorting network on $n$ wires has depth at most $d$. By the [zero-one principle](/zero-one-principle/), it is enough to sort each input in $\{0, 1\}^n$.

## Variants

- **Minimum size.** Count comparators instead of layers; see [minimum-size sorting network](/minimum-size-sorting-network/).
- **Both costs.** Find the smallest size among the networks of minimum depth, or the whole Pareto front; see [depth-size tradeoff](/depth-size-tradeoff/).
- **Merging and selection.** Find the smallest depth of a network that merges two sorted sequences, or that selects the $t$ smallest items.
- **Upper bounds only.** For $n \ge 18$, find networks with fewer layers than the best known ones.

## Examples

- **$n = 4$.** The layers $\{[0{:}1], [2{:}3]\}$, $\{[0{:}2], [1{:}3]\}$, $\{[1{:}2]\}$ sort 4 items, so $d(4) \le 3$. Two layers have at most 4 comparators, but each sorting network on 4 wires needs at least $\lceil \lg 4! \rceil = 5$. So $d(4) = 3$.
- **$n = 5, 7, 9$.** A layer has at most $\lfloor n/2 \rfloor$ comparators, so $d(n) \ge \lceil s(n) / \lfloor n/2 \rfloor \rceil$, where $s(n)$ is the minimum size. This gives $\lceil 9/2 \rceil = 5$, $\lceil 16/3 \rceil = 6$ and $\lceil 25/4 \rceil = 7$, which are the values of $d(5)$, $d(7)$ and $d(9)$. For $n = 11$ it gives only $\lceil 35/5 \rceil = 7 < 8$.
- **$n = 16$.** Batcher's [odd-even merge sort](/odd-even-merge-sort/) and [bitonic sort](/bitonic-sort/) have depth 10, and the optimal depth is $d(16) = 9$.

## Known algorithms

**Search over output sets.** As for the size problem, run each network prefix on all $2^n$ inputs of zeros and ones and keep the set $S$ of outputs. A breadth-first search adds one layer per step, keeps one prefix per set, and stops when a set has $n + 1$ elements. This is practical for $n \le 6$, because each step tries each matching of the wires as a new layer.

**Fixed first layer.** Parberry showed that the search may assume that the first layer is $[0{:}1], [2{:}3], \ldots$, with $\lfloor n/2 \rfloor$ comparators. He used this, symmetry, and a long run on a supercomputer to prove that no network on 9 inputs has depth 6. Since $d(10) \le 7$ and $d(10) \ge d(9)$, this also gives $d(10) = 7$.

**SAT encodings.** Bundala and Závodný encode "there is a network of depth $d$ on $n$ wires that sorts each 0-1 input" as a formula with one variable for each possible comparator in each layer. They first find the few two-layer prefixes that are needed up to equivalence, and then call a SAT solver once per prefix. In this way they proved $d(n)$ for $11 \le n \le 16$. Codish, Cruz-Filipe, Ehlers, Müller and Schneider-Kamp improved the encoding, studied the possible last layers, and proved $d(17) = 10$.

**Upper bounds for larger $n$.** Networks for larger $n$ come from Batcher's merges of smaller optimal networks and from heuristic searches; Dobbelaere's list collects the best known ones.

## Bounds

**Lower bounds for each $n$.**

- *Cones.* After $t$ layers, the item on one wire depends on at most $2^t$ inputs, and the smallest output of a sorting network depends on all $n$ inputs. So $d(n) \ge \lceil \lg n \rceil$.
- *Counting.* A network of depth $d$ has at most $d \lfloor n/2 \rfloor$ comparators and must have at least $\lceil \lg n! \rceil$, so $d(n) \ge \lceil \lg n! \rceil / \lfloor n/2 \rfloor$, which is about $2 \lg n$ for large $n$.

See [sorting network depth lower bound](/sorting-network-depth-lower-bound/) for the proofs.

**The known values.** The values for $n \le 8$ are in Knuth, the values for 9 and 10 are due to Parberry, those for 11 to 16 to Bundala and Závodný, and the value for 17 to Codish et al.

| $n$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| $d(n)$ | 0 | 1 | 3 | 3 | 5 | 5 | 6 | 6 | 7 | 7 | 8 | 8 | 9 | 9 | 9 | 9 | 10 |
| $\lceil \lg n \rceil$ | 0 | 1 | 2 | 2 | 3 | 3 | 3 | 3 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 5 |

The function is non-decreasing, because removing the wire of the largest item and the comparators on its path turns a network for $n$ wires into one for $n - 1$ wires that is not deeper.

**Asymptotic bounds.** Batcher's networks give $d(n) \le \tfrac12 \lceil \lg n \rceil (\lceil \lg n \rceil + 1)$. The AKS network gives $d(n) = O(\log n)$, so $d(n) = \Theta(\log n)$, but its constant is so large that Batcher's networks are less deep for each $n$ that occurs in practice.

## Reductions

- **To SAT.** For fixed $n$ and $d$, the existence of a network of depth $d$ is a SAT instance with $O(d n^2)$ variables for the comparators and $O(d n)$ variables for each of the $2^n$ inputs. This is the basis of the proofs for $n \ge 11$.
- **To verification.** Checking a candidate network is the [sorting network verification](/sorting-network-verification/) problem, which is [co-NP-complete](/co-np-complete/) for general networks.
- **From smaller $n$.** A network for $n$ wires gives one for $n - 1$ wires of at most the same depth, so lower bounds pass from $n - 1$ to $n$, and upper bounds pass from $n$ to $n - 1$. For example, $d(15) = 9$ follows from $d(16) \le 9$ and $d(13) \ge 9$.

## Applications

- **Hardware sorters.** In a circuit the depth is the delay, so a network of minimum depth gives the fastest sorter of a fixed number of items.
- **SIMD and GPU kernels.** Each layer is a set of independent compare-exchanges that runs as one vector step, so the number of layers sets the running time of sorting kernels for small fixed sizes.
- **Base cases.** Larger networks built by Batcher's merges inherit the depth of their base cases.

## References
