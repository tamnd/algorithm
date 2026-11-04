---
tag: DN2ZN2
kind: model
slug: sorting-network
name: Sorting network
aliases:
- comparator network
- comparison network
area: sorting/sorting-networks
level: intro
summary: A fixed, data-independent network of comparators that sorts every input.
prereqs: [comparator, sorting-problem, comparison-model]
see_also: [network-size, network-depth, zero-one-principle, odd-even-merge-sort, bitonic-sort, aks-sorting-network, minimum-size-sorting-network, minimum-depth-sorting-network]
sources:
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.3.4, Networks for sorting (the model, the standard form, Theorem Z, Batcher's networks and the table of the best networks for small n)
  - book: isbn:9780262032933
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, second edition
    locator: Chapter 27, Sorting Networks (Section 27.1, Comparison networks)
  - paper: doi:10.1145/1468075.1468121
    title: K. E. Batcher, Sorting networks and their applications, AFIPS Spring Joint Computer Conference 32 (1968)
    locator: pp. 307 to 314
  - paper: doi:10.1007/BF02579338
    title: M. Ajtai, J. Komlós and E. Szemerédi, Sorting in c log n parallel steps, Combinatorica 3(1) (1983)
    locator: pp. 1 to 19
  - paper: doi:10.1016/j.jcss.2016.09.004
    title: D. Bundala, M. Codish, L. Cruz-Filipe, P. Schneider-Kamp and J. Závodný, Optimal-depth sorting networks, Journal of Computer and System Sciences 84 (2017)
    locator: pp. 185 to 204 (optimal depth for n up to 16)
  - paper: doi:10.1016/j.jcss.2015.11.014
    title: M. Codish, L. Cruz-Filipe, M. Frank and P. Schneider-Kamp, Sorting nine inputs requires twenty-five comparisons, Journal of Computer and System Sciences 82(3) (2016)
    locator: pp. 551 to 563
  - paper: doi:10.1007/BF02090393
    title: Ian Parberry, A computer-assisted optimal depth lower bound for nine-input sorting networks, Mathematical Systems Theory 24 (1991)
    locator: pp. 101 to 116
  - paper: doi:10.1016/j.jcss.2016.04.004
    title: M. Codish, L. Cruz-Filipe, T. Ehlers, M. Müller and P. Schneider-Kamp, Sorting networks, to the end and back again, Journal of Computer and System Sciences 104 (2019)
    locator: pp. 184 to 201 (depth 10 is optimal for 17 inputs)
  - paper: "Jannis Harder, An answer to the Bose-Nelson sorting problem for 11 and 12 channels, arXiv:2012.04400 (2020)"
    locator: the main theorem (s(11) = 35 and s(12) = 39)
  - url: https://bertdobbelaere.github.io/sorting_networks.html
    title: Bert Dobbelaere, List of sorting networks
    locator: the summary table of the best known size and depth for n up to 64
---

A sorting network is a fixed sequence of [comparators](/comparator/) on $n$ wires that puts every input into sorted order. Which pairs of wires it compares, and in which order, does not depend on the input, so it is a data-oblivious way to solve the [sorting problem](/sorting-problem/). Its two costs are the [size](/network-size/), the number of comparators, and the [depth](/network-depth/), the number of parallel steps. Batcher's networks have depth $\Theta(\log^2 n)$, and the [AKS network](/aks-sorting-network/) has the optimal depth $\Theta(\log n)$.

## The machine

The network has $n$ wires, numbered $0$ to $n - 1$. Each wire holds one item of a set with a total order. At the start, wire $i$ holds the input item $x_i$.

A comparator $[i{:}j]$ with $i < j$ reads the items $a$ on wire $i$ and $b$ on wire $j$. It writes $\min(a, b)$ to wire $i$ and $\max(a, b)$ to wire $j$. This is one step of the machine, and it is the only operation on items.

A comparator network is a finite sequence of comparators $C_1, C_2, \ldots, C_s$. It runs the comparators in this order. The output is the content $y_0, y_1, \ldots, y_{n-1}$ of the wires at the end. The network is a *sorting network* when $y_0 \le y_1 \le \cdots \le y_{n-1}$ for each input. The output is then a permutation of the input in sorted order.

Two comparators that use four different wires do not interact, so they can run at the same time. A *layer* is a set of comparators with no common wire. Each network splits into layers: put each comparator in the first layer after the last layer that uses one of its wires. The layers run one after the other.

The diagram of a network draws each wire as a horizontal line and each comparator as a vertical segment between its two wires, with time going from left to right. The network on 4 wires with the comparators $[0{:}1], [2{:}3], [0{:}2], [1{:}3], [1{:}2]$ has 3 layers: $\{[0{:}1], [2{:}3]\}$, $\{[0{:}2], [1{:}3]\}$ and $\{[1{:}2]\}$. On the input $(3, 1, 4, 2)$ it runs as follows.

| step | comparator | wires 0 to 3 |
|---|---|---|
| input | | 3 1 4 2 |
| 1 | $[0{:}1]$ | 1 3 4 2 |
| 2 | $[2{:}3]$ | 1 3 2 4 |
| 3 | $[0{:}2]$ | 1 3 2 4 |
| 4 | $[1{:}3]$ | 1 3 2 4 |
| 5 | $[1{:}2]$ | 1 2 3 4 |

The first layer sorts two pairs. The second layer puts the minimum on wire 0 and the maximum on wire 3. The last comparator orders the two middle items. By the [zero-one principle](/zero-one-principle/), a check of the 16 inputs of zeros and ones proves that this network sorts every input of 4 items.

**Standard and general form.** A *general* comparator may put the minimum on the higher wire. A network with such comparators that sorts can be changed into a standard one, with only comparators $[i{:}j]$ for $i < j$, of the same size and depth: at each comparator that puts the minimum on the higher wire, exchange the names of its two wires in the rest of the network (Knuth, Section 5.3.4). So the model uses the standard form without loss.

**Data independence.** The sequence of comparators is part of the network, not of the input. The network can not test an item and then choose what to do next. This is the difference from a [comparison sort](/comparison-sort/) such as [merge sort](/merge-sort/), whose next comparison depends on the earlier answers.

## What it counts

The model has two measures of cost.

- The [size](/network-size/) $s$ is the number of comparators. It is the work, or the time of the network on one processor.
- The [depth](/network-depth/) $d$ is the number of layers. It is the time when each layer runs in one parallel step, on $\lfloor n/2 \rfloor$ comparators that work at the same time.

The two measures are related by $d \le s \le d \lfloor n/2 \rfloor$, because each layer has at least one and at most $\lfloor n/2 \rfloor$ comparators. For a fixed $n$, the best size and the best depth are often not reached by the same network. The page [depth-size tradeoff](/depth-size-tradeoff/) gives the cases.

Simple sorts give simple networks. For $n$ wires:

| network | size | depth | $n = 8$ |
|---|---|---|---|
| insertion or bubble sort, comparators $[j-1{:}j]$ | $n(n-1)/2$ | $2n - 3$ | 28 comparators, depth 13 |
| [odd-even transposition sort](/odd-even-transposition-sort/), $n$ rounds | $n(n-1)/2$ | $n$ | 28 comparators, depth 8 |
| [Batcher's odd-even merge sort](/odd-even-merge-sort/) | $\frac{n}{4} \lg n (\lg n - 1) + n - 1$ | $\frac{1}{2} \lg n (\lg n + 1)$ | 19 comparators, depth 6 |
| [bitonic sort](/bitonic-sort/) | $\frac{n}{4} \lg n (\lg n + 1)$ | $\frac{1}{2} \lg n (\lg n + 1)$ | 24 comparators, depth 6 |

The formulas of the last two rows hold for $n$ a power of 2.

## Relation to other models

**The comparison model.** A sorting network is an algorithm of the [comparison model](/comparison-model/) whose comparisons are fixed in advance. So each lower bound of that model holds for networks. In particular, a sorting network of size $s$ sorts with $s$ comparisons, so $s \ge \lceil \lg n! \rceil$. The converse fails: an adaptive sort can do better than each network. For $n = 5$, merge insertion sorts with 7 comparisons, but each sorting network on 5 wires has at least 9 comparators. So the network model is strictly weaker than the comparison model for the size of a sort.

**Parallel machines.** A network of depth $d$ is a parallel algorithm with $d$ steps on $\lfloor n/2 \rfloor$ processors, each of which does one compare-exchange in each step. Each item is read by one processor at a time, so it runs on the exclusive-read exclusive-write [PRAM](/pram-model/) in $O(d)$ time. In the [work-span model](/work-span-model/), the work is the size and the span is the depth. See the [parallel sorting problem](/parallel-sorting-problem/) for algorithms that are not networks, such as [Cole's merge sort](/cole-merge-sort/).

**Boolean circuits.** On the inputs 0 and 1, a comparator computes $\min(a, b) = a \wedge b$ and $\max(a, b) = a \vee b$. So a sorting network of size $s$ and depth $d$ gives a monotone [Boolean circuit](/boolean-circuit/) of $2s$ gates and depth $d$. Output wire $n - k$ of the network computes the threshold function "at least $k$ of the inputs are 1". The middle output is the majority function. With the AKS network, this gives monotone circuits of depth $O(\log n)$ for majority. See [circuit complexity](/circuit-complexity/).

**Hardware and data-oblivious code.** A network maps to hardware with one unit for each comparator. In software, the fixed pattern of memory accesses has no branches that depend on the data. This makes networks fast on SIMD and GPU hardware, and safe in code that must not leak the data through its access pattern. The [counting networks](/counting-network/) of concurrent programming are built on the same plan as the [bitonic](/bitonic-sort/) network.

## Known results in the model

Here $s(n)$ is the least size and $d(n)$ is the least depth of a sorting network on $n$ wires, and $\lg = \log_2$.

**General lower bounds.** $s(n) \ge \lceil \lg n! \rceil$, from the comparison model. $d(n) \ge \lceil \lg n \rceil$, because after $t$ layers the item on a wire depends on at most $2^t$ inputs, and the minimum depends on all $n$. See the [depth lower bound](/sorting-network-depth-lower-bound/). These bounds give $s(n) = \Omega(n \log n)$ and $d(n) = \Omega(\log n)$.

**Testing a network.** The [zero-one principle](/zero-one-principle/): a comparator network sorts each input if and only if it sorts each of the $2^n$ inputs of zeros and ones. The problem to decide whether a given network sorts is [co-NP-complete](/co-np-complete/). See [sorting network verification](/sorting-network-verification/).

**Constructions.** Batcher (1968) gave two networks of depth $\frac12 \lceil \lg n \rceil (\lceil \lg n \rceil + 1)$: [odd-even merge sort](/odd-even-merge-sort/) and [bitonic sort](/bitonic-sort/). Both are built from [merging networks](/merging-network/). The [pairwise sorting network](/pairwise-sorting-network/) of Parberry has the same size and depth as the odd-even network. Ajtai, Komlós and Szemerédi (1983) gave a network of depth $O(\log n)$ and size $O(n \log n)$, so both lower bounds are tight up to a constant factor. The constant of the AKS network is so large that Batcher's networks are smaller for each $n$ of practical size.

**Exact values for small $n$.** The table gives $s(n)$ and $d(n)$ where they are known, and the best known size where it is not. The lower bound $\lceil \lg n! \rceil$ is in the second column.

| $n$ | $\lceil \lg n! \rceil$ | $s(n)$ | $d(n)$ | Batcher size |
|---|---|---|---|---|
| 2 | 1 | 1 | 1 | 1 |
| 3 | 3 | 3 | 3 | 3 |
| 4 | 5 | 5 | 3 | 5 |
| 5 | 7 | 9 | 5 | 9 |
| 6 | 10 | 12 | 5 | 12 |
| 7 | 13 | 16 | 6 | 16 |
| 8 | 16 | 19 | 6 | 19 |
| 9 | 19 | 25 | 7 | 26 |
| 10 | 22 | 29 | 7 | 31 |
| 11 | 26 | 35 | 8 | 37 |
| 12 | 29 | 39 | 8 | 41 |
| 16 | 45 | 60 or less | 9 | 63 |

The sizes for $n \le 8$ were proved optimal by Floyd and Knuth, the sizes for $n = 9$ and $10$ by Codish, Cruz-Filipe, Frank and Schneider-Kamp (2016), and the sizes for $n = 11$ and $12$ by Harder (2020). The depths for $n \le 8$ are in Knuth, Section 5.3.4. Parberry (1991) proved the depths for $n = 9$ and $10$, and Bundala and Závodný (2014) proved them for $n \le 16$. For $n = 17$ the optimal depth is 10 (Codish, Cruz-Filipe, Ehlers, Müller and Schneider-Kamp). The best known network on 16 wires has 60 comparators ([Green's network](/green-filter/)), and its optimality is open. The details are on the pages [minimum-size sorting network](/minimum-size-sorting-network/) and [minimum-depth sorting network](/minimum-depth-sorting-network/). The Batcher column is the size of Knuth's merge exchange form of the odd-even network.

### Pitfalls

- **A network is not a comparison sort with the same count.** The lower bound $\lceil \lg n! \rceil$ is often not reached by networks: $s(5) = 9 > 7$. Use $s(n)$, not the number of comparisons of the best sort.
- **Depth is not the number of comparators on the longest wire only.** The depth counts layers, and a comparator must wait for both of its wires. Compute it with the rule above, not by counting the comparators on each wire.
- **A random test does not prove that a network sorts.** A network can fail on one input of zeros and ones out of $2^n$. Check all $2^n$ such inputs, or use a proof.
- **The order of comparators is part of the network.** Two comparators that share a wire do not commute in general. Moving a comparator to another layer can break a network.

## References
