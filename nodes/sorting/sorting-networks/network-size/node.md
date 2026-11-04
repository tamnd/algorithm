---
tag: GZW76D
kind: concept
slug: network-size
name: Network size
aliases:
- number of comparators
area: sorting/sorting-networks
level: intro
summary: The total number of comparators in a sorting network.
prereqs: [sorting-network]
see_also: [network-depth, minimum-size-sorting-network, depth-size-tradeoff, odd-even-merge-sort, bitonic-sort, green-filter, aks-sorting-network, comparison-sort-lower-bound]
sources:
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.3.4, Networks for sorting (the number of comparators, the networks of Floyd and Knuth for n up to 8)
  - paper: doi:10.1016/j.jcss.2015.11.014
    title: M. Codish, L. Cruz-Filipe, M. Frank and P. Schneider-Kamp, Sorting nine inputs requires twenty-five comparisons, Journal of Computer and System Sciences 82(3) (2016)
    locator: pp. 551 to 563
  - paper: "Jannis Harder, An answer to the Bose-Nelson sorting problem for 11 and 12 channels, arXiv:2012.04400 (2020)"
    locator: the main theorem (s(11) = 35 and s(12) = 39)
  - url: https://bertdobbelaere.github.io/sorting_networks.html
    title: Bert Dobbelaere, List of sorting networks
    locator: the summary table of the best known size and depth for n up to 64
  - paper: doi:10.1007/BF02579338
    title: M. Ajtai, J. Komlós and E. Szemerédi, Sorting in c log n parallel steps, Combinatorica 3(1) (1983)
    locator: pp. 1 to 19
---

The size of a comparator network is the number of [comparators](/comparator/) in it. It is the total work of the network: a sequential program that runs the network makes exactly this many comparisons, on each input. Each [sorting network](/sorting-network/) on $n$ wires has size at least $\lceil \lg n! \rceil$, Batcher's [odd-even merge sort](/odd-even-merge-sort/) has size $\Theta(n \log^2 n)$, and the [AKS network](/aks-sorting-network/) has size $O(n \log n)$. The smallest size $s(n)$ is known only for $n \le 12$.

## In plain words

The size of a network is how many comparators it has. Each comparator does one comparison, so the size is the number of comparisons that the network makes. A network makes all its comparisons on every input, even when the input is already sorted.

A small size means cheap hardware and little work. A network can have few comparators and still be slow on a parallel machine, if the comparators must wait for each other. That second cost is the depth.

## The idea

**Size against comparisons.** In the [comparison model](/comparison-model/) an algorithm can choose its next comparison from the results of the earlier ones. A network can not. So the size of the best sorting network is at least the number of comparisons of the best sorting algorithm, and it is often larger. For $n = 5$, the [Ford-Johnson algorithm](/ford-johnson-algorithm/) sorts with 7 comparisons, but each sorting network on 5 wires has at least 9 comparators.

**The information bound.** Run a sorting network of size $s$ on the $n!$ orders of $n$ different items. The results of the $s$ comparators fix which permutation the network applies, and different orders need different permutations. So $2^s \ge n!$ and

$$s(n) \ge \lceil \lg n! \rceil = n \lg n - n \lg e + O(\log n).$$

This is the [comparison sort lower bound](/comparison-sort-lower-bound/). It is tight for $n \le 4$ and not tight for $n \ge 5$.

**A connectivity bound.** View the wires as vertices and each comparator as an edge. If this graph has two parts with no edge between them, no item ever moves from one part to the other, and the network can not sort. So the graph is connected and $s(n) \ge n - 1$. This bound is weak, but the same idea of following where an item can go is the start of many stronger arguments.

**Upper bounds.** The networks of insertion sort and of [odd-even transposition sort](/odd-even-transposition-sort/) have $n(n-1)/2$ comparators. Batcher's networks have $\Theta(n \log^2 n)$ comparators: for $n = 2^k$, odd-even merge sort has $\tfrac14 n k (k - 1) + n - 1$ and [bitonic sort](/bitonic-sort/) has $\tfrac14 n k (k + 1)$. Ajtai, Komlós and Szemerédi built networks of size $O(n \log n)$ and depth $O(\log n)$, so $s(n) = \Theta(n \log n)$. Their constant is so large that Batcher's networks are smaller for each $n$ that occurs in practice.

**Redundant comparators.** A comparator is *redundant* in a network when it never exchanges its two items, on any input. Removing it does not change the output. By the [zero-one principle](/zero-one-principle/), a comparator $[i{:}j]$ is redundant if and only if no 0-1 input reaches it with a 1 on wire $i$ and a 0 on wire $j$, so this can be tested with $2^n$ inputs. Removing the comparators that touch extra wires turns a network for $2^k$ wires into a network for fewer wires.

## Examples

The smallest sizes that are proved, with the information bound and the size of Batcher's merge exchange:

| $n$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| $\lceil \lg n! \rceil$ | 0 | 1 | 3 | 5 | 7 | 10 | 13 | 16 | 19 | 22 | 26 | 29 |
| $s(n)$ | 0 | 1 | 3 | 5 | 9 | 12 | 16 | 19 | 25 | 29 | 35 | 39 |
| Batcher | 0 | 1 | 3 | 5 | 9 | 12 | 16 | 19 | 26 | 31 | 37 | 41 |

The networks for $n \le 8$ that reach $s(n)$ are due to Floyd and Knuth, who also proved that they are optimal (Knuth, Section 5.3.4). Codish, Cruz-Filipe, Frank and Schneider-Kamp proved $s(9) = 25$ and $s(10) = 29$ with a computer search in 2016, and Harder proved $s(11) = 35$ and $s(12) = 39$ in 2020. For $n = 13, 14, 15, 16, 17$ the smallest known networks have $45, 51, 56, 60, 71$ comparators. The 60-comparator network for 16 wires is [Green's network](/green-filter/).

A small check: the 4-wire network $[0{:}1], [2{:}3], [0{:}2], [1{:}3], [1{:}2]$ has size 5 and depth 3. Since $\lceil \lg 4! \rceil = \lceil \lg 24 \rceil = 5$, no sorting network on 4 wires is smaller.

**Counting the size of a recursive network.** For odd-even merge sort, the merge of two sorted lists of $m/2$ items each has $M(m) = 2M(m/2) + m/2 - 1$ comparators with $M(2) = 1$, so $M(m) = \tfrac12 m (\lg m - 1) + 1$. The sort has $S(n) = 2S(n/2) + M(n)$, which gives $1, 5, 19, 63, 191$ for $n = 2, 4, 8, 16, 32$.

## Where it is used

- **Hardware.** In a sorting circuit each comparator is a block of gates, so the size is the cost in chip area.
- **Sequential oblivious code.** A program that runs a network on one processor takes time proportional to the size. Small fixed sorts in libraries and in oblivious algorithms for secure computation use networks of small size.
- **Optimal networks for small $n$.** The search for $s(n)$ is the [minimum-size sorting network](/minimum-size-sorting-network/) problem. It is one of the few problems where computer proofs fixed the exact values.
- **Trade-offs.** For many $n$, no network has both the smallest size and the smallest depth. See [depth-size trade-off](/depth-size-tradeoff/).

## References
