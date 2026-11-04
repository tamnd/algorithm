---
tag: Z5Q77D
kind: problem
slug: minimum-size-sorting-network
name: Minimum-size sorting network
aliases:
- optimal-size sorting network
- Bose-Nelson sorting problem
area: sorting/sorting-networks
level: advanced
summary: Find a sorting network on n inputs with the fewest comparators.
prereqs: [sorting-network, network-size]
see_also: [minimum-depth-sorting-network, depth-size-tradeoff, green-filter, zero-one-principle, sorting-network-verification, comparison-sort-lower-bound, odd-even-merge-sort]
sources:
  - paper: "Jannis Harder, An answer to the Bose-Nelson sorting problem for 11 and 12 channels, arXiv:2012.04400 (2020)"
    locator: Section 1 (history and the table of upper bounds), Lemma 17 (Van Voorhis's bound), Theorem 61 and Corollary 62
  - paper: doi:10.1016/j.jcss.2015.11.014
    title: M. Codish, L. Cruz-Filipe, M. Frank and P. Schneider-Kamp, Sorting nine inputs requires twenty-five comparisons, Journal of Computer and System Sciences 82(3) (2016)
    locator: pp. 551 to 563
  - paper: doi:10.1109/TC.1972.5009021
    title: David C. Van Voorhis, An improved lower bound for sorting networks, IEEE Transactions on Computers C-21(6) (1972)
    locator: pp. 612 to 613
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.3.4, Networks for sorting (the best known networks for small n)
  - url: https://bertdobbelaere.github.io/sorting_networks.html
    title: Bert Dobbelaere, List of sorting networks
    locator: the summary table of the best known size and depth for n up to 64
---

The minimum-size sorting network problem asks, for a given $n$, for a [sorting network](/sorting-network/) on $n$ wires with the fewest [comparators](/comparator/), and for the smallest such number $s(n)$. It is also called the Bose-Nelson sorting problem. The values of $s(n)$ are known only for $n \le 12$; the last ones, $s(11) = 35$ and $s(12) = 39$, were proved by a computer search in 2020. Asymptotically $s(n) = \Theta(n \log n)$, but the constant is not known.

## In plain words

A sorting network makes a fixed list of comparisons, and the question is how short this list can be for $n$ items. Finding a short list is a matter of skill and search. Proving that no shorter list exists is the hard part, because the number of possible lists grows very fast.

For up to 12 items the answer is known. For 13 items, a network with 45 comparisons is known, and no one knows whether 43 or 44 are enough. For large $n$ the known methods are far from the best possible.

## Definition

**Input.** An integer $n \ge 1$.

**Output.** A sorting network on $n$ wires of the smallest [size](/network-size/) $s(n)$.

The decision form asks, for given $n$ and $k$, whether some sorting network on $n$ wires has at most $k$ comparators. By the untangling theorem of Floyd and Knuth, a network of general comparators that sorts can be changed into a network of standard comparators with the same size, so $s(n)$ is the same in both models. By the [zero-one principle](/zero-one-principle/), "sorts" means "sorts each input in $\{0, 1\}^n$".

## Variants

- **Fixed depth.** Find the smallest size among the networks of depth at most $d$. This gives the Pareto front of the [depth-size tradeoff](/depth-size-tradeoff/).
- **Minimum depth.** Find the smallest number of layers; see [minimum-depth sorting network](/minimum-depth-sorting-network/).
- **Merging and selection.** Find the smallest network that merges two sorted sequences of lengths $p$ and $q$ (see [merging network](/merging-network/)), or that puts the $t$ smallest items on the first $t$ wires.
- **Upper bounds only.** For $n \ge 13$, find networks smaller than the best known ones. This is a search problem without a proof of optimality.

## Examples

- **$n = 4$.** The network $[0{:}1], [2{:}3], [0{:}2], [1{:}3], [1{:}2]$ has 5 comparators. Each network with $k$ comparators has at most $2^k$ different runs, and a sorting network needs a different run for each of the $4! = 24$ orders, so $k \ge \lceil \lg 24 \rceil = 5$. So $s(4) = 5$.
- **$n = 5$.** The counting bound gives only $\lceil \lg 120 \rceil = 7$, but $s(5) = 9$. A breadth-first search over the sets of 0-1 outputs, as in [Known algorithms](#known-algorithms), finds no sorting network with 8 comparators and finds one with 9. The same search gives $s(6) = 12$ in a few minutes.
- **$n = 16$.** [Green's network](/green-filter/) has 60 comparators, and Batcher's [odd-even merge sort](/odd-even-merge-sort/) has 63. Van Voorhis's bound gives $s(16) \ge 55$.

## Known algorithms

**Search over output sets.** Run a network prefix on all $2^n$ inputs of zeros and ones and keep the set $S$ of outputs. Two prefixes with the same set behave the same from then on, so a search can store sets instead of networks. A prefix sorts when $|S| = n + 1$. A breadth-first search that adds one comparator per step and drops repeated sets gives $s(n)$ exactly:

```python
from itertools import combinations

def min_size(n: int) -> int:
    level = {frozenset(range(1 << n))}
    k = 0
    while min(len(s) for s in level) > n + 1:
        k += 1
        level = {frozenset(v ^ ((1 << i) | (1 << j)) if v >> i & 1 and not v >> j & 1 else v for v in s)
                 for s in level for i, j in combinations(range(n), 2)}
    return k
```

This is practical for $n \le 6$. The generate-and-prune method of Codish, Cruz-Filipe, Frank and Schneider-Kamp adds two kinds of pruning: it keeps only one set up to a permutation of the wires, and it drops a set $S$ when $S$ is *subsumed* by another set $T$ of the same level: some permutation $\pi$ of the wires gives $\pi(T) \subseteq S$. With this method they proved $s(9) = 25$ in 2014.

**Dynamic programming with a pruning bound.** Harder generalized Van Voorhis's bound to *partial* sorting networks, which sort only a given set of inputs. This gives a lower bound on the size of each partial network that a search reaches, and a dynamic program that uses it computed $s(11) = 35$. The program writes a certificate, and a checker proved correct in Isabelle/HOL checks the certificate.

**Heuristic search for upper bounds.** For $n \ge 13$, the best known networks come from hand constructions and from computer searches that try to improve a prefix and complete it, such as the SorterHunter program used for Dobbelaere's list. These searches give no lower bounds.

## Bounds

**Lower bounds.** Two general bounds hold for each $n$.

- *The counting bound.* $s(n) \ge \lceil \lg n! \rceil$, because a network of size $k$ has at most $2^k$ runs. See [comparison sort lower bound](/comparison-sort-lower-bound/).
- *Van Voorhis's bound.* $s(n) \ge s(n - 1) + \lceil \lg n \rceil$ for each $n \ge 2$. The idea: follow the path of the largest input from one input wire to the last output and delete the comparators on it. What remains sorts $n - 1$ items, and for a well chosen input wire the path has at least $\lceil \lg n \rceil$ comparators (Harder, Lemma 17).

Van Voorhis's bound is better than the counting bound for $n \ge 5$, and it is tight for $n = 2, 3, 4, 6, 8, 10, 12$.

**The known values.** The upper bounds for $n \ge 13$ are from Dobbelaere's list, and the lower bounds for $n \ge 13$ are those given by Van Voorhis's bound from $s(12) = 39$.

| $n$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| $\lceil \lg n! \rceil$ | 0 | 1 | 3 | 5 | 7 | 10 | 13 | 16 | 19 | 22 | 26 | 29 | 33 | 37 | 41 | 45 | 49 |
| lower bound | 0 | 1 | 3 | 5 | 9 | 12 | 16 | 19 | 25 | 29 | 35 | 39 | 43 | 47 | 51 | 55 | 60 |
| upper bound | 0 | 1 | 3 | 5 | 9 | 12 | 16 | 19 | 25 | 29 | 35 | 39 | 45 | 51 | 56 | 60 | 71 |

**Asymptotic bounds.** The counting bound gives $s(n) \ge n \lg n - O(n)$. The [AKS network](/aks-sorting-network/) gives $s(n) = O(n \log n)$, so $s(n) = \Theta(n \log n)$. For each $n$ that occurs in practice, Batcher's networks of size $\Theta(n \log^2 n)$ are much smaller than the AKS networks.

## Reductions

- **To verification.** Checking a candidate network is the [sorting network verification](/sorting-network-verification/) problem, which is [co-NP-complete](/co-np-complete/). So a guess-and-check method for the decision form uses an NP machine with a co-NP oracle when $n$ is given in unary. No better upper bound on the complexity of the decision form is known, and no hardness result for it is known.
- **To satisfiability.** "Is there a sorting network on $n$ wires with $k$ comparators?" can be written as a [SAT](/sat/) formula with one block of variables per comparator and one copy of the network for each 0-1 input. This is practical only for small $n$, and it is more useful for the depth problem, where the number of layers is small.
- **From smaller $n$.** Removing the path of the largest input turns a network for $n$ wires into one for $n - 1$ wires, which is the proof of Van Voorhis's bound.

## Applications

- **Base cases of larger networks.** Batcher's constructions combine small sorting networks, so a smaller network for small $n$ gives a smaller network for each larger $n$ built from it.
- **Fixed-size sorting in code and hardware.** A small sorting network gives branch-free code or a circuit with the fewest compare-exchange steps for a fixed number of items.
- **Tests for search methods.** The values $s(9)$ to $s(12)$ were benchmarks for new search and proof methods: generate-and-prune with subsumption, and certificates checked by a proof assistant.

## References
