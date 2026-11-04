---
tag: 5GBDTC
kind: concept
slug: depth-size-tradeoff
name: Depth-size tradeoff
aliases:
- depth versus size
area: sorting/sorting-networks
level: advanced
summary: The tension between minimizing network depth and minimizing network size.
prereqs: [network-depth, network-size]
see_also: [minimum-size-sorting-network, minimum-depth-sorting-network, green-filter, odd-even-merge-sort, odd-even-transposition-sort, aks-sorting-network]
sources:
  - paper: "José A. R. Fonollosa, Joint size and depth optimization of sorting networks, arXiv:1806.00305 (2018)"
    locator: the abstract and the results for 10 and 12 channels
  - url: https://bertdobbelaere.github.io/sorting_networks.html
    title: Bert Dobbelaere, List of sorting networks
    locator: the networks for 10, 12 and 16 inputs, with their sizes and depths
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.3.4, Networks for sorting (the best known networks for small n, and their delay)
  - paper: doi:10.1007/BF02579338
    title: M. Ajtai, J. Komlós and E. Szemerédi, Sorting in c log n parallel steps, Combinatorica 3(1) (1983)
    locator: pp. 1 to 19
---

The depth-size trade-off is the fact that, for some numbers of inputs, no [sorting network](/sorting-network/) has both the smallest possible [size](/network-size/) and the smallest possible [depth](/network-depth/). For $n \le 9$ one network reaches both optima, but for $n = 10$ a network of optimal depth 7 needs 31 [comparators](/comparator/), while the optimal size 29 needs 8 layers. So the best network depends on how much each cost matters. For large $n$ the trade-off disappears in the asymptotic sense: the [AKS network](/aks-sorting-network/) has size $O(n \log n)$ and depth $O(\log n)$, both optimal up to constant factors.

## In plain words

A sorting network has two costs. The size is how many comparators it uses, which is the total work. The depth is how many rounds it needs, which is the time on a parallel machine. One would like both to be as small as possible.

For small numbers of inputs, there are networks that win on both counts. For 10 inputs, there are not: the fastest networks use more comparators than the smallest ones, and the smallest networks need one more round. So a designer must choose.

## The idea

**Pareto optimal networks.** Call a pair $(s, d)$ *achievable* for $n$ when some sorting network on $n$ wires has size $s$ and depth $d$. A network is *Pareto optimal* when no other network is at least as good in both costs and better in one. Let $s(n)$ be the smallest size and $d(n)$ the smallest depth. The trade-off exists for $n$ exactly when the pair $(s(n), d(n))$ is not achievable.

**What is known for small $n$.** Fonollosa used SAT solvers to find the smallest size for each depth, for networks up to 12 channels.

| $n$ | Pareto optimal pairs (size, depth) | status |
|---|---|---|
| 1 to 9 | $(s(n), d(n))$ | one network reaches both optima |
| 10 | $(29, 8)$ and $(31, 7)$ | 7 layers need 31 comparators |
| 11 | $(35, 8)$ | 8 or 9 layers need at least 35 comparators |
| 12 | $(39, 9)$ and $(40, 8)$ | 8 layers need 40 comparators |

For $n = 9$ the values $s(9) = 25$ and $d(9) = 7$ are reached by one network. For $n = 10$ and $n = 12$ the two optima are not reached together. For larger $n$ only bounds are known. For $n = 16$ the smallest known network has 60 comparators and depth 10 ([Green's network](/green-filter/)), and a network with 61 comparators and depth 9 is known. The optimal depth $d(16) = 9$ is proved, and no network with 60 comparators and depth 9 is known.

**Why depth costs comparators.** A network of small depth must do much work in the first layers, before it knows which comparisons are useful. A network of small size can wait and choose comparators that depend on the effect of the earlier ones, which puts them in a chain. The two extreme simple networks show this on adjacent wires: the insertion network and [odd-even transposition sort](/odd-even-transposition-sort/) both have $n(n-1)/2$ comparators, but depth $2n - 3$ and $n$.

**Asymptotic picture.** Batcher's [odd-even merge sort](/odd-even-merge-sort/) has size $\Theta(n \log^2 n)$ and depth $\Theta(\log^2 n)$. The AKS network has size $O(n \log n)$ and depth $O(\log n)$, both optimal up to a constant factor, so up to constants there is no trade-off. Each network of depth $d$ has size at most $d \lfloor n/2 \rfloor$, because a layer has at most $\lfloor n/2 \rfloor$ comparators. So a network of depth $O(\log n)$ has size $O(n \log n)$ automatically, and the open questions are about the constants.

**Trade-offs within a construction.** Many constructions have a parameter that moves cost from one measure to the other. The [bitonic sort](/bitonic-sort/) and odd-even merge sort have the same depth, but the odd-even merge saves about $\tfrac12 n \lg n$ comparators. For a fixed $n$, a computer search can often remove one layer at the price of one or two extra comparators, as in the cases $n = 10$, $12$ and $16$ above.

## Examples

- **Ten inputs.** A sorting network with 29 comparators has depth at least 8, and one with depth 7 has at least 31 comparators. Both kinds exist. A designer who runs the network on 5 parallel comparator units per step takes the depth 7 network; one who runs it sequentially takes the 29-comparator network.
- **Sixteen inputs.** Green's network: 60 comparators, depth 10. Batcher's odd-even merge sort: 63 comparators, depth 10. A network with 61 comparators and depth 9 is in Dobbelaere's list. The first is the best known for size, the third has optimal depth.
- **Eight inputs.** Batcher's odd-even merge sort has 19 comparators and depth 6, and $s(8) = 19$ and $d(8) = 6$. So one network is optimal in both measures.

## Where it is used

- **Choosing a network for hardware.** In a circuit the size is the area and the depth is the delay. Tables of Pareto optimal networks let a designer choose by the cost that matters.
- **SIMD sorting kernels.** On SIMD hardware each layer costs a few instructions, independent of how many comparators it has. So the depth matters more than the size, and networks of small depth are preferred.
- **Searches for optimal networks.** SAT encodings of the [minimum-size](/minimum-size-sorting-network/) and [minimum-depth](/minimum-depth-sorting-network/) problems can fix both a size and a depth, and so they find the Pareto front directly.

## References
