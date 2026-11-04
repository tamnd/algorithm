---
tag: MF2BDW
kind: concept
slug: network-depth
name: Network depth
aliases:
- parallel time of a network
- number of layers
area: sorting/sorting-networks
level: intro
summary: The longest chain of comparators on any wire, i.e. the parallel running time of the network.
prereqs: [sorting-network]
see_also: [network-size, minimum-depth-sorting-network, sorting-network-depth-lower-bound, depth-size-tradeoff, odd-even-merge-sort, bitonic-sort, aks-sorting-network, parallel-sorting-depth-lower-bound]
sources:
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.3.4, Networks for sorting (delay time of a network)
  - book: isbn:9780262032933
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, second edition
    locator: Section 27.1, Comparison networks (the depth of a wire and of a network)
  - paper: doi:10.1007/BF02090393
    title: Ian Parberry, A computer-assisted optimal depth lower bound for nine-input sorting networks, Mathematical Systems Theory 24 (1991)
    locator: pp. 101 to 116 (depth 7 is optimal for 9 and 10 inputs)
  - paper: doi:10.1007/978-3-319-04921-2_19
    title: Daniel Bundala and Jakub Závodný, Optimal sorting networks, LATA 2014, Lecture Notes in Computer Science 8370
    locator: pp. 236 to 247 (optimal depth for 11 to 16 inputs)
  - paper: doi:10.1016/j.jcss.2016.04.004
    title: M. Codish, L. Cruz-Filipe, T. Ehlers, M. Müller and P. Schneider-Kamp, Sorting networks, to the end and back again, Journal of Computer and System Sciences 104 (2019)
    locator: pp. 184 to 201 (depth 10 is optimal for 17 inputs)
  - paper: doi:10.1007/BF02579338
    title: M. Ajtai, J. Komlós and E. Szemerédi, Sorting in c log n parallel steps, Combinatorica 3(1) (1983)
    locator: pp. 1 to 19
---

The depth of a comparator network is the largest number of [comparators](/comparator/) on one path from an input to an output. Equivalently, it is the smallest number of layers of comparators with disjoint wires into which the network can be split. A parallel machine runs one layer per step, so the depth is the parallel running time of the network, and the [size](/network-size/) is its total work. Each [sorting network](/sorting-network/) on $n$ wires has depth at least $\lceil \lg n \rceil$, Batcher's networks have depth $\tfrac12 \lg n (\lg n + 1)$, and the [AKS network](/aks-sorting-network/) reaches $O(\log n)$.

## In plain words

Comparators that use different wires do not wait for each other, so they can work at the same time. A set of such comparators is a layer. The depth counts the layers. If one comparator takes one unit of time, a network of depth 6 gives its answer after 6 units of time, however many comparators each layer has.

A network with few layers can still have many comparators, and a network with few comparators can need many layers. Depth measures speed on parallel hardware, and size measures cost.

## The idea

**Two equivalent definitions.** Let a network have the comparators $C_1, \ldots, C_s$ in this order. Give each wire a *level*, 0 at the start. Process the comparators in order: for $C_t = [i{:}j]$, set both levels to $\max(\text{level}_i, \text{level}_j) + 1$, and say that $C_t$ is in layer $\max(\text{level}_i, \text{level}_j) + 1$. The depth is the largest level at the end. The comparators of one layer have disjoint wires: two comparators on a common wire get different levels. A comparator in layer $\ell$ follows a comparator in layer $\ell - 1$ on one of its wires, so there is a path of $\ell$ comparators that ends at it. So the depth is both the length of the longest path and the number of layers of this greedy split, and no split into fewer layers exists. CLRS defines the depth of a wire in the same way.

**Reordering.** Two comparators on four different wires commute. So the order of comparators inside a layer does not matter, and the network can be written layer by layer. This is how most tables of small networks are given.

**A first lower bound.** After $d$ layers, the item on one wire is a function of at most $2^d$ inputs: a comparator joins the inputs that its two wires depend on. The smallest output of a sorting network depends on each of the $n$ inputs, because each input can be the smallest. So $2^d \ge n$ and

$$d \ge \lceil \lg n \rceil.$$

A layer has at most $\lfloor n/2 \rfloor$ comparators, and a sorting network needs at least $\lceil \lg n! \rceil$ comparators, by the counting argument of the [comparison model](/comparison-model/). So also $d \ge \lceil \lg n! \rceil / \lfloor n/2 \rfloor$, which is about $2 \lg n$ for large $n$. Both bounds are $\Theta(\log n)$. See [sorting network depth lower bound](/sorting-network-depth-lower-bound/).

**Upper bounds.** [Bitonic sort](/bitonic-sort/) and [odd-even merge sort](/odd-even-merge-sort/) have depth $\tfrac12 k(k+1)$ for $n = 2^k$, which is $\Theta(\log^2 n)$. Ajtai, Komlós and Szemerédi built networks of depth $O(\log n)$ in 1983, so the lower bound is tight up to a constant factor. Their constant is very large, and for each $n$ that occurs in practice Batcher's networks have smaller depth.

**Depth of a sort is not depth of a merge.** Merging two sorted lists of $n/2$ items needs depth $\lg n$ when $n$ is a power of 2, and Batcher's merges reach it. Sorting by merges in a tree of $\lg n$ levels then costs $\sum_{j \le k} j = \tfrac12 k(k+1)$ layers. Depth $O(\log n)$ needs a different idea, such as the approximate halvers of the AKS network.

## Examples

| network on $n$ wires | depth | depth for $n = 8$ |
|---|---|---|
| insertion or bubble sort with adjacent comparators | $2n - 3$ | 13 |
| [odd-even transposition sort](/odd-even-transposition-sort/) | $n$ | 8 |
| bitonic sort, $n = 2^k$ | $\tfrac12 k (k + 1)$ | 6 |
| odd-even merge sort, $n = 2^k$ | $\tfrac12 k (k + 1)$ | 6 |
| AKS network | $O(\log n)$ | not useful |

The insertion network on adjacent wires has $n(n-1)/2$ comparators. The insertion of item $i$, for $i = 1, \ldots, n - 1$, uses the comparators $[i-1{:}i], [i-2{:}i-1], \ldots, [0{:}1]$, and the greedy split puts $[j-1{:}j]$ of this insertion into layer $2i - j$. So the insertions overlap in time, and the last comparator $[0{:}1]$ is in layer $2(n-1) - 1 = 2n - 3$. Odd-even transposition sort has the same $n(n-1)/2$ comparators, arranged in $n$ layers: the even pairs and the odd pairs, in turn. So the same size can come with very different depths.

The smallest possible depth $d(n)$ is known for $n \le 17$:

| $n$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| $d(n)$ | 0 | 1 | 3 | 3 | 5 | 5 | 6 | 6 | 7 | 7 | 8 | 8 | 9 | 9 | 9 | 9 | 10 |
| $\lceil \lg n \rceil$ | 0 | 1 | 2 | 2 | 3 | 3 | 3 | 3 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 5 |

Parberry proved the values for 9 and 10 inputs with a computer search in 1991. Bundala and Závodný proved them for 11 to 16 inputs with a SAT solver in 2014, and Codish, Cruz-Filipe, Ehlers, Müller and Schneider-Kamp proved $d(17) = 10$. See [minimum-depth sorting network](/minimum-depth-sorting-network/).

**Computing the depth.** The greedy split above takes $O(s + n)$ time for a network of size $s$.

```
def depth(net, n):
    level = [0] * n
    for i, j in net:
        level[i] = level[j] = max(level[i], level[j]) + 1
    return max(level, default=0)
```

## Where it is used

- **Parallel sorting.** On a machine with one processor per pair of wires, or in hardware, the depth is the running time. SIMD sorts of 8 or 16 values in registers use networks of small depth.
- **Circuits.** A comparator on $b$-bit numbers is a small circuit, so a sorting network of depth $d$ gives a Boolean circuit of depth $O(d \log b)$, because two $b$-bit numbers can be compared in depth $O(\log b)$. A network of depth $O(\log n)$ puts sorting in [NC](/nc/) with this kind of circuit.
- **Optimal small networks.** Tables of networks for small $n$ give the smallest depth, the smallest size, and the trade-off between them. See [depth-size trade-off](/depth-size-tradeoff/).
- **Lower bounds for other models.** The bound $d \ge \lceil \lg n \rceil$ uses only the fact that each comparator has two inputs. The same fan-in argument gives the $\Omega(\log n)$ bound for [parallel sorting](/parallel-sorting-depth-lower-bound/) on circuits with gates of bounded fan-in.

## References
